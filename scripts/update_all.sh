# Update country data (data/countries/*/*.csv)
python update_countries.py
# Merge all country data in single file (data/vaccinations.csv)
python merge_countries.py
# Combina vaccination data with regional population and update data/vaccinations.csv
python cross_with_population.py
# Generate API files with available data
python upadte_api_v1.py