import pandas as pd


def main():
    url = "https://raw.githubusercontent.com/ccodwg/Covid19Canada/master/timeseries_prov/vaccine_administration_timeseries_prov.csv"
    df = pd.read_csv(url)

    df = df.rename(columns={
        "date_vaccine_administered": "date",
        "province": "region",
        "cumulative_avaccine": "total_vaccinations"
    })
    df.loc[:, "date"] = pd.to_datetime(df.loc[:, "date"], format="%d-%m-%Y")
    df.loc[:, "date"] = df.loc[:, "date"].dt.strftime("%Y-%m-%d")
    df.loc[:, "country"] = "Canada"
    df = df[["date", "country", "region", "total_vaccinations"]]
    df.to_csv("data/countries/Canada.csv", index=False)


if __name__ == "__main__":
    main()