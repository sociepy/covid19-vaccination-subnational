import pandas as pd


def main():
    url = "https://raw.githubusercontent.com/civio/covid-vaccination-spain/main/data.csv"
    df = pd.read_csv(url, dtype={"dosis administradas": str})
    df = df.rename(columns={
        "informe": "date",
        "comunidad autónoma": "region",
        "dosis administradas": "total_vaccinations"
    })
    df.loc[:, "date"] = pd.to_datetime(df.loc[:, "date"], format="%d/%m/%Y")
    df.loc[:, "date"] = df.loc[:, "date"].dt.strftime("%Y-%m-%d")
    df.loc[:, "total_vaccinations"] = df.loc[:, "total_vaccinations"].apply(lambda x: int(x.replace(".", "")))
    df.loc[:, "location"] = "Spain"
    df = df[["location", "region", "date", "total_vaccinations"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv("data/countries/Spain.csv", index=False)


if __name__ == "__main__":
    main()