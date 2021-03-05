import io
import requests
import pandas as pd
from covid_updater.scraping.base import Scraper


class AustriaScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="Austria",
            country_iso="AT",
            data_url="http://info.gesundheitsministerium.gv.at/data/timeline-eimpfpass.csv",
            data_url_reference="https://info.gesundheitsministerium.gv.at/",
            region_renaming={
                "Kärnten": "Karnten",
                "Niederösterreich": "Niederosterreich",
                "Oberösterreich": "Oberosterreich",
            },
            column_renaming={
                "Datum": "date",
                "Name": "region",
                "EingetrageneImpfungen": "total_vaccinations",
                "Teilgeimpfte": "people_vaccinated",
                "Vollimmunisierte": "people_fully_vaccinated",
            },
        )

    def load_data(self):
        #  Avoid SSL "kew too small" error
        # ref: https://stackoverflow.com/questions/38015537/python-requests-exceptions-sslerror-dh-key-too-small
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "HIGH:!DH:!aNULL"
        try:
            requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += (
                "HIGH:!DH:!aNULL"
            )
        except AttributeError:
            # no pyopenssl support used / needed / available
            pass
        # Load
        raw = requests.get(self.data_url)
        text = raw.content.decode()
        return pd.read_csv(
            io.StringIO(text),
            sep=";",
            usecols=[
                "Datum",
                "Name",
                "EingetrageneImpfungen",
                "Teilgeimpfte",
                "Vollimmunisierte",
            ],
        )

    def _process(self, df):
        # Column proccess
        df.loc[:, "date"] = df.loc[:, "date"].str.slice(0, 10)
        #  Ignore some entries (field: region, value: Österreich)
        df = df.loc[df["region"] != "Österreich"]
        return df
