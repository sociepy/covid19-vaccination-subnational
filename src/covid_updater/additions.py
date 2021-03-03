from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import re
import requests
from covid_updater.scraping.core import automated_countries


url_incremental = "https://github.com/owid/covid-19-data/tree/master/scripts/scripts/vaccinations/automations/incremental"
url_batch = "https://github.com/owid/covid-19-data/tree/master/scripts/scripts/vaccinations/automations/batch"


def get_owid_diff_countries(include_manual: bool = False):
    """Get possible new additions to project.

    Retrieves countries in OWID dataset and checks if these are in sociepy's.
    """
    # Load data from OWID
    path = (
        "https://github.com/owid/covid-19-data/raw/master/scripts/scripts/vaccinations/automations/automation_state."
        "csv"
    )
    df = pd.read_csv(path)
    locations_owid_automated = df[df.automated == True].location.tolist()
    countries = [c for c in locations_owid_automated if c not in automated_countries]
    if include_manual:
        locations_owid_manual = df[df.automated == False].location.tolist()
        countries += locations_owid_manual
    return countries


def get_country_py_files(url: str) -> list:
    """Get list of py files under certain GitHub URL location."""
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, "html.parser")
    elems = soup.find_all(class_="css-truncate css-truncate-target d-block width-fit")
    files = [
        "{}/{}".format(url.replace("tree", "raw"), elem.text)
        for elem in elems
        if (
            elem.text.endswith(".py")
            and elem.text not in ("__init__.py", "vaxutils.py")
        )
    ]
    return files


def get_country_name_from_py_file(url: str) -> str:
    """Get country name from url."""
    return url.split("/")[-1].replace(".py", "").replace("_", " ").capitalize()


def extract_source(url: str) -> str:
    """Extract source used in py file."""
    file_content = requests.get(url).content.decode()
    regex = 'source = "(.*)"\\n'
    p = re.compile(regex)
    urls = p.findall(file_content)
    if len(urls) == 1:
        return urls[0]
    else:
        return ""  # raise ValueError("More than one source founded. Check Regex!")


def get_owid_diff_source_urls(verbose: bool = False) -> list:
    """Get list with countries and potential source urls."""
    country_py_files = get_country_py_files(url_incremental) + get_country_py_files(
        url_batch
    )
    owid_countries = get_owid_diff_countries()
    country_py_files = [
        url
        for url in country_py_files
        if get_country_name_from_py_file(url) in owid_countries
    ]
    info = []
    for i, url in enumerate(country_py_files):
        info.append(
            {
                "country": get_country_name_from_py_file(url),
                "source_url": extract_source(url),
            }
        )
        if (i % 5 == 0) and verbose:
            print(url, "({}/{})".format(i, len(country_py_files)))
    return info
