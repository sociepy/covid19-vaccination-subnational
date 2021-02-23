"""
Reference: https://github.com/owid/covid-19-data/blob/master/scripts/scripts/vaccinations/automations/batch/denmark.py
"""
import requests
import pandas as pd
from datetime import datetime, timedelta
from covid_updater.scraping.base import IncrementalScraper


class DenmarkScraper(IncrementalScraper):
    def __init__(self):
        super().__init__(
            country="Denmark",
            country_iso="DK",
            data_url=(
                "https://services5.arcgis.com/Hx7l9qUpAnKPyvNz/ArcGIS/rest/services/Vaccine_REG_linelist_gdb/"
                "FeatureServer/{code}/query?where=1%3D1&objectIds=&time=&resultType=none&outFields=*&f=pjson"
            ),
            data_url_reference="https://covid19.ssi.dk/overvagningsdata/vaccinationstilslutning",
            region_renaming={"Sjælland": "Sjaelland"},
            column_renaming={
                "Regionsnavn_current": "region",
                "antal_foerste_vacc": "people_vaccinated",
                "antal_faerdig_vacc": "people_fully_vaccinated",
            },
            do_cumsum_fields=[
                "people_vaccinated",
                "people_fully_vaccinated",
                "total_vaccinations",
            ],
        )

    def _load_dose(self, url, date_field):
        data = requests.get(url).json()
        df = pd.DataFrame.from_records(elem["attributes"] for elem in data["features"])
        date = pd.to_datetime(df[date_field], unit="ms").dt.strftime("%Y-%m-%d")
        df = df.assign(date=date)
        return df

    def load_data(self):
        # Load
        df_1 = self._load_dose(self.data_url.format(code=19), "first_vaccinedate")
        df_2 = self._load_dose(self.data_url.format(code=20), "second_vaccinedate")
        df_2 = df_2[["date", "Regionsnavn_current", "antal_faerdig_vacc"]]
        return pd.merge(df_1, df_2, how="left", on=["date", "Regionsnavn_current"])

    def _process(self, df):
        df.loc[:, "total_vaccinations"] = df.loc[:, "people_vaccinated"].fillna(
            0
        ) + df.loc[:, "people_fully_vaccinated"].fillna(0)
        return df
