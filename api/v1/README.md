# API

For a given country, you can access [all the tracked data](#all-data) using its ISO code:

```
https://sociepy.org/covid19-vaccination-subnational/api/v1/all/country_by_iso/[COUNTRY_ISO].json
```

Alternatively, you can check [latest data](#latest-data):

```
https://sociepy.org/covid19-vaccination-subnational/api/v1/latest/country_by_iso/[COUNTRY_ISO].json
```

To see which countries are available you can check [this table](https://sociepy.org/covid19-vaccination-subnational/#data-sources) or directly via the API:

[`https://sociepy.org/covid19-vaccination-subnational/api/v1/metadata.json`](https://sociepy.org/covid19-vaccination-subnational/api/v1/metadata.json)


This API is inspired by [https://india-covid19vaccine.github.io](https://india-covid19vaccine.github.io)

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
| `data.data.total_vaccinations`  | string | Cummulative number of vaccinations reported on this date and region (first doses + second doses).  |

### Example
> [sociepy.org/covid19-vaccination-subnational/api/v1/all/country_by_iso/AT.json](https://sociepy.org/covid19-vaccination-subnational/api/v1/all/country_by_iso/AT.json)

```json
{
    "country": "Austria",
    "country_iso": "AT",
    "last_update": "2021-02-04",
    "first_update": "2021-01-10",
    "source_url": "https://info.gesundheitsministerium.gv.at/",
    "data": [
        {
            "region_iso": "AT-1",
            "region_name": "Burgenland",
            "data": [
                {
                    "date": "2021-01-10",
                    "total_vaccinations": 64
                },
                {
                    "date": "2021-01-12",
                    "total_vaccinations": 127
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
                    "date": "2021-02-03",
                    "total_vaccinations": 50897
                },
                {
                    "date": "2021-02-04",
                    "total_vaccinations": 52556
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
| `data.total_vaccinations`  | string | Last cummulative number of vaccinations reported in this region (first doses + second doses).  |


```json
{
    "country": "Brazil",
    "country_iso": "BR",
    "last_update": "2021-02-03",
    "source_url": "https://github.com/wcota/covid19br/",
    "data": [
        {
            "region_name": "Acre",
            "region_iso": "BR-AC",
            "date": "2021-02-03",
            "total_vaccinations": 7229
        },
        ...
        {
            "region_name": "Tocantins",
            "region_iso": "BR-TO",
            "date": "2021-02-03",
            "total_vaccinations": 10683
        }
    ]
}
```