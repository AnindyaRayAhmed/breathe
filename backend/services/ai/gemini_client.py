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
        output_text = ""

        # 1. Check for custom 'output_text'
        if "output_text" in data and data["output_text"]:
            output_text = str(data["output_text"])

        # 2. Check for standard Gemini structure (candidates[0].content.parts[0].text)
        if not output_text:
            try:
                candidates = data.get("candidates", [])
                if candidates:
                    content = candidates[0].get("content", {})
                    parts = content.get("parts", [])
                    if parts:
                        text_val = parts[0].get("text", "")
                        if text_val:
                            output_text = str(text_val)
            except (IndexError, AttributeError, KeyError):
                pass

        # 3. Check for candidates[0].text
        if not output_text:
            try:
                candidates = data.get("candidates", [])
                if candidates and "text" in candidates[0] and candidates[0]["text"]:
                    output_text = str(candidates[0]["text"])
            except (IndexError, AttributeError, KeyError):
                pass

        # 4. Check for top-level 'text'
        if not output_text and "text" in data and data["text"]:
            output_text = str(data["text"])

        if output_text:
            # Clean up potential markdown code fences (e.g. ```json ... ```)
            cleaned = output_text.strip()
            if cleaned.startswith("```"):
                lines = cleaned.splitlines()
                if len(lines) > 1 and lines[0].startswith("```"):
                    lines = lines[1:]
                if len(lines) > 0 and lines[-1].strip() == "```":
                    lines = lines[:-1]
                cleaned = "\n".join(lines).strip()
            return cleaned

        raise GeminiClientError(f"Gemini response did not include output_text or candidate text. Response keys: {list(data.keys())}")
