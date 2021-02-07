import pandas as pd
from covid_updater.scraping.base import Scraper


class SwitzerlandScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="Switzerland", 
            country_iso="CH", 
            data_url="https://github.com/rsalzer/COVID_19_VACC/raw/main/data.csv", 
            data_url_reference="https://github.com/rsalzer/COVID_19_VACC/", 
            region_renaming={
                "Kärnten": "Karnten",
                "Niederösterreich": "Niederosterreich",
                "Oberösterreich": "Oberosterreich"
            }, 
            column_renaming={
                "geounit": "region_iso",
                "ncumul_vacc": "total_vaccinations"
            },
            mode_iso_merge="region"
        )

    def load_data(self):
        # Load
        df = pd.read_csv(self.data_url, usecols=["geounit", "date", "ncumul_vacc"])
        df = df.loc[~df.loc[:, "geounit"].isin(["CHFL", "FL"])].reset_index(drop=True)
        return df

    def _process(self, df):
        df.loc[:, "region_iso"] = self.country_iso + "-" + df.loc[:, "region_iso"]
        return df
