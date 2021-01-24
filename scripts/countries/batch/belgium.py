import urllib.request
import pandas as pd
from utils import merge_iso


source_file = "data/countries/Belgium.csv"


def download_xlsx(url, tmp_file="tmp/belgium.xlsx"):
    local_tmp_file = "tmp/belgium.xlsx"
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686)"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
    with open(local_tmp_file, "wb") as f:
        f.write(the_page)
    df = pd.read_excel(local_tmp_file)
    return df


def main():
    # Load data
    url = "https://covid-vaccinatie.be/en/vaccines-administered.xlsx"
    df = download_xlsx(url)

    # Rename columns
    df = df.rename(columns={
        "Date": "date",
        "Region": "region",
        "Doses administered": "total_vaccinations"
    })

    # Process columns
    df.loc[:, "location"] = "Belgium"
    df.loc[:, "date"] = pd.to_datetime(df.loc[:, "date"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")

    # Remove NaNs
    df = df.loc[~df.loc[:, "region"].isnull()]

    # Iso
    df = merge_iso(df, country_iso="BE")

    # Export
    df = df[["location", "region", "date", "location_iso", "region_iso", "total_vaccinations"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv(source_file, index=False)


if __name__ == "__main__":
    main()