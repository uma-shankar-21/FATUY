import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message


class MessageService:

    async def create_message(
        self,
        db: AsyncSession,
        conversation_id: uuid.UUID,
        role: str,
        content: str,
    ) -> Message:

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        db.add(message)

        await db.commit()

        await db.refresh(message)

        return message


message_service = MessageService()