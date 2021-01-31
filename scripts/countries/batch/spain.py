import pandas as pd
from covid_updater.iso import merge_iso
from covid_updater.tracking import update_country_tracking
from covid_updater.utils import keep_min_date


COUNTRY = "Spain"
COUNTRY_ISO = "ES"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://raw.githubusercontent.com/civio/covid-vaccination-spain/main/data.csv"
DATA_URL_REFERENCE = "https://github.com/civio/covid-vaccination-spain/"
REGION_RENAMING = {
    "Andalucía": "Andalucia",
    "Aragón": "Aragon",
    "Asturias": "Asturias, Principado de",
    "Baleares": "Illes Balears",
    "C. Valenciana": "Valenciana, Comunidad",
    "Castilla La Mancha": "Castilla-La Mancha",
    "Cataluña": "Catalunya",
    "Madrid": "Madrid, Comunidad de",
    "Murcia": "Murcia, Region de",
    "Navarra": "Navarra, Comunidad Foral de",
    "País Vasco": "Pais Vasco",
}


def main():
    df = pd.read_csv(DATA_URL, dtype={"personas con pauta completa": str})
    df = df.rename(columns={
        "informe": "date",
        "comunidad autónoma": "region",
        "dosis administradas": "total_vaccinations",
        "personas con pauta completa": "people_fully_vaccinated"
    })
    df.loc[:, "people_fully_vaccinated"] = df.loc[:, "people_fully_vaccinated"].fillna("nan")

    df = df.astype({
        "total_vaccinations": str,
        "people_fully_vaccinated": str
    })

    df = df[~(df.loc[:, "region"]=="Totales")]
    df.loc[:, "region"] = df.loc[:, "region"].replace(REGION_RENAMING)
    df.loc[:, "date"] = pd.to_datetime(df.loc[:, "date"], format="%d/%m/%Y")
    df.loc[:, "date"] = df.loc[:, "date"].dt.strftime("%Y-%m-%d")
    df.loc[:, "total_vaccinations"] = df.loc[:, "total_vaccinations"].apply(lambda x: int(x.replace(".", "")))
    df.loc[:, "people_fully_vaccinated"] = df.loc[:, "people_fully_vaccinated"].apply(
        lambda x: int(x.replace(".", "") if x != "nan" else 0)
    )
    df.loc[:, "people_vaccinated"] = df.loc[:, "total_vaccinations"] - df.loc[:, "people_fully_vaccinated"]
    df.loc[:, "location"] = COUNTRY
    # Add ISO codes
    df = merge_iso(df, country_iso=COUNTRY_ISO)
    
    # Export
    df = df[["location", "region", "date", "location_iso", "region_iso", 
             "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
    df = keep_min_date(df)
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