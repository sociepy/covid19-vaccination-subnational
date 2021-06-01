# Subnational COVID-19 vaccination data
**⚠️ Note: This project is not actively maintained, if you want to take over let me know via the issues section. As an alternative project, you can find regional data for some countries at [govex/COVID-19](https://github.com/govex/COVID-19/tree/master/data_tables/vaccine_data/global_data).**

### [**API**](https://sociepy.org/covid19-vaccination-subnational/data/api/v1) | [**Download data**](data/vaccinations.csv) | [**GitHub**](https://github.com/sociepy/covid19-vaccination-subnational)

![refresh](https://github.com/sociepy/covid19-vaccination-subnational/workflows/refresh/badge.svg?branch=main)
![GitHub last commit](https://img.shields.io/github/last-commit/sociepy/covid19-vaccination-subnational)
[![Website link!](https://img.shields.io/badge/website-link-1abc9c.svg)](https://sociepy.org/covid19-vaccination-subnational/)
[![API link!](https://img.shields.io/badge/API-link-1abc9c.svg)](https://sociepy.org/covid19-vaccination-subnational/data/api/v1)

<!-- Place this tag where you want the button to render. -->
<a class="github-button" href="https://github.com/sociepy" data-color-scheme="no-preference: light; light: dark; dark: light;" data-size="large" aria-label="Follow @sociepy on GitHub">Follow @sociepy</a>
<!-- Place this tag where you want the button to render. -->
<a class="github-button" href="https://github.com/sociepy/covid19-vaccination-subnational"
data-color-scheme="no-preference: light; light: dark; dark: light;" data-icon="octicon-star" data-size="large"
aria-label="Star sociepy/covid19-vaccination-subnational on GitHub">Star</a>
<!-- Place this tag where you want the button to render. -->
<a class="github-button" href="https://github.com/sociepy/covid19-vaccination-subnational/fork"
data-color-scheme="no-preference: light; light: dark; dark: light;" data-icon="octicon-repo-forked" data-size="large"
aria-label="Fork sociepy/covid19-vaccination-subnational on GitHub">Fork</a>


COVID-19 vaccination data at subnational level. To ensure its officiality, the source data is carefully verified.

All country data can be found in a [single
csv file](https://raw.githubusercontent.com/sociepy/covid19-vaccination-subnational/main/data/vaccinations.csv). If you
are interested in indiviual country data, you may want to check [countries](data/countries) folder.

Additionally, we provide a static API endpoint, which contains the data per country as JSONs. For more details check [here](https://sociepy.org/covid19-vaccination-subnational/data/api/v1).


### Thanks to
This project is inspired by wonderful project [owid/covid-19-data](https://github.com/owid/covid-19-data), adopting
some of its structure, and is open to integration if deemed appropriate.
In addition, thanks to all of the people involved in the different [source data](#data-sources) initiatives.


## Content
* [Data sources](#data-sources)
* [Data format](#data-format)
* [JSON Endpoint API](data/api/v1/README.md)
* [Contribute](#contribute)
* [Documentation](docs/CODE.md) (WIP 🚧)
* [License](#license)


## Data sources
This project wouldn't be possible without the great resources available online.

| Country           | Source                                                                                                                                                                                                                                                                                                                                                                 | 2-Dose   | Last update   |
|:------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|:--------------|
| 🇪🇸 Spain          | [https://github.com/civio/covid-vaccination-spain/](https://github.com/civio/covid-vaccination-spain/)                                                                                                                                                                                                                                                                 | ✅        | 2021-06-01    |
| 🇦🇷 Argentina      | [http://datos.salud.gob.ar/dataset/vacunas-contra-covid-19-dosis-aplicadas-en-la-republica-argentina](http://datos.salud.gob.ar/dataset/vacunas-contra-covid-19-dosis-aplicadas-en-la-republica-argentina)                                                                                                                                                             | ✅        | 2021-06-01    |
| 🇺🇾 Uruguay        | [https://github.com/3dgiordano/covid-19-uy-vacc-data/](https://github.com/3dgiordano/covid-19-uy-vacc-data/)                                                                                                                                                                                                                                                           | ✅        | 2021-06-01    |
| 🇧🇷 Brazil         | [https://github.com/wcota/covid19br/](https://github.com/wcota/covid19br/)                                                                                                                                                                                                                                                                                             | ✅        | 2021-06-01    |
| 🇰🇷 Korea          | [https://ncv.kdca.go.kr/](https://ncv.kdca.go.kr/)                                                                                                                                                                                                                                                                                                                     | ✅        | 2021-06-01    |
| 🇷🇺 Russia         | [https://gogov.ru/articles/covid-v-stats](https://gogov.ru/articles/covid-v-stats)                                                                                                                                                                                                                                                                                     | ✅        | 2021-06-01    |
| 🇱🇧 Lebanon        | [https://impact.cib.gov.lb/home/dashboard/vaccine](https://impact.cib.gov.lb/home/dashboard/vaccine)                                                                                                                                                                                                                                                                   | ❌        | 2021-06-01    |
| 🇦🇺 Australia      | [https://covidlive.com.au/report/vaccinations](https://covidlive.com.au/report/vaccinations)                                                                                                                                                                                                                                                                           | ❌        | 2021-06-01    |
| 🇹🇷 Turkey         | [https://covid19asi.saglik.gov.tr/](https://covid19asi.saglik.gov.tr/)                                                                                                                                                                                                                                                                                                 | ✅        | 2021-06-01    |
| 🇵🇪 Peru           | [https://gis.minsa.gob.pe/GisVisorVacunados/](https://gis.minsa.gob.pe/GisVisorVacunados/)                                                                                                                                                                                                                                                                             | ❌        | 2021-06-01    |
| 🇮🇹 Italy          | [https://github.com/italia/covid19-opendata-vaccini/](https://github.com/italia/covid19-opendata-vaccini/)                                                                                                                                                                                                                                                             | ✅        | 2021-06-01    |
| 🇳🇴 Norway         | [https://www.fhi.no/sv/vaksine/koronavaksinasjonsprogrammet/koronavaksinasjonsstatistikk/](https://www.fhi.no/sv/vaksine/koronavaksinasjonsprogrammet/koronavaksinasjonsstatistikk/)                                                                                                                                                                                   | ✅        | 2021-06-01    |
| 🇸🇰 Slovakia       | [https://github.com/Institut-Zdravotnych-Analyz/covid19-data/](https://github.com/Institut-Zdravotnych-Analyz/covid19-data/)                                                                                                                                                                                                                                           | ✅        | 2021-06-01    |
| 🇫🇮 Finland        | [https://piikki.juiciness.io/](https://piikki.juiciness.io/)                                                                                                                                                                                                                                                                                                           | ✅        | 2021-05-31    |
| 🇬🇧 United Kingdom | [https://coronavirus.data.gov.uk/details/download](https://coronavirus.data.gov.uk/details/download)                                                                                                                                                                                                                                                                   | ✅        | 2021-05-31    |
| 🇧🇪 Belgium        | [https://covid-vaccinatie.be/en](https://covid-vaccinatie.be/en)                                                                                                                                                                                                                                                                                                       | ✅        | 2021-05-31    |
| 🇩🇪 Germany        | [https://github.com/mathiasbynens/covid-19-vaccinations-germany/](https://github.com/mathiasbynens/covid-19-vaccinations-germany/)                                                                                                                                                                                                                                     | ✅        | 2021-05-31    |
| 🇫🇷 France         | [https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-personnes-vaccinees-contre-la-covid-19-1/](https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-personnes-vaccinees-contre-la-covid-19-1/)                                                                                                                                                           | ✅        | 2021-05-31    |
| 🇩🇰 Denmark        | [https://covid19.ssi.dk/overvagningsdata/vaccinationstilslutning](https://covid19.ssi.dk/overvagningsdata/vaccinationstilslutning)                                                                                                                                                                                                                                     | ✅        | 2021-05-31    |
| 🇨🇿 Czechia        | [https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/](https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/)                                                                                                                                                                                                                                                           | ✅        | 2021-05-31    |
| 🇨🇦 Canada         | [https://github.com/ccodwg/Covid19Canada](https://github.com/ccodwg/Covid19Canada)                                                                                                                                                                                                                                                                                     | ✅        | 2021-05-31    |
| 🇦🇹 Austria        | [https://info.gesundheitsministerium.gv.at/](https://info.gesundheitsministerium.gv.at/)                                                                                                                                                                                                                                                                               | ✅        | 2021-05-31    |
| 🇨🇱 Chile          | [https://github.com/juancri/covid19-vaccination/](https://github.com/juancri/covid19-vaccination/)                                                                                                                                                                                                                                                                     | ✅        | 2021-05-30    |
| 🇸🇪 Sweden         | [https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/vaccination-mot-covid-19/statistik/statistik-over-registrerade-vaccinationer-covid-19/](https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/vaccination-mot-covid-19/statistik/statistik-over-registrerade-vaccinationer-covid-19/) | ✅        | 2021-05-23    |
| 🇮🇸 Iceland        | [https://e.infogram.com/c3bc3569-c86d-48a7-9d4c-377928f102bf](https://e.infogram.com/c3bc3569-c86d-48a7-9d4c-377928f102bf)                                                                                                                                                                                                                                             | ✅        | 2021-05-11    |
| 🇺🇦 Ukraine        | [https://health-security.rnbo.gov.ua/vaccination](https://health-security.rnbo.gov.ua/vaccination)                                                                                                                                                                                                                                                                     | ✅        | 2021-05-07    |
| 🇮🇳 India          | [https://india-covid19vaccine.github.io](https://india-covid19vaccine.github.io)                                                                                                                                                                                                                                                                                       | ✅        | 2021-05-03    |
| 🇨🇭 Switzerland    | [https://github.com/rsalzer/COVID_19_VACC/](https://github.com/rsalzer/COVID_19_VACC/)                                                                                                                                                                                                                                                                                 | ✅        | 2021-04-04    |
| 🇺🇸 United States  | [https://github.com/youyanggu/covid19-cdc-vaccination-data](https://github.com/youyanggu/covid19-cdc-vaccination-data)                                                                                                                                                                                                                                                 | ✅        | 2021-03-07    |
| 🇵🇱 Poland         | [https://www.gov.pl/web/szczepimysie/raport-szczepien-przeciwko-covid-19](https://www.gov.pl/web/szczepimysie/raport-szczepien-przeciwko-covid-19)                                                                                                                                                                                                                     | ✅        | 2021-02-11    |

## Data format
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
| `total_vaccinations_per_100` 	| `total_vaccinations` per 100 habitants. |
| `people_vaccinated_per_100` 	| `people_vaccinated` per 100 habitants.	|
|  `people_fully_vaccinated_per_100` 	| `people_fully_vaccinated` per 100 habitants. 	|

Note: for `people_vaccinated` and `people_fully_vaccinated` we are dependent on the necessary data being made available,
so we may not be able to make these metrics available for some countries.

## Contribute
The updates are done using [update_all.sh](scripts/update_all.sh) script. For more details on the scripts being used,
check [here](scripts/README.md).


### Set up environment
Install the package:

```
$ pip install -e .
```

### Execute update

```
$ bash scripts/update_all.sh
```

### Add new countries
**New: Use [this notebook](docs/add-new-scraper.ipynb) as a guideline on how to add a new country scraper!**

If you know of any reference publishing vaccination regional data for other countries, your contribution is very much
appreciated! It is extremely helpfull if you could [report this in the issues](https://github.com/sociepy/covid19-vaccination-subnational/issues/new). Also, if you feel like automating it by
yourself (that'd be awesome!), please fork this repository and issue a pull request
with your changes.

The country scraping logic lives within the package module, specifically in
[covid_updater.scraping](src/covid_updater/scraping/). More details to be added [here](docs/CODE.md) soon.

### Bugs
We do our best to ensure that the data is reliable. However, as the project grows and source website change their
format, some bugs might appear. If you detect any, please [report this in the issues section](https://github.com/sociepy/covid19-vaccination-subnational/issues/new).

## Documentation
See [documentation](docs/CODE.md) (WIP 🚧)

## License
See [LICENSE](LICENSE).

> This site or product includes IP2Location™ ISO 3166-2 Subdivision Code which available from
> https://www.ip2location.com.
