# -*- coding: utf-8 -*-
"""Update population data.

file: data/population.csv
"""


import os
import argparse
import qwikidata
import qwikidata.sparql
import pandas as pd
from covid_updater.population import get_population


def get_parser():
    parser = argparse.ArgumentParser(description="Merge all country data into single csv file.")
    parser.add_argument(
        "input_path",
        type=str,
        help="Path to vaccination data file. Used to extract list of regions to get population for.",
        default="data/vaccination.csv"
    )
    parser.add_argument(
        "output_path",
        type=str,
        help="Path to population data file.",
        default="data/population.csv"
    )
    args = parser.parse_args()
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    # Load new data
    df = pd.read_csv(args.input_path, index_col=False)
    df = df[df["region_iso"] != "-"]
    region_iso_list = df.loc[:, "region_iso"].unique()
    df = get_population(region_iso_list)
    # Merge with current data
    if os.path.isfile(args.output_path):
        df_current = pd.read_csv(args.output_path, index_col=False)
        key = df.loc[:, "region_iso"].astype(str) + df.loc[:, "date"]
        df_current = df_current[~(df_current["region_iso"].astype(str) + df_current["date"]).isin(key)]
        df = pd.concat([df, df_current])
    # Export
    df.drop_duplicates()
    df = df[["region_iso", "date", "population"]]
    df = df.sort_values(by="region_iso")
    df.to_csv(args.output_path, index=False)


if __name__ == "__main__":
    main()