from datetime import datetime
import pytz
import requests
import pandas as pd
from covid_updater.scraping.base import IncrementalScraper


class PeruScraper(IncrementalScraper):
    def __init__(self):
        super().__init__(
            country="Peru", 
            country_iso="PE", 
            data_url="https://gis.minsa.gob.pe/WebApiReplica/api/Departamento/ListarVacunadosPublico", 
            data_url_reference="https://gis.minsa.gob.pe/GisVisorVacunados/", 
            column_renaming={
                "Id": "region_iso",
                "Vacunados": "total_vaccinations"
            },
            mode_iso_merge="region",
            field_renaming={
                "region_iso": {
                    1: "PE-AMA",
                    2: "PE-ANC",
                    3: "PE-APU",
                    4: "PE-ARE",
                    5: "PE-AYA",
                    6: "PE-CAJ",
                    7: "PE-CAL",
                    8: "PE-CUS",
                    9: "PE-HUV",
                    10: "PE-HUC",
                    11: "PE-ICA",
                    12: "PE-JUN",
                    13: "PE-LAL",
                    14: "PE-LAM",
                    15: "PE-LIM",
                    16: "PE-LOR",
                    17: "PE-MDD",
                    18: "PE-MOQ",
                    19: "PE-PAS",
                    20: "PE-PIU",
                    21: "PE-PUN",
                    22: "PE-SAM",
                    23: "PE-TAC",
                    24: "PE-TUM",
                    25: "PE-UCA"
                }
            }
        )

    def load_data(self):
        headers = {'Content-type': 'application/json', 'Accept': '*/*'}
        json = {"DisaCodigo":0, "IdDepartamento":""}
        request = requests.post(
            self.data_url,
            json=json,
            headers=headers
        )
        request.raise_for_status()
        data = request.json()
        df = pd.DataFrame.from_dict(data["Data"])[["Id", "Vacunados"]]
        return df

    def _process(self, df):
        # Date format
        df.loc[:, "date"] = datetime.now(pytz.timezone("America/Lima")).date().strftime("%Y-%m-%d")
        return df
