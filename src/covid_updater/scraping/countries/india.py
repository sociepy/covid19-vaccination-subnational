import pandas as pd
from datetime import datetime
from covid_updater.scraping.base import Scraper


class IndiaScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="India", 
            country_iso="IN", 
            data_url="https://github.com/india-covid19vaccine/india-covid19vaccine.github.io/raw/main/csv/state_timeline.csv", 
            data_url_reference="https://india-covid19vaccine.github.io", 
            column_renaming={
                "state_code": "region_iso",
                "total_doses": "total_vaccinations",
                "total_vaccinated": "people_vaccinated",
                "total_fully_vaccinated": "people_fully_vaccinated"
            },
            mode_iso_merge="region",
            field_renaming={
                "region_iso": {
                    "CG": "CT",
                    "OD": "OR",
                    "TS": "TG",
                    "UK": "UT"
                }
            }
        )

    def load_data(self):
        df = pd.read_csv(self.data_url)
        # Unpivot
        # df = df.melt(id_vars=["state_code"], var_name="date", value_name="total_vaccinations")
        return df

    def _process(self, df):
        df = df.loc[~(df.loc[:, "region_iso"] == "MISC")].copy()

        # ISO
        df.loc[:, "region_iso"] = "IN-" + df.loc[:, "region_iso"]

        # Date format
        df.loc[:, "date"] = df.loc[:, "date"].apply(lambda x: datetime.strptime(x, "%d/%m/%Y").strftime("%Y-%m-%d"))
        return df
