"""Inspired by OWID repo:

https://github.com/owid/covid-19-data/blob/master/scripts/scripts/vaccinations/run_python_scripts.py
"""
import pandas as pd
from datetime import datetime
import os
from glob import glob


scripts_path = "scripts/countries/*/*.py"
scripts = glob(scripts_path)


# Update files
for script in scripts:
    print(f"{datetime.now().replace(microsecond=0)} - {script}")
    os.system(f"python {script}")


# Merge csvs and generate new data file
print(f"{datetime.now().replace(microsecond=0)} - Creating data.csv")
path = "output/countries"
files = [f for f in os.listdir(path=path) if f.endswith(f".csv")]
df = pd.concat([pd.read_csv(os.path.join(path, f)) for f in files])
df.to_csv("output/data.csv")
