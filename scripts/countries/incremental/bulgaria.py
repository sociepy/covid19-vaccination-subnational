from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import pytz
import datetime


source_file = "data/countries/Bulgaria.csv"
replace = {
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
    df_source = pd.read_csv(source_file)
    
    # Request and Get data
    url = "https://coronavirus.bg/bg/statistika"
    page = requests.get(url)
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
        df = df[df.loc[:, "region"] != "Общо"]
        df.loc[:, "region"] = df.loc[:, "region"].replace(replace)
        df.loc[:, "date"] = date
        df.loc[:, "location"] = "Bulgaria"
        df = df[["date", "location", "region", "total_vaccinations"]]
        df = pd.concat([df, df_source])
        df.to_csv("output/countries/United_Kingdom.csv", index=False)


if __name__ == "__main__":
    main()