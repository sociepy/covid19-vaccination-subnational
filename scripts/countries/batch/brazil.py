"""
https://github.com/owid/covid-19-data/blob/master/scripts/scripts/vaccinations/automations/incremental/brazil.py
"""
import pandas as pd
from covid_updater.iso import load_iso
from covid_updater.tracking import update_country_tracking
from covid_updater.utils import keep_min_date


COUNTRY = "Brazil"
COUNTRY_ISO = "BR"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv"
DATA_URL_REFERENCE = "https://github.com/wcota/covid19br/"


def main():
    # ISO df
    df_iso = load_iso()

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
    df = df.merge(df_iso, on="region_iso")
    df = df.rename(columns={
        "subdivision_name": "region"
    })
    df.loc[:, "location"] = COUNTRY

    # Avoid repeating reports
    df = keep_min_date(df)

    # Export
    df = df[["location", "region", "date", "location_iso", "region_iso", "total_vaccinations"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv(OUTPUT_FILE, index=False)

    # Tracking
    update_country_tracking(
        country=COUNTRY,
        url=DATA_URL_REFERENCE,
        last_update=df["date"].max()
    )

if __name__ == "__main__":
    main()