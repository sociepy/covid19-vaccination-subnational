import pandas as pd
from covid_updater.iso import load_iso
from covid_updater.tracking import update_country_tracking


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
    df_iso = load_iso()
    df_ch = df_ch.merge(df_iso, on="region_iso")
    df_ch = df_ch.rename(columns={
        "subdivision_name": "region",
    })

    # Export
    df_ch = df_ch[["location", "region", "date", "location_iso", "region_iso", "total_vaccinations"]]
    df_ch = df_ch.sort_values(by=["region", "date"])
    df_ch.to_csv(OUTPUT_FILE_CH, index=False)

    # Tracking
    update_country_tracking(
        country=COUNTRY_CH,
        url=DATA_URL_REFERENCE,
        last_update=df["date"].max()
    )


def main_li(df):
    # Liechestein
    df_li = df.loc[df.loc[:, "region_iso"] == "FL"].reset_index(drop=True)
    df_li.loc[:, "region_iso"] = df_li.loc[:, "region_iso"].replace({"FL": COUNTRY_LI})
    df_li.loc[:, "location"] = COUNTRY_LI
    df_li.loc[:, "location_iso"] = COUNTRY_ISO_LI
    df_li.loc[:, "region"] = "-"

    df_li = df_li[["location", "region", "date", "location_iso", "region_iso", "total_vaccinations"]]
    df_li = df_li.sort_values(by=["region", "date"])
    df_li.to_csv(OUTPUT_FILE_LI, index=False)

    # Tracking
    update_country_tracking(
        country=COUNTRY_LI,
        url=DATA_URL_REFERENCE,
        last_update=df["date"].max()
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