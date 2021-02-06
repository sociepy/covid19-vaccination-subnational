"""Update population data

file: data/population.csv
"""


import qwikidata
import qwikidata.sparql
import pandas as pd
from covid_updater.population import get_population


def main():
    # Load new data
    df = pd.read_csv("data/vaccinations.csv", index_col=False)
    df = df[df["region_iso"] != "-"]
    region_iso_list = df.loc[:, "region_iso"].unique()
    df = get_population(region_iso_list)
    # Merge with current data
    df_current = pd.read_csv("data/population.csv", index_col=False)
    key = df.loc[:, "region_iso"].astype(str) + df.loc[:, "date"]
    df_current = df_current[~(df_current["region_iso"].astype(str) + df_current["date"]).isin(key)]
    df = pd.concat([df, df_current])
    # Export
    df.to_csv("data/population.csv", index=False)


if __name__ == "__main__":
    main()