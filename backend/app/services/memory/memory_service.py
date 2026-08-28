from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.memory import UserMemory

from app.services.memory.embedding_service import (
    embedding_service,
)


class MemoryService:

    async def create_memory(
        self,
        db: AsyncSession,
        user_id: UUID,
        content: str,
        memory_type: str,
        importance: int = 1,
    ) -> UserMemory:

        # ==========================================
        # 1. GENERATE EMBEDDING
        # ==========================================

        embedding = (
            await embedding_service.generate_embedding(
                text=content,
            )
        )

        # ==========================================
        # 2. CREATE MEMORY
        # ==========================================

        memory = UserMemory(
            user_id=user_id,
            content=content,
            memory_type=memory_type,
            importance=importance,
            embedding=embedding,
        )

        db.add(memory)

        # ==========================================
        # 3. SAVE TO POSTGRES
        # ==========================================

        await db.commit()

        await db.refresh(memory)

        return memory

    async def search_relevant_memories(
        self,
        db: AsyncSession,
        user_id: UUID,
        query: str,
        limit: int = 5,
    ) -> list[UserMemory]:

        # ==========================================
        # 1. GENERATE QUERY EMBEDDING
        # ==========================================

        query_embedding = (
            await embedding_service.generate_embedding(
                text=query,
            )
        )

        # ==========================================
        # 2. SEMANTIC VECTOR SEARCH
        # ==========================================

        result = await db.execute(
            select(
                UserMemory
            )
            .where(
                UserMemory.user_id == user_id
            )
            .where(
                UserMemory.embedding.is_not(None)
            )
            .order_by(
                UserMemory.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(limit)
        )

        memories = result.scalars().all()

        return memories

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

        # ==========================================
        # UPDATE CONTENT + EMBEDDING
        # ==========================================

        if content is not None:

            memory.content = content

            memory.embedding = (
                await embedding_service.generate_embedding(
                    text=content,
                )
            )

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
        query: str,
        limit: int = 5,
    ) -> list[dict]:

        relevant_memories = await self.search_relevant_memories(
            db=db,
            user_id=user_id,
            query=query,
            limit=limit,
        )

        return [
            {
                "content": memory.content,
                "memory_type": memory.memory_type,
                "importance": memory.importance,
            }
            for memory in relevant_memories
        ]


memory_service = MemoryService()