from fastapi import FastAPI
from dotenv import load_dotenv
from es.es_service import execute_batting_query

app = FastAPI()
load_dotenv()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/query")
async def query_batting():
    return execute_batting_query(query={
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {"term":{"Player": "Virat Kohli"}}
      ]
    }
  },
  "aggs": {
    "yearwise_runs_scored": {
      "terms": {
        "field": "Year"
      },
      "aggs": {
        "total_runs": {
          "sum": {
            "field": "Runs"
          }
        }
      }
    }
  }
})
