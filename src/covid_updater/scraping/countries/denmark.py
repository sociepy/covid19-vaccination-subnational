"""
Reference: https://github.com/owid/covid-19-data/blob/master/scripts/scripts/vaccinations/automations/batch/denmark.py
"""
import urllib.request
from datetime import datetime
import tabula
import pandas as pd
from bs4  import BeautifulSoup
from covid_updater.scraping.base import IncrementalScraper


class DenmarkScraper(IncrementalScraper):
    def __init__(self):
        super().__init__(
            country="Denmark", 
            country_iso="DK", 
            data_url="https://covid19.ssi.dk/overvagningsdata/vaccinationstilslutning", 
            data_url_reference="https://covid19.ssi.dk/overvagningsdata/vaccinationstilslutning", 
            region_renaming={
                "Ukendt**": "Others",
                "Ukendt*": "Others",
                "Ukendt": "Others",
                "Sjælland": "Sjaelland"
            }, 
            column_renaming={
                0: "region",
                2: "people_vaccinated",
                4: "people_fully_vaccinated"
            }
        )
        self.regions = [
            "Hovedstaden",
            "Midtjylland",
            "Nordjylland",
            "Sjælland",
            "Syddanmark"
        ]

    def _load_tables_from_html(self):
        html_page = urllib.request.urlopen(self.data_url)
        soup = BeautifulSoup(html_page, "html.parser")
        pdf_path = soup.find('a', text="Download her").get("href")  # Get path to newest pdf
        # Get preliminary dataframe
        column_string = {'dtype': str , 'header': None}  # Force dtype to be object because of thousand separator
        kwargs = {'pandas_options': column_string,}
        tables = tabula.read_pdf(pdf_path, pages="all", **kwargs)
        return tables

    def _get_date_from_tables(self, tables):
        for tbl in tables:
            if "Vaccinationsdato" in tbl[0].values:
                df = pd.DataFrame(tbl)
                break
        df = df.drop([0, 1, 2, 3])
        date = df.loc[:, 0].apply(lambda x: datetime.strptime(x, "%d-%m-%Y").strftime("%Y-%m-%d")).max()
        return date

    def _get_df_from_tables(self, tables):
        for tbl in tables:
            if "Region" in tbl[0].values:
                df = pd.DataFrame(tbl)
                break
        df = df.astype(pd.StringDtype())
        if df.shape != (11, 7):
            raise Exception("Shape of table changed!")
        if not all(region in df[0].dropna().tolist() for region in self.regions):
            raise Exception("Region missing!")
        df = df.drop([0, 1, 2, 3, len(df)-1])
        return df

    def _remove_delimiter(self, x):
        if not pd.isnull(x):
            return int(x.replace(".", ""))
        else:
            return 0

    def load_data(self):
        # Load
        tables = self._load_tables_from_html()
        df = self._get_df_from_tables(tables)
        date = self._get_date_from_tables(tables)
        df.loc[:, "date"]  = date
        return df

    def _process(self, df):
        df.loc[:, "people_vaccinated"] = df.loc[:, "people_vaccinated"].apply(
            self._remove_delimiter
        ).fillna(0).astype(int)
        df.loc[:, "people_fully_vaccinated"] = df.loc[:, "people_fully_vaccinated"].apply(
            self._remove_delimiter
        ).astype("Int64")
        df.loc[:, "total_vaccinations"] = df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
        return df

    def _postprocess(self, df):
        df = super()._postprocess(df)
        df.loc[df["region"]=="Others", "location_iso"] = self.country_iso
        return df