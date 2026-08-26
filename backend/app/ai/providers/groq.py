from typing import Any

from groq import AsyncGroq

from app.core.config import settings
from app.ai.providers.base import BaseAIProvider


class GroqProvider(BaseAIProvider):

    def __init__(self):
        self.client = AsyncGroq(
            api_key=settings.GROQ_API_KEY
        )

    async def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:

        response = await self.client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto" if tools else None,
        )

        message = response.choices[0].message

        tool_calls = []

        if message.tool_calls:
            for tool_call in message.tool_calls:

                tool_calls.append({
                    "id": tool_call.id,
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments,
                })

        return {
            "content": message.content,
            "tool_calls": tool_calls,
        }