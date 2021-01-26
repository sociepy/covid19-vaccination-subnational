# Subnational COVID-19 vaccination data 
### [Download data 🗂️](data/vaccinations.csv)

COVID-19 vaccination data at subnational level for several countries. The source data is verified in order to ensure its
officiality. Dataset can be found in [`data/vaccinations.csv`](data/vaccinations.csv).

**This project is inspired by wonderful project [owid/covid-19-data](https://github.com/owid/covid-19-data), adopting
some of its structure, and is open to integration if deemed approriate.**

It works by running scripts on a daily basis, which gather data from different [sources](#sources).

## Data
### Data sources
| Country  	| source 	|
|-	|-	|
| 🇦🇷 Argentina    | http://datos.salud.gob.ar/dataset/vacunas-contra-covid-19-dosis-aplicadas-en-la-republica-argentina   |
| 🇦🇹 Austria  | https://info.gesundheitsministerium.gv.at/ 	|
| 🇧🇪 Belgium  	| https://covid-vaccinatie.be/en/ 	|
| 🇧🇷 Brazil  	| https://github.com/wcota/covid19br/master/cases-brazil-total.csv 	|
| 🇧🇬 Bulgaria  	| https://coronavirus.bg/bg/statistika 	|
| 🇨🇦 Canada  	| https://github.com/ccodwg/Covid19Canada/ 	|
| 🇨🇱 Chile  	| https://github.com/juancri/covid19-vaccination/blob/master/output/chile-vaccination.csv 	|
| 🇩🇰 Denmark  	| https://covid19.ssi.dk/overvagningsdata/vaccinationstilslutning 	|
| 🇫🇷 France  	| https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-personnes-vaccinees-contre-la-covid-19/ 	|
| 🇩🇪 Germany  	| https://github.com/mathiasbynens/covid-19-vaccinations-germany/ 	|
| 🇮🇹 Italy  	| https://github.com/italia/covid19-opendata-vaccini/ 	|
| 🇳🇴 Norway  	| https://www.fhi.no/sv/vaksine/koronavaksinasjonsprogrammet/koronavaksinasjonsstatistikk/ 	|
| 🇵🇱 Poland	| https://www.gov.pl/web/szczepimysie/raport-szczepien-przeciwko-covid-19	|
| 🇸🇰 Slovakia	| https://github.com/Institut-Zdravotnych-Analyz/covid19-data/blob/main/OpenData_Slovakia_Vaccination_Regions.csv 	|
| 🇪🇸 Spain  	| https://github.com/civio/covid-vaccination-spain/ 	|
| 🇸🇪 Sweden  	| https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/vaccination-mot-covid-19/statistik-over-forbrukade-vaccindoser/ 	|
| 🇬🇧 United Kingdom  	| https://coronavirus.data.gov.uk/details/download 	|
| 🇺🇸 United States  	| https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=vaccination_data 	|

### Format
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
|  `people_fully_vaccinated` 	| Total number of people who received all doses prescribed by the vaccination protocol. If a person receives the first dose of a 2-dose vaccine, this metric stays the same. If they receive the second dose, the metric goes up by 1. 	|

Note: for `people_vaccinated` and `people_fully_vaccinated` we are dependent on the necessary data being made available,
so we may not be able to make these metrics available for some countries.

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