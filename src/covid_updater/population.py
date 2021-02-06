from datetime import datetime
import qwikidata
import qwikidata.sparql
import pandas as pd


def get_population(region_iso_list: list):
    """Get population from given regions.

    Regions identified by `region_iso`.
    
    Args:
        region_iso_list (list): Iterable with iso codes.

    Returns:
        pandas.DataFrame: Retrieved data. Two columns: region_iso, population
    """
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
    res = qwikidata.sparql.return_sparql_query_results(query)
    res = [(item["value"]["value"], int(item["population"]["value"])) for item in res["results"]["bindings"]]
    df = pd.DataFrame(res, columns=["region_iso", "population"])
    df.loc[:, "date"] = datetime.now().date().strftime("%Y-%m-%d")
    return df
