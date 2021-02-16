# -*- coding: utf-8 -*-
"""Update API v1 data files

files: api/v1/*/*/*.json
"""
import os
import argparse
import json
import pandas as pd


region_fields = ["region", "region_iso"]
data_fields = ["date", "total_vaccinations", "total_vaccinations_per_100"]
rename_fields = {"region": "region_name"}


def get_parser():
    parser = argparse.ArgumentParser(description="Update API files.")
    parser.add_argument(
        "input_vaccinations_path",
        type=str,
        help="Path to vaccinations data file.",
        default="data/countries"
    )
    parser.add_argument(
        "input_country_info_path",
        type=str,
        help="Path country info file.",
        default="data/country_info.csv"
    )
    parser.add_argument(
        "output_folder",
        type=str,
        help="Path to place all API files.",
        default="data/api/v1"
    )
    args = parser.parse_args()
    return parser


def build_api_json(df, country, country_iso, source):
    df = df[region_fields + data_fields]
    df = df.astype({"total_vaccinations": int})
    dfg = df.groupby(region_fields).apply(lambda x: x.drop(columns=region_fields).to_dict(orient="records"))
    dfg.name = "data"
    data = dfg.tolist()
    regions = dfg.index
    api_json_all = {
        "country": country,
        "country_iso": country_iso,
        "last_update": df["date"].max(),
        "first_update": df["date"].min(),
        "source_url": source,
        "data": [
            {
                "region_iso": region[1],
                "region_name": region[0],
                "data": data_sample
            } for region, data_sample in zip(regions, data)
        ]
    }
    dfg = df.groupby(region_fields)[data_fields].max()
    data = dfg.reset_index().rename(columns=rename_fields).to_dict(orient="records")
    api_json_latest = {
        "country": country,
        "country_iso": country_iso,
        "last_update": df["date"].max(),
        "source_url": source,
        "data": data
    }
    return api_json_all, api_json_latest


def main():
    parser = get_parser()
    args = parser.parse_args()

    export_folder_all = os.path.join(args.output_folder, "all/country_by_iso/")
    export_folder_latest = os.path.join(args.output_folder, "latest/country_by_iso/")
    api_endpoint = f"https://sociepy.org/covid19-vaccination-subnational/{args.output_folder}"

    # Load data
    df_country_info = pd.read_csv(args.input_country_info_path, index_col="country_iso")
    df_vaccinations = pd.read_csv(args.input_vaccinations_path)

    # Build and export JSONs
    metadata = []
    country_isos = df_country_info.index.tolist()
    for country_iso in country_isos:
        country, source = df_country_info.loc[country_iso, ["country", "data_source_url"]]
        print(f"  Generating API file for {country}...", sep=",")
        df_country = df_vaccinations[df_vaccinations["location_iso"] == country_iso]
        # Metadata
        metadata.append({
            "country_iso": country_iso,
            "country_name": country,
            "last_update": df_country["date"].max(),
            "first_update": df_country["date"].min(),
            "source_url": source,
            "api_url_all": f"{api_endpoint}/all/country_by_iso/{country_iso}.json",
            "api_url_latest": f"{api_endpoint}/latest/country_by_iso/{country_iso}.json"
        })
        # Build APIs (all + latest)
        api_json_all, api_json_latest = build_api_json(df_country, country, country_iso, source)
        # Export all
        path = os.path.join(export_folder_all, f"{country_iso}.json")
        with open(path, "w") as f:
            json.dump(api_json_all, f, indent=4)
        # Export latest
        path = os.path.join(export_folder_latest, f"{country_iso}.json")
        with open(path, "w") as f:
            json.dump(api_json_latest, f, indent=4)
    path = os.path.join(args.output_folder, f"metadata.json")
    print(f"Generating metadata file {path}...")
    with open(path, "w") as f:
        json.dump(metadata, f, indent=4)


if __name__ == "__main__":
    main()