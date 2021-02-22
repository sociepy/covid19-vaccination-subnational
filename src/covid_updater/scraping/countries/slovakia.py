import pandas as pd
from covid_updater.scraping.base import Scraper


class SlovakiaScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="Slovakia",
            country_iso="SK",
            data_url="https://raw.githubusercontent.com/Institut-Zdravotnych-Analyz/covid19-data/main/Vaccination/OpenData_Slovakia_Vaccination_Regions.csv",
            data_url_reference="https://github.com/Institut-Zdravotnych-Analyz/covid19-data/",
            region_renaming={
                "Trenčiansky kraj": "Trenciansky kraj",
                "Banskobystrický kraj": "Banskobystricky kraj",
                "Bratislavský kraj": "Bratislavsky kraj",
                "Košický kraj": "Kosicky kraj",
                "Nitriansky kraj": "Nitriansky kraj",
                "Prešovský kraj": "Presovsky kraj",
                "Trnavský kraj": "Trnavsky kraj",
                "Žilinský kraj": "Zilinsky kraj",
            },
            column_renaming={
                "Date": "date",
                "Region": "region",
                "first_dose": "people_vaccinated",
                "second_dose": "people_fully_vaccinated",
            },
            do_cumsum_fields=[
                "total_vaccinations",
                "people_vaccinated",
                "people_fully_vaccinated",
            ],
        )

    def load_data(self):
        # Load
        df = pd.read_csv(self.data_url, sep=";")
        return df

    def _process(self, df):
        df.loc[:, "total_vaccinations"] = (
            df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
        )
        return df
