from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.memory import UserMemory


class MemoryService:

    async def create_memory(
        self,
        db: AsyncSession,
        user_id: UUID,
        content: str,
        memory_type: str,
        conversation_id: UUID | None = None,
        importance: int = 1,
    ) -> UserMemory:

        memory = UserMemory(
            user_id=user_id,
            conversation_id=conversation_id,
            content=content,
            memory_type=memory_type,
            importance=importance,
        )

        db.add(memory)

        await db.commit()

        await db.refresh(memory)

        return memory

    async def get_memories(
        self,
        db: AsyncSession,
        user_id: UUID,
        limit: int = 20,
    ) -> list[UserMemory]:

        result = await db.execute(
            select(UserMemory)
            .where(
                UserMemory.user_id == user_id
            )
            .order_by(
                UserMemory.importance.desc(),
                UserMemory.created_at.desc(),
            )
            .limit(limit)
        )

        return result.scalars().all()


    async def update_memory(
        self,
        db: AsyncSession,
        memory_id: UUID,
        user_id: UUID,
        content: str | None = None,
        importance: int | None = None,
    ) -> UserMemory | None:

        result = await db.execute(
            select(UserMemory)
            .where(
                UserMemory.id == memory_id,
                UserMemory.user_id == user_id,
            )
        )

        memory = result.scalar_one_or_none()

        if memory is None:
            return None

        if content is not None:
            memory.content = content

        if importance is not None:
            memory.importance = importance

        await db.commit()

        await db.refresh(memory)

        return memory


    async def delete_memory(
        self,
        db: AsyncSession,
        memory_id: UUID,
        user_id: UUID,
    ) -> bool:

        result = await db.execute(
            select(UserMemory)
            .where(
                UserMemory.id == memory_id,
                UserMemory.user_id == user_id,
            )
        )

        memory = result.scalar_one_or_none()

        if memory is None:
            return False

        await db.delete(memory)

        await db.commit()

        return True

    async def get_memory_context(
        self,
        db: AsyncSession,
        user_id: UUID,
        limit: int = 20,
    ) -> list[dict]:

        memories = await self.get_memories(
            db=db,
            user_id=user_id,
            limit=limit,
        )

        return [
            {
                "content": memory.content,
                "memory_type": memory.memory_type,
                "importance": memory.importance,
            }
            for memory in memories
        ]

memory_service = MemoryService()