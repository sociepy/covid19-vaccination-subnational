import pandas as pd
from utils import merge_iso


replace = {
    "BC": "British Columbia",
    "NL": "Newfoundland and Labrador", 
    "NWT": "Northwest Territories", 
    "PEI": "Prince Edward Island"
}


def main():
    url = "https://raw.githubusercontent.com/ccodwg/Covid19Canada/master/timeseries_prov/vaccine_administration_timeseries_prov.csv"
    df = pd.read_csv(url)

    df = df.rename(columns={
        "date_vaccine_administered": "date",
        "province": "region",
        "cumulative_avaccine": "total_vaccinations"
    })
    # Date
    df.loc[:, "date"] = pd.to_datetime(df.loc[:, "date"], format="%d-%m-%Y")
    df.loc[:, "date"] = df.loc[:, "date"].dt.strftime("%Y-%m-%d")
    # New cols
    df.loc[:, "region"] = df.loc[:, "region"].replace(replace)
    df.loc[:, "location"] = "Canada"
    # Add ISO codes
    df = merge_iso(df, country_iso="CA")
    # Reorder columns
    df = df[["location", "region", "date", "location_iso", "region_iso", "total_vaccinations"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv("data/countries/Canada.csv", index=False)


if __name__ == "__main__":
    main()