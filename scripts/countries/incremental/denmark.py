"""
Reference: https://github.com/owid/covid-19-data/blob/master/scripts/scripts/vaccinations/automations/batch/denmark.py
"""
import urllib.request
import tabula
import pandas as pd
from bs4  import BeautifulSoup
from datetime import datetime
from covid_updater.iso import ISODB
from covid_updater.utils import export_data


COUNTRY = "Denmark"
COUNTRY_ISO = "DK"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://covid19.ssi.dk/overvagningsdata/vaccinationstilslutning"
DATA_URL_REFERENCE = DATA_URL
REGION_RENAMING = {
    "Ukendt**": "Others",
    "Ukendt*": "Others",
    "Ukendt": "Others",
    "Sjælland": "Sjaelland"
}
regions = [
    "Hovedstaden",
    "Midtjylland",
    "Nordjylland",
    "Sjælland",
    "Syddanmark"
]


def get_date(dfs_from_pdf):
    df = dfs_from_pdf[0]  # Hardcoded
    df = df.drop([0, 1, 2, 3])
    date = pd.to_datetime(df[0], format="%d-%m-%Y").max().strftime("%Y-%m-%d")
    return date


def main():
    # Load current data
    df_source = pd.read_csv(OUTPUT_FILE)

    # Locate newest pdf
    html_page = urllib.request.urlopen(DATA_URL)
    soup = BeautifulSoup(html_page, "html.parser")
    pdf_path = soup.find('a', text="Download her").get("href")  # Get path to newest pdf
    # Get preliminary dataframe
    column_string = {'dtype': str , 'header': None}  # Force dtype to be object because of thousand separator
    kwargs = {'pandas_options': column_string,}
    dfs_from_pdf = tabula.read_pdf(pdf_path, pages="all", **kwargs)  # len(dfs_from_pdf) == 8 ?
    #date = datetime.strptime(pdf_path.split("-")[-2], "%d%m%Y").strftime("%Y-%m-%d")
    date = get_date(dfs_from_pdf)

    # Get preliminary dataframe
    column_string = {'dtype': str , 'header': None}  # Force dtype to be object because of thousand separator
    kwargs = {'pandas_options': column_string,}
    dfs_from_pdf = tabula.read_pdf(pdf_path, pages="all", **kwargs)
    df = dfs_from_pdf[1] # Hardcoded

    if df.shape != (11, 7):
        raise Exception("Shape of table changed!")
    if not all(region in df[0].tolist() for region in regions):
        raise Exception("Region missing!")
    
    # Drop columns
    df = df.drop([0, 1, 2, 3, len(df)-1])
    # Rename columns
    df = df.rename(columns={
        0: "region",
        2: "people_vaccinated",
        4: "people_fully_vaccinated"
    })
    df = df.astype(str)

    # Remove numeric 1000-separator
    df.loc[:, "people_vaccinated"] = df.loc[:, "people_vaccinated"].apply(
        lambda x: int(x.replace(".", ""))).fillna(0).astype(int)
    def del_separator(x):
        if x != 'nan':
            return int(x.replace(".", ""))
        else:
            return 0
    df.loc[:, "people_fully_vaccinated"] = df.loc[:, "people_fully_vaccinated"].apply(lambda x: del_separator(x)).astype("Int64")

    # Process region column
    df.loc[:, "region"] = df.loc[:, "region"].replace(REGION_RENAMING)

    # Get new columns
    df.loc[:, "total_vaccinations"] = df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
    df.loc[:, "location"]  = COUNTRY
    df.loc[:, "date"]  = date

    # Add ISO codes
    df = ISODB().merge(df, country_iso=COUNTRY_ISO)
    df.loc[df["region"]=="Others", "location_iso"] = COUNTRY_ISO

    # Concat
    df_source = df_source.loc[~(df_source.loc[:, "date"] == date)]
    df = pd.concat([df, df_source])

    # Export
    export_data(
        df=df,
        data_url_reference=DATA_URL_REFERENCE,
        output_file=OUTPUT_FILE
    )

if __name__ == "__main__":
    main()