import pandas as pd


def main():
    url = "https://raw.githubusercontent.com/mathiasbynens/covid-19-vaccinations-germany/main/data/data.csv"
    df = pd.read_csv(url, usecols=["date", "state", "vaccinationsCumulative"], parse_dates=["date"])
    df = df.rename(columns={
        "state": "region",
        "vaccinationsCumulative": "total_vaccinations",
    })
    df.loc[:, "date"] = pd.to_datetime(df.loc[:, "date"], format="%Y-%m-%d")
    df.loc[:, "date"] = df.loc[:, "date"].dt.strftime("%Y-%m-%d")
    df.loc[:, "country"] = "Germany"
    df = df[["date", "country", "region", "total_vaccinations"]]
    df.to_csv("data/countries/Germany.csv", index=False)


if __name__ == "__main__":
    main()