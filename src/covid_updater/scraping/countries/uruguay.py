import requests
import pandas as pd
from covid_updater.scraping.base import Scraper


class UruguayScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="Uruguay",
            country_iso="UY",
            data_url="https://raw.githubusercontent.com/3dgiordano/covid-19-uy-vacc-data/main/data/Subnational.csv",
            data_url_reference="https://github.com/3dgiordano/covid-19-uy-vacc-data/",
        )

    def load_data(self):
        return pd.read_csv(self.data_url)

    def process(self, df):
        return df
