import urllib
import pandas as pd
from datetime import datetime
from covid_updater.utils import read_xlsx_from_url, export_data
from covid_updater.iso import ISODB


COUNTRY = "Belgium"
COUNTRY_ISO = "BE"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://covid-vaccinatie.be/en/vaccines-administered.xlsx"
DATA_URL_REFERENCE = "https://covid-vaccinatie.be/en"


def main():
    # Load
    df = read_xlsx_from_url(DATA_URL)

    # Rename
    df = df.rename(
        columns={
            "Date": "date",
            "Region": "region",
            "1st dose": "people_vaccinated",
            "2nd dose": "people_fully_vaccinated",
        }
    )

    # Remove NaN regions
    df = df.loc[~df.loc[:, "region"].isnull()]

    #  Process
    df.loc[:, "people_fully_vaccinated"] = (
        df.loc[:, "people_fully_vaccinated"].fillna(0).astype(int)
    )
    df.loc[:, "total_vaccinations"] = (
        df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
    )
    df.loc[:, "location"] = COUNTRY
    df.loc[:, "date"] = df.loc[:, "date"].apply(
        lambda x: datetime.strptime(x, "%d/%m/%Y").strftime("%Y-%m-%d")
    )

    # Cumsum
    df = df.sort_values(by="date")
    df["people_vaccinated"] = df.groupby("region")["people_vaccinated"].cumsum().values
    df["people_fully_vaccinated"] = (
        df.groupby("region")["people_fully_vaccinated"].cumsum().values
    )
    df["total_vaccinations"] = (
        df.groupby("region")["total_vaccinations"].cumsum().values
    )

    #  ISO
    df = ISODB().merge(df, country_iso=COUNTRY_ISO)

    #  Export
    export_data(df=df, data_url_reference=DATA_URL_REFERENCE, output_file=OUTPUT_FILE)


if __name__ == "__main__":
    main()
