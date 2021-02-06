# Subnational COVID-19 vaccination data 
### [Download data 🗂️ ⬇️](data/vaccinations.csv) | [API](api/v1) | [GitHub](https://github.com/sociepy/covid19-vaccination-subnational)

COVID-19 vaccination data at subnational level. To ensure its officiality, the source data is carefully verified.

> 🆕 API static endpoint available [here](https://sociepy.org/covid19-vaccination-subnational/api/v1)

> CSV dataset can be found [here](https://raw.githubusercontent.com/sociepy/covid19-vaccination-subnational/main/data/vaccinations.csv).


This project is inspired by wonderful project [owid/covid-19-data](https://github.com/owid/covid-19-data), adopting
some of its structure, and is open to integration if deemed approriate.

## Content
* [Repository organization](#repository-organization)
* [Data sources](#data-sources)
* [CSV API](#api)
* [JSON Endpoint API](api/v1/README.md)
* [Contribute](#contribute)
* [Documentation](docs/CODE.md) (WIP 🚧)
* [License](#license)


## Data sources
This project wouldn't be possible without the great resources available online.

{data_sources}

## API
The data pretends to resemble the API proposed by [owid/covid-19-data](https://github.com/owid/covid-19-data). Find
below the field description, mainly provided by [OWID](https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/README.md).

| Field 	| Description 	|
|-	|-	|
| `location` 	| Name of the country. 	|
| `region` 	| Name of the subnational region of the country. 	|
| `date` 	| Date of the observation. 	|
| `location_iso` 	| ISO 3166-1 country codes (XX) 	|
| `region_iso` 	| ISO 3166-2 region codes (XX-YY or XX-YYY). 	|
| `total_vaccinations` 	| Total number of doses administered. This is counted as a single dose, and may not equal the total number of people vaccinated, depending on the specific dose regime (e.g. people receive multiple doses). If a person receives one dose of the vaccine, this metric goes up by 1. If they receive a second dose, it goes up by 1 again. 	|
| `people_vaccinated` 	| Total number of people who received at least one vaccine dose. If a person receives the first dose of a 2-dose vaccine, this metric goes up by 1. If they receive the second dose, the metric stays the same. 	|
|  `people_fully_vaccinated`    | Total number of people who received all doses prescribed by the vaccination protocol. If a person receives the first dose of a 2-dose vaccine, this metric stays the same. If they receive the second dose, the metric goes up by 1.  |
| `total_vaccinations_per_100` 	| `tota_vaccinations` per 100 habitants. |
| `people_vaccinated_per_100` 	| `people_vaccinated` per 100 habitants.	|
|  `people_fully_vaccinated_per_100` 	| `people_fully_vaccinated` per 100 habitants. 	|

Note: for `people_vaccinated` and `people_fully_vaccinated` we are dependent on the necessary data being made available,
so we may not be able to make these metrics available for some countries.

## Contribute
The data is updated using the script [`update_data.py`](scripts/update_data.py). This script first runs all
[country/scripts](scripts/countries/), generates [country data](data/countries/) and finally merges these into file [`vaccinations.csv`](data/vaccinations.csv).

```
$ pip install -e .
$ python scripts/update_vaccinations.py
```

There is a script per country, each of them acting as ETL for the specific country. These scripts are classified into
two categories:

- [`batch`](scripts/countries/batch): Gets the whole data (all dates) from a source file and overwrites the existing data.
- [`incremental`](scripts/countries/incremental): Gets last date's data and appends it to existing data.

Other folders [`archived`](scripts/countries/archived) and [`input`](scripts/countries/input) contain
archived scripts and auxiliary third party files, respectively.

### Add new countries
If you know of any reference publishing vaccination regional data for other countries, your contribution is very much
appreciated! It is extremely helpfull if you could [report this in the issues](https://github.com/sociepy/covid19-vaccination-subnational/issues/new). Also, if you feel like automating it by
yourself (that'd be awesome!), please fork this repository and issue a pull request
with your changes.

### Bugs
We do our best to ensure that the data is reliable. However, as the project grows and source website change their
format, some bugs might appear. If you detect any, please [report this in the issues section](https://github.com/sociepy/covid19-vaccination-subnational/issues/new).

## Documentation
See [documentation](docs/CODE.md) (WIP 🚧)

## License
See [LICENSE](LICENSE).

> This site or product includes IP2Location™ ISO 3166-2 Subdivision Code which available from
> https://www.ip2location.com.
