"""HTTP routes. Thin by design — all logic lives in the pipeline."""
from __future__ import annotations

from fastapi import APIRouter, Request

from app.core.schemas import Answer, QueryRequest

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@router.post("/query", response_model=Answer)
async def query(req: QueryRequest, request: Request) -> Answer:
    pipeline = request.app.state.pipeline
    return await pipeline.answer(req.question, top_k=req.top_k)
