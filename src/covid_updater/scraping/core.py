from covid_updater.scraping.countries.austria import AustriaScraper
from covid_updater.scraping.countries.india import IndiaScraper
from covid_updater.scraping.countries.sweden import SwedenScraper
from covid_updater.scraping.countries.united_states import UnitedStatesScraper
from covid_updater.scraping.countries.belgium import BelgiumScraper
from covid_updater.scraping.countries.brazil import BrazilScraper
from covid_updater.scraping.countries.czechia import CzechiaScraper
from covid_updater.scraping.countries.germany import GermanyScraper
from covid_updater.scraping.countries.italia import ItalyScraper


scrappers = [
    AustriaScraper(),
    IndiaScraper(),
    SwedenScraper(),
    UnitedStatesScraper(),
    BelgiumScraper(),
    BrazilScraper(),
    CzechiaScraper(),
    GermanyScraper(),
    ItalyScraper()
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