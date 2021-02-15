# API: Subnational COVID-19 vaccination data

For a given country, you can access [all the tracked data](#all-data) using its [ISO 3166-1 alpha-2 code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2):

```
https://sociepy.org/covid19-vaccination-subnational/data/api/v1/all/country_by_iso/[COUNTRY_ISO].json
```

Alternatively, you can check [latest data](#latest-data):

```
https://sociepy.org/covid19-vaccination-subnational/data/api/v1/latest/country_by_iso/[COUNTRY_ISO].json
```

### Available countries:
[`https://sociepy.org/covid19-vaccination-subnational/data/api/v1/metadata.json`](https://sociepy.org/covid19-vaccination-subnational/data/api/v1/metadata.json)


### Thanks to
[@sanyam-git](https://github.com/sanyam-git) and their project [https://india-covid19vaccine.github.io](https://india-covid19vaccine.github.io), which has inspired this API.

## All data
Get all available data for a country.

### Fields

| field name   | type   | description.                                   |
|--------------|--------|------------------------------------------------|
| `country`      | string | Name of the country.                           |
| `country_iso`  | string | [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) code of the country.                |
| `last_update`  | string | Date of the last data entry, as "YYYY-MM-DD".  |
| `first_update` | string | Date of the first data entry, as "YYYY-MM-DD". |
| `source_url`   | string | Data source URL.                               |
| `data`         | list   | Data per region.                          |
| `data.region_name`  | string | Name of the region.  |
| `data.region_iso`  | string | [ISO 3166-2](https://en.wikipedia.org/wiki/ISO_3166-2) code of the region.  |
| `data.data`         | list   | Region data per date.                          |
| `data.data.date`  | string | Date data entry, as "YYYY-MM-DD".  |
| `data.data.total_vaccinations`  | int | Cummulative number of vaccinations reported on this date and region (first doses + second doses).  |
| `data.data.total_vaccinations_per_100`  | float | Cummulative number of vaccinations reported on this date and region (first doses + second doses) per 100 inhabitants.  |


### Example

Austria: [`https://sociepy.org/covid19-vaccination-subnational/data/api/v1/all/country_by_iso/AT.json`](https://sociepy.org/covid19-vaccination-subnational/data/api/v1/all/country_by_iso/AT.json)

```json
{
    "country": "Austria",
    "country_iso": "AT",
    "last_update": "2021-02-13",
    "first_update": "2021-01-10",
    "source_url": "https://info.gesundheitsministerium.gv.at/",
    "data": [
        {
            "region_iso": "AT-1",
            "region_name": "Burgenland",
            "data": [
                {
                    "date": "2021-01-10",
                    "total_vaccinations": 64,
                    "total_vaccinations_per_100": 0.022
                },
                {
                    "date": "2021-01-12",
                    "total_vaccinations": 127,
                    "total_vaccinations_per_100": 0.043
                },
                ...
            ]
        },
        ...
        {
            "region_iso": "AT-9",
            "region_name": "Wien",
            "data": [
                ...
                {
                    "date": "2021-02-12",
                    "total_vaccinations": 78723,
                    "total_vaccinations_per_100": 4.119
                },
                {
                    "date": "2021-02-13",
                    "total_vaccinations": 83686,
                    "total_vaccinations_per_100": 4.379
                }
            ]
        }
 
```

## Latest data
Get latest data for a country.

### Fields

| field name   | type   | description.                                   |
|--------------|--------|------------------------------------------------|
| `country`      | string | Name of the country.                           |
| `country_iso`  | string | [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) code of the country.                |
| `last_update`  | string | Date of the last data entry, as "YYYY-MM-DD".  |
| `source_url`   | string | Data source URL.                               |
| `data`         | list   | Data per region.                          |
| `data.region_name`  | string | Name of the region.  |
| `data.region_iso`  | string | [ISO 3166-2](https://en.wikipedia.org/wiki/ISO_3166-2) code of the region.  |
| `data.date`  | string | Date data entry, as "YYYY-MM-DD". Note that some regions may have different update frequencies.  |
| `data.total_vaccinations`  | int | Last cummulative number of vaccinations reported in this region (first doses + second doses).  |
| `data.total_vaccinations_per_100`  | float | Cummulative number of vaccinations reported on this date and region (first doses + second doses) per 100 inhabitants.  |

### Example

Brazil: [`https://sociepy.org/covid19-vaccination-subnational/data/api/v1/latest/country_by_iso/BR.json`](https://sociepy.org/covid19-vaccination-subnational/data/api/v1/latest/country_by_iso/BR.json)


```json
{
    "country": "Brazil",
    "country_iso": "BR",
    "last_update": "2021-02-12",
    "source_url": "https://github.com/wcota/covid19br/",
    "data": [
        {
            "region_name": "Acre",
            "region_iso": "BR-AC",
            "date": "2021-02-12",
            "total_vaccinations": 12310,
            "total_vaccinations_per_100": 1.396
        },
        ...
        {
            "region_name": "Tocantins",
            "region_iso": "BR-TO",
            "date": "2021-02-12",
            "total_vaccinations": 24198,
            "total_vaccinations_per_100": 1.561
        }
    ]
}
```