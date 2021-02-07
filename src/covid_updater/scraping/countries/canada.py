import pandas as pd
from datetime import datetime
from covid_updater.scraping.base import Scraper


class CanadaScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="Canada", 
            country_iso="CA", 
            data_url="https://github.com/juancri/covid19-vaccination/raw/master/output/chile-vaccination.csv", 
            data_url_reference="https://github.com/ccodwg/Covid19Canada", 
            region_renaming={
                "BC": "British Columbia",
                "NL": "Newfoundland and Labrador", 
                "NWT": "Northwest Territories", 
                "PEI": "Prince Edward Island"
            }
        )

    def load_data(self):
        DATA_URL_1 = "https://raw.githubusercontent.com/ccodwg/Covid19Canada/master/timeseries_prov/vaccine_administration_timeseries_prov.csv"
        COLUMNS_RENAMING = {
            "date_vaccine_administered": "date",
            "province": "region",
            "cumulative_avaccine": "total_vaccinations"
        }
        df = pd.read_csv(DATA_URL_1, usecols=COLUMNS_RENAMING.keys())
        df = df.rename(columns=COLUMNS_RENAMING)
        # Date
        df.loc[:, "date"] = df.loc[:, "date"].apply(lambda x: datetime.strptime(x, "%d-%m-%Y").strftime("%Y-%m-%d"))

        # Add completed vaccinations
        DATA_URL_2 = "https://raw.githubusercontent.com/ccodwg/Covid19Canada/master/timeseries_prov/vaccine_completion_timeseries_prov.csv"
        COLUMNS_RENAMING = {
            "date_vaccine_completed": "date",
            "province": "region",
            "cumulative_cvaccine": "people_fully_vaccinated"
        }
        df_2 = pd.read_csv(DATA_URL_2, usecols=COLUMNS_RENAMING.keys())
        df_2 = df_2.rename(columns=COLUMNS_RENAMING)
        # Date
        df_2.loc[:, "date"] = pd.to_datetime(df_2.loc[:, "date"], format="%d-%m-%Y")
        df_2.loc[:, "date"] = df_2.loc[:, "date"].dt.strftime("%Y-%m-%d")

        df = df.merge(df_2, on=["region", "date"], how="left")
        return df

    def _process(self, df):
        df.loc[:, "people_fully_vaccinated"] = df.loc[:, "people_fully_vaccinated"].fillna(0).astype(int)
        df.loc[:, "people_vaccinated"] = df.loc[:, "total_vaccinations"] - df.loc[:, "people_fully_vaccinated"].astype(int)
        return df
