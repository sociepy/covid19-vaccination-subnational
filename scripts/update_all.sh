# Make sure to run this script from project root directory
# $ bash scripts/update_all.sh

COUNTRY_DATA_FOLDER_PATH="data/countries2/"
SOURCE_INFO_PATH="data/country_info.csv"
VACCINATIONS_DATA_PATH="data/vaccinations2.csv"
POPULATION_DATA_PATH="data/population.csv"
API_PATH="data/api/v2"
README_TEMPLATE_PATH="_templates/README.template.md"
README_PATH="README.md"

# echo ">>> GENERATE POPULATION FILE <<<"
# python scripts/update_population.py ${POPULATION_DATA_PATH}
# Update country data (data/countries/*/*.csv)
echo ">>> UPDATING COUNTRIES <<<"
python scripts/update_countries.py ${COUNTRY_DATA_FOLDER_PATH} ${SOURCE_INFO_PATH}
# Merge all country data in single file (data/vaccinations.csv)
echo ">>> MERGING DATA <<<"
python scripts/merge_countries.py ${COUNTRY_DATA_FOLDER_PATH} ${VACCINATIONS_DATA_PATH}
# Combine vaccination data with regional population and update data/vaccinations.csv
echo ">>> ADDING POPULATION INFO <<<"
python scripts/update_vaccinations_with_population.py ${VACCINATIONS_DATA_PATH} ${POPULATION_DATA_PATH}
# Generate API files with available data
echo ">>> UPDATING API FILES <<<"
python scripts/update_api_v1.py ${COUNTRY_DATA_FOLDER_PATH} ${API_PATH}