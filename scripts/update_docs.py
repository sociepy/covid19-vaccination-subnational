# -*- coding: utf-8 -*-
import argparse
import pandas as pd
from covid_updater.docs import generate_readme


def get_parser():
    parser = argparse.ArgumentParser(description="Merge all country data into single csv file.")
    parser.add_argument(
        "input_country_info_path",
        type=str,
        help="Path to country info file.",
        default="data/vaccination.csv"
    )
    parser.add_argument(
        "input_readme_template_path",
        type=str,
        help="Path to README template file.",
        default="data/vaccination.csv"
    )
    parser.add_argument(
        "output_readme_path",
        type=str,
        help="Path to to-be-generated README.",
        default="data/population.csv"
    )
    args = parser.parse_args()
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    generate_readme(
        input_country_info=args.input_country_info_path,
        input_readme_template=args.input_readme_template_path,
        output_readme=args.output_readme_path
    )


if __name__ == "__main__":
    main()