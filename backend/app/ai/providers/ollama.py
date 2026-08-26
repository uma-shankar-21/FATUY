from typing import Any

import httpx

from app.core.config import settings
from app.ai.providers.base import BaseAIProvider


class OllamaProvider(BaseAIProvider):

    async def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:

        payload = {
            "model": settings.OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
        }

        if tools:
            payload["tools"] = tools

        async with httpx.AsyncClient(timeout=60.0) as client:

            response = await client.post(
                f"{settings.OLLAMA_BASE_URL}/api/chat",
                json=payload,
            )

            response.raise_for_status()

            result = response.json()

        message = result.get("message", {})

        tool_calls = []

        for tool_call in message.get("tool_calls", []):

            function = tool_call.get("function", {})

            tool_calls.append({
                "id": tool_call.get("id"),
                "name": function.get("name"),
                "arguments": function.get("arguments"),
            })

        return {
            "content": message.get("content"),
            "tool_calls": tool_calls,
        }