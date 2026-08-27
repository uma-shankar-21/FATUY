from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message


class ContextService:

    async def get_context(
        self,
        db: AsyncSession,
        conversation_id,
        limit: int = 20,
    ) -> list[dict]:

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

        messages = reversed(messages)

        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]


context_service = ContextService()