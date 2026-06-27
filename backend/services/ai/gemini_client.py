from __future__ import annotations

from typing import Any

import httpx

from backend.core.config import Settings, get_settings


class GeminiClientError(RuntimeError):
    pass


class GeminiClient:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    async def generate_structured_output(self, prompt: str, schema: dict[str, Any]) -> str:
        if not self.settings.gemini_enabled:
            raise GeminiClientError("Gemini is not configured.")

        payload = {
            "model": self.settings.ai_model,
            "input": prompt,
            "response_format": {
                "type": "text",
                "mime_type": "application/json",
                "schema": schema,
            },
        }
        headers = {
            "x-goog-api-key": self.settings.ai_api_key,
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=self.settings.gemini_timeout_seconds) as client:
                response = await client.post(
                    self.settings.gemini_api_base_url,
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise GeminiClientError("Gemini request timed out.") from exc
        except httpx.HTTPError as exc:
            raise GeminiClientError("Gemini request failed.") from exc

        data = response.json()
        output_text = data.get("output_text", "")
        if output_text:
            return output_text

        raise GeminiClientError("Gemini response did not include output_text.")
