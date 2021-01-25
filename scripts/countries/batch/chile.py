import numpy as np
import pandas as pd
from utils import merge_iso


source_file = "data/countries/Chile.csv"


replace = {
    "Araucanía": "La Araucania",
    "Aysén": "Aisen del General Carlos Ibanez del Campo",
    "Biobío": "Biobio",
    "Los Ríos": "Los Rios",
    "Tarapacá": "Tarapaca",
    "Valparaíso": "Valparaiso",
    "Ñuble": "Nuble",
    "O’Higgins": "Libertador General Bernardo O'Higgins",
    "Metropolitana": "Region Metropolitana de Santiago"
}


def load_data(url):
    # Get preliminari df
    df = pd.read_csv(url)
    df = df.loc[~(df["Region"] == "Total")]#.T
    cols  = df.columns[df.columns >= "2021-01-23"]
    df  = df[cols]
    
    # Get number of regions
    num_regions = df["Region"].nunique()
    
    # Get vaccine numbers
    df = df.sort_values(by=["Dose", "Region"]).set_index(["Dose", "Region"])
    people_vaccinated = df.loc["First"].values.T.reshape(-1, 1).squeeze()
    people_fully_vaccinated = df.loc["Second"].values.T.reshape(-1, 1).squeeze()
    total_vaccinations = people_vaccinated + people_fully_vaccinated
    
    # Build missing columns
    regions = df.loc["First"].index.tolist()
    num_dates = df.shape[1]
    dates = df.columns
    dates = list(np.repeat(dates, num_regions))
    regions = list(np.repeat(regions, num_dates))
    
    # Build DataFrame
    df = pd.DataFrame({
        "total_vaccinations": total_vaccinations,
        "people_vaccinated": people_vaccinated,
        "people_fully_vaccinated": people_fully_vaccinated,
        "date": dates,
        "region": regions
    })

    df.loc[: "location"] = "chile"
    
    return df


def main():
    # Load data
    url = "https://github.com/juancri/covid19-vaccination/raw/master/output/chile-vaccination.csv"
    df = load_data(url)

    # Replace region names
    df.loc[:, "region"] = df.loc[:, "region"].replace(replace)

    # ISO
    df = merge_iso(df, "CL")

    # Export
    df = df[["location", "region", "date", "location_iso", "region_iso", "total_vaccinations"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv(source_file, index=False)


if __name__ == "__main__":
    main()