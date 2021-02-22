import pandas as pd
import numpy as np
from covid_updater.scraping.base import Scraper


class ChileScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="Chile",
            country_iso="CL",
            data_url="https://github.com/juancri/covid19-vaccination/raw/master/output/chile-vaccination.csv",
            data_url_reference="https://github.com/juancri/covid19-vaccination/",
            region_renaming={
                "Araucanía": "La Araucania",
                "Aysén": "Aisen del General Carlos Ibanez del Campo",
                "Biobío": "Biobio",
                "Los Ríos": "Los Rios",
                "Tarapacá": "Tarapaca",
                "Valparaíso": "Valparaiso",
                "Ñuble": "Nuble",
                "O’Higgins": "Libertador General Bernardo O'Higgins",
                "Metropolitana": "Region Metropolitana de Santiago",
            },
        )

    def load_data(self):
        # Load
        df = pd.read_csv(self.data_url)
        # Filter
        df = df.loc[~(df["Region"] == "Total")]  # .T
        cols = df.columns[df.columns >= "2021-01-23"]
        df = df[cols]
        return df

    def _preprocess(self, df):
        # Get number of regions
        num_regions = df["Region"].nunique()

        # Get vaccine numbers
        df = df.sort_values(by=["Dose", "Region"]).set_index(["Dose", "Region"])
        people_vaccinated = df.loc["First"].values.reshape(-1, 1).squeeze()
        people_fully_vaccinated = df.loc["Second"].values.reshape(-1, 1).squeeze()
        total_vaccinations = people_vaccinated + people_fully_vaccinated

        # Build missing columns
        regions = df.loc["First"].index.tolist()
        num_dates = df.shape[1]
        dates = df.columns
        dates = dates.tolist() * num_regions
        regions = list(np.repeat(regions, num_dates))

        # Build DataFrame
        df = pd.DataFrame(
            {
                "total_vaccinations": total_vaccinations,
                "people_vaccinated": people_vaccinated,
                "people_fully_vaccinated": people_fully_vaccinated,
                "date": dates,
                "region": regions,
                "location": self.country,
            }
        )
        df = super()._preprocess(df)
        return df

    def _process(self, df):
        return df
