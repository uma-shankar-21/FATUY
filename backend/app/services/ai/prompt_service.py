from app.services.banking.banking_context_builder import (
    banking_context_builder,
)


class PromptService:

    def build_messages(
        self,
        conversation_messages: list[dict],
        long_term_memories: list[dict],
        banking_context: dict,
    ) -> list[dict]:

        formatted_banking_context = (
            banking_context_builder.format_context(
                banking_context
            )
        )


        # Format long-term memories
        if long_term_memories:

            formatted_memories = "\n".join(
                [
                    (
                        f"- {memory['content']} "
                        f"(type: {memory['memory_type']}, "
                        f"importance: {memory['importance']})"
                    )
                    for memory in long_term_memories
                ]
            )

        else:

            formatted_memories = (
                "No long-term memories are available "
                "for this user."
            )


        system_message = {
            "role": "system",
            "content": f"""
You are a helpful Banking AI Assistant.

You assist users with banking-related questions.

You may receive banking data and long-term memory about
the current user.

IMPORTANT RULES:

1. Use only the banking data provided below.
2. Do not invent account balances, transactions, loans, or payments.
3. If the requested banking information is not available,
   clearly say so.
4. Do not expose information belonging to other users.
5. Answer naturally and clearly.
6. If the user asks a general question unrelated to banking,
   answer normally.
7. Banking data may be empty when it is not relevant to the
   user's request.
8. Long-term memory belongs only to the current user.
9. Use long-term memory only when it is relevant to the
   user's current request.
10. Do not invent facts that are not present in the provided
    long-term memory.

LONG-TERM USER MEMORY:

{formatted_memories}

CURRENT USER BANKING CONTEXT:

{formatted_banking_context}
""".strip(),
        }


        messages = [
            system_message,
            *conversation_messages,
        ]

        return messages


prompt_service = PromptService()