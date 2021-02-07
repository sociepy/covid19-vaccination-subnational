> Work in progress
**Note: All scripts should be run from the project's root directory.**

To run an update on the data, simply [update_all.sh](update_all.sh) script (for more info check the script file).

```bash
$ bash scripts/update_all.sh
```

| Script name          | Description |
|----------------------|-------------|
| `create_iso_db.py` | Create/Update ISO file. Note that this should not be required, as de database is kept updated. |
| `update_population.py` | Update population file, contianing regional population. |
| `update_countries.py` | Update country data. This runs scraping. Check script to choose a subset of countries. |
| `merge_countries.py` | Merge all country data into single file. |
| `update_vaccinations_with_population.py` | Add population-related parameters to vaccination data. |
| `update_api_v1.py ` | Update API files (JSONs). |
| `update_docs.py` | Update documentation, such as [README.md](../README.md)|
