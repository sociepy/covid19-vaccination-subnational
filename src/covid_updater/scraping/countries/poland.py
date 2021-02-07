import pandas as pd
import json
from bs4  import BeautifulSoup
import requests
from datetime import datetime
import pytz
from covid_updater.scraping.base import IncrementalScraper


class PolandScraper(IncrementalScraper):
    def __init__(self):
        super().__init__(
            country="Poland", 
            country_iso="PL", 
            data_url="https://services9.arcgis.com/RykcEgwHWuMsJXPj/arcgis/rest/services/wojewodztwa_szczepienia_widok3/" + \
          "FeatureServer/0/query?f=json&where=1=1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields" + \
          "=*&orderByFields=SZCZEPIENIA_DZIENNIE desc&resultOffset=0&resultRecordCount=16&resultType=standard&cacheHint=true", 
            data_url_reference="https://www.gov.pl/web/szczepimysie/raport-szczepien-przeciwko-covid-19", 
            region_renaming={
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
            }, 
            column_renaming={
                "jpt_nazwa_": "region",
                "SZCZEPIENIA_SUMA": "total_vaccinations",
                "DAWKA_2_SUMA": "people_fully_vaccinated"
            }
        )

    def load_data(self):
        dix = json.loads(requests.get(self.data_url).content)
        feats = [d["attributes"] for d in dix["features"]]
        df = pd.DataFrame(feats)
        return df

    def _process(self, df):
        today = datetime.now(pytz.timezone("Europe/Warsaw")).date().strftime("%Y-%m-%d")
        df.loc[:, "date"] = today
        df.loc[:, "people_vaccinated"] = df.loc[:, "total_vaccinations"] - df.loc[:, "people_fully_vaccinated"]
        return df
