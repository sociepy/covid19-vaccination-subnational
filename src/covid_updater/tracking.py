"""Module to track references and updates."""
import os
import pandas as pd


this_directory = os.path.abspath(os.path.dirname(__file__))
COUNTRY_TRACKING_FILE = os.path.join(this_directory, "assets/country_tracking.csv")


def update_country_tracking(country, url, last_update, output_file=COUNTRY_TRACKING_FILE):
    """Update tracking info from a country.

    This includes last update and information source url.

    Args:
        country (str): Name of the country.
        url (str): Data source url.
        last_update (str): Date of last update.
    """
    if os.path.isfile(output_file):
        df = pd.read_csv(output_file)
    else:
        df = pd.DataFrame()
    df = df.append({
        "country": country,
        "data_source_url": url,
        "last_update":last_update
    }, ignore_index=True)
    df.to_csv(output_file, index=False)


def get_country_tracking(output_file=COUNTRY_TRACKING_FILE):
    """Load country tracking info.
    
    Returns:
        pandas.DataFrame: Country tracking info.
    """
    df = pd.read_csv(output_file)
    return df