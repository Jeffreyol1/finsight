"""Retrieval layer.

Phase 0 ships a stub with a few hand-written passages so the end-to-end path
runs today. Phase 1 replaces `StubRetriever` with a real implementation backed
by Postgres + pgvector (semantic search), and Phase 2 adds keyword (BM25) search
plus a cross-encoder re-ranker — all behind this same `.retrieve()` signature.
"""
from __future__ import annotations

from app.core.schemas import Chunk

# A tiny in-memory corpus standing in for indexed filings.
_CANNED_CORPUS: list[Chunk] = [
    Chunk(
        source="ACME 10-K 2024",
        text=(
            "Total revenue for fiscal 2024 was $4.2 billion, an increase of 11% "
            "year over year, driven primarily by growth in the cloud services "
            "segment."
        ),
    ),
    Chunk(
        source="ACME 10-K 2024",
        text=(
            "Operating margin expanded to 18.5% from 16.2% in the prior year as "
            "the company realized efficiencies from its data-center consolidation."
        ),
    ),
    Chunk(
        source="ACME Q4 2024 Earnings Call",
        text=(
            "Management guided to full-year 2025 revenue growth in the range of "
            "9% to 12%, citing continued enterprise demand and a strong pipeline."
        ),
    ),
]


# Common words that carry no topical meaning. Without filtering these, a
# question like "what is the best pizza topping?" matches finance passages
# purely on the word "the" — exactly the false-grounding bug this prevents.
# (Real semantic retrieval in Phase 1 sidesteps this whole class of problem.)
_STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "of", "in", "on", "for", "to", "and", "or", "with", "as", "at", "by",
    "from", "that", "this", "these", "those", "it", "its", "what", "which",
    "who", "how", "did", "do", "does", "you", "your", "best", "most", "much",
}


def _significant_terms(text: str) -> set[str]:
    """Lowercase, strip punctuation, drop short words and stopwords."""
    cleaned = (w.lower().strip(".,%$?!()'\"") for w in text.split())
    return {w for w in cleaned if len(w) > 2 and w not in _STOPWORDS}


class StubRetriever:
    """Naive keyword-overlap retriever — a placeholder, not the real thing."""

    def __init__(self, corpus: list[Chunk] | None = None) -> None:
        self._corpus = corpus if corpus is not None else _CANNED_CORPUS

    def retrieve(self, query: str, top_k: int = 5) -> list[Chunk]:
        terms = _significant_terms(query)
        scored: list[Chunk] = []
        for chunk in self._corpus:
            words = _significant_terms(chunk.text)
            overlap = len(terms & words)
            denom = len(terms) or 1
            scored.append(chunk.model_copy(update={"score": overlap / denom}))

        scored.sort(key=lambda c: c.score, reverse=True)
        return scored[:top_k]