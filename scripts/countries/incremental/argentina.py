import pandas as pd
from bs4  import BeautifulSoup
import urllib.request
from datetime import datetime
import locale
from covid_updater.iso import merge_iso
from covid_updater.tracking import update_country_tracking
from covid_updater.utils import keep_min_date


COUNTRY = "Argentina"
COUNTRY_ISO = "AR"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "http://datos.salud.gob.ar/dataset/vacunas-contra-covid-19-dosis-aplicadas-en-la-republica-argentina"
DATA_URL_REFERENCE = DATA_URL
REGION_RENAMING = {
    "CABA": "Ciudad Autonoma de Buenos Aires",
    "Córdoba": "Cordoba",
    "Entre Ríos": "Entre Rios",
    "Neuquén": "Neuquen",
    "Río Negro": "Rio Negro",
    "Tucumán": "Tucuman"
}
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')



def get_df(soup):
    s = soup.find(class_="pkg-actions")
    if "DESCARGAR" in str(s):
        url = s.find_all("a")[1].get("href")
        df = pd.read_csv(url)
    else:
        raise Exception("HTML changed, no file to download was found!")
    return df
    
def get_date(soup):
    try:
        s = soup.find(id="info-container")
        rows = s.find_all(class_="col-xs-5 title")
        idx = [idx for idx, row in enumerate(rows) if row.text.strip() == "Fecha de actualización"][0]
        date_str = rows[idx].parent.find(class_="col-xs-7 value").text.strip()
        date = datetime.strptime(date_str, "%d de %B de %Y").strftime("%Y-%m-%d")
    except:
        raise Exception("Date could not be retrieved!")
    return date


def main():
    # Load current data
    df_source = pd.read_csv(OUTPUT_FILE)

    # Load new data
    html_page = urllib.request.urlopen(DATA_URL)
    soup = BeautifulSoup(html_page, "html.parser")

    # Get new date
    date = get_date(soup)

    # Get df
    df = get_df(soup)

    # Rename columns
    df = df.rename(columns={
        "primera_dosis_cantidad": "people_vaccinated",
        "segunda_dosis_cantidad": "people_fully_vaccinated",
        "jurisdiccion_nombre": "region"
    })

    # Process columns
    df.loc[:, "region"] = df.loc[:, "region"].replace(REGION_RENAMING)
    df.loc[:, "total_vaccinations"] = df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
    df.loc[:, "location"] = COUNTRY
    df.loc[:, "date"] = date

    # Add ISO codes
    df = merge_iso(df, country_iso=COUNTRY_ISO)

    # Concatenate
    df_source = df_source.loc[~(df_source.loc[:, "date"] == date)]
    df = pd.concat([df, df_source])

    # Export
    df = df[["location", "region", "date", "location_iso", "region_iso",
                "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
    df = keep_min_date(df)
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