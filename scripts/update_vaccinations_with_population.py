# -*- coding: utf-8 -*-
"""Update vaccinations file with population data.

Adds metrics relative to region population.
"""
import argparse
import pandas as pd


def get_parser():
    parser = argparse.ArgumentParser(
        description="Update vaccination data with population-related metrics."
    )
    parser.add_argument(
        "input_vaccination_path", type=str, help="Path to vaccination data file."
    )
    parser.add_argument(
        "input_population_path", type=str, help="Path to population data file."
    )
    args = parser.parse_args()
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    print("Adding indices relative to population")

    # Load population data
    df_pop = pd.read_csv(args.input_population_path, index_col=False)
    df_pop = df_pop.drop_duplicates()
    # Get latest population value for each region
    df_dates = pd.DataFrame(df_pop.groupby("region_iso").date.max()).reset_index()
    df_pop = df_pop.merge(df_dates, on=["region_iso", "date"])[
        ["region_iso", "population"]
    ]
    # Join vaccination + population data
    df_vac = pd.read_csv(args.input_vaccination_path, index_col=False)
    df = df_vac.merge(df_pop, on="region_iso", how="left")

    columns = ["total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]
    for column in columns:
        df.loc[:, f"{column}_per_100"] = (
            100 * df.loc[:, column] / df.loc[:, "population"]
        ).apply(lambda x: round(x, 2))

    #  Process data
    df.loc[:, columns] = df.loc[:, columns].astype("Int64")
    df = df.drop(columns=["population"])
    df = df.sort_values(by=["location", "region", "date"])
    df.to_csv(args.input_vaccination_path, index=False)


if __name__ == "__main__":
    main()
