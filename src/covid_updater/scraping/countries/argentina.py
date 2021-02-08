import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
import locale
from covid_updater.scraping.base import IncrementalScraper


class ArgentinaScraper(IncrementalScraper):
    def __init__(self):
        super().__init__(
            country="Argentina", 
            country_iso="AR", 
            data_url="http://datos.salud.gob.ar/dataset/vacunas-contra-covid-19-dosis-aplicadas-en-la-republica-argentina", 
            data_url_reference="http://datos.salud.gob.ar/dataset/vacunas-contra-covid-19-dosis-aplicadas-en-la-republica-argentina", 
            region_renaming={
                "CABA": "Ciudad Autonoma de Buenos Aires",
                "Córdoba": "Cordoba",
                "Entre Ríos": "Entre Rios",
                "Neuquén": "Neuquen",
                "Río Negro": "Rio Negro",
                "Tucumán": "Tucuman"
            }, 
            column_renaming={
                "primera_dosis_cantidad": "people_vaccinated",
                "segunda_dosis_cantidad": "people_fully_vaccinated",
                "jurisdiccion_nombre": "region"
            }
        )
        #locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    def _get_date_from_soup(self, soup):
        try:
            s = soup.find(id="info-container")
            rows = s.find_all(class_="col-xs-5 title")
            idx = [idx for idx, row in enumerate(rows) if row.text.strip() == "Fecha de actualización"][0]
            date_str = rows[idx].parent.find(class_="col-xs-7 value").text.strip()
            date = datetime.strptime(date_str, "%d de %B de %Y").strftime("%Y-%m-%d")
        except:
            raise Exception("Date could not be retrieved!")
        return date

    def _get_df_from_soup(self, soup):
        s = soup.find(class_="pkg-actions")
        if "DESCARGAR" in str(s):
            url = s.find_all("a")[1].get("href")
            try:
                df = pd.read_csv(url)
            except:
                raise Exception("Data file not valid!")
        else:
            raise Exception("HTML changed, no file to download was found!")
        return df

    def load_data(self):
        # Get HTML
        html_page = urllib.request.urlopen(self.data_url)
        soup = BeautifulSoup(html_page, "html.parser")
        # Parse HTML -> DataFrame
        date = self._get_date_from_soup(soup)
        df = self._get_df_from_soup(soup)
        df.loc[:, "date"] = date
        return df

    def _process(self, df):
        df.loc[:, "total_vaccinations"] = df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
        return df
