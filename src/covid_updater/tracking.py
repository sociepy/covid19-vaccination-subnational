"""Module to track references and updates."""
import os
import pandas as pd


this_directory = os.path.abspath(os.path.dirname(__file__))
COUNTRY_TRACKING_FILE = os.path.join(this_directory, "assets/country_tracking.csv")


def update_country_tracking(country, url, last_update, second_dose, output_file=COUNTRY_TRACKING_FILE):
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
    else:
        s = pd.Series(
            data=[url, last_update, second_dose],
            index=["data_source_url", "last_update", "second_dose"],
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