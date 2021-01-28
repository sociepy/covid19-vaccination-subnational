import pandas as pd
from utils import merge_iso

source_file = "data/countries/Austria.csv"


replace = {
    "Kärnten": "Karnten",
    "Niederösterreich": "Niederosterreich",
    "Oberösterreich": "Oberosterreich"
}


def main():
    # Load
    url = "https://info.gesundheitsministerium.gv.at/data/timeline.csv"
    df = pd.read_csv(
        url,
        sep=";",
        usecols=["Datum", "Name", "EingetrageneImpfungen", "Teilgeimpfte", "Vollimmunisierte"]
    )
    df = df.loc[df["Name"]!="Österreich"]

    # Rename columns
    df = df.rename(columns={
        "Datum": "date",
        "Name": "region",
        "EingetrageneImpfungen": "total_vaccinations",
        "Teilgeimpfte": "people_vaccinated",
        "Vollimmunisierte": "people_fully_vaccinated"
    })
    df.loc[:, "region"] = df.loc[:, "region"].replace(replace)

    # Column proccess
    df.loc[:, "date"] = df.date.str.slice(0, 10)
    df.loc[:, "location"] = "Austria"

    # Add ISO codes
    df = merge_iso(df, country_iso="AT")

    # Export
    df = df[["location", "region", "date", "location_iso", "region_iso", 
             "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv(source_file, index=False)


if __name__ == "__main__":
    main()