import pandas as pd
import requests
from utils import merge_iso


source_file = "data/countries/United_States.csv"
replace = {
    "New York State": "New York"
}


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
        df.loc[:, "region"] = df.loc[:, "region"].replace(replace)
        df.loc[:, "date"] = pd.to_datetime(df.loc[:, "date"], format="%Y-%m-%d")
        df.loc[:, "date"] = df.loc[:, "date"].dt.strftime("%Y-%m-%d")
        df = df[~df["region"].isin(["United States", "Long Term Care"])]
        df.loc[:, "location"] = "United States"
        # Add ISO codes
        df = merge_iso(df, country_iso="US")
        df.loc[df["region"]=="Federated States of Micronesia", "location_iso"] = "FM"
        df.loc[df["region"]=="Marshall Islands", "location_iso"] = "MH"
        df.loc[df["region"]=="Puerto Rico", "location_iso"] = "PR"
        df.loc[df["region"]=="Republic of Palau", "location_iso"] = "PW"
        df.loc[df["region"]=="Bureau of Prisons", "location_iso"] = "US"
        df.loc[df["region"]=="Dept of Defense", "location_iso"] = "US"
        df.loc[df["region"]=="Indian Health Svc", "location_iso"] = "US"
        df.loc[df["region"]=="Veterans Health", "location_iso"] = "US"
        # Concat
        df = pd.concat([df, df_source])
        # Reorder columns
        df = df[["location", "region", "date", "location_iso", "region_iso",
                 "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
        df = df.sort_values(by=["region", "date"])
        df.to_csv(source_file, index=False)


if __name__ == "__main__":
    main()