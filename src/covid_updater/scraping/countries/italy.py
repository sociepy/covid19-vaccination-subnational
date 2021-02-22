import pandas as pd
from covid_updater.scraping.base import Scraper


class ItalyScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="Italy",
            country_iso="IT",
            data_url="https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-summary-latest.csv",
            data_url_reference="https://github.com/italia/covid19-opendata-vaccini/",
            region_renaming={
                "ABR": "Abruzzo",
                "VEN": "Veneto",
                "UMB": "Umbria",
                "TOS": "Toscana",
                "SIC": "Sicilia",
                "SAR": "Sardegna",
                "PUG": "Puglia",
                "PIE": "Piemonte",
                "PAT": "Provincia autonoma di Trento",
                "PAB": "Provincia autonoma di Bolzano - Alto Adige",
                "MOL": "Molise",
                "VDA": "Valle d'Aosta",
                "LOM": "Lombardia",
                "LIG": "Liguria",
                "LAZ": "Lazio",
                "FVG": "Friuli Venezia Giulia",
                "EMR": "Emilia-Romagna",
                "CAM": "Campania",
                "CAL": "Calabria",
                "BAS": "Basilicata",
                "MAR": "Marche",
            },
            column_renaming={
                "data_somministrazione": "date",
                "area": "region",
                "totale": "total_vaccinations",
                "prima_dose": "people_vaccinated",
                "seconda_dose": "people_fully_vaccinated",
            },
            do_cumsum_fields=[
                "total_vaccinations",
                "people_vaccinated",
                "people_fully_vaccinated",
            ],
        )

    def load_data(self):
        # Load
        df = pd.read_csv(self.data_url)
        return df

    def _process(self, df):
        df = df[df.loc[:, "region"] != "ITA"]
        return df
