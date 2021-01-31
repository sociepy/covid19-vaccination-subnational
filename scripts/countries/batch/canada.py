import pandas as pd
from covid_updater.iso import ISODB
from covid_updater.utils import export_data


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
    COLUMNS_RENAMING = {
        "date_vaccine_administered": "date",
        "province": "region",
        "cumulative_avaccine": "total_vaccinations"
    }
    df = pd.read_csv(DATA_URL_1, usecols=COLUMNS_RENAMING.keys())
    df = df.rename(columns=COLUMNS_RENAMING)
    # Date
    df.loc[:, "date"] = pd.to_datetime(df.loc[:, "date"], format="%d-%m-%Y")
    df.loc[:, "date"] = df.loc[:, "date"].dt.strftime("%Y-%m-%d")
    # New cols
    df.loc[:, "region"] = df.loc[:, "region"].replace(REGION_RENAMING)
    df.loc[:, "location"] = COUNTRY
    # Add ISO codes
    df = ISODB().merge(df, country_iso=COUNTRY_ISO)

    
    # Add completed vaccinations
    COLUMNS_RENAMING = {
        "date_vaccine_completed": "date",
        "province": "region",
        "cumulative_cvaccine": "people_fully_vaccinated"
    }
    df_2 = pd.read_csv(DATA_URL_2, usecols=COLUMNS_RENAMING.keys())
    df_2 = df_2.rename(columns=COLUMNS_RENAMING)
    # Date
    df_2.loc[:, "date"] = pd.to_datetime(df_2.loc[:, "date"], format="%d-%m-%Y")
    df_2.loc[:, "date"] = df_2.loc[:, "date"].dt.strftime("%Y-%m-%d")
    # New cols
    df_2.loc[:, "region"] = df_2.loc[:, "region"].replace(REGION_RENAMING)
    df = df.merge(df_2, on=["region", "date"], how="left")
    df.loc[:, "people_fully_vaccinated"] = df.loc[:, "people_fully_vaccinated"].fillna(0).astype(int)
    df.loc[:, "people_vaccinated"] = df.loc[:, "total_vaccinations"] - df.loc[:, "people_fully_vaccinated"].astype(int)

    # Export
    export_data(
        df=df,
        data_url_reference=DATA_URL_REFERENCE,
        output_file=OUTPUT_FILE
    )


if __name__ == "__main__":
    main()