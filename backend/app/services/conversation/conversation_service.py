import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation


class ConversationService:

    async def create_conversation(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        title: str | None = None,
    ) -> Conversation:

        conversation = Conversation(
            user_id=user_id,
            title=title,
        )

        db.add(conversation)

        await db.commit()

        await db.refresh(conversation)

        return conversation


conversation_service = ConversationService()