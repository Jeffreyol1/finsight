"""A deterministic mock provider.

It performs no network calls and needs no API key, so the whole system runs
end-to-end out of the box (and tests stay fast and free). It deliberately
echoes the retrieved context with inline [n] markers, which proves the grounding
wiring works before we plug in a real model in a later phase.
"""
from __future__ import annotations

from app.core.schemas import Chunk
from app.llm.base import LLMProvider


class MockProvider(LLMProvider):
    name = "mock"

    async def generate(self, question: str, context: list[Chunk]) -> str:
        if not context:
            return "I don't have enough information in the provided sources to answer that."

        top = context[0]
        cited = " ".join(f"[{i + 1}]" for i in range(len(context)))
        return (
            f"(mock answer) Based on the retrieved sources {cited}, the most "
            f"relevant passage from {top.source} states: \"{top.text[:160]}...\" "
            f"A real model will synthesize a grounded answer here once configured."
        )
