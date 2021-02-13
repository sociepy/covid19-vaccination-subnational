#!/bin/bash
#
# Make sure to run this script from project root directory
# $ bash scripts/update_all.sh
#
# If a new country is added, make sure to use --update-population option so that population info for new country is
# available when building population-related metrics:
# $ bash scripts/update_all.sh --update-population
#
update_population=$1

COUNTRY_DATA_FOLDER_PATH="data/countries/"
COUNTRY_INFO_PATH="data/country_info.csv"
VACCINATIONS_DATA_PATH="data/vaccinations.csv"
POPULATION_DATA_PATH="data/population.csv"
API_PATH="data/api/v1"
README_TEMPLATE_PATH="_templates/README.template.md"
README_PATH="README.md"


# Update country data (data/countries/*/*.csv)
echo ">>> UPDATING COUNTRIES <<<"
python scripts/update_countries.py ${COUNTRY_DATA_FOLDER_PATH} ${COUNTRY_INFO_PATH}
# Merge all country data in single file (data/vaccinations.csv)
echo ">>> MERGING DATA <<<"
python scripts/merge_countries.py ${COUNTRY_DATA_FOLDER_PATH} ${VACCINATIONS_DATA_PATH}
# Update population file
if [ "$update_population" = --update-population ] ; then
    echo ">>> GENERATE POPULATION FILE <<<"
    python scripts/update_population.py ${VACCINATIONS_DATA_PATH} ${POPULATION_DATA_PATH}
fi
# Combine vaccination data with regional population and update data/vaccinations.csv
echo ">>> ADDING POPULATION INFO <<<"
python scripts/update_vaccinations_with_population.py ${VACCINATIONS_DATA_PATH} ${POPULATION_DATA_PATH}
# Generate API files with available data
echo ">>> UPDATING API FILES <<<"
python scripts/update_api_v1.py ${VACCINATIONS_DATA_PATH} ${COUNTRY_INFO_PATH} ${API_PATH}
# Update docs
echo ">>> UPDATING DOCS <<<"
python scripts/update_docs.py ${COUNTRY_INFO_PATH} ${README_TEMPLATE_PATH} ${README_PATH}