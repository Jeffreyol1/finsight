"""Factory that turns a config string into a concrete provider.

Phase 0 only ships the mock. The commented branches show exactly where Claude /
OpenAI implementations slot in — each just subclasses LLMProvider and reuses
`build_grounded_prompt`, so adding one later touches nothing else.
"""
from __future__ import annotations

from app.config import settings
from app.llm.base import LLMProvider
from app.llm.mock import MockProvider


def get_provider(name: str | None = None) -> LLMProvider:
    name = (name or settings.llm_provider).lower()

    if name == "mock":
        return MockProvider()

    # Phase 4: real providers behind the same interface.
    # if name == "anthropic":
    #     from app.llm.anthropic_provider import AnthropicProvider
    #     return AnthropicProvider(api_key=settings.anthropic_api_key)
    # if name == "openai":
    #     from app.llm.openai_provider import OpenAIProvider
    #     return OpenAIProvider(api_key=settings.openai_api_key)

    raise ValueError(f"Unknown LLM provider: {name!r}")
