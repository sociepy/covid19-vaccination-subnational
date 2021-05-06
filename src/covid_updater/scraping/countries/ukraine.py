from datetime import datetime
import pytz

import requests
import pandas as pd
from covid_updater.scraping.base import IncrementalScraper


class UkraineScraper(IncrementalScraper):
    def __init__(self):
        super().__init__(
            country="Ukraine",
            country_iso="UA",
            data_url="https://health-security.rnbo.gov.ua/api/vaccination/process/map",
            data_url_reference="https://health-security.rnbo.gov.ua/vaccination",
            region_renaming={
                "м. Київ": "Kyiv",
                "Дніпропетровська область": "Dnipropetrovska oblast",
                "Львівська область": "Lvivska oblast",
                "Київська область": "Kyivska oblast",
                "Харківська область": "Kharkivska oblast",
                "Полтавська область": "Poltavska oblast",
                "Донецька область": "Donetska oblast",
                "Вінницька область": "Vinnytska oblast",
                "Одеська область": "Odeska oblast",
                "Черкаська область": "Cherkaska oblast",
                "Запорізька область": "Zaporizka oblast",
                "Житомирська область": "Zhytomyrska oblast",
                "Миколаївська область": "Mykolaivska oblast",
                "Хмельницька область": "Khmelnytska oblast",
                "Сумська область": "Sumska oblast",
                "Тернопільська область": "Ternopilska oblast",
                "Херсонська область": "Khersonska oblast",
                "Івано-Франківська область": "Ivano-Frankivska oblast",
                "Рівненська область": "Rivnenska oblast",
                "Закарпатська область": "Zakarpatska oblast",
                "Кіровоградська область": "Kirovohradska oblast",
                "Волинська область": "Volynska oblast",
                "Чернігівська область": "Chernihivska oblast",
                "Чернівецька область": "Chernivetska oblast",
                "Луганська область": "Luhanska oblast",
            },
        )

    def load_data(self):
        # Load
        params_1 = {"distributionBy": "vaccine", "dose": 1}
        params_2 = {"distributionBy": "vaccine", "dose": 2}
        data_1 = requests.get(self.data_url, params=params_1).json()
        data_2 = requests.get(self.data_url, params=params_2).json()
        return self._build_df(data_1, data_2)

    def _build_df(self, data_1, data_2):
        _map = {
            elem["properties"]["name"]: elem["properties"]["daily"]["total"][
                "cumulative"
            ]
            for elem in data_2
        }
        data = [
            {
                "region": elem["properties"]["name"],
                "people_vaccinated": elem["properties"]["daily"]["total"]["cumulative"],
                "people_fully_vaccinated": _map[elem["properties"]["name"]],
            }
            for elem in data_1
        ]
        return pd.DataFrame(data)

    def _process(self, df):
        return df.assign(
            total_vaccinations=df["people_fully_vaccinated"] + df["people_vaccinated"],
            date=datetime.now().date(pytz.timezone("Europe/Kiev")).strftime("%Y-%m-%d"),
        )
