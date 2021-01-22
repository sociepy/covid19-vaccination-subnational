"""
https://github.com/owid/covid-19-data/blob/master/scripts/scripts/vaccinations/automations/incremental/brazil.py
"""
import pandas as pd


source_file = "data/countries/Brazil.csv"


def main():
    # ISO df
    df_iso = pd.read_csv("scripts/countries/input/ISO_3166_2.csv")

    # Get data
    url = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv"
    df = pd.read_csv(url, usecols=["state", "date", "vaccinated"])
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
    df.loc[:, "region_iso"] = "BR-" + df.loc[:, "state"]

    # Get region name
    df = df.merge(df_iso, on="region_iso")
    df = df.rename(columns={
        "subdivision_name": "region",
    })
    df.loc[:, "location"] = "Brazil"

    # Export
    df = df[["location", "region", "date", "location_iso", "region_iso", "total_vaccinations"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv(source_file, index=False)


if __name__ == "__main__":
    main()