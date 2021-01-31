"""Inspired by OWID repo:

https://github.com/owid/covid-19-data/blob/master/scripts/scripts/vaccinations/run_python_scripts.py

Merge data/countries/* csv data into vdata/accinations.csv file
"""
import pandas as pd
from datetime import datetime
import os
from glob import glob

PATH_COUNTRIES = "data/countries/"
PATH_DATA = "data/vaccinations"

print(f"{datetime.now().replace(microsecond=0)} - Creating {PATH_DATA}")

# Load country data
files = [os.path.join(PATH_COUNTRIES, f) for f in os.listdir(path=PATH_COUNTRIES) if f.endswith(f".csv")]
df = pd.concat(files)

# Process data
colnames = ["total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]
df.loc[:, colnames] = df.loc[:, colnames].astype("Int64")

# Export
df = df.sort_values(by=["location", "region", "date"])
df.to_csv(PATH_DATA, index=False)
