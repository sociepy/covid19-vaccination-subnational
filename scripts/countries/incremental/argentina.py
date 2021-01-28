import pandas as pd
from bs4  import BeautifulSoup
import urllib.request
from utils import merge_iso
from datetime import datetime
import locale


locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
source_file = "data/countries/Argentina.csv"
replace = {
    "CABA": "Ciudad Autonoma de Buenos Aires",
    "Córdoba": "Cordoba",
    "Entre Ríos": "Entre Rios",
    "Neuquén": "Neuquen",
    "Río Negro": "Rio Negro",
    "Tucumán": "Tucuman"
}


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
    df_source = pd.read_csv(source_file)

    # Load new data
    url = "http://datos.salud.gob.ar/dataset/vacunas-contra-covid-19-dosis-aplicadas-en-la-republica-argentina"
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, "html.parser")

    # Get new date
    date = get_date(soup)
    if date > df_source["date"].max():
        # Get df
        df = get_df(soup)

        # Rename columns
        df = df.rename(columns={
            "primera_dosis_cantidad": "people_vaccinated",
            "segunda_dosis_cantidad": "people_fully_vaccinated",
            "jurisdiccion_nombre": "region"
        })

        # Process columns
        df.loc[:, "region"] = df.loc[:, "region"].replace(replace)
        df.loc[:, "total_vaccinations"] = df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
        df.loc[:, "location"] = "Argentina"
        df.loc[:, "date"] = date

        # Add ISO codes
        df = merge_iso(df, country_iso="AR")

        # Export
        df_source = df_source.loc[~(df_source.loc[:, "date"] == date)]
        df = pd.concat([df, df_source])
        df = df[["location", "region", "date", "location_iso", "region_iso",
                 "total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]]
        df = df.sort_values(by=["region", "date"])
        df.to_csv(source_file, index=False)


if __name__ == "__main__":
    main()