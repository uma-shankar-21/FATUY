import json
import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import redis_client

from app.services.expired_conversation.expired_conversation_service import (
    expired_conversation_service,
)

from app.services.outbox.outbox_service import (
    outbox_service,
)

from app.core.kafka import (
    CONVERSATION_EXPIRED_TOPIC,
)


logger = logging.getLogger(__name__)


class RedisSessionService:

    SESSION_PREFIX = "chat_session:"


    def _session_key(
        self,
        session_id: UUID,
    ) -> str:

        return (
            f"{self.SESSION_PREFIX}{session_id}"
        )


    async def get_session(
        self,
        session_id: UUID,
    ) -> dict | None:

        session_key = self._session_key(
            session_id
        )

        logger.info(
            "Getting Redis session | key=%s",
            session_key,
        )

        session_data = await redis_client.get(
            session_key
        )

        if session_data is None:

            logger.warning(
                "Redis session not found | "
                "session_id=%s",
                session_id,
            )

            return None


        return json.loads(
            session_data
        )


    async def remove_session(
        self,
        session_id: UUID,
    ) -> None:

        session_key = self._session_key(
            session_id
        )

        await redis_client.delete(
            session_key
        )

        logger.info(
            "Redis session deleted | "
            "session_id=%s",
            session_id,
        )


    async def handle_expired_session(
        self,
        db: AsyncSession,
        session_id: UUID,
        user_id: UUID,
        messages: list[dict],
    ):

        logger.info(
            "Creating expired conversation | "
            "session_id=%s | user_id=%s",
            session_id,
            user_id,
        )


        # ==========================================
        # SAVE EXPIRED CONVERSATION
        # ==========================================

        expired_conversation = (
            await expired_conversation_service.create(
                db=db,
                session_id=session_id,
                user_id=user_id,
                messages=messages,
            )
        )


        logger.info(
            "Expired conversation created | id=%s",
            expired_conversation.id,
        )


        # ==========================================
        # CREATE OUTBOX EVENT
        # ==========================================

        event = await outbox_service.create_event(
            db=db,
            topic=CONVERSATION_EXPIRED_TOPIC,
            payload={
                "expired_conversation_id": str(
                    expired_conversation.id
                )
            },
        )


        logger.info(
            "Outbox event created | "
            "event_id=%s | topic=%s",
            event.id,
            event.topic,
        )


        return expired_conversation


redis_session_service = RedisSessionService()