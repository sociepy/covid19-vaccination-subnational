import pandas as pd
from datetime import datetime
from covid_updater.scraping.base import Scraper


class UnitedStatesScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="United States",
            country_iso="US",
            data_url="https://github.com/youyanggu/covid19-cdc-vaccination-data/raw/main/aggregated_adjusted.csv",
            data_url_reference="https://github.com/youyanggu/covid19-cdc-vaccination-data",
            column_renaming={
                "Location": "region_iso",
                "Date": "date",
                "Doses_Administered": "total_vaccinations",
                "Administered_Dose1": "people_vaccinated",
                "Administered_Dose2": "people_fully_vaccinated",
            },
            mode_iso_merge="region",
        )

    def load_data(self):
        df = pd.read_csv(
            self.data_url,
            usecols=[
                "Date",
                "Location",
                "Doses_Administered",
                "Administered_Dose1",
                "Administered_Dose2",
            ],
        )
        df = df.dropna(subset=["Doses_Administered"])
        return df

    def _process(self, df):
        df = df.loc[~(df.loc[:, "region_iso"] == "US")].copy()
        #  ISO
        df.loc[:, "region_iso"] = "US-" + df.loc[:, "region_iso"]
        return df
