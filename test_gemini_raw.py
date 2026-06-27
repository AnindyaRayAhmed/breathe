import asyncio
import json
import httpx
from backend.core.config import get_settings
from backend.services.ai.gemini_client import GeminiClient

async def test():
    client = GeminiClient()
    # Mocking prompt for testing endpoint behavior
    if not client.settings.ai_api_key:
        print("NO API KEY, ABORTING SCRIPT")
        return

    payload = {
        "model": client.settings.ai_model,
        "input": "test prompt",
        "response_format": {
            "type": "text",
            "mime_type": "application/json",
            "schema": {}
        }
    }
    headers = {
        "x-goog-api-key": client.settings.ai_api_key,
        "Content-Type": "application/json",
    }
    
    print("Calling API...")
    async with httpx.AsyncClient() as c:
        resp = await c.post(client.settings.gemini_api_base_url, headers=headers, json=payload)
        print("Status Code:", resp.status_code)
        try:
            print("Response JSON:", json.dumps(resp.json(), indent=2))
        except Exception as e:
            print("Raw text:", resp.text)

if __name__ == "__main__":
    asyncio.run(test())
