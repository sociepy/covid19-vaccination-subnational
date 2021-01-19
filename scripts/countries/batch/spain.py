import pandas as pd
from utils import merge_iso


replace = {
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
    url = "https://raw.githubusercontent.com/civio/covid-vaccination-spain/main/data.csv"
    df = pd.read_csv(url)
    df = df.rename(columns={
        "informe": "date",
        "comunidad autónoma": "region",
        "dosis administradas": "total_vaccinations",
        "personas con pauta completa": "people_fully_vaccinated"
    })
    df = df.astype({
        "total_vaccinations": str,
        "people_fully_vaccinated": str
    })
    df = df[~(df.loc[:, "region"]=="Totales")]
    df.loc[:, "region"] = df.loc[:, "region"].replace(replace)
    df.loc[:, "date"] = pd.to_datetime(df.loc[:, "date"], format="%d/%m/%Y")
    df.loc[:, "date"] = df.loc[:, "date"].dt.strftime("%Y-%m-%d")
    df.loc[:, "total_vaccinations"] = df.loc[:, "total_vaccinations"].apply(lambda x: int(x.replace(".", "")))
    df.loc[:, "people_fully_vaccinated"] = df.loc[:, "people_fully_vaccinated"].apply(
        lambda x: int(x.replace(".", "") if x != "nan" else 0)
    )
    df.loc[:, "people_vaccinated"] = df.loc[:, "total_vaccinations"] - df.loc[:, "people_fully_vaccinated"]
    df.loc[:, "location"] = "Spain"
    # Add ISO codes
    df = merge_iso(df, country_iso="ES")
    # Reorder columns
    df = df[["location", "region", "date", "location_iso", "region_iso", 
             "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv("data/countries/Spain.csv", index=False)


if __name__ == "__main__":
    main()