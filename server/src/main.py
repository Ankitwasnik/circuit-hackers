import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(project_root)

from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from src.service.process_query import get_results

app = FastAPI()

# Get CORS origins from environment variables
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return {"message": "Hello World"}


class QueryRequestData(BaseModel):
    question: str


@app.post("/query")
async def query_batting(request_data: QueryRequestData):
    return get_results(request_data.question)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("API_PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
