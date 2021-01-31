import pandas as pd
from covid_updater.iso import merge_iso
from covid_updater.tracking import update_country_tracking
from covid_updater.utils import keep_min_date


COUNTRY = "Germany"
COUNTRY_ISO = "DE"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://raw.githubusercontent.com/mathiasbynens/covid-19-vaccinations-germany/main/data/data.csv"
DATA_URL_REFERENCE = "https://github.com/mathiasbynens/covid-19-vaccinations-germany/"
REGION_RENAMING = {
    "Baden-Württemberg": "Baden-Wurttemberg",
    "Thüringen": "Thuringen"
}


def main():
    df = pd.read_csv(DATA_URL, usecols=["date", "state", "firstDosesCumulative", "secondDosesCumulative"])
    df = df.rename(columns={
        "state": "region",
        "firstDosesCumulative": "people_vaccinated",
        "secondDosesCumulative": "people_fully_vaccinated"
    })
    df.loc[:, "total_vaccinations"] = df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
    df.loc[:, "region"] = df.loc[:, "region"].replace(REGION_RENAMING)
    df.loc[:, "date"] = pd.to_datetime(df.loc[:, "date"], format="%Y-%m-%d")
    df.loc[:, "date"] = df.loc[:, "date"].dt.strftime("%Y-%m-%d")
    df.loc[:, "location"] = COUNTRY
    # Add ISO codes
    df = merge_iso(df, country_iso=COUNTRY_ISO)

    # Avoid repeating reports
    df = keep_min_date(df)

    # Export
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