import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime


def main():
    # Request data
    url = "https://covid-vaccinatie.be/en/vaccines-administered"
    page_content = requests.get(url, headers={'User-Agent': 'Custom'}).content
    soup = BeautifulSoup(page_content, "html.parser")

    # Get table data
    table = soup.find(class_="table table-striped table-dark table-hover mb-0")
    elems = table.find_all("tr")

    # Gather data
    dix = {
        "date": [],
        "region": [],
        "total_vaccinations": []
    }
    for elem in elems:
        day, month = elem.find('td').text.strip().split("/")
        year = datetime.datetime.now().year
        date = datetime.date(year, int(month), int(day))
        if date > datetime.datetime.now().date():
            date = datetime.date(year-1, int(month), int(day))
        date = date.strftime("%Y-%m-%d")
        total_vaccinations = elem.find(class_="font-weight-bold text-success").text
        total_vaccinations = int(total_vaccinations.split("+")[-1].strip().replace(",", ""))
        region = elem.find(class_="d-none").text
        dix["date"].append(date)
        dix["region"].append(region)
        dix["total_vaccinations"].append(total_vaccinations)

    # Build DataFrame
    df = pd.DataFrame(dix)
    df.loc[:, "location"] = "Belgium"
    df = df.sort_values(by="date")
    df["total_vaccinations"] = df.groupby("region")["total_vaccinations"].cumsum().values
    df = df[["location", "region", "date", "total_vaccinations"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv("data/countries/Belgium.csv", index=False)


if __name__ == "__main__":
    main()