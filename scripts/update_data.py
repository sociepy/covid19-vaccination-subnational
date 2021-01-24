"""Inspired by OWID repo:

https://github.com/owid/covid-19-data/blob/master/scripts/scripts/vaccinations/run_python_scripts.py
"""
import pandas as pd
from datetime import datetime
import os
from glob import glob


SKIP = ["bulgaria.py", "utils.py"]

scripts_path = "scripts/countries/*/*.py"
batch = glob("scripts/countries/batch/*.py")
incremental = glob("scripts/countries/incremental/*.py")
scripts = batch + incremental


# Update files
for script in scripts:
    if os.path.basename(script) not in SKIP:
        print(f"{datetime.now().replace(microsecond=0)} - {script}")
        os.system(f"python {script}")


# Merge csvs and generate new data file
print(f"{datetime.now().replace(microsecond=0)} - Creating data/vaccinations.csv")
path = "data/countries/"
files = [f for f in os.listdir(path=path) if f.endswith(f".csv")]
df = pd.concat([pd.read_csv(os.path.join(path, f)) for f in files])
colnames = ["total_vaccinations", "people_vaccinated", "people_fully_vaccinated"]
df.loc[:, colnames] = df.loc[:, colnames].astype("Int64")
df = df.sort_values(by=["location", "region", "date"])
df.to_csv("data/vaccinations.csv", index=False)
