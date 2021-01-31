from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import pytz
import datetime
from covid_updater.iso import merge_iso
from covid_updater.tracking import update_country_tracking


COUNTRY = "Bulgaria"
COUNTRY_ISO = "BG"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://coronavirus.bg/bg/statistika"
DATA_URL_REFERENCE = DATA_URL_REFERENCE
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
    "Ямбол": "Yambol"
}


def main():
    # Load current data
    df_source = pd.read_csv(OUTPUT_FILE)
    
    # Request and Get data
    page = requests.get(DATA_URL)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("p", string=re.compile("Ваксинирани лица по")).parent.find("table")
    df = pd.read_html(str(table))[0]
    df = df.droplevel(level=0, axis=1)
    date = str(datetime.datetime.now(pytz.timezone("Europe/Sofia")).date() - datetime.timedelta(days=1))
    
    if date > df_source["date"].max():
        df = df.rename(columns={
            "Област": "region",
            "Общо": "total_vaccinations"
        })
        df = df[~(df.loc[:, "region"]=="Общо")]
        df.loc[:, "region"] = df.loc[:, "region"].replace(replace)
        df.loc[:, "date"] = date
        df.loc[:, "location"] = COUNTRY
        
        # Add ISO codes
        df = merge_iso(df, country_iso=COUNTRY_ISO)
        
        # Concat
        df = pd.concat([df, df_source])

        # Reorder columns
        df = df[["location", "region", "date", "location_iso", "region_iso", "total_vaccinations"]]
        df = df.sort_values(by=["region", "date"])
        df.to_csv(OUTPUT_FILE, index=False)

        # Tracking
        update_country_tracking(
            country=COUNTRY,
            url=DATA_URL_REFERENCE,
            last_update=df["date"].max()
        )


if __name__ == "__main__":
    main()