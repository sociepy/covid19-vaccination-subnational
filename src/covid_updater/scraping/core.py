from covid_updater.scraping.countries.austria import AustriaScraper
from covid_updater.scraping.countries.india import IndiaScraper
from covid_updater.scraping.countries.sweden import SwedenScraper
from covid_updater.scraping.countries.united_states import UnitedStatesScraper
from covid_updater.scraping.countries.belgium import BelgiumScraper
from covid_updater.scraping.countries.brazil import BrazilScraper
from covid_updater.scraping.countries.czechia import CzechiaScraper
from covid_updater.scraping.countries.germany import GermanyScraper
from covid_updater.scraping.countries.italy import ItalyScraper
from covid_updater.scraping.countries.slovakia import SlovakiaScraper
from covid_updater.scraping.countries.spain import SpainScraper
from covid_updater.scraping.countries.united_kingdom import UnitedKingdomScraper
from covid_updater.scraping.countries.argentina import ArgentinaScraper
from covid_updater.scraping.countries.poland import PolandScraper
from covid_updater.scraping.countries.france import FranceScraper
from covid_updater.scraping.countries.denmark import DenmarkScraper
from covid_updater.scraping.countries.norway import NorwayScraper
from covid_updater.scraping.countries.switzerland import SwitzerlandScraper
from covid_updater.scraping.countries.chile import ChileScraper
from covid_updater.scraping.countries.canada import CanadaScraper
from covid_updater.scraping.countries.peru import PeruScraper
from covid_updater.scraping.countries.turkey import TurkeyScraper
from covid_updater.scraping.countries.iceland import IcelandScraper
from covid_updater.scraping.countries.australia import AustraliaScraper
from covid_updater.scraping.countries.lebanon import LebanonScraper
from covid_updater.scraping.countries.russia import RussiaScraper
from covid_updater.scraping.countries.finland import FinlandScraper


scrapers = [
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
    NorwayScraper(),
    SwitzerlandScraper(),
    ChileScraper(),
    CanadaScraper(),
    PeruScraper(),
    TurkeyScraper(),
    IcelandScraper(),
    AustraliaScraper(),
    LebanonScraper(),
    RussiaScraper(),
    FinlandScraper(),
]
automated_countries = [scrapper.country for scrapper in scrapers]
scrapers_dict = {scrapper.country_iso: scrapper for scrapper in scrapers}
iso_codes = list(scrapers_dict.keys())


def get_country_scraper(iso_code: str):
    """Get country scraper.

    Args:
        iso_code (str): ISO code 3166 alpha-2 of a country.

    Returns:
        Scraper: Country scraper.

    Raises:
        ValueError: If no scraper available for given iso code.

    """
    if iso_code in scrapers_dict:
        return scrapers_dict.get(iso_code)
    else:
        raise ValueError(
            f"Not available iso code. Available iso codes are: {iso_codes}"
        )
