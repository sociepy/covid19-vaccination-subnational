"""Module to track references and updates."""
import os
import pandas as pd
import flag


def country_info_csv_as_md(country_info_path):
    # Load tracking csv
    df = pd.read_csv(country_info_path)

    # Process columns
    df.loc[:, "second_dose"] = df.loc[:, "second_dose"].apply(lambda x: "✅" if x==1 else "❌")
    df.loc[:, "data_source_url"] = df.loc[:, "data_source_url"].apply(lambda x: f"[{x}]({x})")

    # Rename + Reorder columns
    df = df.rename(columns={
        "country": "Country",
        "data_source_url": "Source",
        "second_dose": "2-Dose",
        "last_update": "Last update"
    })

    # Add flag
    flags = df["country_iso"].apply(lambda x: flag.flag(x))
    df.loc[:, "Country"] = flags + " " + df.loc[:, "Country"]

    # Reorder columns
    df = df[["Country", "Source", "2-Dose", "Last update"]]
    df = df.sort_values("Last update", ascending=False)

    # Get markdown
    table_md = df.to_markdown(index=False)
    return table_md


def generate_readme(input_country_info, input_readme_template, output_readme):
    # Load table
    table_md = country_info_csv_as_md(country_info_path=input_country_info)

    # Export README
    with open(input_readme_template, "r") as f:
        readme = f.read()
    readme = readme.format(data_sources=table_md)
    with open(output_readme, "w") as f:
        f.write(readme)