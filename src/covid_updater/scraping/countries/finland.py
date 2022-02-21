import json
import requests
import pandas as pd
from covid_updater.scraping.base import Scraper


class FinlandScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="Finland",
            country_iso="FI",
            data_url="https://piikki-api.lab.juiciness.io/administrations/areas",
            data_url_reference="https://piikki.juiciness.io/",
            region_renaming={
                "Åland": "Aland",
                "South Karelia Hospital District": "Etela-Karjala",
                "South Ostrobothnia Hospital District": "Etela-Pohjanmaa",
                "South Savo Hospital District": "Etela-Savo",
                "Helsinki and Uusimaa Hospital District": "Uusimaa",
                "Itä-Savo Hospital District": "Etela-Savo",
                "Kainuu Hospital District": "Kainuu",
                "Kanta-Häme Hospital District": "Kanta-Hame",
                "Central Ostrobothnia Hospital District": "Keski-Pohjanmaa",
                "Central Finland Hospital District": "Keski-Suomi",
                "Kymenlaakso Hospital District": "Kymenlaakso",
                "Lappi Hospital District": "Lappi",
                "Länsi-Pohja Hospital District": "Lappi",
                "Pirkanmaa Hospital District": "Pirkanmaa",
                "North Karelia Hospital District": "Pohjois-Karjala",
                "North Ostrobothnia Hospital District": "Pohjois-Pohjanmaa",
                "North Savo Hospital District": "Pohjois-Savo",
                "Päijät-Häme Hospital District": "Paijat-Hame",
                "Satakunta Hospital District": "Satakunta",
                "Vaasa Hospital District": "Pohjanmaa",
                "Southwest Finland Hospital District": "Varsinais-Suomi",
            },
            column_renaming={
                "firstDoseShots": "people_vaccinated",
                "secondDoseShots": "people_fully_vaccinated",
            },
            do_cumsum_fields=[
                "people_vaccinated",
                "people_fully_vaccinated",
                "total_vaccinations",
            ],
        )

    def load_data(self):
        data_raw = json.loads(requests.get(self.data_url).content)
        dfs = [
            pd.DataFrame.from_records(sample["shotHistory"]).assign(
                region=sample["areaName"]
            )
            for sample in data_raw
        ]
        return pd.concat(dfs)

    def _process(self, df):
        # Column proccess
        df.loc[:, "date"] = pd.to_datetime(df.date).apply(
            lambda x: x.strftime("%Y-%m-%d")
        )
        # Regions to be ignored
        df = df[~df["region"].isin(["All areas", "Other areas"])]
        # Avoid duplicates
        df = df.groupby(["location", "region", "date"]).sum().reset_index()
        # Add missing fields
        df.loc[:, "total_vaccinations"] = (
            df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
        )
        return df
