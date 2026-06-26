"""The LLM provider abstraction.

Every concrete model (Claude, OpenAI, a local model, or the mock) implements
this one interface. The rest of the app depends only on `LLMProvider`, never on
a specific vendor SDK. This is what lets us do model routing and swap providers
later without touching the pipeline — and it reads as real engineering judgment
in an interview.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from app.core.schemas import Chunk


class LLMProvider(ABC):
    """Abstract base for any text-generation backend."""

    name: str = "base"

    @abstractmethod
    async def generate(self, question: str, context: list[Chunk]) -> str:
        """Produce an answer to `question` grounded in `context` passages."""
        raise NotImplementedError


def build_grounded_prompt(question: str, context: list[Chunk]) -> str:
    """Assemble the prompt shared by all real providers.

    The instructions here are the heart of grounding: answer only from the
    provided context, and say so when the context is insufficient.
    """
    numbered = "\n\n".join(
        f"[{i + 1}] (source: {c.source})\n{c.text}" for i, c in enumerate(context)
    )
    return (
        "You are a financial research assistant. Answer the question using ONLY "
        "the numbered context passages below. Cite passages inline like [1], [2]. "
        "If the context does not contain the answer, say you don't have enough "
        "information rather than guessing.\n\n"
        f"Context:\n{numbered}\n\n"
        f"Question: {question}\n\nAnswer:"
    )
