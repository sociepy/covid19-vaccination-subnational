from covid_updater.scraping.countries.austria import AustriaScraper
from covid_updater.scraping.countries.india import IndiaScraper
from covid_updater.scraping.countries.sweden import SwedenScraper
from covid_updater.scraping.countries.united_states import UnitedStatesScraper
from covid_updater.scraping.countries.belgium import BelgiumScraper
from covid_updater.scraping.countries.brazil import BrazilScraper
from covid_updater.scraping.countries.czechia import CzechiaScraper
from covid_updater.scraping.countries.germany import GermanyScraper
from covid_updater.scraping.countries.italia import ItalyScraper
from covid_updater.scraping.countries.slovakia import SlovakiaScraper
from covid_updater.scraping.countries.spain import SpainScraper
from covid_updater.scraping.countries.united_kingdom import UnitedKingdomScraper
from covid_updater.scraping.countries.argentina import ArgentinaScraper
from covid_updater.scraping.countries.poland import PolandScraper
from covid_updater.scraping.countries.france import FranceScraper
from covid_updater.scraping.countries.denmark import DenmarkScraper
from covid_updater.scraping.countries.norway import NorwayScraper


scrappers = [
    AustriaScraper(),
    IndiaScraper(),
    SwedenScraper(),
    UnitedStatesScraper(),
    BelgiumScraper(),
    BrazilScraper(),
    CzechiaScraper(),
    GermanyScraper(),
    ItalyScraper(),
    SlovakiaScraper(),
    SpainScraper(),
    UnitedKingdomScraper(),
    ArgentinaScraper(),
    PolandScraper(),
    FranceScraper(),
    DenmarkScraper(),
    NorwayScraper()
]
scrappers_dict = {scrapper.country_iso: scrapper for scrapper in scrappers}
iso_codes = list(scrappers_dict.keys())


def get_country_scraper(iso_code: str):
    """Get country scraper.

    Args:
        iso_code (str): ISO code 3166 alpha-2 of a country.
    
    Returns:
        Scraper: Country scraper.
    
    Raises:
        ValueError: If no scraper available for given iso code.

    """
    if iso_code in scrappers_dict:
        return scrappers_dict.get(iso_code)
    else:
        raise ValueError(f"Not available iso code. Available iso codes are: {iso_codes}")