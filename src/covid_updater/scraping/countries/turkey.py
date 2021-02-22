from datetime import datetime
import pytz
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
from covid_updater.scraping.base import IncrementalScraper


class TurkeyScraper(IncrementalScraper):
    def __init__(self):
        super().__init__(
            country="Turkey",
            country_iso="TR",
            data_url="https://covid19asi.saglik.gov.tr/",
            data_url_reference="https://covid19asi.saglik.gov.tr/",
            region_renaming={
                "Adıyaman": "Adiyaman",
                "Afyon": "Afyonkarahisar",
                "Ağrı": "Agri",
                "Aydın": "Aydin",
                "Balıkesir": "Balikesir",
                "Bingöl": "Bingol",
                "Çanakkale": "Canakkale",
                "Çankırı": "Cankiri",
                "Çorum": "Corum",
                "Diyarbakır": "Diyarbakir",
                "Elazığ": "Elazig",
                "Eskişehir": "Eskisehir",
                "Gümüşhane": "Gumushane",
                "İstanbul": "Istanbul",
                "İzmir": "Izmir",
                "Kırklareli": "Kirklareli",
                "Kırşehir": "Kirsehir",
                "Kütahya": "Kutahya",
                "Kahramanmaraş": "Kahramanmaras",
                "Muğla": "Mugla",
                "Muş": "Mus",
                "Nevşehir": "Nevsehir",
                "Niğde": "Nigde",
                "Tekirdağ": "Tekirdag",
                "Şanlıurfa": "Sanliurfa",
                "Uşak": "Usak",
                "Kırıkkale": "Kirikkale",
                "Şırnak": "Sirnak",
                "Bartın": "Bartin",
                "Iğdır": "Igdir",
                "Karabük": "Karabuk",
                "Düzce": "Duzce",
            },
        )

    def load_data(self):
        #  Get HTML data
        html_page = urllib.request.urlopen(self.data_url)
        soup = BeautifulSoup(html_page, "html.parser")
        states_html = soup.find(id="turkiye").find_all("g")
        #  Parse HTML data
        regions = []
        total_vaccinations = []
        people_vaccinated = []
        people_fully_vaccinated = []
        for state_html in states_html:
            regions.append(state_html.get("data-adi"))
            total_vaccinations.append(
                int(state_html.get("data-toplam").replace(".", ""))
            )
            people_vaccinated.append(
                int(state_html.get("data-birinci-doz").replace(".", ""))
            )
            people_fully_vaccinated.append(
                int(state_html.get("data-ikinci-doz").replace(".", ""))
            )
        #  Build dataframe
        df = pd.DataFrame.from_dict(
            {
                "region": regions,
                "total_vaccinations": total_vaccinations,
                "people_vaccinated": people_vaccinated,
                "people_fully_vaccinated": people_fully_vaccinated,
            }
        )
        return df

    def _process(self, df):
        df = df.assign(
            date=datetime.now(pytz.timezone("Asia/Istanbul")).strftime("%Y-%m-%d")
        )
        return df
