"""Module to track references and updates."""
import os
import pandas as pd
import flag


def country_api_links_as_md(country_info_path, api_url):
    # Load tracking csv
    df = pd.read_csv(country_info_path)
    df = df.sort_values("country")

    #  Prettify country + flag
    flags = df["country_iso"].apply(lambda x: flag.flag(x))
    df.loc[:, "Country"] = flags + " " + df.loc[:, "country"]

    #  Build df
    url_base = f"{api_url}/{{mode}}/country_by_iso/{{iso}}.json"
    df["All data"] = df.country_iso.apply(
        lambda x: "[link]({url})".format(url=url_base.format(mode="all", iso=x))
    )
    df["Latest data"] = df.country_iso.apply(
        lambda x: "[link]({url})".format(url=url_base.format(mode="latest", iso=x))
    )
    df = df[["Country", "All data", "Latest data"]]

    # Get markdown
    return df.to_markdown(index=False)


def country_info_csv_as_md(country_info_path):
    # Load tracking csv
    df = pd.read_csv(country_info_path)

    # Process columns
    df.loc[:, "second_dose"] = df.loc[:, "second_dose"].apply(
        lambda x: "✅" if x == 1 else "❌"
    )
    df.loc[:, "data_source_url"] = df.loc[:, "data_source_url"].apply(
        lambda x: f"[{x}]({x})"
    )

    # Rename + Reorder columns
    df = df.rename(
        columns={
            "country": "Country",
            "data_source_url": "Source",
            "second_dose": "2-Dose",
            "last_update": "Last update",
        }
    )

    # Add flag
    flags = df["country_iso"].apply(lambda x: flag.flag(x))
    df.loc[:, "Country"] = flags + " " + df.loc[:, "Country"]

    #  Reorder columns
    df = df[["Country", "Source", "2-Dose", "Last update"]]
    df = df.sort_values("Last update", ascending=False)

    # Get markdown
    table_md = df.to_markdown(index=False)
    return table_md


def generate_readme(input_country_info, input_readme_template, output_readme):
    #  Load table
    table_md = country_info_csv_as_md(country_info_path=input_country_info)

    # Export README
    with open(input_readme_template, "r") as f:
        readme = f.read()
    readme = readme.format(data_sources=table_md)
    with open(output_readme, "w") as f:
        f.write(readme)


def generate_api_links(
    api_url, input_country_info, input_api_links_template, output_api_links
):
    #  Load table
    table_md = country_api_links_as_md(
        country_info_path=input_country_info, api_url=api_url
    )

    # Export API LINKS
    with open(input_api_links_template, "r") as f:
        api_links = f.read()
    api_links = api_links.format(table=table_md)
    with open(output_api_links, "w") as f:
        f.write(api_links)
