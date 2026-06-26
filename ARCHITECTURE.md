# Architecture

This document explains how FinSight is put together and *why* — the design
decisions and tradeoffs are the part worth talking about in an interview.

## System overview

FinSight is a classic **RAG (retrieval-augmented generation)** system with the
quality controls a finance domain demands. A question flows through four stages:

```
                ┌──────────────┐
  question ───▶ │  Retriever   │  find the most relevant source passages
                └──────┬───────┘
                       ▼
                ┌──────────────┐
                │ Ground gate  │  is the best passage relevant enough?
                └──────┬───────┘   no ──▶ refuse (don't hallucinate)
                       ▼ yes
                ┌──────────────┐
                │ LLM provider │  generate an answer grounded in the passages
                └──────┬───────┘
                       ▼
                ┌──────────────┐
                │   Assemble   │  attach citations + metadata, return
                └──────────────┘
```

The orchestration lives in `app/pipeline.py`; everything else is a swappable
implementation behind a small interface.

## Components and responsibilities

| Component | File | Responsibility | Swappable to |
|-----------|------|----------------|--------------|
| Schemas | `core/schemas.py` | Shared data contracts (`Chunk`, `Citation`, `Answer`) | — (the stable spine) |
| Retriever | `retrieval/retriever.py` | Find candidate passages for a query | pgvector (P1) → hybrid + re-rank (P2) |
| Ground gate | `pipeline.py` | Refuse when retrieval is too weak | tune threshold / per-source rules |
| LLM provider | `llm/base.py`, `llm/mock.py` | Generate grounded text | Claude / OpenAI / local (P4) |
| Pipeline | `pipeline.py` | Orchestrate the stages | — |
| API | `api/routes.py`, `main.py` | HTTP surface, dependency wiring | — |

## Key design decisions

**1. Interfaces before implementations.** The pipeline depends on an abstract
`LLMProvider` and a retriever with a fixed `.retrieve()` signature, never on a
vendor SDK. That's why we can ship a mock today and slot in Claude later by
touching exactly one factory function. It's also what makes model *routing*
(cheap model for easy questions, strong model for hard ones) a later add rather
than a rewrite.

**2. A mock provider as a first-class citizen.** Running end-to-end with no API
key keeps local dev, tests, and CI fast, free, and deterministic. The mock
echoes retrieved context with `[n]` markers specifically to prove the *grounding
wiring* works before correctness depends on a real model.

**3. Refusal is a feature.** The ground gate (`min_grounding_score`) makes the
system say "I don't have enough information" rather than fabricate. For financial
data, a wrong-but-confident answer is the worst outcome, so we bias toward
silence under uncertainty.

**4. One database for vectors *and* keywords.** Phase 1/2 use Postgres +
pgvector for semantic search and Postgres full-text/BM25 for keyword search —
instead of bolting on a separate hosted vector DB. Fewer moving parts, real SQL
depth, and a more production-realistic story.

**5. Dependencies wired once at startup.** `main.py`'s lifespan handler builds
the object graph and stores it on `app.state`, keeping routes thin and making
everything trivial to substitute in tests.

## Data flow in Phase 1+ (preview)

Ingestion will be its own offline path: `PDF/HTML filing -> parse -> chunk (with
section + page metadata) -> embed -> store in pgvector`. Query-time retrieval
then runs against that index. Keeping ingestion and query separate means we can
re-index or change chunking strategy without touching the serving path.

## Evaluation strategy (Phase 3 — the core idea)

Most AI projects can't answer "is it actually good?" FinSight will ship a
**golden dataset** of question/expected-answer/expected-source triples and an
automated harness scoring:

- **Retrieval recall** — did we retrieve the passage that contains the answer?
- **Faithfulness** — is every claim in the answer supported by retrieved text?
- **Citation accuracy** — do the cited sources actually back the statements?

These run in CI so a prompt tweak or model swap that regresses quality **fails
the build**. This is the single most differentiating piece of the project.

## Tech stack and rationale

- **FastAPI + Pydantic** — async, typed, auto OpenAPI docs; strong AI ecosystem.
- **Postgres + pgvector** — vector + relational + keyword search in one engine.
- **Docker Compose** — reproducible local environment.
- **GCP Cloud Run** (Phase 5) — serverless containers; matches existing GCP experience.
- **GitHub Actions** — CI for tests and the eval harness.
