from __future__ import annotations

from fastapi.testclient import TestClient

from backend.main import app


def test_gemini_test_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/api/debug/gemini-test")

    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "model_used" in data
    assert "latency_seconds" in data
    assert "error_message" in data
    assert "parsed_response" in data
