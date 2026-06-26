"""Application settings, loaded from environment variables (and .env in dev).

Centralizing config means no scattered os.getenv calls, and it documents every
knob the system has in one place.
"""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Which LLM implementation to use. "mock" runs with zero external
    # dependencies and no API key — perfect for local dev, tests, and CI.
    llm_provider: str = "mock"

    # Real provider keys (unused while llm_provider == "mock").
    anthropic_api_key: str | None = None
    openai_api_key: str | None = None

    # Postgres + pgvector. Wired up in Phase 1; harmless to define now.
    database_url: str = "postgresql://finsight:finsight@db:5432/finsight"

    # If the best retrieved passage scores below this, we refuse to answer
    # instead of guessing. This single threshold is our anti-hallucination guard.
    min_grounding_score: float = 0.15

    app_name: str = "FinSight"


settings = Settings()
