import requests
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
from covid_updater.iso import ISODB
from covid_updater.utils import export_data


COUNTRY = "Belgium"
COUNTRY_ISO = "BE"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://covid-vaccinatie.be/en"
DATA_URL_REFERENCE = DATA_URL


def download_xlsx(url, tmp_file="tmp/belgium.xlsx"):
    local_tmp_file = "tmp/belgium.xlsx"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686)"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
    with open(local_tmp_file, "wb") as f:
        f.write(the_page)
    df = pd.read_excel(local_tmp_file)
    return df


def get_date(url):
    df_dates = download_xlsx(url)
    df_dates.loc[:, "Date"] = pd.to_datetime(
        df_dates.loc[:, "Date"], format="%d/%m/%Y"
    ).dt.strftime("%Y-%m-%d")
    df_dates = df_dates.groupby("Region").agg({"Date": "max"})
    df_dates = df_dates.rename(columns={"Date": "date"})
    return df_dates


def main():
    # Load current data
    df_source = pd.read_csv(OUTPUT_FILE)

    # Load data
    page_content = requests.get(DATA_URL, headers={"User-Agent": "Custom"}).content
    soup = BeautifulSoup(page_content, "html.parser")

    # Get new data
    boxes = soup.findAll(class_="col-12 col-md-6 col-xl-4")
    new_data = []
    if len(boxes) == 3:
        for box in boxes:
            fields = box.findAll(class_="col-12")
            if len(fields) == 4:
                region = fields[0].text.strip()
                if "Vaccines administered" in fields[1].text:
                    total, regional = fields[1].findAll(class_="col-auto text-end")
                    dose_1, dose_2 = list(
                        map(
                            lambda x: int(x.replace(",", "")),
                            regional.text.strip().split("\n"),
                        )
                    )
                    new_data.append([region, dose_1, dose_2])
    df = pd.DataFrame(
        new_data, columns=["region", "people_vaccinated", "people_fully_vaccinated"]
    )

    # Process
    df.loc[:, "total_vaccinations"] = (
        df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
    )
    df.loc[:, "location"] = COUNTRY

    # Join with date
    url = "https://covid-vaccinatie.be/en/vaccines-administered.xlsx"
    df_dates = get_date(url)
    df = df.merge(df_dates, left_on="region", right_on="Region", how="left")

    # ISO
    df = ISODB().merge(df, country_iso=COUNTRY_ISO)

    # Concatenate
    region = df_dates.index.tolist()
    date = df_dates.date.tolist()
    df_source = df_source.loc[
        ~(df_source["region"].isin(region) & df_source["date"].isin(date))
    ]
    df = pd.concat([df, df_source])

    #  Export
    export_data(df=df, data_url_reference=DATA_URL_REFERENCE, output_file=OUTPUT_FILE)


if __name__ == "__main__":
    main()
