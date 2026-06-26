"""The RAG pipeline: retrieve -> ground-check -> generate -> assemble answer.

This orchestrator is the spine of the system. Note the grounding gate: if the
best retrieved passage is too weak, we refuse to answer instead of letting the
model invent a number. In a finance product, a confident wrong answer is worse
than "I don't know" — so refusal is a feature, not a limitation.
"""
from __future__ import annotations

from app.config import settings
from app.core.schemas import Answer, Citation, Chunk
from app.llm.base import LLMProvider
from app.retrieval.retriever import StubRetriever


class RAGPipeline:
    def __init__(self, retriever: StubRetriever, provider: LLMProvider) -> None:
        self._retriever = retriever
        self._provider = provider

    async def answer(self, question: str, top_k: int = 5) -> Answer:
        chunks: list[Chunk] = self._retriever.retrieve(question, top_k=top_k)
        best_score = chunks[0].score if chunks else 0.0
        grounded = best_score >= settings.min_grounding_score

        if not grounded:
            return Answer(
                answer=(
                    "I don't have enough relevant information in the indexed "
                    "documents to answer that confidently."
                ),
                citations=[],
                grounded=False,
                metadata={"best_score": best_score, "provider": self._provider.name},
            )

        text = await self._provider.generate(question, chunks)
        citations = [
            Citation(source=c.source, snippet=c.text[:200], score=c.score)
            for c in chunks
        ]
        return Answer(
            answer=text,
            citations=citations,
            grounded=True,
            metadata={
                "best_score": best_score,
                "retrieved": len(chunks),
                "provider": self._provider.name,
            },
        )
