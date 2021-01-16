import pandas as pd
from datetime import datetime


source_file = "data/countries/Austria.csv"


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
        # Remove rows
        df = df[~df["region"].isin(["Österreich", "Stand"])]
        # Add columns
        df.loc[:, "country"] = "Austria"
        df.loc[:, "date"] = date.strftime("%Y-%m-%d")
        # Export
        df = df[["date", "country", "region", "total_vaccinations"]]
        df = pd.concat([df, df_source])
        df.to_csv(source_file, index=False)


if __name__ == "__main__":
    main()