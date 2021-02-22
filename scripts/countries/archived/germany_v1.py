import pandas as pd
from covid_updater.iso import ISODB
from covid_updater.utils import export_data


COUNTRY = "Germany"
COUNTRY_ISO = "DE"
OUTPUT_FILE = f"data/countries/{COUNTRY}.csv"
DATA_URL = "https://raw.githubusercontent.com/mathiasbynens/covid-19-vaccinations-germany/main/data/data.csv"
DATA_URL_REFERENCE = "https://github.com/mathiasbynens/covid-19-vaccinations-germany/"
REGION_RENAMING = {"Baden-Württemberg": "Baden-Wurttemberg", "Thüringen": "Thuringen"}


def main():
    df = pd.read_csv(
        DATA_URL,
        usecols=["date", "state", "firstDosesCumulative", "secondDosesCumulative"],
    )
    df = df.rename(
        columns={
            "state": "region",
            "firstDosesCumulative": "people_vaccinated",
            "secondDosesCumulative": "people_fully_vaccinated",
        }
    )
    df.loc[:, "total_vaccinations"] = (
        df.loc[:, "people_vaccinated"] + df.loc[:, "people_fully_vaccinated"]
    )
    df.loc[:, "region"] = df.loc[:, "region"].replace(REGION_RENAMING)
    df.loc[:, "date"] = pd.to_datetime(df.loc[:, "date"], format="%Y-%m-%d")
    df.loc[:, "date"] = df.loc[:, "date"].dt.strftime("%Y-%m-%d")
    df.loc[:, "location"] = COUNTRY

    # Add ISO codes
    df = ISODB().merge(df, country_iso=COUNTRY_ISO)

    #  Export
    export_data(df=df, data_url_reference=DATA_URL_REFERENCE, output_file=OUTPUT_FILE)


if __name__ == "__main__":
    main()
