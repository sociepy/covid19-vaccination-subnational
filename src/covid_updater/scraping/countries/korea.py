import urllib.request
from datetime import datetime
import pytz
import pandas as pd
from bs4 import BeautifulSoup
from covid_updater.scraping.base import IncrementalScraper


class KoreaScraper(IncrementalScraper):
    def __init__(self):
        super().__init__(
            country="Korea",
            country_iso="KR",
            data_url="http://ncv.kdca.go.kr/mainStatus.es?mid=a11702000000",
            data_url_reference="ncv.kdca.go.kr/",
            region_renaming={
                "서울": "Seoul-teukbyeolsi",
                "부산": "Busan-gwangyeoksi",
                "대구": "Daegu-gwangyeoksi",
                "인천": "Incheon-gwangyeoksi",
                "광주": "Gwangju-gwangyeoksi",
                "대전": "Daejeon-gwangyeoksi",
                "울산": "Ulsan-gwangyeoksi",
                "세종": "Sejong-teukbyeoljachisi",
                "경기": "Gyeonggi-do",
                "강원": "Gangwon-do",
                "충북": "Chungcheongbuk-do",
                "충남": "Chungcheongnam-do",
                "전북": "Jeollabuk-do",
                "전남": "Jeollanam-do",
                "경북": "Gyeongsangbuk-do",
                "경남": "Gyeongsangnam-do",
                "제주": "Jeju-teukbyeoljachido",
            },
        )

    def load_data(self):
        # Read table from html
        html_page = urllib.request.urlopen(self.data_url)
        soup = BeautifulSoup(html_page, "html.parser")
        divs = soup.find_all(class_="data_table tbl_scrl_mini")
        table = divs[1].find_all("table")[0]
        # Convert to pandas
        df = pd.read_html(str(table))[0]
        df.columns = [
            "region",
            "delete",
            "people_vaccinated",
            "delete",
            "people_fully_vaccinated",
        ]
        return df.drop(columns=["delete"])

    def _process(self, df):
        df = df.assign(date=datetime.now(pytz.timezone("Asia/Seoul")).date())
        df.loc[:, "total_vaccinations"] = (
            df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
        )
        return df
