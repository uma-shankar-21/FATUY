class MemorySummaryService:

    def build_messages(
        self,
        conversation_messages: list[dict],
    ) -> list[dict]:

        conversation_text = "\n".join(
            (
                f"{message['role']}: "
                f"{message['content']}"
            )
            for message in conversation_messages
        )

        return [
            {
                "role": "system",
                "content": """
You extract useful long-term memory
from user conversations.

Create a concise summary containing only
information that may be useful in future
conversations.

Do not include temporary questions,
casual greetings, or unnecessary details.

Do not invent information.

Return only the memory summary.
""".strip(),
            },
            {
                "role": "user",
                "content": (
                    "Conversation:\n\n"
                    f"{conversation_text}"
                ),
            },
        ]


memory_summary_service = (
    MemorySummaryService()
)