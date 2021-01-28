"""Inspired by OWID repo:

https://github.com/owid/covid-19-data/blob/master/scripts/scripts/vaccinations/run_python_scripts.py

Update data/countries/* csv data.
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
