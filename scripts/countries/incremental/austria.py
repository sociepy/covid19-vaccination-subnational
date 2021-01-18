import pandas as pd
from datetime import datetime
from utils import merge_iso


source_file = "data/countries/Austria.csv"
replace = {
    "Kärnten": "Karnten",
    "Niederösterreich": "Niederosterreich",
    "Oberösterreich": "Oberosterreich"
}


def main():
    # Load current data
    df_source = pd.read_csv(source_file)
    
    # Load new data
    url = "https://info.gesundheitsministerium.gv.at/data/laender.csv"
    df = pd.read_csv(url, usecols=["Name", "Auslieferungen"], sep=";")
    # Get date
    date = df[df["Name"] == "Stand"]["Auslieferungen"].iloc[0]
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")

    if (date > df_source["date"].max()):
        # Renaming
        df = df.rename(columns={
            "Name": "region",
            "Auslieferungen": "total_vaccinations",
        })
        df.loc[:, "region"] = df.loc[:, "region"].replace(replace)
        # Remove rows
        df = df[~df["region"].isin(["Österreich", "Stand"])]
        # Add columns
        df.loc[:, "location"] = "Austria"
        df.loc[:, "date"] = date
        # Add ISO codes
        df = merge_iso(df, country_iso="AT")
        # Concat
        df = pd.concat([df, df_source])
        # Reorder
        df = df[["location", "region", "date", "location_iso", "region_iso", "total_vaccinations"]]
        df = df.sort_values(by=["region", "date"])
        df.to_csv(source_file, index=False)


if __name__ == "__main__":
    main()