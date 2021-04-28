import pandas as pd
from datetime import datetime
from covid_updater.scraping.base import Scraper


def week_to_date(row):
    """https://github.com/owid/covid-19-data/blob/master/scripts/scripts/vaccinations/automations/batch/sweden.py"""
    origin_date = (
        pd.to_datetime("2019-12-29")
        if row["Vecka"] >= 52
        else pd.to_datetime("2021-01-03")
    )
    return origin_date + pd.DateOffset(days=7 * int(row["Vecka"]))


class SwedenScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="Sweden",
            country_iso="SE",
            data_url="https://fohm.maps.arcgis.com/sharing/rest/content/items/fc749115877443d29c2a49ea9eca77e9/data",
            data_url_reference="https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/vaccination-mot-covid-19/statistik/statistik-over-registrerade-vaccinationer-covid-19/",
            region_renaming={
                "Stockholm": "Stockholms lan",
                "Västerbotten": "Vasterbottens lan",
                "Norrbotten": "Norrbottens lan",
                "Uppsala": "Uppsala lan",
                "Södermanland": "Sodermanlands lan",
                "Östergötland": "Ostergotlands lan",
                "Jönköping": "Jonkopings lan",
                "Kronoberg": "Kronobergs lan",
                "Kalmar": "Kalmar lan",
                "Gotland": "Gotlands lan",
                "Blekinge": "Blekinge lan",
                "Skåne": "Skane lan",
                "Halland": "Hallands lan",
                "Västra Götaland": "Vastra Gotalands lan",
                "Värmland": "Varmlands lan",
                "Örebro": "Orebro lan",
                "Västmanland": "Vastmanlands lan",
                "Dalarna": "Dalarnas lan",
                "Gävleborg": "Gavleborgs lan",
                "Västernorrland": "Vasternorrlands lan",
                "Jämtland": "Jamtlands lan",
            },
            column_renaming={"Region": "region"},
        )

    def load_data(self):
        # Load
        df = pd.read_excel(
            self.data_url,
            sheet_name="Vaccinerade tidsserie",
            usecols=["Region", "Vecka", "År", "Antal vaccinerade", "Vaccinationsstatus"],
        )
        return df

    def _process(self, df):
        #  Remove Sweden total data
        df = df.loc[df["region"] != "| Sverige |"].copy()
        #  Add date field
        df.loc[:, "date"] = df.apply(week_to_date, axis=1).dt.date.astype(str)
        #  Reshape DataFrame
        df = df.pivot_table(
            values="Antal vaccinerade",
            index=[
                c for c in df.columns if c not in ("Vaccinationsstatus", "Antal vaccinerade")
            ],
            columns="Vaccinationsstatus",
        ).reset_index()
        df = df.rename(
            columns={"Minst 1 dos": "people_vaccinated", "Färdigvaccinerade": "people_fully_vaccinated"}
        )
        #  Add total_vaccinations field
        df.loc[:, "total_vaccinations"] = (
            df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
        )
        return df
