from __future__ import annotations

import json
import logging
import time
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from backend.core.config import get_settings
from backend.services.ai.gemini_client import GeminiClient, GeminiClientError

logger = logging.getLogger(__name__)
router = APIRouter(tags=["debug"])


class GeminiTestResponse(BaseModel):
    success: bool
    model_used: str
    parsed_response: Any | None = None
    error_message: str | None = None
    latency_seconds: float


@router.get("/debug/gemini-test", response_model=GeminiTestResponse)
async def test_gemini() -> GeminiTestResponse:
    settings = get_settings()
    client = GeminiClient(settings)

    test_schema = {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
            }
        },
        "required": ["message"],
    }

    prompt = "Reply in JSON format with a JSON object containing the key 'message' set to 'Hello from Breathe Gemini Integration Audit'."

    start_time = time.perf_counter()
    success = False
    parsed_response = None
    error_message = None

    try:
        raw_output = await client.generate_structured_output(
            prompt=prompt,
            schema=test_schema,
        )
        parsed_response = json.loads(raw_output)
        success = True
    except GeminiClientError as exc:
        error_message = f"Gemini client error: {exc}"
        logger.exception("Debug Gemini test call failed with GeminiClientError")
    except Exception as exc:
        error_message = f"Unexpected error: {exc}"
        logger.exception("Debug Gemini test call failed with unexpected error")

    latency = time.perf_counter() - start_time

    return GeminiTestResponse(
        success=success,
        model_used=settings.ai_model,
        parsed_response=parsed_response,
        error_message=error_message,
        latency_seconds=round(latency, 4),
    )
