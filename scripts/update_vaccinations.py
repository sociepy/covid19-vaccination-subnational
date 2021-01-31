import os


SCRIPTS = ["update_countries.py", "merge_countries.py"]


# Run all scripts
for script in SCRIPTS:
    os.system(f"python scripts/{script}")