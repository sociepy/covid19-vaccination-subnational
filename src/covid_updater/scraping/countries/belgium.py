import pandas as pd
from datetime import datetime
from covid_updater.utils import read_xlsx_from_url
from covid_updater.scraping.base import Scraper


class BelgiumScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="Belgium", 
            country_iso="BE", 
            data_url="http://covid-vaccinatie.be/en/vaccines-administered.xlsx", 
            data_url_reference="https://covid-vaccinatie.be/en",
            column_renaming={
                "Date": "date",
                "Region": "region",
                "1st dose": "people_vaccinated",
                "2nd dose": "people_fully_vaccinated"
            },
            do_cumsum_fields=["people_fully_vaccinated", "total_vaccinations", "people_vaccinated"]
        )

    def load_data(self):
        # Load
        df = read_xlsx_from_url(self.data_url)
        return df

    def _process(self, df):
        df.loc[:, "people_fully_vaccinated"] = df.loc[:, "people_fully_vaccinated"].fillna(0).astype(int)
        df.loc[:, "people_vaccinated"] = df.loc[:, "people_vaccinated"].fillna(0).astype(int)
        df.loc[:, "total_vaccinations"] = df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
        df.loc[:, "date"] = df.loc[:, "date"].apply(lambda x: datetime.strptime(x, "%d/%m/%Y").strftime("%Y-%m-%d"))
        return df
