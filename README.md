# circuit-hackers — Dashify

Dashify turns a plain-English question about IPL cricket batting stats into a chart.

Type a question like *"Who hit the most sixes in 2021?"* into the UI. The backend
uses an LLM agent to translate the question into an Elasticsearch query ("nl2esq"),
runs it against an Elasticsearch index of IPL batting stats, transforms the result
into chart-ready JSON, and the frontend renders it as a bar, line, pie, or doughnut
chart.

## How it works

1. **Client** (`client/charts-app2`) sends the natural-language question to the
   server via `POST /query`.
2. **nl2esq agent** (`server/src/agent/nl2esq.py`) — a LangChain agent backed by
   OpenAI — writes an Elasticsearch DSL query from the question, using few-shot
   examples (`server/data/few_shot_examples.py`) selected by semantic similarity
   (FAISS + OpenAI embeddings), and executes it against Elasticsearch.
3. **Transformer chain** (`server/src/chain/transform_response.py`) converts the
   raw Elasticsearch response into `{ labels, datasets }` chart data via another
   LLM call.
4. **Client** renders the result with Chart.js.

## Project structure

```
client/
  charts-app2/   # active client — Vite + React + TypeScript + Tailwind CSS
  chart-app/     # earlier prototype (Create React App), kept for reference
server/          # FastAPI backend, LangChain + OpenAI + Elasticsearch
```

## Server setup

See [server/README.md](server/README.md) for details. Quick start:

```bash
cd server
cp .env.sample .env   # fill in OpenAI + Elasticsearch credentials
./scripts/setup.sh    # creates .venv and installs dependencies
./scripts/run.sh      # starts the API on http://localhost:8000
```

Required environment variables (`server/.env.sample`):

| Variable | Purpose |
|---|---|
| `LLM_PROVIDER` | LLM provider to use (currently only `openai`) |
| `OPENAI_CHAT_MODEL_NAME` | OpenAI chat model, e.g. `gpt-4o` |
| `OPENAI_EMBEDDING_MODEL_NAME` | OpenAI embedding model, e.g. `text-embedding-ada-002` |
| `OPENAI_API_KEY` | OpenAI API key |
| `ES_API_KEY` | Elasticsearch API key |
| `ES_SERVER_URL` | Elasticsearch endpoint |
| `ES_BATTING_INDEX_NAME` | Elasticsearch index holding IPL batting stats |
| `API_PORT` | Port the FastAPI server listens on (default `8000`) |
| `CORS_ORIGINS` | Comma-separated allowed origins for the client |

## Client setup

The active client is `client/charts-app2`:

```bash
cd client/charts-app2
cp .env.sample .env   # VITE_SERVER_URL defaults to http://localhost:8000
npm install
npm run dev
```

`client/chart-app` is an earlier Create React App prototype kept for reference;
it is not maintained and its API usage predates the current server contract.

## API

- `GET /` — health check
- `POST /query` — body `{ "question": "<natural language question>" }`,
  returns `{ "labels": [...], "datasets": [...] }` for charting
