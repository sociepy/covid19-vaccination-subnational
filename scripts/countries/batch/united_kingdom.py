import pandas as pd
from covid_updater.iso import merge_iso
from covid_updater.tracking import update_country_tracking


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
    df = merge_iso(df, country_iso=COUNTRY_ISO)
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