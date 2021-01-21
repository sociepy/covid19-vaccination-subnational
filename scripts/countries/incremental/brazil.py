"""
https://github.com/owid/covid-19-data/blob/master/scripts/scripts/vaccinations/automations/incremental/brazil.py
"""
import pandas as pd


source_file = "data/countries/Brazil.csv"


def main():
    # Load current data
    df_source = pd.read_csv(source_file)

    # ISO df
    df_iso = pd.read_csv("scripts/countries/input/ISO_3166_2.csv")

    # Get data
    url = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-total.csv"
    df = pd.read_csv(url, usecols=["state", "date", "vaccinated"])
    df = df.rename(columns={
        "vaccinated": "total_vaccinated"
    })
    # Get region iso
    df = df[~(df.loc[:, "state"]=="TOTAL")]
    df.loc[:, "region_iso"] = "BR-" + df.loc[:, "state"]

    # Get region name
    df = df.merge(df_iso, on="region_iso")
    df = df.rename(columns={
        "subdivision_name": "region",
    })
    df.loc[:, "location"] = "Brazil"

    # Export
    regions = df["region"].tolist()
    dates = df["date"].tolist()
    df_source = df_source.loc[~((df_source["region"].isin(regions)) & (df_source["date"].isin(dates)))]
    df = pd.concat([df, df_source])
    df = df[["location", "region", "date", "location_iso", "region_iso", "total_vaccinations"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv(source_file, index=False)


if __name__ == "__main__":
    main()