from datetime import datetime
from math import ceil
import qwikidata
import qwikidata.sparql
import pandas as pd


def build_query(region_iso_list: list):
    query = """
    SELECT ?item ?value ?population
    WHERE
    {
    ?item p:P1082 [pq:P585 ?date; ps:P1082 ?population].
    ?item wdt:P300 ?value.
    FILTER NOT EXISTS {?item p:P1082 [pq:P585 ?date_] FILTER (?date_ > ?date)}
    FILTER(?value IN %s)
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
    }
    """ % str(tuple(region_iso_list))
    return query


def get_population(region_iso_list: list):
    """Get population from given regions.

    Regions identified by `region_iso`.
    
    Args:
        region_iso_list (list): Iterable with iso codes.

    Returns:
        pandas.DataFrame: Retrieved data. Two columns: region_iso, population
    """
    chunk_size = 450
    num_iter = ceil(len(region_iso_list)/chunk_size)
    dfs = []
    for i in range(num_iter):
        query = build_query(region_iso_list[i*chunk_size:(i+1)*chunk_size])
        res = qwikidata.sparql.return_sparql_query_results(query)
        res = [(item["value"]["value"], int(item["population"]["value"])) for item in res["results"]["bindings"]]
        df_ = pd.DataFrame(res, columns=["region_iso", "population"])
        df_.loc[:, "date"] = datetime.now().date().strftime("%Y-%m-%d")
        dfs.append(df_)
    df = pd.concat(dfs)
    df = df.drop_duplicates()
    df = df.groupby(["region_iso", "date"]).max().reset_index()
    return df
