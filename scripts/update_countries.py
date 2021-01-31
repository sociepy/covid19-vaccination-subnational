"""Inspired by OWID repo:

https://github.com/owid/covid-19-data/blob/master/scripts/scripts/vaccinations/run_python_scripts.py

Update data/countries/* csv data.
"""
import pandas as pd
from datetime import datetime
import os
from glob import glob


SKIP = ["bulgaria.py", "utils.py"]
BATCH_PATH = glob("scripts/countries/batch/*.py")
INCREMENTAL_PATH = glob("scripts/countries/incremental/*.py")
SCRIPTS_PATH = BATCH_PATH + INCREMENTAL_PATH


for script in SCRIPTS_PATH:
    if os.path.basename(script) not in SKIP:
        # Run country script
        print(f"{datetime.now().replace(microsecond=0)} - {script}")
        os.system(f"python {script}")
