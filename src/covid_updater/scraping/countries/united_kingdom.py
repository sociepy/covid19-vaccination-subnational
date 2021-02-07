import pandas as pd
from covid_updater.scraping.base import Scraper


class UnitedKingdomScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="United Kingdom", 
            country_iso="GB", 
            data_url="https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&metric=cumPeopleVaccinatedFirstDoseByPublishDate&metric=cumPeopleVaccinatedSecondDoseByPublishDate&metric=cumPeopleVaccinatedCompleteByPublishDate&format=csv", 
            data_url_reference="https://coronavirus.data.gov.uk/details/download", 
            column_renaming={
                "areaName": "region",
                "cumPeopleVaccinatedFirstDoseByPublishDate": "people_vaccinated",
                "cumPeopleVaccinatedSecondDoseByPublishDate": "people_fully_vaccinated"
            }
        )

    def load_data(self):
        # Load
        df = pd.read_csv(self.data_url)
        return df

    def _process(self, df):
        # Column proccess
        df.loc[:, "total_vaccinations"] = df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
        # Ignore some entries (field: region, value: Österreich)
        df = df.loc[df["region"] != "Österreich"]
        return df
