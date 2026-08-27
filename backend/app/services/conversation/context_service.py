import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message


SHORT_TERM_MEMORY_LIMIT = 20


class ContextService:

    async def get_context(
        self,
        db: AsyncSession,
        conversation_id: uuid.UUID,
        limit: int = SHORT_TERM_MEMORY_LIMIT,
    ) -> list[dict[str, str]]:

        result = await db.execute(
            select(Message)
            .where(
                Message.conversation_id == conversation_id
            )
            .order_by(
                Message.created_at.desc()
            )
            .limit(limit)
        )

        messages = result.scalars().all()

        messages.reverse()

        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]


context_service = ContextService()