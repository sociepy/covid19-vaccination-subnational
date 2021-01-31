import numpy as np
import pandas as pd
from covid_updater.iso import ISODB
from covid_updater.tracking import update_country_tracking
from covid_updater.utils import export_data


COUNTRY = "Chile"
COUNTRY_ISO = "CL"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://github.com/juancri/covid19-vaccination/raw/master/output/chile-vaccination.csv"
DATA_URL_REFERENCE = "https://github.com/juancri/covid19-vaccination/"
REGION_RENAMING = {
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
    df = pd.read_csv(DATA_URL)
    df = df.loc[~(df["Region"] == "Total")]#.T
    cols  = df.columns[df.columns >= "2021-01-23"]
    df  = df[cols]
    
    # Get number of regions
    num_regions = df["Region"].nunique()
    
    # Get vaccine numbers
    df = df.sort_values(by=["Dose", "Region"]).set_index(["Dose", "Region"])
    people_vaccinated = df.loc["First"].values.reshape(-1, 1).squeeze()
    people_fully_vaccinated = df.loc["Second"].values.reshape(-1, 1).squeeze()
    total_vaccinations = people_vaccinated + people_fully_vaccinated
    
    # Build missing columns
    regions = df.loc["First"].index.tolist()
    num_dates = df.shape[1]
    dates = df.columns
    dates = dates.tolist() * num_regions
    regions = list(np.repeat(regions, num_dates))
    
    # Build DataFrame
    df = pd.DataFrame({
        "total_vaccinations": total_vaccinations,
        "people_vaccinated": people_vaccinated,
        "people_fully_vaccinated": people_fully_vaccinated,
        "date": dates,
        "region": regions
    })

    df.loc[:, "location"] = COUNTRY
    
    return df


def main():
    # Load data
    df = load_data(DATA_URL)

    # Replace region names
    df.loc[:, "region"] = df.loc[:, "region"].replace(REGION_RENAMING)

    # ISO
    df = ISODB().merge(df, country_iso=COUNTRY_ISO)

    # Export
    export_data(
        df=df,
        data_url_reference=DATA_URL_REFERENCE,
        output_file=OUTPUT_FILE
    )


if __name__ == "__main__":
    main()