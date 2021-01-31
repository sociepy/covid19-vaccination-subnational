import os
import pandas as pd


this_directory = os.path.abspath(os.path.dirname(__file__))
ISO_ORIGINAL_FILE = os.path.join(this_directory, "assets/IP2LOCATION-ISO3166-2.CSV")
ISO_NEW_FILE = os.path.join(this_directory, "assets/ISO_3166_2.csv")


def merge_iso(df, country_iso):
    """Merge input dataframe with ISOs, using region as join field.

    Args:
        df (pandas.DataFrame): ISO data.
        country_iso (str): Country ISO code

    Returns:
        pandas.DataFrame: Joined table.
    """
    df_iso = load_iso()
    df_iso_country = df_iso[df_iso["location_iso"]==country_iso]
    df = df.merge(df_iso_country, left_on="region", right_on="subdivision_name", how="left")
    df["region_iso"] = df[["region_iso"]].fillna("-")
    df = df.drop(columns=["subdivision_name"])
    return df


def load_iso():
    """Load ISO file.

    Returns:
        pandas.DataFrame: ISO codes as DataFrame.
    """
    return pd.read_csv(ISO_NEW_FILE)


def generate_iso():
    """Update ISO file."""
    df_iso = pd.read_csv(ISO_ORIGINAL_FILE)
    df_iso = df_iso.rename(columns={
        "country_code": "location_iso",
        "code": "region_iso"
    })
    # Change names
    iso_replace = {
        "Friuli-Venezia Giulia": "Friuli Venezia Giulia",
        "Brussels Hoofdstedelijk Gewest": "Brussels"
    }
    df_iso.loc[:, "subdivision_name"] = df_iso.loc[:, "subdivision_name"].replace(iso_replace)

    # Add new elements
    new_items = [
        ["IT", "IT-TN", "Provincia autonoma di Trento"],
        ["IT", "IT-BZ", "Provincia autonoma di Bolzano - Alto Adige"],
        ["FR", "FR-RE", "La Reunion"],
        ["FR", "FR-YT", "Mayotte"],
        ["BE", "BE-VLG", "Flanders"],
        ["BE", "BE-WAL", "Wallonia"],
        ["US", "US-AS", "American Samoa"],
        ["US", "US-GU", "Guam"],
        ["US", "US-VI", "Virgin Islands"],
        ["US", "US-MP", "Northern Mariana Islands"],
        ["FR", "FR-MQ", "Martinique"],
        ["FR", "FR-GP", "Guadeloupe"],
        ["FR", "FR-GF", "Guyane"],
        ["NO", "NO-46", "Vestland"],
        ["NO", "NO-42", "Agder"],
        ["NO", "NO-30", "Viken"],
        ["NO", "NO-54", "Troms og Finnmark"],
        ["NO", "NO-50", "Trondelag"],
        ["NO", "NO-38", "Vestfold og Telemark"],
        ["NO", "NO-34", "Innlandet"],
        ["CL", "CL-NB", "Nuble"]
    ]
    new_items = pd.DataFrame(new_items, columns=["location_iso", "region_iso", "subdivision_name"])
    df_iso = df_iso.append(new_items, ignore_index=True)
    df_iso = df_iso.sort_values(["location_iso", "region_iso"])
    df_iso.to_csv(ISO_NEW_FILE, index=False)
