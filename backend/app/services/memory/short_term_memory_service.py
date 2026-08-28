import json
import uuid

from app.core.config import settings
from app.core.redis import redis_client


class ShortTermMemoryService:

    def _get_session_key(
        self,
        session_id: uuid.UUID,
    ) -> str:

        return f"short_term_memory:{session_id}"


    async def create_session(
        self,
        session_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> None:

        key = self._get_session_key(session_id)

        session_data = {
            "session_id": str(session_id),
            "user_id": str(user_id),
            "messages": [],
        }

        await redis_client.set(
            key,
            json.dumps(session_data),
            ex=settings.SHORT_TERM_MEMORY_TTL,
        )


    async def get_session(
        self,
        session_id: uuid.UUID,
    ) -> dict | None:

        key = self._get_session_key(session_id)

        data = await redis_client.get(key)

        if data is None:
            return None

        return json.loads(data)


    async def add_message(
        self,
        session_id: uuid.UUID,
        role: str,
        content: str,
    ) -> None:

        key = self._get_session_key(session_id)

        data = await redis_client.get(key)

        if data is None:
            raise ValueError("Session expired or does not exist")

        session_data = json.loads(data)

        session_data["messages"].append(
            {
                "role": role,
                "content": content,
            }
        )

        await redis_client.set(
            key,
            json.dumps(session_data),
            ex=settings.SHORT_TERM_MEMORY_TTL,
        )


    async def get_messages(
        self,
        session_id: uuid.UUID,
    ) -> list[dict]:

        session = await self.get_session(
            session_id=session_id,
        )

        if session is None:
            raise ValueError("Session expired or does not exist")

        return session["messages"]


    async def refresh_session(
        self,
        session_id: uuid.UUID,
    ) -> bool:

        key = self._get_session_key(session_id)

        result = await redis_client.expire(
            key,
            settings.SHORT_TERM_MEMORY_TTL,
        )

        return bool(result)


    async def delete_session(
        self,
        session_id: uuid.UUID,
    ) -> None:

        key = self._get_session_key(session_id)

        await redis_client.delete(key)


short_term_memory_service = ShortTermMemoryService()