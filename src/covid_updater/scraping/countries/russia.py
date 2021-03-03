import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
from covid_updater.scraping.base import IncrementalScraper


class RussiaScraper(IncrementalScraper):
    def __init__(self):
        super().__init__(
            country="Russia",
            country_iso="RU",
            data_url="https://gogov.ru/articles/covid-v-stats",
            data_url_reference="https://gogov.ru/articles/covid-v-stats",
            region_renaming={
                "Москва": "Moskva",
                "Московская обл.": "Moskovskaya oblast'",
                "Санкт-Петербург": "Sankt-Peterburg",
                "Свердловская обл.": "Sverdlovskaya oblast'",
                "Краснодарский край": "Krasnodarskiy kray",
                "Челябинская обл.": "Chelyabinskaya oblast'",
                "Самарская обл.": "Samarskaya oblast'",
                "Воронежская обл.": "Voronezhskaya oblast'",
                "Нижегородская обл.": "Nizhegorodskaya oblast'",
                "Татарстан": "Tatarstan, Respublika",
                "Башкортостан": "Bashkortostan, Respublika",
                "Ростовская обл.": "Rostovskaya oblast'",
                "Белгородская обл.": "Belgorodskaya oblast'",
                "Саратовская обл.": "Saratovskaya oblast'",
                "Новосибирская обл.": "Novosibirskaya oblast'",
                "Ставропольский край": "Stavropol'skiy kray",
                "Кемеровская обл.": "Kemerovskaya oblast'",
                "Алтайский край": "Altayskiy kray",
                "Красноярский край": "Krasnoyarskiy kray",
                "Оренбургская обл.": "Orenburgskaya oblast'",
                "Тверская обл.": "Tverskaya oblast'",
                "Тульская обл.": "Tul'skaya oblast'",
                "Волгоградская обл.": "Volgogradskaya oblast'",
                "Саха": "Sakha, Respublika",
                "Пермский край": "Permskiy kray",
                "Курская обл.": "Kurskaya oblast'",
                "Ивановская обл.": "Ivanovskaya oblast'",
                "Липецкая обл.": "Lipetskaya oblast'",
                "Тюменская обл.": "Tyumenskaya oblast'",
                "Ханты-Мансийский АО": "Khanty-Mansiyskiy avtonomnyy okrug",
                "Брянская обл.": "Bryanskaya oblast'",
                "Иркутская обл.": "Irkutskaya oblast'",
                "Ярославская обл.": "Yaroslavskaya oblast'",
                "Забайкальский край": "Zabaykal'skiy kray",
                "Тамбовская обл.": "Tambovskaya oblast'",
                "Ленинградская обл.": "Leningradskaya oblast'",
                "Омская обл.": "Omskaya oblast'",
                "Мордовия": "Mordoviya, Respublika",
                "Владимирская обл.": "Vladimirskaya oblast'",
                "Кировская обл.": "Kirovskaya oblast'",
                "Ульяновская обл.": "Ul'yanovskaya oblast'",
                "Калужская обл.": "Kaluzhskaya oblast'",
                "Хабаровский край": "Khabarovskiy kray",
                "Пензенская обл.": "Penzenskaya oblast'",
                "Костромская обл.": "Kostromskaya oblast'",
                "Сахалинская обл.": "Sakhalinskaya oblast'",
                "Вологодская обл.": "Vologodskaya oblast'",
                "Калининградская обл.": "Kaliningradskaya oblast'",
                "Удмуртия": "Udmurtskaya Respublika",
                "Астраханская обл.": "Astrakhanskaya oblast'",
                "Рязанская обл.": "Ryazanskaya oblast'",
                "Курганская обл.": "Kurganskaya oblast'",
                "Томская обл.": "Tomskaya oblast'",
                "Архангельская обл.": "Arkhangel'skaya oblast'",
                "Бурятия": "Buryatiya, Respublika",
                "Смоленская обл.": "Smolenskaya oblast'",
                "Ямало-Ненецкий АО": "Yamalo-Nenetskiy avtonomnyy okrug",
                "Карелия": "Kareliya, Respublika",  # HE
                "Мурманская обл.": "Murmanskaya oblast'",
                "Чечня": "Chechenskaya Respublika",  # HE
                "Орловская обл.": "Orlovskaya oblast'",
                "Коми": "Komi, Respublika",
                "Чувашия": "Chuvashskaya Respublika",
                "Новгородская обл.": "Novgorodskaya oblast'",
                "Псковская обл.": "Pskovskaya oblast'",
                "Хакасия": "Khakasiya, Respublika",
                "Марий Эл": "Mariy El, Respublika",
                "Дагестан": "Dagestan, Respublika",
                "Камчатский край": "Kamchatskiy kray",
                "Северная Осетия": "Severnaya Osetiya, Respublika",
                "Ингушетия": "Ingushetiya, Respublika",
                "Адыгея": "Adygeya, Respublika",
                "Кабардино-Балкария": "Kabardino-Balkarskaya Respublika",
                "Тыва": "Tyva, Respublika",
                "Калмыкия": "Kalmykiya, Respublika",
                "Магаданская обл.": "Magadanskaya oblast'",
                "Карачаево-Черкесия": "Karachayevo-Cherkesskaya Respublika",
                "Алтай": "Altay, Respublika",
                "Еврейская АО": "Yevreyskaya avtonomnaya oblast'",
                "Чукотский АО": "Chukotskiy avtonomnyy okrug",
                "Амурская обл.": "Amurskaya oblast'",
                "Приморский край": "Primorskiy kray",
                "Ненецкий АО": "Nenetskiy avtonomnyy okrug",
            },
            column_renaming={
                "регион": "region",
                "привито, чел.": "people_vaccinated",
                "привито двумя комп., чел.": "people_fully_vaccinated",
                "обнов-лено": "date",
            },
        )

    def load_data(self, wait=False):
        # Set up driver
        op = Options()
        op.add_argument("--headless")
        driver = webdriver.Chrome(options=op)

        driver.get(self.data_url)
        if wait:
            time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find(id="m-table")
        return pd.read_html(str(div))[0]

    def _parse_date(self, date_string):
        return datetime.strptime(f"{str(date_string)}.2021", "%d.%m.%Y").strftime(
            "%Y-%m-%d"
        )

    def _parse_vaccination_fields(self, df):
        def _remove_space(value):
            return int(value.replace(" ", ""))

        df.loc[:, "people_fully_vaccinated"] = (
            df.loc[:, "people_fully_vaccinated"]
            .fillna("-1")
            .apply(_remove_space)
            .astype("Int64")
            .replace({-1: pd.NA})
        )
        df.loc[:, "people_vaccinated"] = (
            df.loc[:, "people_vaccinated"]
            .fillna("-1")
            .apply(_remove_space)
            .astype("Int64")
            .replace({-1: pd.NA})
        )
        msk = df.people_fully_vaccinated.isnull() | df.people_vaccinated.isnull()
        df.loc[msk, "total_vaccinations"] = pd.NA
        df.loc[~msk, "total_vaccinations"] = (
            df.loc[~msk, "people_fully_vaccinated"].astype("Int64")
            + df.loc[~msk, "people_vaccinated"]
        )
        return df

    def _process(self, df):
        #  Parse date
        df["date"] = df["date"].apply(self._parse_date)
        #  Get vaccinations counts
        df = df.pipe(self._parse_vaccination_fields)
        # Remove non-widely-recognized regions
        df = df[~df["region"].isin(["Крым", "Севастополь"])]
        return df
