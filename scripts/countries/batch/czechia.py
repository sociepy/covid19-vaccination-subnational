import pandas as pd
from utils import merge_iso


source_file = "data/countries/Czechia.csv"


rename = {
    "Hlavní město Praha": "Praha, Hlavni mesto",
    "Jihomoravský kraj": "Jihomoravsky kraj",
    "Moravskoslezský kraj": "Moravskoslezsky kraj",
    "Ústecký kraj": "Ustecky kraj",
    "Středočeský kraj": "Stredocesky kraj",
    "Plzeňský kraj": "Plzensky kraj",
    "Pardubický kraj": "Pardubicky kraj",
    "Olomoucký kraj": "Olomoucky kraj",
    "Zlínský kraj": "Zlinsky kraj",
    "Královéhradecký kraj": "Kralovehradecky kraj",
    "Kraj Vysočina": "Kraj Vysocina",
    "Karlovarský kraj": "Karlovarsky kraj",
    "Jihočeský kraj": "Jihocesky kraj",
    "Liberecký kraj": "Liberecky kraj"
}


def main():
    # Load data
    url = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani.csv"
    df = pd.read_csv(url)

    # Check 1
    cols = ["datum", "vakcina", "kraj_nuts_kod", "kraj_nazev", "vekova_skupina", "prvnich_davek", "druhych_davek", "celkem_davek"]
    if not all([col in df.columns for col in cols]):
        raise Exception("API changed")

    # Column renaming
    df = df.rename(columns={
        "datum": "date",
        "kraj_nazev": "region",
        "prvnich_davek": "people_vaccinated",
        "druhych_davek": "people_fully_vaccinated",
        "celkem_davek": "total_vaccinations"
    })

    # Add counts per day
    df = df.groupby(by=["date", "region"]).agg(
        people_vaccinated=("people_vaccinated", sum),
        people_fully_vaccinated=("people_fully_vaccinated", sum),
        total_vaccinations=("total_vaccinations", sum)
    ).reset_index()

    # Check 2
    if not (df["total_vaccinations"] == df["people_vaccinated"] + df["people_fully_vaccinated"]).all():
        raise Exception("Error in columns. dose_1 + dose_2 != total_doses")

    # Rename regions
    df.loc[:, "region"] = df.loc[:, "region"].replace(rename)
    df.loc[:, "location"] = "Czechia"

    # ISO
    df = merge_iso(df, "CZ")

    # Compute cumsums
    df = df.sort_values(by="date")
    df.loc[:, "total_vaccinations"] = df.groupby("region")["total_vaccinations"].cumsum().values
    df.loc[:, "people_vaccinated"] = df.groupby("region")["people_vaccinated"].cumsum().values
    df.loc[:, "people_fully_vaccinated"] = df.groupby("region")["people_fully_vaccinated"].cumsum().values

    # Export
    df = df[["location", "region", "date", "location_iso", "region_iso", 
             "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv(source_file, index=False)


if __name__ == "__main__":
    main()