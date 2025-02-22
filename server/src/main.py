import os
import sys
from fastapi import FastAPI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from dotenv import load_dotenv

load_dotenv()

from src.service.es_service import execute_batting_query

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/query")
async def query_batting():
    return execute_batting_query(
        query={
            "size": 0,
            "query": {"bool": {"filter": [{"term": {"Player": "Virat Kohli"}}]}},
            "aggs": {
                "yearwise_runs_scored": {
                    "terms": {"field": "Year"},
                    "aggs": {"total_runs": {"sum": {"field": "Runs"}}},
                }
            },
        }
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("API_PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
