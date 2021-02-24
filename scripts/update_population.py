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
    parser = argparse.ArgumentParser(
        description="Update population data file with all regions in the project."
    )
    parser.add_argument(
        "input_path",
        type=str,
        help="Path to vaccination data file. Used to extract list of regions to get population for.",
        default="data/vaccination.csv",
    )
    parser.add_argument(
        "output_path",
        type=str,
        help="Path to population data file.",
        default="data/population.csv",
    )
    args = parser.parse_args()
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    #  Load new data
    df = pd.read_csv(args.input_path, index_col=False)
    df = df[df["region_iso"] != "-"]
    region_iso_list = df.loc[:, "region_iso"].unique()
    df = get_population(region_iso_list)
    #  Merge with current data
    if os.path.isfile(args.output_path):
        df_current = pd.read_csv(args.output_path, index_col=False)
        key = df.loc[:, "region_iso"].astype(str) + df.loc[:, "date"]
        df_current = df_current[
            ~(df_current["region_iso"].astype(str) + df_current["date"]).isin(key)
        ]
        df = pd.concat([df, df_current])
    #  Add extra TODO: move somewhere else (https://en.wikipedia.org/wiki/Regions_of_Iceland)
    iso_is = pd.DataFrame(
        {
            "region_iso": ["IS-1", "IS-3", "IS-5", "IS-6", "IS-5,IS-6"],
            "date": [
                "2021-02-20",
                "2021-02-20",
                "2021-02-20",
                "2021-02-20",
                "2021-02-20",
            ],
            "population": [233034, 16662, 7322, 30600, 30600 + 7322],
        }
    )
    iso_lb = pd.DataFrame(
        {
            "region_iso": ["LB-BA", "LB-BH", "LB-AK", "LB-AS"],
            "date": ["2014-12-30", "2015-06-30", "2015-06-30", "2015-06-30"],
            "population": [361366, 416427, 389899, 807204],
        }
    )
    df = pd.concat([df, iso_is, iso_lb])
    #  Export
    df.drop_duplicates()
    df = df[["region_iso", "date", "population"]]
    df = df.sort_values(by="region_iso")
    df = df.drop_duplicates()
    df.to_csv(args.output_path, index=False)


if __name__ == "__main__":
    main()
