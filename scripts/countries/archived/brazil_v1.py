"""
https://github.com/owid/covid-19-data/blob/master/scripts/scripts/vaccinations/automations/incremental/brazil.py
"""
import pandas as pd
from covid_updater.iso import ISODB
from covid_updater.utils import export_data


COUNTRY = "Brazil"
COUNTRY_ISO = "BR"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv"
DATA_URL_REFERENCE = "https://github.com/wcota/covid19br/"


def main():
    # Get data
    df = pd.read_csv(DATA_URL, usecols=["state", "date", "vaccinated"])
    df = df.rename(columns={
        "vaccinated": "total_vaccinations"
    })

    # Get data after vaccination started
    start_date =  "2021-01-18"
    df = df.loc[df["date"] >= start_date]

    # Process vaccinations
    df.loc[:, "total_vaccinations"] = df.loc[:, "total_vaccinations"].fillna(0).astype(int)

    # Get region iso
    df = df[~(df.loc[:, "state"]=="TOTAL")]
    df.loc[:, "region_iso"] = f"{COUNTRY_ISO}-" + df.loc[:, "state"]

    # Get region name
    df = ISODB().merge(df, mode="region")
    df.loc[:, "location"] = COUNTRY

    # Export
    export_data(
        df=df,
        data_url_reference=DATA_URL_REFERENCE,
        output_file=OUTPUT_FILE
    )

if __name__ == "__main__":
    main()