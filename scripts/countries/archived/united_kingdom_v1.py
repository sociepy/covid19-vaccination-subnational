import pandas as pd
from covid_updater.iso import ISODB
from covid_updater.utils import export_data


COUNTRY = "United Kingdom"
COUNTRY_ISO = "GB"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv".replace(" ", "_")
DATA_URL = "https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&metric=cumPeopleVaccinatedFirstDoseByPublishDate&metric=cumPeopleVaccinatedSecondDoseByPublishDate&metric=cumPeopleVaccinatedCompleteByPublishDate&format=csv"
DATA_URL_REFERENCE = "https://coronavirus.data.gov.uk/details/download"


def main():
    df = pd.read_csv(DATA_URL)
    df = df.rename(columns={
        "areaName": "region",
        "cumPeopleVaccinatedFirstDoseByPublishDate": "people_vaccinated",
        "cumPeopleVaccinatedSecondDoseByPublishDate": "people_fully_vaccinated"
    })
    df.loc[:, "location"] = COUNTRY
    df.loc[:, "total_vaccinations"] = df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]

    # Add ISO codes
    df = ISODB().merge(df, country_iso=COUNTRY_ISO)
    
    # Export
    export_data(
        df=df,
        data_url_reference=DATA_URL_REFERENCE,
        output_file=OUTPUT_FILE
    )


if __name__ == "__main__":
    main()