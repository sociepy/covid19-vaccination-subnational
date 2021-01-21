import pandas as pd
from utils import merge_iso


source_file = "data/countries/Slovakia.csv"


replace = {
    "Trenčiansky kraj": "Trenciansky kraj",
    "Banskobystrický kraj": "Banskobystricky kraj",
    "Bratislavský kraj": "Bratislavsky kraj",
    "Košický kraj": "Kosicky kraj",
    "Nitriansky kraj": "Nitriansky kraj",
    "Prešovský kraj": "Presovsky kraj",
    "Trnavský kraj": "Trnavsky kraj",
    "Žilinský kraj": "Zilinsky kraj"
}


def main():
    # Load data
    url = "https://raw.githubusercontent.com/Institut-Zdravotnych-Analyz/covid19-data/main/OpenData_Slovakia_Vaccination_Regions.csv"
    df = pd.read_csv(url, sep=";")

    df = df.rename(columns={
        "Date": "date",
        "Region": "region",
        "first_dose": "people_vaccinated",
        "second_dose": "people_fully_vaccinated"
    })

    df.loc[:, "total_vaccinations"] = df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
    df.loc[:, "region"] = df.loc[:, "region"].replace(replace)
    df.loc[:, "location"] = "Slovakia"

    # Get iso codes
    df = merge_iso(df, "SK")

    # Export
    df = df[["location", "region", "date", "location_iso", "region_iso",
             "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv(source_file, index=False)


if __name__ == "__main__":
    main()