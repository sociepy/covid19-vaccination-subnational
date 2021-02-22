from datetime import datetime
import pandas as pd
from covid_updater.scraping.base import Scraper


class SpainScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="Spain",
            country_iso="ES",
            data_url="https://raw.githubusercontent.com/civio/covid-vaccination-spain/main/data.csv",
            data_url_reference="https://github.com/civio/covid-vaccination-spain/",
            region_renaming={
                "Andalucía": "Andalucia",
                "Aragón": "Aragon",
                "Asturias": "Asturias, Principado de",
                "Baleares": "Illes Balears",
                "C. Valenciana": "Valenciana, Comunidad",
                "Castilla La Mancha": "Castilla-La Mancha",
                "Cataluña": "Catalunya",
                "Madrid": "Madrid, Comunidad de",
                "Murcia": "Murcia, Region de",
                "Navarra": "Navarra, Comunidad Foral de",
                "País Vasco": "Pais Vasco",
            },
            column_renaming={
                "informe": "date",
                "comunidad autónoma": "region",
                "dosis administradas": "total_vaccinations",
                "personas con pauta completa": "people_fully_vaccinated",
            },
        )

    def load_data(self):
        # Load
        df = pd.read_csv(
            self.data_url,
            dtype={
                "dosis administradas": pd.StringDtype(),
                "personas con pauta completa": pd.StringDtype(),
            },
        )
        df = df[~(df.loc[:, "comunidad autónoma"] == "Totales")]
        return df

    def remove_delimiter(self, x):
        if not pd.isnull(x):
            return int(x.replace(".", ""))
        else:
            return 0

    def _process(self, df):
        # Date format
        df.loc[:, "date"] = df.loc[:, "date"].apply(
            lambda x: datetime.strptime(x, "%d/%m/%Y").strftime("%Y-%m-%d")
        )
        # Remove point separator from counters
        df.loc[:, "total_vaccinations"] = df.loc[:, "total_vaccinations"].apply(
            self.remove_delimiter
        )
        df.loc[:, "people_fully_vaccinated"] = df.loc[
            :, "people_fully_vaccinated"
        ].apply(self.remove_delimiter)
        # Compute missing counter metrics
        df.loc[:, "people_vaccinated"] = (
            df.loc[:, "total_vaccinations"] - df.loc[:, "people_fully_vaccinated"]
        )
        return df
