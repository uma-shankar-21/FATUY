from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from app.models.expired_conversation import (
    ExpiredConversation,
)


class ExpiredConversationService:

    async def create(
        self,
        db: AsyncSession,
        session_id: UUID,
        user_id: UUID,
        messages: list[dict],
    ) -> ExpiredConversation:

        expired_conversation = ExpiredConversation(
            session_id=session_id,
            user_id=user_id,
            messages=messages,
            status="PENDING",
        )

        db.add(
            expired_conversation
        )

        await db.flush()

        return expired_conversation

    async def get_by_id(
        self,
        db: AsyncSession,
        expired_conversation_id: UUID,
    ) -> ExpiredConversation | None:

        result = await db.execute(
            select(ExpiredConversation)
            .where(
                ExpiredConversation.id
                == expired_conversation_id
            )
        )

        return result.scalar_one_or_none()


    async def mark_processed(
        self,
        db: AsyncSession,
        conversation: ExpiredConversation,
    ) -> None:

        conversation.status = "PROCESSED"

        conversation.processed_at = func.now()

        await db.commit()

    async def mark_failed(
        self,
        db: AsyncSession,
        conversation: ExpiredConversation,
        error: str,
    ) -> None:

        conversation.retry_count += 1

        conversation.last_error = error

        conversation.status = "PENDING"

        await db.commit()

expired_conversation_service = (
    ExpiredConversationService()
)