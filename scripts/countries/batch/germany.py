import pandas as pd
from utils import merge_iso


replace = {
    "Baden-Württemberg": "Baden-Wurttemberg",
    "Thüringen": "Thuringen"
}


def main():
    url = "https://raw.githubusercontent.com/mathiasbynens/covid-19-vaccinations-germany/main/data/data.csv"
    df = pd.read_csv(url, usecols=["date", "state", "firstDosesCumulative", "secondDosesCumulative"])
    df = df.rename(columns={
        "state": "region",
        "firstDosesCumulative": "people_vaccinated",
        "secondDosesCumulative": "people_fully_vaccinated"
    })
    df.loc[:, "total_vaccinations"] = df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
    df.loc[:, "region"] = df.loc[:, "region"].replace(replace)
    df.loc[:, "date"] = pd.to_datetime(df.loc[:, "date"], format="%Y-%m-%d")
    df.loc[:, "date"] = df.loc[:, "date"].dt.strftime("%Y-%m-%d")
    df.loc[:, "location"] = "Germany"
    # Add ISO codes
    df = merge_iso(df, country_iso="DE")
    # Reorder columns
    df = df[["location", "region", "date", "location_iso", "region_iso", 
             "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv("data/countries/Germany.csv", index=False)


if __name__ == "__main__":
    main()