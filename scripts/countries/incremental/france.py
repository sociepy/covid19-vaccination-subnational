import pandas as pd
from covid_updater.iso import ISODB
from covid_updater.utils import export_data


COUNTRY = "France"
COUNTRY_ISO = "FR"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://www.data.gouv.fr/fr/datasets/r/9b1e6c8c-7e1d-47f9-9eb9-f2eeaab60d99"
DATA_URL_REFERENCE = "https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-personnes-vaccinees-contre-la-covid-19-1/"
REGION_RENAMING = {
    1 : "Guadeloupe",
    2 : "Martinique",
    3: "Guyane",
    4: "La Reunion",
    6: "Mayotte",
    11: "Ile-de-France",
    24: "Centre-Val de Loire",
    27: "Bourgogne-Franche-Comte",
    28 : "Normandie",
    32: "Hauts-de-France",
    44: "Grand-Est",
    52: "Pays-de-la-Loire",
    53: "Bretagne",
    75: "Nouvelle-Aquitaine",
    76 : "Occitanie",
    84: "Auvergne-Rhone-Alpes",
    93: "Provence-Alpes-Cote-d'Azur",
    94: "Corse",
}


def main():
    # Load current data
    df_source = pd.read_csv(OUTPUT_FILE)

    # Load new data
    df = pd.read_csv(DATA_URL)
    df = df.rename(columns={
        "reg": "region",
        "jour": "date",
        "n_tot_dose1": "people_vaccinated",
        "n_tot_dose2": "people_fully_vaccinated"
    })

    # Rename regions + Get rid of unknown region 7
    df.loc[:, "region"] = df.loc[:, "region"].replace(REGION_RENAMING)
    df = df[df["region"]!=7]

    # Process columns
    df["people_fully_vaccinated"] = df["people_fully_vaccinated"].astype("Int64").fillna(pd.NA)
    df["total_vaccinations"] = df["people_fully_vaccinated"] + df["people_vaccinated"]
    df.loc[:, "location"] = "France"

    # ISO
    df = ISODB().merge(df, country_iso="FR")

    # Concat
    key = df["region"].astype(str) + df["date"]
    df_source = df_source[~(df_source["region"].astype(str) + df_source["date"]).isin(key)]
    df = pd.concat([df, df_source])

    # Export
    export_data(
        df=df,
        data_url_reference=DATA_URL_REFERENCE,
        output_file=OUTPUT_FILE
    )


if __name__ == "__main__":
    main()