import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
import locale
from covid_updater.scraping.base import IncrementalScraper


class IcelandScraper(IncrementalScraper):
    def __init__(self):
        super().__init__(
            country="Iceland", 
            country_iso="IS", 
            data_url="://e.infogram.com/c3bc3569-c86d-48a7-9d4c-377928f102bf", 
            data_url_reference="://e.infogram.com/c3bc3569-c86d-48a7-9d4c-377928f102bf", 
            region_renaming={
                "Höfuðborgarsvæði": "Hofudborgarsvaedi",
                "Norðurland eystra": "Nordurland eystra",
                "Norðurland vestra": "Nordurland vestra",
                "Suðurnes": "Sudurnes",
                "Suðurland": "Sudurland",
                "Vestfirðir": "Vestfirdir",
                "Norðurland": "Nordurland"
            }
        )

    def _get_soup(self):
        html_page = urllib.request.urlopen(self.data_url)
        return BeautifulSoup(html_page, "html.parser")

    def _find_script(self, soup):
        scripts = soup.find("body").find_all("script")
        key = "window.infographicData="
        for script in scripts:
            if key in script.string:
                s = script.string.replace("window.infographicData=", "")[:-1]
                return json.loads(s)

    def _get_data_list_from_script(script):
        script = find_script(scripts)
        data = (
            script["elements"]["content"]["content"]["entities"]["8752e817-052d-4b0b-9985-52dfe3983bba"]
            ["props"]["chartData"]["data"][0]
        )
        return data

    def load_data(self):
        soup = self._get_soup()
        script = self._find_script(soup)
        data = self._get_data_list_from_script(script)
        df = (
            pd.DataFrame.from_records(ss[0][1:], columns=["region", "people_vaccinated", "people_fully_vaccinated"])
        )
        df = df[~(df.region == "Óskráð")]
        return df

    def _undo_per_100k(df, population_iceland=None):
        if population_iceland is None:
            population_iceland = [
                ["Austurland", 13173],
                ["Höfuðborgarsvæði", 233034],
                ["Norðurland eystra", 30600],
                ["Norðurland vestra", 7322],
                ["Suðurland", 28399],
                ["Suðurnes", 27829],
                ["Vestfirðir", 7115],
                ["Vesturland", 16662],
                ["Norðurland", 30600+7322]
            ]
        df_pop = pd.DataFrame(population_iceland, columns=["region", "population"])
        df = df.merge(df_pop, on="region")
        df["people_vaccinated"] = (df["people_vaccinated"]*df["population"]/100000).apply(round)
        df["people_fully_vaccinated"] = (df["people_fully_vaccinated"]*df["population"]/100000).apply(round)
        return df

    def _process(self, df):
        df = self._undo_per_100k(df)
        df.loc[:, "total_vaccinations"] = df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
        df.loc[:, "date"] = (
            datetime.now(pytz.timezone("Europe/Sofia")).date() - timedelta(days=1)
        ).strftime("%Y-%m-%d")
        return df

    def _postprocess(self, df):
        df = super()._postprocess(df)
        df = df.assign(location_iso=self.country_iso)
        #df.loc[df.region=="Nordurland", "region_iso"] = "IS-6"  # Also accounts for IS-5 ! TODO
        return df
