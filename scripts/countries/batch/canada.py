import pandas as pd
from covid_updater.iso import merge_iso
from covid_updater.tracking import update_country_tracking


COUNTRY = "Canada"
COUNTRY_ISO = "CA"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL_1 = "https://raw.githubusercontent.com/ccodwg/Covid19Canada/master/timeseries_prov/vaccine_administration_timeseries_prov.csv"
DATA_URL_2 = "https://raw.githubusercontent.com/ccodwg/Covid19Canada/master/timeseries_prov/vaccine_completion_timeseries_prov.csv"
DATA_URL_REFERENCE = "https://github.com/ccodwg/Covid19Canada"
REGION_RENAMING = {
    "BC": "British Columbia",
    "NL": "Newfoundland and Labrador", 
    "NWT": "Northwest Territories", 
    "PEI": "Prince Edward Island"
}


def main():
    df = pd.read_csv(DATA_URL_1)

    df = df.rename(columns={
        "date_vaccine_administered": "date",
        "province": "region",
        "cumulative_avaccine": "total_vaccinations"
    })
    # Date
    df.loc[:, "date"] = pd.to_datetime(df.loc[:, "date"], format="%d-%m-%Y")
    df.loc[:, "date"] = df.loc[:, "date"].dt.strftime("%Y-%m-%d")
    # New cols
    df.loc[:, "region"] = df.loc[:, "region"].replace(REGION_RENAMING)
    df.loc[:, "location"] = COUNTRY
    # Add ISO codes
    df = merge_iso(df, country_iso=COUNTRY_ISO)
    # Add completed vaccinations
    df_2 = pd.read_csv(DATA_URL_2)

    df_2 = df_2.rename(columns={
        "date_vaccine_completed": "date",
        "province": "region",
        "cumulative_cvaccine": "people_fully_vaccinated"
    })
    # Date
    df_2.loc[:, "date"] = pd.to_datetime(df_2.loc[:, "date"], format="%d-%m-%Y")
    df_2.loc[:, "date"] = df_2.loc[:, "date"].dt.strftime("%Y-%m-%d")
    # New cols
    df_2.loc[:, "region"] = df_2.loc[:, "region"].replace(REGION_RENAMING)
    df = df.merge(df_2, on=["region", "date"], how="left")
    df.loc[:, "people_fully_vaccinated"] = df.loc[:, "people_fully_vaccinated"].fillna(0).astype(int)
    df.loc[:, "people_vaccinated"] = df.loc[:, "total_vaccinations"] - df.loc[:, "people_fully_vaccinated"].astype(int)
    # Reorder columns
    df = df[["location", "region", "date", "location_iso", "region_iso", 
             "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv(OUTPUT_FILE, index=False)

    # Tracking
    update_country_tracking(
        country=COUNTRY,
        url=DATA_URL_REFERENCE,
        last_update=df["date"].max()
    )


if __name__ == "__main__":
    main()