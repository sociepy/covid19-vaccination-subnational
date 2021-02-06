import pandas as pd


print("Adding indices relative to population")
PATH_VACCINATION_DATA = "data/vaccinations.csv"
PATH_POPULATION_DATA = "data/population.csv"

# Load data
df_pop = pd.read_csv(PATH_POPULATION_DATA, index_col=False)
df_pop = df_pop.loc[df_pop["date"]==df_pop["date"].max(), ["region_iso", "population"]]
df_vac = pd.read_csv(PATH_VACCINATION_DATA, index_col=False)

df = df_vac.merge(df_pop, on="region_iso", how="left")

columns = ["total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]
for column in columns:
    df.loc[:, f"{column}_per_100"] = (100*df.loc[:, column]/df.loc[:, "population"]).apply(lambda x: round(x, 2))

df = df.drop(columns=["population"])
df = df.sort_values(by=["location", "region", "date"])
df.to_csv(PATH_VACCINATION_DATA, index=False)