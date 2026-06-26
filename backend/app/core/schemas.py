"""Core data contracts shared across the pipeline.

Defining these up front (before any real logic) is deliberate: every component
— retriever, LLM provider, API — speaks in these types, so we can swap
implementations later without rewriting callers.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class Chunk(BaseModel):
    """A retrieved passage from a source document."""

    source: str = Field(..., description="Document identifier, e.g. 'AAPL 10-K 2024'")
    text: str = Field(..., description="The passage text itself")
    score: float = Field(0.0, description="Retrieval relevance score (higher = better)")


class Citation(BaseModel):
    """A pointer from the answer back to the source passage that supports it."""

    source: str
    snippet: str
    score: float


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, description="Natural-language question")
    top_k: int = Field(5, ge=1, le=20, description="How many passages to retrieve")


class Answer(BaseModel):
    """The full result returned to the client."""

    answer: str
    citations: list[Citation]
    grounded: bool = Field(
        ...,
        description="True if the answer is backed by retrieved sources. When "
        "retrieval is too weak, we refuse rather than hallucinate.",
    )
    metadata: dict = Field(default_factory=dict)
