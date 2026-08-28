import logging
from uuid import UUID

import redis.asyncio as redis

from app.core.config import settings
from app.core.database import AsyncSessionLocal

from app.services.memory.redis_session_service import (
    redis_session_service,
)


logger = logging.getLogger(__name__)


class SessionExpirationWorker:

    EXPIRY_PREFIX = "conversation-expiry:"


    def __init__(self):

        self.redis = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )


    async def run(self) -> None:

        logger.info(
            "Session expiration worker started"
        )

        pubsub = self.redis.pubsub()

        channel = (
            f"__keyevent@"
            f"{settings.REDIS_DB}"
            f"__:expired"
        )

        await pubsub.subscribe(
            channel
        )

        logger.info(
            "Listening for Redis expiration events | "
            "channel=%s",
            channel,
        )

        try:

            async for message in pubsub.listen():

                if message["type"] != "message":
                    continue


                expired_key = message["data"]


                logger.info(
                    "Redis key expired | key=%s",
                    expired_key,
                )


                # ==========================================
                # ONLY HANDLE SESSION EXPIRATION KEYS
                # ==========================================

                if not expired_key.startswith(
                    self.EXPIRY_PREFIX
                ):

                    continue


                session_id_string = (
                    expired_key.replace(
                        self.EXPIRY_PREFIX,
                        "",
                    )
                )


                logger.info(
                    "Session expiration detected | "
                    "session_id=%s",
                    session_id_string,
                )


                try:

                    session_id = UUID(
                        session_id_string
                    )

                    await self.process_session(
                        session_id=session_id,
                    )

                except Exception:

                    logger.exception(
                        "Failed processing expired session | "
                        "session_id=%s",
                        session_id_string,
                    )

        finally:

            logger.info(
                "Stopping session expiration worker"
            )

            await pubsub.unsubscribe(
                channel
            )

            await pubsub.close()

            await self.redis.close()


    async def process_session(
        self,
        session_id: UUID,
    ) -> None:

        logger.info(
            "Processing expired session | "
            "session_id=%s",
            session_id,
        )


        # ==========================================
        # GET ACTUAL SESSION DATA
        #
        # chat_session:{session_id}
        # ==========================================

        session_data = (
            await redis_session_service.get_session(
                session_id=session_id,
            )
        )


        if session_data is None:

            logger.warning(
                "Session data not found | "
                "session_id=%s",
                session_id,
            )

            return


        user_id = UUID(
            session_data["user_id"]
        )

        messages = session_data.get(
            "messages",
            [],
        )


        logger.info(
            "Session data found | "
            "session_id=%s | "
            "message_count=%s",
            session_id,
            len(messages),
        )


        # ==========================================
        # SAVE TO POSTGRES + CREATE OUTBOX EVENT
        # ==========================================

        async with AsyncSessionLocal() as db:

            expired_conversation = (
                await redis_session_service.handle_expired_session(
                    db=db,
                    session_id=session_id,
                    user_id=user_id,
                    messages=messages,
                )
            )


        logger.info(
            "Expired conversation saved | id=%s",
            expired_conversation.id,
        )


        # ==========================================
        # REMOVE ACTUAL REDIS SESSION
        #
        # Expiry key is already gone automatically.
        # ==========================================

        await redis_session_service.remove_session(
            session_id=session_id,
        )


        logger.info(
            "Expired session fully processed | "
            "session_id=%s",
            session_id,
        )


session_expiration_worker = (
    SessionExpirationWorker()
)