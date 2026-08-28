from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.expired_conversation.expired_conversation_service import (
    expired_conversation_service,
)

from app.services.memory.memory_extractor import (
    memory_extractor,
)

from app.services.memory.memory_service import (
    memory_service,
)


class MemoryProcessor:

    async def process(
        self,
        db: AsyncSession,
        expired_conversation_id: str,
    ) -> None:

        conversation = (
            await expired_conversation_service.get_by_id(
                db=db,
                expired_conversation_id=UUID(
                    expired_conversation_id
                ),
            )
        )

        if conversation is None:

            return

        if conversation.status == "PROCESSED":

            return

        try:

            extracted_memories = (
                await memory_extractor.extract(
                    messages=conversation.messages,
                )
            )

            for memory in extracted_memories:

                await memory_service.create_memory(
                    db=db,
                    user_id=conversation.user_id,
                    content=memory["content"],
                    memory_type=memory.get(
                        "memory_type",
                        "general",
                    ),
                    importance=memory.get(
                        "importance",
                        1,
                    ),
                )

            await expired_conversation_service.mark_processed(
                db=db,
                conversation=conversation,
            )

        except Exception as error:

            await expired_conversation_service.mark_failed(
                db=db,
                conversation=conversation,
                error=str(error),
            )

            raise


memory_processor = MemoryProcessor()