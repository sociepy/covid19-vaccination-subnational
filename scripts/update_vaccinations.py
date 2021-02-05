"""Update data:

- Update country data (data/countries/*.csv).
- Merge country csvs into file data/vaccinations.csv
- Update API data.
"""


import os


SCRIPTS = ["update_countries.py", "merge_countries.py", "api_v1_update.py"]


# Run all scripts
for script in SCRIPTS:
    os.system(f"python scripts/{script}")