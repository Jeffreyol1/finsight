"""FastAPI application entrypoint.

Dependencies are wired once at startup (in the lifespan handler) and stored on
app.state, so routes stay thin and everything is easy to swap in tests.
"""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import settings
from app.llm import get_provider
from app.pipeline import RAGPipeline
from app.retrieval.retriever import StubRetriever


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Compose the object graph once. Later phases swap StubRetriever for the
    # pgvector-backed retriever here — nothing else changes.
    app.state.pipeline = RAGPipeline(
        retriever=StubRetriever(),
        provider=get_provider(),
    )
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten before deploying
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root() -> dict:
    return {"app": settings.app_name, "docs": "/docs", "version": "0.1.0"}
