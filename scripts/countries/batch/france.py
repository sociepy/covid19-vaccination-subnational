import re
import io
import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils import merge_iso


replace = {
    "Auvergne-Rhône-Alpes": "Auvergne-Rhone-Alpes",
    "Bourgogne-Franche-Comté": "Bourgogne-Franche-Comte",
    "Grand Est": "Grand-Est",
    "La Réunion": "La Reunion" ,
    "Pays de la Loire": "Pays-de-la-Loire",
    "Provence-Alpes-Côte d'Azur": "Provence-Alpes-Cote-d'Azur",
    "Île-de-France": "Ile-de-France"
}


def read_psv(str_input: str, **kwargs) -> pd.DataFrame:
    """Read a Pandas object from a pipe-separated table contained within a string.

    Ref: https://stackoverflow.com/a/46471952/
    """

    substitutions = [
        ('^ *', ''),  # Remove leading spaces
        (' *$', ''),  # Remove trailing spaces
        (r' *\| *', '|'),  # Remove spaces between columns
    ]
    if all(line.lstrip().startswith('|') and line.rstrip().endswith('|') for line in str_input.strip().split('\n')):
        substitutions.extend([
            (r'^\|', ''),  # Remove redundant leading delimiter
            (r'\|$', ''),  # Remove redundant trailing delimiter
        ])
    for pattern, replacement in substitutions:
        str_input = re.sub(pattern, replacement, str_input, flags=re.MULTILINE)
    return pd.read_csv(io.StringIO(str_input), **kwargs)


def main():
    # Request & downloa data
    url = "https://www.data.gouv.fr/fr/datasets/r/eb672d49-7cc7-4114-a5a1-fa6fd147406b"
    page_content = requests.get(url, headers={'User-Agent': 'Custom'}).content
    soup = BeautifulSoup(page_content, "html.parser")
    # Build DataFrame
    df = read_psv(str(soup), sep=",")
    df = df.rename(columns={
        "nom": "region",
        "total_vaccines": "total_vaccinations"
    })
    df.loc[:, "region"] = df.loc[:, "region"].replace(replace)
    df.loc[:, "location"] = "France"
    # Add ISO codes
    df = merge_iso(df, country_iso="FR")
    # Reorder columns
    df = df[["location", "region", "date", "location_iso", "region_iso", "total_vaccinations"]]
    df = df.sort_values(by=["region", "date"])
    df.to_csv("data/countries/France.csv", index=False)


if __name__ == "__main__":
    main()