import requests
import pandas as pd
from covid_updater.scraping.base import IncrementalScraper


class UruguayScraper(IncrementalScraper):
    def __init__(self):
        super().__init__(
            country="Uruguay",
            country_iso="UY",
            data_url="https://msp.gxportal.net/data-vaccine.json",
            data_url_reference="https://monitor.uruguaysevacuna.gub.uy/",
            region_renaming={
                "Tacuarembó": "Tacuarembo",
                "Paysandú": "Paysandu",
                "San José": "San Jose",
            },
            column_renaming={
                "id": "region_iso",
                # "name": "region",
                "vaccinated": "total_vaccinations",
            },
            mode_iso_merge="region",
        )

    def load_data(self):
        data = requests.get(self.data_url).json()
        date = max([d["date"] for d in data["vaccine"]["historical"]])
        df = pd.DataFrame.from_dict(data["vaccine"]["map"])[["id", "vaccinated"]]
        return df.assign(date=date)

    def _process(self, df):
        return df
