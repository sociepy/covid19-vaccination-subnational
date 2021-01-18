import pandas as pd
from utils import merge_iso


def main():
    url = "https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&metric=cumPeopleVaccinatedFirstDoseByPublishDate&metric=cumPeopleVaccinatedSecondDoseByPublishDate&metric=cumPeopleVaccinatedCompleteByPublishDate&format=csv"
    df = pd.read_csv(url)
    df = df.rename(columns={
        "areaName": "region",
        "cumPeopleVaccinatedFirstDoseByPublishDate": "people_vaccinated",
        "cumPeopleVaccinatedSecondDoseByPublishDate": "people_fully_vaccinated"
    })
    df.loc[:, "location"] = "United Kingdom"
    df.loc[:, "total_vaccinations"] = df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
    # Add ISO codes
    df = merge_iso(df, country_iso="GB")
    # Reorder columns
    df = df[["location", "region", "date", "location_iso", "region_iso",
             "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv("data/countries/United_Kingdom.csv", index=False)


if __name__ == "__main__":
    main()