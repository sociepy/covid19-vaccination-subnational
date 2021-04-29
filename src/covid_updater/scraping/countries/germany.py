import pandas as pd
from covid_updater.scraping.base import Scraper


class GermanyScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="Germany",
            country_iso="DE",
            data_url="https://raw.githubusercontent.com/mathiasbynens/covid-19-vaccinations-germany/main/data/data.csv",
            data_url_reference="https://github.com/mathiasbynens/covid-19-vaccinations-germany/",
            region_renaming={
                "Baden-Württemberg": "Baden-Wurttemberg",
                "Thüringen": "Thuringen",
            },
            column_renaming={
                "state": "region",
                "atLeastPartiallyVaccinatedCumulative": "people_vaccinated",
                "fullyVaccinatedCumulative": "people_fully_vaccinated",
            },
        )

    def load_data(self):
        # Load
        df = pd.read_csv(
            self.data_url,
            usecols=[
                "date",
                "state",
                "atLeastPartiallyVaccinatedCumulative",
                "fullyVaccinatedCumulative",
                "initialDosesCumulative",
            ],
        )
        return df

    def _process(self, df):
        df.loc[:, "total_vaccinations"] = (
            df.loc[:, "initialDosesCumulative"] + df.loc[:, "people_fully_vaccinated"]
        )
        df = df.drop(columns=["initialDosesCumulative"])
        return df
