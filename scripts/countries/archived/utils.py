import pandas as pd


def merge_iso(df, country_iso):
    df_iso = pd.read_csv("scripts/countries/input/ISO_3166_2.csv")
    df_iso_country = df_iso[df_iso["location_iso"]==country_iso]
    df = df.merge(df_iso_country, left_on="region", right_on="subdivision_name", how="left")
    df["region_iso"] = df[["region_iso"]].fillna("-")
    df = df.drop(columns=["subdivision_name"])
    return df