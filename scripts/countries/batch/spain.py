import pandas as pd


def main():
    url = "https://raw.githubusercontent.com/civio/covid-vaccination-spain/main/data.csv"
    df = pd.read_csv(url, parse_dates=["informe"], dtype={"dosis administradas": str})
    df = df.rename(columns={
        "informe": "date",
        "comunidad autónoma": "region",
        "dosis administradas": "total_vaccinations"
    })
    df.loc[:, "total_vaccinations"] = df.loc[:, "total_vaccinations"].apply(lambda x: int(x.replace(".", "")))
    df.loc[:, "country"] = "Spain"
    df.loc[:, "date"] = df.loc[:, "date"].dt.strftime("%Y-%m-%d")
    df = df[["date", "country", "region", "total_vaccinations"]]
    df.to_csv("output/countries/Spain.csv", index=False)


if __name__ == "__main__":
    main()