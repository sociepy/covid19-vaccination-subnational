import pandas as pd
from covid_updater.scraping.base import Scraper


class CzechiaScraper(Scraper):
    def __init__(self):
        super().__init__(
            country="Czechia",
            country_iso="CZ",
            data_url="https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani.csv",
            data_url_reference="https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/",
            region_renaming={
                "Hlavní město Praha": "Praha, Hlavni mesto",
                "Jihomoravský kraj": "Jihomoravsky kraj",
                "Moravskoslezský kraj": "Moravskoslezsky kraj",
                "Ústecký kraj": "Ustecky kraj",
                "Středočeský kraj": "Stredocesky kraj",
                "Plzeňský kraj": "Plzensky kraj",
                "Pardubický kraj": "Pardubicky kraj",
                "Olomoucký kraj": "Olomoucky kraj",
                "Zlínský kraj": "Zlinsky kraj",
                "Královéhradecký kraj": "Kralovehradecky kraj",
                "Kraj Vysočina": "Kraj Vysocina",
                "Karlovarský kraj": "Karlovarsky kraj",
                "Jihočeský kraj": "Jihocesky kraj",
                "Liberecký kraj": "Liberecky kraj",
            },
            column_renaming={
                "datum": "date",
                "kraj_nazev": "region",
                "prvnich_davek": "people_vaccinated",
                "druhych_davek": "people_fully_vaccinated",
                "celkem_davek": "total_vaccinations",
            },
            do_cumsum_fields=[
                "total_vaccinations",
                "people_vaccinated",
                "people_fully_vaccinated",
            ],
        )

    def load_data(self):
        # Load
        df = pd.read_csv(self.data_url)
        cols = [
            "datum",
            "vakcina",
            "kraj_nuts_kod",
            "kraj_nazev",
            "vekova_skupina",
            "prvnich_davek",
            "druhych_davek",
            "celkem_davek",
        ]
        if not all([col in df.columns for col in cols]):
            raise Exception("API changed")
        return df

    def _process(self, df):
        df = (
            df.groupby(by=["date", "region", "location"])
            .agg(
                people_vaccinated=("people_vaccinated", sum),
                people_fully_vaccinated=("people_fully_vaccinated", sum),
                total_vaccinations=("total_vaccinations", sum),
            )
            .reset_index()
        )
        if not (
            df["total_vaccinations"]
            == df["people_vaccinated"] + df["people_fully_vaccinated"]
        ).all():
            raise Exception("Error in columns. dose_1 + dose_2 != total_doses")
        return df
