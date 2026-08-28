import json
import uuid

from app.core.config import settings
from app.core.redis import redis_client


class SessionExpiredError(Exception):
    pass


class SessionService:

    SESSION_PREFIX = "chat_session:"
    EXPIRY_PREFIX = "conversation-expiry:"


    def _session_key(
        self,
        session_id: uuid.UUID,
    ) -> str:

        return (
            f"{self.SESSION_PREFIX}{session_id}"
        )


    def _expiry_key(
        self,
        session_id: uuid.UUID,
    ) -> str:

        return (
            f"{self.EXPIRY_PREFIX}{session_id}"
        )


    async def create_session(
        self,
        user_id: uuid.UUID,
    ) -> uuid.UUID:

        session_id = uuid.uuid4()

        session_key = self._session_key(
            session_id
        )

        expiry_key = self._expiry_key(
            session_id
        )

        session_data = {
            "session_id": str(session_id),
            "user_id": str(user_id),
            "messages": [],
        }


        # ==========================================
        # SAVE SESSION DATA
        # NO TTL HERE
        # ==========================================

        await redis_client.set(
            session_key,
            json.dumps(session_data),
        )


        # ==========================================
        # EXPIRATION TRIGGER
        # ==========================================

        await redis_client.set(
            expiry_key,
            "1",
            ex=settings.SESSION_TTL_SECONDS,
        )


        return session_id


    async def get_session(
        self,
        session_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> dict:

        session_key = self._session_key(
            session_id
        )

        data = await redis_client.get(
            session_key
        )

        if data is None:

            raise SessionExpiredError(
                "Session expired. Please create a new session."
            )

        session_data = json.loads(
            data
        )

        if session_data["user_id"] != str(user_id):

            raise SessionExpiredError(
                "Session does not belong to this user."
            )

        return session_data


    async def add_message(
        self,
        session_id: uuid.UUID,
        user_id: uuid.UUID,
        role: str,
        content: str,
    ) -> dict:

        session_data = await self.get_session(
            session_id=session_id,
            user_id=user_id,
        )


        # ==========================================
        # ADD MESSAGE
        # ==========================================

        session_data["messages"].append(
            {
                "role": role,
                "content": content,
            }
        )


        session_key = self._session_key(
            session_id
        )

        expiry_key = self._expiry_key(
            session_id
        )


        # ==========================================
        # UPDATE SESSION DATA
        # ==========================================

        await redis_client.set(
            session_key,
            json.dumps(session_data),
        )


        # ==========================================
        # RESET TTL
        # Every new message extends session lifetime
        # ==========================================

        await redis_client.set(
            expiry_key,
            "1",
            ex=settings.SESSION_TTL_SECONDS,
        )


        return session_data


    async def get_messages(
        self,
        session_id: uuid.UUID,
        user_id: uuid.UUID,
        limit: int = 20,
    ) -> list[dict]:

        session_data = await self.get_session(
            session_id=session_id,
            user_id=user_id,
        )

        messages = session_data.get(
            "messages",
            [],
        )

        return messages[-limit:]


    async def session_exists(
        self,
        session_id: uuid.UUID,
    ) -> bool:

        session_key = self._session_key(
            session_id
        )

        return bool(
            await redis_client.exists(
                session_key
            )
        )


    async def get_ttl(
        self,
        session_id: uuid.UUID,
    ) -> int:

        expiry_key = self._expiry_key(
            session_id
        )

        return await redis_client.ttl(
            expiry_key
        )


session_service = SessionService()