"""Phase 0 tests: prove the end-to-end path works and grounding behaves.

These are ordinary unit/integration tests. The dedicated *evaluation* harness
(retrieval recall, answer faithfulness, citation accuracy) arrives in Phase 3 —
that's the crown-jewel piece. These tests keep the wiring honest until then.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    # Entering the context manager runs the lifespan handler, which wires up
    # app.state.pipeline. Without `with`, startup never fires.
    with TestClient(app) as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_query_returns_grounded_answer_with_citations(client):
    r = client.post("/query", json={"question": "What was ACME revenue in 2024?"})
    assert r.status_code == 200
    body = r.json()
    assert body["grounded"] is True
    assert len(body["citations"]) >= 1
    assert any("10-K" in c["source"] for c in body["citations"])


def test_query_refuses_when_unrelated(client):
    # Both phrasings are unrelated to the finance corpus and must refuse.
    # The second one previously leaked through on the stopword "the" — this
    # asserts the stopword-filtering fix holds.
    for q in ("favorite pizza topping?", "what is the best pizza topping?"):
        r = client.post("/query", json={"question": q})
        assert r.status_code == 200
        assert r.json()["grounded"] is False, f"should refuse: {q!r}"


def test_short_question_is_rejected_by_validation(client):
    r = client.post("/query", json={"question": "hi"})
    assert r.status_code == 422  # fails min_length=3