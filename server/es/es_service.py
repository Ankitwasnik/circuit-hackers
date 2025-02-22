from elasticsearch import Elasticsearch
import os

client = Elasticsearch(
  os.getenv('ES_SERVER_URL'),
  api_key=os.getenv('ES_API_KEY')
)

BATTING_INDEX = os.getenv('ES_BATTING_INDEX_NAME')

def get_client_info():
    return client.info()

def execute_query(index, query):
    return client.search(index=index, body=query)

def execute_batting_query(query):
    return execute_query(BATTING_INDEX, query)