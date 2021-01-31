import pandas as pd
from covid_updater.iso import merge_iso
from covid_updater.tracking import update_country_tracking
from covid_updater.utils import keep_min_date


COUNTRY = "Slovakia"
COUNTRY_ISO = "SK"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://raw.githubusercontent.com/Institut-Zdravotnych-Analyz/covid19-data/main/OpenData_Slovakia_Vaccination_Regions.csv"
DATA_URL_REFERENCE = "https://github.com/Institut-Zdravotnych-Analyz/covid19-data/"
REGION_RENAMING = {
    "Trenčiansky kraj": "Trenciansky kraj",
    "Banskobystrický kraj": "Banskobystricky kraj",
    "Bratislavský kraj": "Bratislavsky kraj",
    "Košický kraj": "Kosicky kraj",
    "Nitriansky kraj": "Nitriansky kraj",
    "Prešovský kraj": "Presovsky kraj",
    "Trnavský kraj": "Trnavsky kraj",
    "Žilinský kraj": "Zilinsky kraj"
}


def main():
    # Load data
    df = pd.read_csv(DATA_URL, sep=";")

    df = df.rename(columns={
        "Date": "date",
        "Region": "region",
        "first_dose": "people_vaccinated",
        "second_dose": "people_fully_vaccinated"
    })

    # Cumsum
    df = df.sort_values(by="date")
    df["people_vaccinated"] = df.groupby("region")["people_vaccinated"].cumsum().values
    df["people_fully_vaccinated"] = df.groupby("region")["people_fully_vaccinated"].cumsum().values

    # Add columns
    df.loc[:, "total_vaccinations"] = df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
    df.loc[:, "region"] = df.loc[:, "region"].replace(REGION_RENAMING)
    df.loc[:, "location"] = COUNTRY

    # Get iso codes
    df = merge_iso(df, COUNTRY_ISO)

    # Avoid repeating reports
    df = keep_min_date(df)

    # Export
    df = df[["location", "region", "date", "location_iso", "region_iso",
             "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
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