import pandas as pd


def main_ch(df):
    # Switzerland
    df_ch = df.loc[~df.loc[:, "region_iso"].isin(["CHFL", "FL"])].reset_index(drop=True)

    # Process columns
    df_ch.loc[:, "region_iso"] = "CH-" + df_ch.loc[:, "region_iso"]
    df_ch.loc[:, "location"] = "Switzerland"

    # Get region names
    df_iso = pd.read_csv("scripts/countries/input/ISO_3166_2.csv")
    df_ch = df_ch.merge(df_iso, on="region_iso")
    df_ch = df_ch.rename(columns={
        "subdivision_name": "region",
    })

    # Export
    df_ch = df_ch[["location", "region", "date", "location_iso", "region_iso", "total_vaccinations"]]
    df_ch = df_ch.sort_values(by=["region", "date"])
    df_ch.to_csv("data/countries/Switzerland.csv", index=False)


def main_li(df):
    # Liechestein
    df_li = df.loc[df.loc[:, "region_iso"] == "FL"].reset_index(drop=True)
    df_li.loc[:, "region_iso"] = df_li.loc[:, "region_iso"].replace({"FL": "LI"})
    df_li.loc[:, "location"] = "Liechtenstein"
    df_li.loc[:, "location_iso"] = "LI"
    df_li.loc[:, "region"] = "-"

    df_li = df_li[["location", "region", "date", "location_iso", "region_iso", "total_vaccinations"]]
    df_li = df_li.sort_values(by=["region", "date"])
    df_li.to_csv("data/countries/Liechtenstein.csv", index=False)


def main():
    url = "https://github.com/rsalzer/COVID_19_VACC/raw/main/data.csv"
    df = pd.read_csv(url, usecols=["geounit", "date", "ncumul_vacc"])
    df = df.rename(columns={
        "geounit": "region_iso",
        "ncumul_vacc": "total_vaccinations"
    })

    main_ch(df)
    main_li(df)


if __name__ == "__main__":
    main()