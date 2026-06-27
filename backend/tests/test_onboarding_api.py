from __future__ import annotations

from fastapi.testclient import TestClient

from backend.main import app


def test_onboarding_endpoint_returns_memory_snapshot() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/onboarding",
        json={
            "active_exams": [
                {"name": "JEE", "priority": "high", "exam_date": "2026-01-15"},
                {"name": "BITSAT", "priority": "medium", "exam_date": "2026-05-20"},
            ],
            "primary_stressor_exam": "JEE",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["memory"]["primary_stressor_exam"] == "JEE"
    assert body["memory"]["active_exams"][0]["name"] == "JEE"
