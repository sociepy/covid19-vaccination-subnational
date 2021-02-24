# -*- coding: utf-8 -*-
import argparse
import pandas as pd
from covid_updater.docs import generate_readme, generate_api_links


def get_parser():
    parser = argparse.ArgumentParser(description="Update docs.")
    parser.add_argument(
        "input_country_info_path", type=str, help="Path to country info file."
    )
    parser.add_argument(
        "input_readme_template_path", type=str, help="Path to README template file."
    )
    parser.add_argument(
        "input_api_links_template", type=str, help="Path to API LINKs template file."
    )
    parser.add_argument(
        "output_readme_path", type=str, help="Path to to-be-generated README."
    )
    parser.add_argument(
        "output_api_links",
        type=str,
        help="Path to to-be-generated API LINK file.",
        default="data/population.csv",
    )
    parser.add_argument(
        "api_url", type=str, help="API url.", default="data/population.csv"
    )
    args = parser.parse_args()
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    generate_readme(
        input_country_info=args.input_country_info_path,
        input_readme_template=args.input_readme_template_path,
        output_readme=args.output_readme_path,
    )

    generate_api_links(
        api_url=args.api_url,
        input_country_info=args.input_country_info_path,
        input_api_links_template=args.input_api_links_template,
        output_api_links=args.output_api_links,
    )


if __name__ == "__main__":
    main()
