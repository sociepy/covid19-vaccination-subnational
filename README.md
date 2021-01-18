# Subnational COVID-19 vaccination data 
### [Download data 🗂️](data/vaccinations.csv)

This project aims to gather COVID-19 vaccination data at subnational level for as many countries as possible. The data
can be found in [`data/vaccinations.csv`](data/vaccinations.csv).

**This project is inspired by wonderful project [owid/covid-19-data](https://github.com/owid/covid-19-data) and is open
to integration if deemed approriate.**

It works by running scripts on a daily basis, which gather data from different [sources](#sources).

## Data
The data pretends to resemble the API proposed by [owid/covid-19-data](https://github.com/owid/covid-19-data). Find
below the field description, mainly provided by [OWID](https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/README.md).

* `location`: name of the country.
* `region`: name of the subnational region of the country.
* `date`: date of the observation.
* `location_iso`: ISO 3166-1 country codes (XX)
* `region_iso`: ISO 3166-2 region codes (XX-YY or XX-YYY).
* `total_vaccinations`: total number of doses administered. This is counted as a single dose, and may not equal the total number of people vaccinated, depending on the specific dose regime (e.g. people receive multiple doses). If a person receives one dose of the vaccine, this metric goes up by 1. If they receive a second dose, it goes up by 1 again.
* `people_vaccinated`: total number of people who received at least one vaccine dose. If a person receives the first dose of a 2-dose vaccine, this metric goes up by 1. If they receive the second dose, the metric stays the same.
* `people_fully_vaccinated`: total number of people who received all doses prescribed by the vaccination protocol. If a person receives the first dose of a 2-dose vaccine, this metric stays the same. If they receive the second dose, the metric goes up by 1.

Note: for `people_vaccinated` and `people_fully_vaccinated` we are dependent on the necessary data being made available,
so we may not be able to make these metrics available for some countries.

### Data sources
- Austria: https://info.gesundheitsministerium.gv.at/data/laender.csv
- Belgium: https://covid-vaccinatie.be/en/vaccines-administered
- Bulgaria: https://coronavirus.bg/bg/statistika
- Canada: https://github.com/ccodwg/Covid19Canada/
- Denmark: https://covid19.ssi.dk/overvagningsdata/vaccinationstilslutning
- France: https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-personnes-vaccinees-contre-la-covid-19/
- Germany: https://github.com/mathiasbynens/covid-19-vaccinations-germany/
- Italy: https://github.com/italia/covid19-opendata-vaccini/
- Spain: https://github.com/civio/covid-vaccination-spain/
- United Kingdom: https://coronavirus.data.gov.uk/details/download
- United States: https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=vaccination_data

## Contribute
The data is updated using the script [`update_data.py`](scripts/update_data.py). This script first runs all
[country/scripts](scripts/countries/), which generate [country data](data/countries/) and then joins these results into
file [`vaccinations.csv`](data/vaccinations.csv).

To contribute, feel free to issue PRs with new automated scripts. Note that the automated scripts are divided into two
categories:

- [`batch`](scripts/countries/batch): Gets the whole data (all dates) from a source file and overwrites the existing data.
- [`incremental`](scripts/countries/incremental): Gets last date's data and appends it to existing data.

### Data update
Currently I manually run the [`update_data.py`](scripts/update_data.py) script and update the existing available data in this repo. This approach is described below:

Make sure to install all dependencies, `pip install -r requirements.txt`.

Run

```
$ python scripts/update_data.py
```

File [data/vaccinations.csv](data/vaccinations.csv) is then updated.

## License
See [LICENSE](LICENSE).

> This site or product includes IP2Location™ ISO 3166-2 Subdivision Code which available from
> https://www.ip2location.com.