"""Update vaccinations file with population data.

Adds metrics relative to region population.
"""
import argparse
import pandas as pd


def get_parser():
    parser = argparse.ArgumentParser(description="Merge all country data into single csv file.")
    parser.add_argument(
        "input_vaccination_path",
        type=str,
        help="Path to vaccination data file."
    )
    parser.add_argument(
        "input_population_path",
        type=str,
        help="Path to population data file."
    )
    args = parser.parse_args()
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    print("Adding indices relative to population")

    # Load data
    df_pop = pd.read_csv(args.input_population_path, index_col=False)
    df_pop = df_pop.loc[df_pop["date"]==df_pop["date"].max(), ["region_iso", "population"]]
    df_vac = pd.read_csv(args.input_vaccination_path, index_col=False)

    df = df_vac.merge(df_pop, on="region_iso", how="left")

    columns = ["total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]
    for column in columns:
        df.loc[:, f"{column}_per_100"] = (100*df.loc[:, column]/df.loc[:, "population"]).apply(lambda x: round(x, 2))

    df = df.drop(columns=["population"])
    df = df.sort_values(by=["location", "region", "date"])
    df.to_csv(args.input_vaccination_path, index=False)