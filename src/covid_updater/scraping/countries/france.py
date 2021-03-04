import pandas as pd
from covid_updater.scraping.base import IncrementalScraper


class FranceScraper(IncrementalScraper):
    def __init__(self):
        super().__init__(
            country="France",
            country_iso="FR",
            data_url="https://www.data.gouv.fr/fr/datasets/r/9b1e6c8c-7e1d-47f9-9eb9-f2eeaab60d99",
            data_url_reference="https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-personnes-vaccinees-contre-la-covid-19-1/",
            region_renaming={
                1: "Guadeloupe",
                2: "Martinique",
                3: "Guyane",
                4: "La Reunion",
                6: "Mayotte",
                11: "Ile-de-France",
                24: "Centre-Val de Loire",
                27: "Bourgogne-Franche-Comte",
                28: "Normandie",
                32: "Hauts-de-France",
                44: "Grand-Est",
                52: "Pays-de-la-Loire",
                53: "Bretagne",
                75: "Nouvelle-Aquitaine",
                76: "Occitanie",
                84: "Auvergne-Rhone-Alpes",
                93: "Provence-Alpes-Cote-d'Azur",
                94: "Corse",
            },
            column_renaming={
                "reg": "region",
                "jour": "date",
                "n_tot_dose1": "people_vaccinated",
                "n_tot_dose2": "people_fully_vaccinated",
            },
        )

    def load_data(self):
        # Load
        df = pd.read_csv(self.data_url, sep=";")
        df = df[df["reg"] != 7]
        return df

    def _process(self, df):
        # df["people_fully_vaccinated"] = df["people_fully_vaccinated"].astype("Int64").fillna(pd.NA)
        df["total_vaccinations"] = (
            df["people_fully_vaccinated"] + df["people_vaccinated"]
        )
        return df
