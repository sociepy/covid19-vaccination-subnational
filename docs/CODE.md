# Use the code

## Installation
We recommend installing the software in a virtual environment.

```
pip install -e .
```

Note that some dependencies require additional steps:

- [`tabula-py`](https://github.com/chezou/tabula-py): Ensure you have a Java runtime and that it is visible to environment variable `PATH`.
- [`selenium`](https://github.com/SeleniumHQ/selenium): Download [chromedriver binary](https://chromedriver.chromium.org/downloads) and place it so that it is visible to environment variable `PATH`.

## ISO codes
> This site or product includes IP2Location™ ISO 3166-2 Subdivision Code which available from
> https://www.ip2location.com.

The logic to interact with ISO information lies is found in object [`ISODB`](../src/covid_updater/iso.py#L15).

### Generate ISO code db
To correctly add ISO 3166-2 subnational information, we may require to add additional entries to our existing
 [source table](../src/covid_updater/assets/IP2LOCATION-ISO3166-2.CSV).

Our current logic to create the ISO database can be found in script [`create_iso_db`](../scripts/create_iso_db.py).

If you need to add new entries to the ISO database, modify the aforementioned file and run it.

```
$ python scripts/create_iso_db.py
```

### Load available ISO codes
To check the currently available ISO information use the following code.

```python
>>> from covid_updater.iso import load_iso
>>> df = load_iso()
>>> df.head()
  location_iso     subdivision_name region_iso
0           AD              Canillo      AD-02
1           AD               Encamp      AD-03
2           AD           La Massana      AD-04
3           AD               Ordino      AD-05
4           AD  Sant Julia de Loria      AD-06
```

## Contribute

If you found new country data available, consider implementing the corresponding scraper. Find instructions and a
tutorial in notebook [add-new-scraper.ipynb](add-new-scraper.ipynb).
