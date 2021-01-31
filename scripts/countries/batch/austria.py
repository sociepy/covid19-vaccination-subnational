import pandas as pd
from covid_updater.iso import merge_iso
from covid_updater.tracking import update_country_tracking


COUNTRY = "Austria"
COUNTRY_ISO = "AT"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://info.gesundheitsministerium.gv.at/data/timeline.csv"
DATA_URL_REFERENCE = "https://info.gesundheitsministerium.gv.at/"
REGION_RENAMING = {
    "Kärnten": "Karnten",
    "Niederösterreich": "Niederosterreich",
    "Oberösterreich": "Oberosterreich"
}


def main():
    # Load
    df = pd.read_csv(
        DATA_URL,
        sep=";",
        usecols=["Datum", "Name", "EingetrageneImpfungen", "Teilgeimpfte", "Vollimmunisierte"]
    )
    df = df.loc[df["Name"]!="Österreich"]

    # Rename columns
    df = df.rename(columns={
        "Datum": "date",
        "Name": "region",
        "EingetrageneImpfungen": "total_vaccinations",
        "Teilgeimpfte": "people_vaccinated",
        "Vollimmunisierte": "people_fully_vaccinated"
    })
    df.loc[:, "region"] = df.loc[:, "region"].replace(REGION_RENAMING)

    # Column proccess
    df.loc[:, "date"] = df.date.str.slice(0, 10)
    df.loc[:, "location"] = COUNTRY

    # Add ISO codes
    df = merge_iso(df, country_iso=COUNTRY_ISO)

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