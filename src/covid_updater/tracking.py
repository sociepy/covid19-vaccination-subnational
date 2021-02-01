"""Module to track references and updates."""
import os
import pandas as pd
import flag


this_directory = os.path.abspath(os.path.dirname(__file__))
COUNTRY_TRACKING_FILE = os.path.join(this_directory, "assets/country_tracking.csv")
README_FILE = os.path.join(this_directory, "assets/README.template.md")


def update_country_tracking(country, country_iso, url, last_update, second_dose, output_file=COUNTRY_TRACKING_FILE):
    """Update tracking info from a country.

    This includes last update and information source url.

    Args:
        country (str): Name of the country.
        url (str): Data source url.
        last_update (str): Date of last update.
        second_dose (int): 1 if second dose is being tracked, 0 otherwise.
    """
    # Load tracking file
    if os.path.isfile(output_file):
        df = pd.read_csv(output_file, index_col="country")
    else:
        df = pd.DataFrame()
    # Update/Add country entry
    if country in df.index:
        df.loc[country, "data_source_url"] = url
        df.loc[country, "last_update"] = last_update
        df.loc[country, "second_dose"] = second_dose
        df.loc[country, "country_iso"] = country_iso
    else:
        s = pd.Series(
            data=[country_iso, url, last_update, second_dose],
            index=["country_iso", "data_source_url", "last_update", "second_dose"],
            name=country
        )
        df = df.append(s)
    df.to_csv(output_file)


def get_country_tracking(output_file=COUNTRY_TRACKING_FILE):
    """Load country tracking info.
    
    Returns:
        pandas.DataFrame: Country tracking info.
    """
    df = pd.read_csv(output_file)
    return df


def tracking_csv_as_md():
    # Load tracking csv
    df = pd.read_csv(COUNTRY_TRACKING_FILE)

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


def generate_readme(output_file):
    # Load table
    table_md = tracking_csv_as_md()

    # Export README
    with open(README_FILE, "r") as f:
        readme = f.read()
    readme = readme.format(data_sources=table_md)
    with open(output_file, "w") as f:
        f.write(readme)