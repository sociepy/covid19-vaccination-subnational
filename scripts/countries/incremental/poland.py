import requests
import json
import pytz
import datetime
import pandas as pd
from covid_updater.iso import ISODB
from covid_updater.utils import export_data


COUNTRY = "Poland"
COUNTRY_ISO = "PL"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://services9.arcgis.com/RykcEgwHWuMsJXPj/arcgis/rest/services/wojewodztwa_szczepienia_widok3/" + \
          "FeatureServer/0/query?f=json&where=1=1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields" + \
          "=*&orderByFields=SZCZEPIENIA_DZIENNIE desc&resultOffset=0&resultRecordCount=16&resultType=standard&cacheHint=true"
DATA_URL_REFERENCE = "https://www.gov.pl/web/szczepimysie/raport-szczepien-przeciwko-covid-19"
REGION_RENAMING = {
    "dolnośląskie": "Dolnoslaskie",
    "kujawsko-pomorskie": "Kujawsko-pomorskie",
    "lubelskie": "Lubelskie",
    "lubuskie": "Lubuskie",
    "mazowieckie": "Mazowieckie",
    "małopolskie": "Malopolskie",
    "opolskie": "Opolskie",
    "podkarpackie": "Podkarpackie",
    "podlaskie": "Podlaskie",
    "pomorskie": "Pomorskie",
    "warmińsko-mazurskie": "Warminsko-mazurskie",
    "wielkopolskie": "Wielkopolskie",
    "zachodniopomorskie": "Zachodniopomorskie",
    "łódzkie": "Lodzkie",
    "śląskie": "Slaskie",
    "świętokrzyskie": "Swietokrzyskie"
}


def load_data(url):
    dix = json.loads(requests.get(url).content)
    feats = [d["attributes"] for d in dix["features"]]
    df = pd.DataFrame(feats)
    return df


def main():
    # Load current data
    df_source = pd.read_csv(OUTPUT_FILE)

    # Load data
    df = load_data(DATA_URL)

    # Process columns
    df = df.rename(columns={
        "jpt_nazwa_": "region",
        "SZCZEPIENIA_SUMA": "total_vaccinations",
        "DAWKA_2_SUMA": "people_fully_vaccinated"
    })
    df.loc[:, "location"] = COUNTRY
    date = datetime.datetime.now(pytz.timezone("Europe/Warsaw")).date().strftime("%Y-%m-%d")
    df.loc[:, "date"] = date
    df.loc[:, "people_vaccinated"] = df.loc[:, "total_vaccinations"] - df.loc[:, "people_fully_vaccinated"]
    df.loc[:, "region"] = df.loc[:, "region"].replace(REGION_RENAMING)
    
    # ISO
    df = ISODB().merge(df, country_iso=COUNTRY_ISO)
    
    # Concat
    df_source = df_source.loc[~(df_source.loc[:, "date"] == date)]
    df = pd.concat([df, df_source])

    # Export
    export_data(
        df=df,
        data_url_reference=DATA_URL_REFERENCE,
        output_file=OUTPUT_FILE
    )

if __name__ == "__main__":
    main()