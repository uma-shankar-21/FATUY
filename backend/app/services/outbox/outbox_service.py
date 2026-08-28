from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.outbox import OutboxMessage


class OutboxService:

    async def create_event(
        self,
        db: AsyncSession,
        topic: str,
        payload: dict,
    ) -> OutboxMessage:

        event = OutboxMessage(
            topic=topic,
            payload=payload,
            status="PENDING",
        )

        db.add(event)

        await db.commit()

        await db.refresh(event)

        return event


    async def get_pending_events(
        self,
        db: AsyncSession,
        limit: int = 50,
    ) -> list[OutboxMessage]:

        result = await db.execute(
            select(OutboxMessage)
            .where(
                OutboxMessage.status == "PENDING"
            )
            .order_by(
                OutboxMessage.created_at.asc()
            )
            .limit(limit)
        )

        return result.scalars().all()


    async def mark_processed(
        self,
        db: AsyncSession,
        event: OutboxMessage,
    ) -> None:

        event.status = "PROCESSED"

        await db.commit()


    async def mark_failed(
        self,
        db: AsyncSession,
        event: OutboxMessage,
        error: str,
    ) -> None:

        event.retry_count += 1
        event.last_error = error

        await db.commit()


outbox_service = OutboxService()