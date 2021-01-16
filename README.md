# covid19-vaccination-subnational 
> This is a work in progress 🚧

This project aims to gather COVID-19 vaccination data at subnational level for as many countries as possible. The data
can be found in [data/vaccinations.csv](data/vaccinations.csv).

This project is inspired by [owid/covid-19-data](https://github.com/owid/covid-19-data) and is open to integration if
deemed approriate.

It works by running scripts on a daily basis, which gather data from different [sources](#sources).


### Sources
- Canada: https://github.com/ccodwg/Covid19Canada/
- Germany: https://github.com/mathiasbynens/covid-19-vaccinations-germany/
- Italy: https://github.com/italia/covid19-opendata-vaccini/
- Spain: https://github.com/civio/covid-vaccination-spain/
- USA: https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=vaccination_data

### How to update data
Make sure to install all dependencies, `pip install -r requirements.txt`.

Run

```
$ python scripts/update_data.py
```

File [data/vaccinations.csv](data/vaccinations.csv) is updated.