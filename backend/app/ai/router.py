from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.ai.providers import get_provider

from app.schemas.ai import (
    AIChatRequest,
    AIChatResponse,
)

from app.services.conversation.conversation_service import (
    conversation_service,
)

from app.services.conversation.message_service import (
    message_service,
)

from app.services.conversation.context_service import (
    context_service,
)

from app.services.banking.banking_context_builder import (
    banking_context_builder,
)

from app.services.ai.prompt_service import (
    prompt_service,
)

from app.services.memory.memory_service import (
    memory_service,
)


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/chat",
    response_model=AIChatResponse,
)
async def chat(
    request: AIChatRequest,
    db: AsyncSession = Depends(get_db),
):

    # ==========================================================
    # 1. CREATE OR USE EXISTING CONVERSATION
    # ==========================================================

    if request.conversation_id is None:

        conversation = (
            await conversation_service.create_conversation(
                db=db,
                user_id=request.user_id,
            )
        )

        conversation_id = conversation.id

    else:

        conversation_id = request.conversation_id


    # ==========================================================
    # 2. STORE CURRENT USER MESSAGE
    # ==========================================================

    await message_service.create_message(
        db=db,
        conversation_id=conversation_id,
        role="user",
        content=request.message,
    )


    # ==========================================================
    # 3. LOAD SHORT-TERM MEMORY
    #
    # Last 20 messages from the current conversation
    # ==========================================================

    conversation_messages = (
        await context_service.get_context(
            db=db,
            conversation_id=conversation_id,
            limit=20,
        )
    )


    # ==========================================================
    # 4. LOAD LONG-TERM MEMORY
    #
    # User memories stored in memories table
    # ==========================================================

    long_term_memories = (
        await memory_service.get_memory_context(
            db=db,
            user_id=request.user_id,
            limit=20,
        )
    )


    # ==========================================================
    # 5. BUILD BANKING CONTEXT
    # ==========================================================

    banking_context = (
        await banking_context_builder.build_context(
            db=db,
            user_id=request.user_id,
            message=request.message,
        )
    )


    # ==========================================================
    # 6. BUILD FINAL MESSAGES / MEGA PROMPT
    #
    # Contains:
    #
    # - System instructions
    # - Long-term memory
    # - Banking context
    # - Short-term conversation memory
    # ==========================================================

    messages = prompt_service.build_messages(
        conversation_messages=conversation_messages,
        long_term_memories=long_term_memories,
        banking_context=banking_context,
    )


    # ==========================================================
    # DEBUG: PRINT EXACT DATA SENT TO AI
    # ==========================================================

    print("\n")
    print("=" * 80)
    print("FINAL MESSAGES SENT TO AI")
    print("=" * 80)

    for index, message in enumerate(messages):

        print(f"\nMESSAGE {index + 1}")
        print(f"ROLE: {message['role']}")
        print("-" * 80)
        print(message["content"])

    print("\n")
    print("=" * 80)
    print("END FINAL MESSAGES")
    print("=" * 80)
    print("\n")


    # ==========================================================
    # 7. GET AI PROVIDER
    # ==========================================================

    provider = get_provider(
        request.provider
    )


    # ==========================================================
    # 8. SEND REQUEST TO AI
    # ==========================================================

    result = await provider.chat(
        messages=messages,
    )


    assistant_response = result["content"]


    # ==========================================================
    # 9. STORE AI RESPONSE
    # ==========================================================

    await message_service.create_message(
        db=db,
        conversation_id=conversation_id,
        role="assistant",
        content=assistant_response,
    )


    # ==========================================================
    # 10. RETURN RESPONSE
    # ==========================================================

    return AIChatResponse(
        conversation_id=conversation_id,
        response=assistant_response,
    )