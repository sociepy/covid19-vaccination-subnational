import pandas as pd
from covid_updater.scraping.base import Scraper


class BrazilScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="Brazil", 
            country_iso="BR", 
            data_url="https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv", 
            data_url_reference="https://github.com/wcota/covid19br/", 
            region_renaming={
                "Kärnten": "Karnten",
                "Niederösterreich": "Niederosterreich",
                "Oberösterreich": "Oberosterreich"
            }, 
            column_renaming={
                "vaccinated": "total_vaccinations"
            },
            mode_iso_merge="region"
        )

    def load_data(self):
        # Load
        df = pd.read_csv(self.data_url, usecols=["state", "date", "vaccinated"])
        start_date =  "2021-01-18"
        # Filter
        df = df.loc[df["date"] >= start_date]
        df = df[~(df.loc[:, "state"]=="TOTAL")]
        return df

    def _process(self, df):
        # Column proccess
        df.loc[:, "date"] = df.loc[:, "date"].str.slice(0, 10)
        # Build region iso
        df.loc[:, "region_iso"] = f"{self.country_iso}-" + df.loc[:, "state"]
        # Process vaccinations
        df.loc[:, "total_vaccinations"] = df.loc[:, "total_vaccinations"].fillna(0).astype(int)
        return df
