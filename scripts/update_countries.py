# -*- coding: utf-8 -*-
"""Update country data."""


import os
import argparse
from covid_updater.scraping import get_country_scraper


ISO_CODES = [
    "AR",
    "AT",
    "AU",
    # "BE",
    "BR",
    "CA",
    "CL",
    "CZ",
    "DK",
    "FR",
    "DE",
    "IN",
    "IS",
    "IT",
    "NO",
    # "PL",
    "SK",
    "ES",
    # "SE",
    "CH",
    "US",
    "GB",
    "PE",
    "TR",
    "LB",
    "RU",
    "FI",
    "KR",
    "UY",
]
ISO_CODES.sort()
OUTPUT_PATH = os.path.join("data", "countries")


def get_parser():
    parser = argparse.ArgumentParser(description="Update country data.")
    parser.add_argument(
        "output_data_folder",
        type=str,
        help="Path to folder to export country csv data.",
        default="data/countries/",
    )
    parser.add_argument(
        "output_info_path",
        type=str,
        help="Path to file to export source info data file.",
        default="data/country_info.csv",
    )
    args = parser.parse_args()
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    for iso_code in ISO_CODES:
        scraper = get_country_scraper(iso_code=iso_code)
        print(scraper.country)
        try:
            scraper.run(
                output_file_data=os.path.join(
                    args.output_data_folder, f"{scraper.filename}.csv"
                ),
                output_file_info=args.output_info_path,
            )
        except Exception as e:
            print("error in updating : "+scraper.country)
            print(e)


if __name__ == "__main__":
    main()
