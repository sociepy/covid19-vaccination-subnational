import re
import requests
from datetime import datetime
import locale
from bs4 import BeautifulSoup
import pandas as pd
from covid_updater.iso import ISODB
from covid_updater.utils import export_data


COUNTRY = "Sweden"
COUNTRY_ISO = "SE"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/vaccination-mot-covid-19/statistik-over-forbrukade-vaccindoser/"
DATA_URL_REFERENCE = DATA_URL
REGION_RENAMING = {
    "Stockholm": "Stockholms lan",
    "Västerbotten": "Vasterbottens lan",
    "Norrbotten": "Norrbottens lan",
    "Uppsala": "Uppsala lan",
    "Södermanland": "Sodermanlands lan",
    "Östergötland": "Ostergotlands lan",
    "Jönköping": "Jonkopings lan",
    "Kronoberg": "Kronobergs lan",
    "Kalmar": "Kalmar lan",
    "Gotland": "Gotlands lan",
    "Blekinge": "Blekinge lan",
    "Skåne": "Skane lan",
    "Halland": "Hallands lan",
    "Västra Götaland": "Vastra Gotalands lan",
    "Värmland": "Varmlands lan",
    "Örebro": "Orebro lan",
    "Västmanland": "Vastmanlands lan",
    "Dalarna": "Dalarnas lan",
    "Gävleborg": "Gavleborgs lan",
    "Västernorrland": "Vasternorrlands lan",
    "Jämtland": "Jamtlands lan",
}
locale.setlocale(locale.LC_TIME, "sv_SE")


# Load
def load_data(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    df = load_df(soup)
    date = load_date(soup)
    return df, date


def load_df(soup):
    tables = soup.find(id="content-primary").findAll("table")
    if len(tables) == 2:
        table = tables[1]
        dfs = pd.read_html(str(table))
        if len(dfs) == 1:
            df = dfs[0]
        else:
            raise Exception("Scraping failed (2/2)")
    else:
        raise Exception("Scraping failed (1/2)")
    return df


def load_date(soup):
    date_str = soup.find(id="content-primary").find("h2").text
    date_str = re.search(r"\d+\s\w+\s+202\d", date_str).group(0)
    date = datetime.strptime(date_str, "%d %B %Y").strftime("%Y-%m-%d")
    return date


def column_str2int(x):
    x = x.replace({"–": "0"})
    x = x.str.replace(" ", "").astype(int)
    return x


def main():
    # Load current data
    df_source = pd.read_csv(OUTPUT_FILE)

    # Load data
    df, date = load_data(DATA_URL)

    # Rename columns
    df = df.rename(columns={"Län": "region"})

    # Process columns
    df.loc[:, "total_vaccinations"] = column_str2int(
        df.loc[:, "Moderna"]
    ) + column_str2int(df.loc[:, "Pfizer/BioNTech"])
    df.loc[:, "location"] = COUNTRY
    df.loc[:, "date"] = date

    # Remove total numbers
    df = df.loc[~(df.loc[:, "region"] == "Totala summan")]

    # Get iso codes
    df.loc[:, "region"] = df.loc[:, "region"].replace(REGION_RENAMING)
    df = ISODB().merge(df, country_iso=COUNTRY_ISO)

    # Concat
    df_source = df_source.loc[~(df_source.loc[:, "date"] == date)]
    df = pd.concat([df, df_source])

    #  Export
    export_data(df=df, data_url_reference=DATA_URL_REFERENCE, output_file=OUTPUT_FILE)


if __name__ == "__main__":
    main()
