import json

from app.ai.providers import get_provider


class MemoryExtractor:

    async def extract(
        self,
        messages: list[dict],
    ) -> list[dict]:

        provider = get_provider(
            "ollama"
        )

        prompt = f"""
You are a memory extraction system.

Analyze the conversation below.

Extract ONLY information that is useful for future conversations.

Do NOT store:

- temporary questions
- assistant responses
- current account balances
- individual transaction details
- temporary calculations
- information that belongs to another user

Extract only stable or useful information such as:

- user preferences
- financial goals
- recurring interests
- banking preferences
- important user instructions
- long-term financial context

Return ONLY valid JSON.

Format:

[
    {{
        "content": "memory text",
        "memory_type": "preference",
        "importance": 1
    }}
]

Conversation:

{json.dumps(messages, indent=2)}
""".strip()

        result = await provider.chat(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You extract useful long-term "
                        "user memories."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ]
        )

        content = result["content"]

        try:

            return json.loads(content)

        except json.JSONDecodeError:

            return []


memory_extractor = MemoryExtractor()