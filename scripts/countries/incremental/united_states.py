import pandas as pd
import requests


source_file = "data/countries/United_States.csv"


def main():
    # Load current data
    df_source = pd.read_csv(source_file)
    
    # Load new data from API
    url = "https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=vaccination_data"
    data = requests.get(url).json()
    df = pd.DataFrame(
        data["vaccination_data"]
    ).fillna(0).astype({"Administered_Dose1": int, "Administered_Dose2": int})
    
    # Add data if new is available
    if (df["Date"].nunique()==1) & (df["Date"].min() > df_source["date"].max()):
        cols = ["LongName", "Date", "Administered_Dose1", "Administered_Dose2"]
        df = df[cols]
        # Process columns
        df.loc[:, "total_vaccinations"] = df.loc[:, "Administered_Dose1"] + df.loc[:, "Administered_Dose2"]
        df = df.rename(columns={
            "LongName": "region",
            "Date": "date",
            "Administered_Dose1": "people_vaccinated",
            "Administered_Dose2": "people_fully_vaccinated",
        })
        df = df[~df["region"].isin(["United States", "Long Term Care"])]
        df.loc[:, "country"] = "United States"
        df = df.loc[:, ["date", "country", "region", "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
        df = pd.concat([df, df_source])
        df.to_csv(source_file, index=False)


if __name__ == "__main__":
    main()