import pandas as pd
from covid_updater.iso import merge_iso
from covid_updater.tracking import update_country_tracking
from covid_updater.utils import keep_min_date


COUNTRY = "Italy"
COUNTRY_ISO = "IT"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-summary-latest.csv"
DATA_URL_REFERENCE = "https://github.com/italia/covid19-opendata-vaccini/"
REGION_RENAMING = {
    "ABR": "Abruzzo",
    "VEN": "Veneto",
    "UMB": "Umbria",
    "TOS": "Toscana",
    "SIC": "Sicilia",
    "SAR": "Sardegna",
    "PUG": "Puglia",
    "PIE": "Piemonte",
    "PAT": "Provincia autonoma di Trento",
    "PAB": "Provincia autonoma di Bolzano - Alto Adige",
    "MOL": "Molise",
    "VDA": "Valle d'Aosta",
    "LOM": "Lombardia",
    "LIG": "Liguria",
    "LAZ": "Lazio",
    "FVG": "Friuli Venezia Giulia",
    "EMR": "Emilia-Romagna",
    "CAM": "Campania",
    "CAL": "Calabria",
    "BAS": "Basilicata",
    "MAR": "Marche"
}


def main():
    df = pd.read_csv(DATA_URL, parse_dates=["data_somministrazione"])
    df = df.rename(columns={
        "data_somministrazione": "date",
        "area": "region",
        "totale": "total_vaccinations",
        "prima_dose": "people_vaccinated",
        "seconda_dose": "people_fully_vaccinated"
    })
    df.loc[:, "date"] = pd.to_datetime(df.loc[:, "date"], format="%Y-%m-%d")
    df.loc[:, "date"] = df.loc[:, "date"].dt.strftime("%Y-%m-%d")
    df.loc[:, "location"] = COUNTRY
    # Compute cumsums
    df = df.sort_values(by="date")
    df["total_vaccinations"] = df.groupby("region")["total_vaccinations"].cumsum().values
    df["people_vaccinated"] = df.groupby("region")["people_vaccinated"].cumsum().values
    df["people_fully_vaccinated"] = df.groupby("region")["people_fully_vaccinated"].cumsum().values
    df = df[df.loc[:, "region"] != "ITA"]
    # Add ISO codes
    df.loc[:, "region"] = df.loc[:, "region"].replace(REGION_RENAMING)
    df = merge_iso(df, country_iso=COUNTRY_ISO)
    
    # Avoid repeating reports
    df = keep_min_date(df)
    
    # Export
    df = df[["location", "region", "date", "location_iso", "region_iso", 
             "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv(OUTPUT_FILE, index=False)

    # Tracking
    update_country_tracking(
        country=COUNTRY,
        url=DATA_URL_REFERENCE,
        last_update=df["date"].max()
    )

if __name__ == "__main__":
    main()