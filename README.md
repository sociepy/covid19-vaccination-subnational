# Subnational COVID-19 vaccination data 
### [Download data 🗂️ ⬇️](https://raw.githubusercontent.com/sociepy/covid19-vaccination-subnational/main/data/vaccinations.csv)

COVID-19 vaccination data at subnational level. The source data is verified in order to ensure its officiality.

> Dataset can be found in file [`data/vaccinations.csv`](data/vaccinations.csv).

ℹ️ This project is inspired by wonderful project [owid/covid-19-data](https://github.com/owid/covid-19-data), adopting
some of its structure, and is open to integration if deemed approriate.

## Content
* [Data sources](#data-sources)
* [API](#api)
* [Contribute](#contribute)
* [License](#license)
## Data sources
| Country  	| Source 	| 2-dose |
|-	|-	|- |
| 🇦🇷 Argentina    | http://datos.salud.gob.ar/dataset/vacunas-contra-covid-19-dosis-aplicadas-en-la-republica-argentina   | ✅ |
| 🇦🇹 Austria  | https://info.gesundheitsministerium.gv.at/ 	| ✅ |
| 🇧🇪 Belgium  	| https://covid-vaccinatie.be/en/ 	| ✅ |
| 🇧🇷 Brazil  	| https://github.com/wcota/covid19br/ 	| ❌ |
| 🇧🇬 Bulgaria  	| https://coronavirus.bg/bg/statistika 	| ❌ |
| 🇨🇦 Canada  	| https://github.com/ccodwg/Covid19Canada/ 	| ✅ |
| 🇨🇱 Chile  	| https://github.com/juancri/covid19-vaccination/ 	| ✅ |
| 🇨🇿 Czechia  	| https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ 	| ✅ |
| 🇩🇰 Denmark  	| https://covid19.ssi.dk/overvagningsdata/vaccinationstilslutning 	| ✅ |
| 🇫🇷 France  	| https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-personnes-vaccinees-contre-la-covid-19/ 	| ❌ |
| 🇩🇪 Germany  	| https://github.com/mathiasbynens/covid-19-vaccinations-germany/ 	| ✅ |
| 🇮🇹 Italy  	| https://github.com/italia/covid19-opendata-vaccini/ 	| ✅ |
| 🇱🇮 Liechtenstein | https://github.com/rsalzer/COVID_19_VACC/	| ❌ |
| 🇳🇴 Norway  	| https://www.fhi.no/sv/vaksine/koronavaksinasjonsprogrammet/koronavaksinasjonsstatistikk/ 	| ✅ |
| 🇵🇱 Poland	| https://www.gov.pl/web/szczepimysie/raport-szczepien-przeciwko-covid-19	| ✅ |
| 🇸🇰 Slovakia	| https://github.com/Institut-Zdravotnych-Analyz/covid19-data/ 	| ✅ |
| 🇪🇸 Spain  	| https://github.com/civio/covid-vaccination-spain/ 	| ✅ |
| 🇸🇪 Sweden  	| https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/vaccination-mot-covid-19/statistik-over-forbrukade-vaccindoser/ 	| ❌ |
| 🇨🇭 Switzerland	| https://github.com/rsalzer/COVID_19_VACC/ 	| ❌ |
| 🇬🇧 United Kingdom  	| https://coronavirus.data.gov.uk/details/download 	| ✅ |
| 🇺🇸 United States  	| https://covid.cdc.gov/covid-data-tracker/COVIDData/	| ✅ |

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
|  `people_fully_vaccinated` 	| Total number of people who received all doses prescribed by the vaccination protocol. If a person receives the first dose of a 2-dose vaccine, this metric stays the same. If they receive the second dose, the metric goes up by 1. 	|

Note: for `people_vaccinated` and `people_fully_vaccinated` we are dependent on the necessary data being made available,
so we may not be able to make these metrics available for some countries.

## Contribute
The data is updated using the script [`update_data.py`](scripts/update_data.py). This script first runs all
[country/scripts](scripts/countries/), generates [country data](data/countries/) and finally merges these into file [`vaccinations.csv`](data/vaccinations.csv).

```
$ pip install -r requirements.txt
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

## License
See [LICENSE](LICENSE).

> This site or product includes IP2Location™ ISO 3166-2 Subdivision Code which available from
> https://www.ip2location.com.


| Country  	| Source 	| 2-dose |
|-	|-	|- |
| 🇦🇷 Argentina    | http://datos.salud.gob.ar/dataset/vacunas-contra-covid-19-dosis-aplicadas-en-la-republica-argentina   | ✅ |
| 🇦🇹 Austria  | https://info.gesundheitsministerium.gv.at/ 	| ✅ |
| 🇧🇪 Belgium  	| https://covid-vaccinatie.be/en/ 	| ✅ |


| Country  	| Source 	| 2-dose 	|
|-	|-	|- |
| 🇦🇷 Argentina    | test   | ✅ 	|
| 🇦🇹 Austria  | https://info.gesundheitsministerium.gv.at/ 	| ✅ 	|
| 🇧🇪 Belgium  	| https://covid-vaccinatie.be/en/ 	| ✅ 	|