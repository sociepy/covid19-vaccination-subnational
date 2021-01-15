import pandas as pd


area_mapping = {
    "ABR": "Abruzzo",
    "VEN": "Veneto",
    "UMB": "Umbria",
    "TOS": "Toscana",
    "SIC": "Sicilia",
    "SAR": "Sardegna",
    "PUG": "Puglia",
    "PIE": "Piemonte",
    "PAT": "Provincia Autonoma di Trento",
    "PAB": "Provincia Autonoma di Bolzano",
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
    url = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-summary-latest.csv"
    df = pd.read_csv(url, parse_dates=["data_somministrazione"])
    df = df.rename(columns={
        "data_somministrazione": "date",
        "area": "region",
        "totale": "total_vaccinations"
    })
    df.loc[:, "country"] = "Italy"
    df.loc[:, "date"] = df.loc[:, "date"].dt.strftime("%Y-%m-%d")
    # Compute total_vaccination (cumsum)
    df = df.sort_values(by="date")
    df["total_vaccinations"] = df.groupby("region")["total_vaccinations"].cumsum().values
    df = df[df.loc[:, "region"] != "ITA"]
    # Replace area codes with area names
    df["region"] = df["region"].replace(area_mapping)
    df = df.loc[:, ["date", "country", "region", "total_vaccinations"]]
    df.to_csv("output/countries/Italy.csv", index=False)


if __name__ == "__main__":
    main()