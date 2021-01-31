import pandas as pd
from covid_updater.iso import ISODB
from covid_updater.tracking import update_country_tracking
from covid_updater.utils import export_data


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
    df = df.loc[df["Name"] != "Österreich"]

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
    df = ISODB().merge(df, country_iso=COUNTRY_ISO)

    # Export
    export_data(
        df=df,
        data_url_reference=DATA_URL_REFERENCE,
        output_file=OUTPUT_FILE
    )


if __name__ == "__main__":
    main()