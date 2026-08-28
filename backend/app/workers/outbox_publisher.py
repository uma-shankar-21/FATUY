import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal

from app.services.kafka.kafka_producer import (
    kafka_producer,
)

from app.services.outbox.outbox_service import (
    outbox_service,
)


logger = logging.getLogger(__name__)


class OutboxPublisher:

    async def publish_pending_events(
        self,
        db: AsyncSession,
    ) -> None:

        logger.info(
            "Checking database for pending outbox events"
        )

        events = (
            await outbox_service.get_pending_events(
                db=db,
                limit=50,
            )
        )

        logger.info(
            "Pending outbox events found | count=%s",
            len(events),
        )

        for event in events:

            try:

                logger.info(
                    "Publishing outbox event | "
                    "id=%s | topic=%s | payload=%s",
                    event.id,
                    event.topic,
                    event.payload,
                )

                await kafka_producer.send(
                    topic=event.topic,
                    message=event.payload,
                )

                logger.info(
                    "Kafka publish successful | event_id=%s",
                    event.id,
                )

                await outbox_service.mark_processed(
                    db=db,
                    event=event,
                )

                logger.info(
                    "Outbox event marked PROCESSED | event_id=%s",
                    event.id,
                )

            except Exception:

                logger.exception(
                    "Failed to publish outbox event | event_id=%s",
                    event.id,
                )

                await outbox_service.mark_failed(
                    db=db,
                    event=event,
                    error="Kafka publish failed",
                )


    async def run(self) -> None:

        logger.info(
            "Outbox publisher started"
        )

        while True:

            try:

                async with AsyncSessionLocal() as db:

                    await self.publish_pending_events(
                        db=db,
                    )

            except Exception:

                logger.exception(
                    "Outbox publisher failed"
                )

            await asyncio.sleep(5)


outbox_publisher = OutboxPublisher()