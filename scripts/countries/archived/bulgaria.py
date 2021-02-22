from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import pytz
import datetime
from covid_updater.iso import ISODB
from covid_updater.utils import export_data


COUNTRY = "Bulgaria"
COUNTRY_ISO = "BG"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://coronavirus.bg/bg/statistika"
DATA_URL_REFERENCE = DATA_URL
REGION_RENAMING = {
    "Благоевград": "Blagoevgrad",
    "Бургас": "Burgas",
    "Варна": "Varna",
    "Велико Търново": "Veliko Tarnovo",
    "Видин": "Vidin",
    "Враца": "Vratsa",
    "Габрово": "Gabrovo",
    "Добрич": "Dobrich",
    "Кърджали": "Kardzhali",
    "Кюстендил": "Kyustendil",
    "Ловеч": "Lovech",
    "Монтана": "Montana",
    "Пазарджик": "Pazardzhik",
    "Перник": "Pernik",
    "Плевен": "Pleven",
    "Пловдив": "Plovdiv",
    "Разград": "Razgrad",
    "Русе": "Ruse",
    "Силистра": "Silistra",
    "Сливен": "Sliven",
    "Смолян": "Smolyan",
    "София": "Sofia",
    "София (столица)": "Sofia (stolitsa)",
    "Стара Загора": "Stara Zagora",
    "Търговище": "Targovishte",
    "Хасково": "Haskovo",
    "Шумен": "Shumen",
    "Ямбол": "Yambol",
}


def main():
    # Load current data
    df_source = pd.read_csv(OUTPUT_FILE)

    # Request and Get data
    page = requests.get(DATA_URL)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("p", string=re.compile("Ваксинирани лица по")).parent.find(
        "table"
    )
    df = pd.read_html(str(table))[0]
    df = df.droplevel(level=0, axis=1)
    date = str(
        datetime.datetime.now(pytz.timezone("Europe/Sofia")).date()
        - datetime.timedelta(days=1)
    )

    df = df.rename(columns={"Област": "region", "Общо": "total_vaccinations"})
    df = df[~(df.loc[:, "region"] == "Общо")]
    df.loc[:, "region"] = df.loc[:, "region"].replace(replace)
    df.loc[:, "date"] = date
    df.loc[:, "location"] = COUNTRY

    # Add ISO codes
    df = ISODB().merge(df, country_iso=COUNTRY_ISO)

    #  Concat
    df_source = df_source.loc[~(df_source.loc[:, "date"] == date)]
    df = pd.concat([df, df_source])

    #  Export
    export_data(df=df, data_url_reference=DATA_URL_REFERENCE, output_file=OUTPUT_FILE)


if __name__ == "__main__":
    main()
