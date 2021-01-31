import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from covid_updater.iso import merge_iso


source_file = "data/countries/Norway.csv"


replace = {
    "Møre og Romsdal": 'More og Romsdal',
    "Trøndelag": "Trondelag"
}


def load_driver(url):
    op = Options()
    op.add_argument("--headless")
    driver = webdriver.Chrome(options=op)
    driver.get(url)
    return driver


def load_data(driver):
    # Get rows
    elems = driver.find_elements_by_class_name("options")
    elems[1].find_element_by_id("viewTable").send_keys("\n")
    tables = driver.find_elements_by_tag_name("tbody")
    table = tables[1]
    rows = table.find_elements_by_tag_name("tr")

    regions = []
    vaccinations = []
    for row in rows:
        region, vaccination = [x.text for x in row.find_elements_by_tag_name("td")]
        regions.append(region)
        vaccinations.append(int(vaccination))
    
    df = pd.DataFrame({"region": regions, "total_vaccinations": vaccinations})
    return df


def load_date(driver):
    elem = driver.find_element_by_class_name("fhi-date")
    date = elem.find_elements_by_tag_name("time")[-1].get_attribute("datetime")
    return date


def main():
    # Load current file
    df_source = pd.read_csv(source_file)

    # Load new data
    url = "https://www.fhi.no/sv/vaksine/koronavaksinasjonsprogrammet/koronavaksinasjonsstatistikk/"
    driver = load_driver(url)
    try:
        df = load_data(driver)
    except:
        raise Exception("Data could not be loaded. Check your scraping!")
    try:
        date = load_date(driver)
    except:
        raise Exception("Date not found!")

    df.loc[:, "location"] = "Norway"
    df.loc[:, "date"] = date

    # Process region column
    df.loc[:, "region"] = df.loc[:, "region"].replace(replace)

    # Add ISO codes
    df = merge_iso(df, country_iso="NO")

    # Export
    df_source = df_source.loc[~(df_source.loc[:, "date"] == date)]
    df = pd.concat([df, df_source])
    df = df[["location", "region", "date", "location_iso", "region_iso", "total_vaccinations"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv(source_file, index=False)


if __name__ == "__main__":
    main()