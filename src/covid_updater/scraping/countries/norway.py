import json
import requests
import pandas as pd
from covid_updater.scraping.base import IncrementalScraper
from covid_updater.scraping.utils import load_driver


class NorwayScraper(IncrementalScraper):
    def __init__(self):
        super().__init__(
            country="Norway", 
            country_iso="NO", 
            data_url="https://www.fhi.no/sv/vaksine/koronavaksinasjonsprogrammet/koronavaksinasjonsstatistikk/", 
            data_url_reference="https://www.fhi.no/sv/vaksine/koronavaksinasjonsprogrammet/koronavaksinasjonsstatistikk/", 
            region_renaming={
                "agder": "Agder",
                "innlandet": "Innlandet",
                "møre og romsdal": "More og Romsdal",
                "nordland": "Nordland",
                "oslo": "Oslo",
                "rogaland": "Rogaland",
                "troms og finnmark": "Troms og Finnmark",
                "trøndelag": "Trondelag",
                "vestfold og telemark": "Vestfold og Telemark",
                "vestland": "Vestland",
                "viken": "Viken" 
            }, 
            column_renaming={
                "primera_dosis_cantidad": "people_vaccinated",
                "segunda_dosis_cantidad": "people_fully_vaccinated",
                "jurisdiccion_nombre": "region"
            }
        )

    def _get_date(self):
        driver = load_driver(self.data_url)
        elem = driver.find_element_by_class_name("fhi-date")
        date = elem.find_elements_by_tag_name("time")[-1].get_attribute("datetime")
        return date

    def load_data(self):
        # Load dose 1 data
        url = "https://www.fhi.no/api/chartdata/api/99112"
        dix = json.loads(requests.get(url).content)
        df_dose1 = pd.DataFrame(dix, columns=["region", "people_vaccinated"])
        # Load dose 2 data
        url = "https://www.fhi.no/api/chartdata/api/99111"
        dix = json.loads(requests.get(url).content)
        df_dose2 = pd.DataFrame(dix, columns=["region", "people_fully_vaccinated"])
        # Remove row
        df_dose1 = df_dose1.loc[~(df_dose2["region"] == "Fylke")]
        df_dose2 = df_dose2.loc[~(df_dose2["region"] == "Fylke")]
        # Merge
        df = df_dose1.merge(df_dose2, on="region", how="left")
        return df

    def _process(self, df):
        df.loc[:, "date"] = self._get_date()
        df.loc[:, "total_vaccinations"] = df.loc[:, "people_fully_vaccinated"] + df.loc[:, "people_vaccinated"]
        return df
