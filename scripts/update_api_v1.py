"""Update API v1 data files

files: api/v1/*/*/*.json
"""
import os
import json
from glob import glob
import pandas as pd


region_fields = ["region", "region_iso"]
data_fields = ["date", "total_vaccinations"]
rename_fields = {"region": "region_name"}
export_folder = "data/api/v1"
export_folder_all = f"{export_folder}/all/country_by_iso/"
export_folder_latest =f"{export_folder}/latest/country_by_iso/"
api_endpoint = f"https://sociepy.org/covid19-vaccination-subnational/{export_folder}"


def build_api_json(df, country, country_iso, source):
    df = df[region_fields + data_fields]

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
    metadata = []
    countries_path = [f for f in glob("data/countries/*") if f.endswith(".csv")]
    country_tracking = pd.read_csv("src/covid_updater/assets/country_tracking.csv")
    for country_path in countries_path:
        print(country_path)
        # Load
        df = pd.read_csv(country_path)
        country_iso = df["location_iso"].value_counts().index.tolist()[0]
        country = df["location"].value_counts().index.tolist()[0]
        source = country_tracking.loc[country_tracking["country_iso"] == country_iso, "data_source_url"].values[0]
        # Process
        print(f"Generating API file for {country}...", sep=",")
        api_json_all, api_json_latest = build_api_json(df, country, country_iso, source)
        # Export all
        path = os.path.join(export_folder_all, f"{country_iso}.json")
        with open(path, "w") as f:
            json.dump(api_json_all, f, indent=4)
        # Export latest
        path = os.path.join(export_folder_latest, f"{country_iso}.json")
        with open(path, "w") as f:
            json.dump(api_json_latest, f, indent=4)
        
        metadata.append({
            "country_iso": country_iso,
            "country_name": country,
            "last_update": df["date"].max(),
            "first_update": df["date"].min(),
            "source_url": source,
            "api_url_all": f"{api_endpoint}/all/{country_iso}.json",
            "api_url_latest": f"{api_endpoint}/latest/country_by_iso/{country_iso}.json"
        })

    path = os.path.join(export_folder, f"metadata.json")
    print(f"Generating metadata file {path}...")
    with open(path, "w") as f:
        json.dump(metadata, f, indent=4)


if __name__ == "__main__":
    main()