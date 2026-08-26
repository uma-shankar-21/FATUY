from typing import Any

import httpx

from app.core.config import settings
from app.ai.providers.base import BaseAIProvider


class VLLMProvider(BaseAIProvider):

    async def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:

        payload = {
            "model": settings.VLLM_MODEL,
            "messages": messages,
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        async with httpx.AsyncClient(timeout=60.0) as client:

            response = await client.post(
                f"{settings.VLLM_BASE_URL}/chat/completions",
                json=payload,
            )

            response.raise_for_status()

            result = response.json()

        message = result["choices"][0]["message"]

        tool_calls = []

        for tool_call in message.get("tool_calls", []):

            tool_calls.append({
                "id": tool_call["id"],
                "name": tool_call["function"]["name"],
                "arguments": tool_call["function"]["arguments"],
            })

        return {
            "content": message.get("content"),
            "tool_calls": tool_calls,
        }