import os
from elasticsearch import Elasticsearch
from langchain_core.tools import tool

from src.utils.es_index import ESIndex

client = Elasticsearch(os.getenv("ES_SERVER_URL"), api_key=os.getenv("ES_API_KEY"))


def get_client_info():
    return client.info()


@tool
def execute_query(index_key, query):
    """
    Execute a search query on a specified Elasticsearch index.

    Args:
        index_key (str): The key used to determine the Elasticsearch index.
                         Must be one of ["BATTING", "BOWLING"].
        query (dict): The search query in Elasticsearch DSL format.

    Returns:
        dict: The search results from Elasticsearch.
    """
    index_name = ESIndex.get_index(index_key)
    return client.search(index=index_name, body=query)


def execute_batting_query(query):
    return execute_query(ESIndex.BATTING, query)
