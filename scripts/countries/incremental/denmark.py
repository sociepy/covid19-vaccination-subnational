"""
Reference: https://github.com/owid/covid-19-data/blob/master/scripts/scripts/vaccinations/automations/batch/denmark.py
"""
import urllib
import tabula
import pandas as pd
from bs4  import BeautifulSoup
from datetime import datetime


source_file = "data/countries/Denmark.csv"


def main():
    # Load current data
    df_source = pd.read_csv(source_file)

    # Load new data
    url = "https://covid19.ssi.dk/overvagningsdata/vaccinationstilslutning"

    # Locate newest pdf
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, "html.parser")
    pdf_path = soup.find('a', text="Download her").get("href")  # Get path to newest pdf
    date = datetime.strptime(pdf_path.split("-")[-2], "%d%m%Y").strftime("%Y-%m-%d")
    if date > df_source["date"].max():
        # Get preliminary dataframe
        df = pd.DataFrame()
        column_string = {'dtype': str , 'header': None}  # Force dtype to be object because of thousand separator in Europe
        kwargs = {'pandas_options': column_string,}
        dfs_from_pdf = tabula.read_pdf(pdf_path, pages="all", **kwargs)
        df = dfs_from_pdf[1]

        # Rename columns
        df = df.rename(columns={
            0: "region",
            2: "people_vaccinated",
            4: "people_fully_vaccinated"
        })
        df = df.astype(str)

        # Remove numeric 1000-separator
        df.loc[:, "people_vaccinated"] = df.loc[:, "people_vaccinated"].apply(lambda x: int(x.replace(".", ""))).fillna(0).astype(int)
        def del_separator(x):
            if x != 'nan':
                return int(x.replace(".", ""))
            else:
                return 0
        df.loc[:, "people_fully_vaccinated"] = df.loc[:, "people_fully_vaccinated"].apply(lambda x: del_separator(x)).astype("Int64")

        # Process region column
        df.loc[:, "region"] = df.loc[:, "region"].replace({
            "Ukendt**": "Others", "Ukendt*": "Others", "Ukendt": "Others", "Sjælland": "Sjaelland"
        })
        df = df[~(df["region"]=="I alt")]

        # Get new columns
        df.loc[:, "total_vaccinations"] = df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
        df.loc[:, "location"]  = "Denmark"
        df.loc[:, "date"]  = datetime.strptime(pdf_path.split("-")[-2], "%d%m%Y").strftime("%Y-%m-%d")

        # Order columns
        df = df.loc[:, ["date", "location", "region", "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]

        # Export
        df = pd.concat([df, df_source])
        df = df[["location", "region", "date", "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
        df = df.sort_values(by=["region", "date"])
        df.to_csv(source_file, index=False)