import urllib.request
from datetime import datetime, timedelta
import pytz
import pandas as pd
from bs4 import BeautifulSoup
from covid_updater.scraping.base import IncrementalScraper


class AustraliaScraper(IncrementalScraper):
    def __init__(self):
        super().__init__(
            country="Australia",
            country_iso="AU",
            data_url="https://covidlive.com.au/report/vaccinations",
            data_url_reference="https://covidlive.com.au/report/vaccinations",
            region_renaming={
                "NSW": "New South Wales",
                "WA": "Western Australia",
                "SA": "South Australia",
                "ACT": "Australian Capital Territory",
                "NT": "Northern Territory",
            },
            column_renaming={
                "DATE": "date",
                "STATE": "region",
                "DOSES": "total_vaccinations",
            },
        )

    def load_data(self):
        # Read HTML
        html_page = urllib.request.urlopen(self.data_url)
        soup = BeautifulSoup(html_page, "html.parser")
        # Extract table
        table = soup.find(id="content").find_all("table")[0]
        df = pd.read_html(str(table))[0][["STATE", "DOSES"]]
        df = df[df["STATE"] != "Australia"]
        return df

    def _assign_dates(self, df):
        df.loc[
            df["region"].isin(
                [
                    "Victoria",
                    "Tasmania",
                    "New South Wales",
                    "Australian Capital Territory",
                ]
            ),
            "date",
        ] = datetime.now(pytz.timezone("Australia/Canberra")).date()
        df.loc[df["region"] == "Western Australia", "date"] = datetime.now(
            pytz.timezone("Australia/Perth")
        ).date()
        df.loc[df["region"] == "Northern Territory", "date"] = datetime.now(
            pytz.timezone("Australia/Darwin")
        ).date()
        df.loc[df["region"] == "South Australia", "date"] = datetime.now(
            pytz.timezone("Australia/Adelaide")
        ).date()
        df.loc[df["region"] == "Queensland", "date"] = datetime.now(
            pytz.timezone("Australia/Brisbane")
        ).date()
        return df

    def _process(self, df):
        return self._assign_dates(df)
        return df
