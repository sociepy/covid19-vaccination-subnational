import pandas as pd
from covid_updater.iso import ISODB
from covid_updater.tracking import update_country_tracking
from covid_updater.utils import export_data


COUNTRY_CH = "Switzerland"
COUNTRY_ISO_CH = "CH"
OUTPUT_FILE_CH = f"data/countries/{COUNTRY_CH}.csv"
COUNTRY_LI = "Liechtenstein"
COUNTRY_ISO_LI = "LI"
OUTPUT_FILE_LI = f"data/countries/{COUNTRY_LI}.csv"
DATA_URL = "https://github.com/rsalzer/COVID_19_VACC/raw/main/data.csv"
DATA_URL_REFERENCE = "https://github.com/rsalzer/COVID_19_VACC/"


def main_ch(df):
    # Switzerland
    df_ch = df.loc[~df.loc[:, "region_iso"].isin(["CHFL", "FL"])].reset_index(drop=True)

    # Process columns
    df_ch.loc[:, "region_iso"] = f"{COUNTRY_ISO_CH}-" + df_ch.loc[:, "region_iso"]
    df_ch.loc[:, "location"] = COUNTRY_CH

    # Get region names
    df_ch = ISODB().merge(df_ch, mode="region")

    # Export
    export_data(
        df=df_ch,
        data_url_reference=DATA_URL_REFERENCE,
        output_file=OUTPUT_FILE_CH
    )


def main_li(df):
    # Liechestein
    df_li = df.loc[df.loc[:, "region_iso"] == "FL"].reset_index(drop=True)
    df_li.loc[:, "region_iso"] = df_li.loc[:, "region_iso"].replace({"FL": COUNTRY_LI})
    df_li.loc[:, "location"] = COUNTRY_LI
    df_li.loc[:, "location_iso"] = COUNTRY_ISO_LI
    df_li.loc[:, "region"] = "-"

    # Export
    export_data(
        df=df_li,
        data_url_reference=DATA_URL_REFERENCE,
        output_file=OUTPUT_FILE_LI
    )


def main():
    df = pd.read_csv(DATA_URL, usecols=["geounit", "date", "ncumul_vacc"])
    df = df.rename(columns={
        "geounit": "region_iso",
        "ncumul_vacc": "total_vaccinations"
    })

    main_ch(df)
    main_li(df)


if __name__ == "__main__":
    main()