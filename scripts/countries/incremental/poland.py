import requests
import json
import pytz
import datetime
import pandas as pd
from utils import merge_iso


source_file = "data/countries/Poland.csv"


replace = {
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
    df_source = pd.read_csv(source_file)

    # Load data
    url = "https://services9.arcgis.com/RykcEgwHWuMsJXPj/arcgis/rest/services/wojewodztwa_szczepienia_widok3/" + \
          "FeatureServer/0/query?f=json&where=1=1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields" + \
          "=*&orderByFields=SZCZEPIENIA_DZIENNIE desc&resultOffset=0&resultRecordCount=16&resultType=standard&cacheHint=true"
    df = load_data(url)

    # Process columns
    df = df.rename(columns={
        "jpt_nazwa_": "region",
        "SZCZEPIENIA_SUMA": "total_vaccinations",
        "DAWKA_2_SUMA": "people_fully_vaccinated"
    })
    df.loc[:, "location"] = "Poland"
    date = datetime.datetime.now(pytz.timezone("Europe/Warsaw")).date().strftime("%Y-%m-%d")
    df.loc[:, "date"] = date
    df.loc[:, "people_vaccinated"] = df.loc[:, "total_vaccinations"] - df.loc[:, "people_fully_vaccinated"]
    df.loc[:, "region"] = df.loc[:, "region"].replace(replace)
    
    # ISO
    df = merge_iso(df, "PL")
    
    # Export
    df_source = df_source.loc[~(df_source.loc[:, "date"] == date)]
    df = df[["location", "region", "date", "location_iso", "region_iso",
             "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv(source_file, index=False)


if __name__ == "__main__":
    main()