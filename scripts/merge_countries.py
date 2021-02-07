"""Inspired by OWID repo:

https://github.com/owid/covid-19-data/blob/master/scripts/scripts/vaccinations/run_python_scripts.py

Example: Merge data/countries/*.csv data into data/accinations.csv file
"""
import os
from datetime import datetime
from glob import glob
import argparse
import pandas as pd


def get_parser():
    parser = argparse.ArgumentParser(description="Merge all country data into single csv file.")
    parser.add_argument(
        "input_data_folder",
        type=str,
        help="Path where all country data is placed."
    )
    parser.add_argument(
        "output_path",
        type=str,
        help="Path to file to export merged data."
    )
    args = parser.parse_args()
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    
    # Load country data
    files = [
        pd.read_csv(os.path.join(args.input_data_folder, f)) \
            for f in os.listdir(path=args.input_data_folder) if f.endswith(f".csv")
    ]
    df = pd.concat(files)

    # Process data
    colnames = ["total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]
    df.loc[:, colnames] = df.loc[:, colnames].astype("Int64")

    # Export
    df = df.sort_values(by=["location", "region", "date"])
    df.to_csv(args.output_path, index=False)


if __name__ == "__main__":
    main()
