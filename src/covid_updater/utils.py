import os
import urllib.request
import pandas as pd
from covid_updater.tracking import update_country_tracking, generate_readme


project_dir = os.path.abspath(os.path.join(__file__, "../../.."))
COLUMNS_ALL = ["location", "region", "date", "location_iso", "region_iso", 
             "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]
COLUMNS_ORDER = ["region", "date"]
COLUMNS_INT = ["total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]


def read_xlsx_from_url(url, tmp_file="tmp/file.xlsx"):
    """Download and load xls file from URL.

    Args:
        url (str): File url.
        tmp_file (str, optional): Local temporal filename. Defaults to "tmp/file.xlsx".

    Returns:
        pandas.DataFrame: Data loaded.
    """
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686)"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
    try:
        with open(tmp_file, "wb") as f:
            f.write(the_page)
    except:
        raise Exception("Make sure that folders leading to `tmp_file` exist. You may try to create a folder named" + \
                        "`tmp` in the project root directory and re-run this.")
    df = pd.read_excel(tmp_file)
    return df


def keep_min_date(df):
    df = df.copy()
    cols = df.columns
    # Remove NaNs
    count_cols = [col for col in COLUMNS_INT if col in cols]
    df.loc[:, count_cols] = df.loc[:, count_cols].fillna(-1).astype(int)
    # Goup by    
    df = df.groupby(
        by=[col for col in df.columns if col != "date"]
    ).min().reset_index()

    # Bring NaNs back
    df.loc[:, count_cols] = df.loc[:, count_cols].astype("Int64").replace({-1: pd.NA})
    return df.loc[:, cols]


def export_data(df, data_url_reference, output_file):
    locations = df["location"].unique().tolist()
    if len(locations) != 1:
        raise Exception("More than one country detected!")
    country_iso = df["location_iso"].value_counts().index.tolist()[0]
    country = locations[0]
    last_update = df["date"].max()
    second_dose = int("people_fully_vaccinated" in df.columns)

    # Reorder columns
    cols = [col for col in COLUMNS_ALL if col in df.columns]
    df = df[cols]

    # Avoid repeating reports
    df = keep_min_date(df)

    # Ensure Int types
    count_cols = [col for col in COLUMNS_INT if col in cols]
    df[count_cols] = df[count_cols].astype("Int64").fillna(pd.NA)

    # Export
    df = df.sort_values(by=COLUMNS_ORDER)
    df.to_csv(output_file, index=False)

    # Tracking
    update_country_tracking(
        country=country,
        country_iso=country_iso,
        url=data_url_reference,
        last_update=last_update,
        second_dose=second_dose
    )

    # Update readme
    generate_readme(output_file=os.path.join(project_dir, "README.md"))