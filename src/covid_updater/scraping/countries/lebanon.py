import os
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from covid_updater.scraping.base import IncrementalScraper


class LebanonScraper(IncrementalScraper):
    def __init__(self):
        super().__init__(
            country="Lebanon",
            country_iso="LB",
            data_url=(
                "https://dashboard.impactlebanon.com/s/public/elasticsearch/vaccine_appointment_data/_search?"
                "rest_total_hits_as_int=true&ignore_unavailable=true&ignore_throttled=true&preference=1614158503339&"
                "timeout=30000ms"
            ),
            data_url_reference="https://impact.cib.gov.lb/home/dashboard/vaccine",
            region_renaming={
                "Akkar عكار": "Aakkar",
                "El Hermel الهرمل": "Baalbek-Hermel",
                "Baalbek بعلبك": "Baalbek-Hermel",
                "Beirut بيروت": "Beyrouth",
                "Rachaya راشيا": "Beqaa",
                "West Bekaa البقاع الغربي": "Beqaa",
                "Zahle زحلة": "Beqaa",
                "Aley عاليه": "Mont-Liban",
                "Baabda بعبدا": "Mont-Liban",
                "Jbeil جبيل": "Mont-Liban",
                "Chouf الشوف": "Mont-Liban",
                "Kesrwane كسروان": "Mont-Liban",
                "El Meten المتن": "Mont-Liban",
                "Bent Jbeil بنت جبيل": "Nabatiye",
                "Hasbaya حاصبيا": "Nabatiye",
                "Marjaayoun مرجعيون": "Nabatiye",
                "El Nabatieh النبطية": "Nabatiye",
                "El Batroun البترون": "Liban-Nord",
                "Bcharre بشري": "Liban-Nord",
                "El Koura الكورة": "Liban-Nord",
                "El Minieh-Dennie المنية الضنية": "Liban-Nord",
                "Tripoli طرابلس": "Liban-Nord",
                "Zgharta زغرتا": "Liban-Nord",
                "Saida صيدا": "Liban-Sud",
                "Jezzine جزين": "Liban-Sud",
                "Sour صور": "Liban-Sud",
            },
        )

    def _load_json_request(self, date, date_start=None):
        this_directory = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(this_directory, "assets", "lebanon.json.txt")
        with open(path, "r") as f:
            json_field = f.read()
        if date_start is None:
            date_start = "2021-02-01T00:00:00.000Z"
        json_field = json_field.replace("__VAR_date_start__", date_start).replace(
            "__VAR_date_end__", date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        )
        return json.loads(json_field)

    def _load_data_raw(self, date):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "kbn-version": "7.6.1",
            "Origin": "https://dashboard.impactlebanon.com",
            "Connection": "keep-alive",
            "Referer": "https://dashboard.impactlebanon.com/s/public/app/kibana",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
        js = self._load_json_request(date)
        request = requests.post(self.data_url, json=js, headers=headers)
        data = request.json()
        return data

    def load_data(self, date=None):
        if date is None:
            date = datetime.now()
        data = self._load_data_raw(date)
        return pd.DataFrame(
            [
                {
                    "region": elem["key"],
                    "total_vaccinations": elem["3"]["value"],
                    "date": date.strftime("%Y-%m-%d"),
                }
                for elem in data["aggregations"]["2"]["buckets"]
            ]
        )

    def _process(self, df):
        df = df.groupby(["region", "location", "date"], as_index=False).sum()
        return df[df["region"].isin(set(self.region_renaming.values()))]
