# FinSight — Grounded AI for Financial Documents

A retrieval-augmented research assistant that answers natural-language questions
about financial filings (10-K / 10-Q, earnings calls) **grounded in the source,
with inline citations** — and refuses to answer when the evidence is weak.

> **Why this project exists:** anyone can wrap an LLM API. The engineering that
> matters is *proving* the system is correct, fast, and cheap — and handling the
> ways AI fails. In finance, a confidently wrong number is a disaster, so
> rigorous retrieval, grounding, and **evaluation** aren't extras here; they're
> the whole point.

## Status

**Phase 0 — Foundation (complete).** Runnable end-to-end path (`question -> retrieve
-> ground-check -> generate -> cited answer`), a provider-agnostic LLM layer with
a zero-dependency mock, Docker skeleton, and tests. Runs with **no API key**.

See [`ARCHITECTURE.md`](./ARCHITECTURE.md) for the design and the full phase plan.

## Quickstart (no Docker, no API key)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open <http://localhost:8000/docs> (interactive API) and try:

```bash
curl -s localhost:8000/query \
  -H 'content-type: application/json' \
  -d '{"question":"What was ACME revenue growth in 2024?"}' | python -m json.tool
```

You'll get an answer with `citations` and a `grounded` flag. Ask something
unrelated and watch it refuse instead of guessing — that's the anti-hallucination
gate working.

## Quickstart (Docker)

```bash
cp .env.example .env
docker compose up --build
```

Brings up Postgres + pgvector (for Phase 1) and the API on port 8000.

## Run the tests

```bash
cd backend && pytest -q
```

## Project structure

```
finsight/
├── docker-compose.yml         # db (pgvector) + backend
├── ARCHITECTURE.md            # design, data flow, decisions, roadmap
└── backend/
    ├── Dockerfile
    ├── requirements.txt
    └── app/
        ├── main.py            # FastAPI app + lifespan wiring
        ├── config.py          # settings (pydantic-settings)
        ├── pipeline.py        # retrieve -> ground-check -> generate
        ├── api/routes.py      # /health, /query
        ├── core/schemas.py    # shared data contracts
        ├── llm/               # provider interface + mock + factory
        └── retrieval/         # stub retriever (pgvector comes in Phase 1)
```

## Roadmap

| Phase | Focus | Headline deliverable |
|------|-------|----------------------|
| 0 ✅ | Foundation | Runnable cited-answer path + mock provider |
| 1 | Working MVP | Document ingestion + chunking + pgvector semantic search + UI |
| 2 | Make it good | Hybrid (vector + BM25) retrieval + cross-encoder re-ranking |
| 3 | **Prove it works** | **Evaluation harness (faithfulness, citation accuracy) in CI** |
| 4 | Fast & cheap | Semantic caching, streaming, model routing, observability |
| 5 | Ship it | Deploy to GCP Cloud Run, polish, writeup |

Phase 3 is the crown jewel — automated quality measurement wired into CI is what
separates this from a demo.
