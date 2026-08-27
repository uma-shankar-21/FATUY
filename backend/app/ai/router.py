from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.ai.providers import get_provider

from app.schemas.ai import (
    AIChatRequest,
    AIChatResponse,
)

from app.services.session.session_service import (
    session_service,
    SessionExpiredError,
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
    # 1. CREATE NEW SESSION OR VALIDATE EXISTING SESSION
    # ==========================================================

    if request.session_id is None:

        session_id = await session_service.create_session(
            user_id=request.user_id,
        )

    else:

        session_id = request.session_id

        try:

            await session_service.get_session(
                session_id=session_id,
                user_id=request.user_id,
            )

        except SessionExpiredError as error:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            )


    # ==========================================================
    # 2. STORE USER MESSAGE IN REDIS
    #
    # TTL resets to 30 minutes
    # ==========================================================

    await session_service.add_message(
        session_id=session_id,
        user_id=request.user_id,
        role="user",
        content=request.message,
    )


    # ==========================================================
    # 3. LOAD SHORT-TERM MEMORY FROM REDIS
    # ==========================================================

    short_term_messages = (
        await session_service.get_messages(
            session_id=session_id,
            user_id=request.user_id,
            limit=20,
        )
    )


    # ==========================================================
    # 4. LOAD LONG-TERM MEMORY FROM POSTGRES
    #
    # Later Phase 9 will improve this using vector retrieval.
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
    # 6. BUILD FINAL PROMPT
    # ==========================================================

    messages = prompt_service.build_messages(
        conversation_messages=short_term_messages,
        long_term_memories=long_term_memories,
        banking_context=banking_context,
    )


    # ==========================================================
    # DEBUG
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
    # 8. ASK AI
    # ==========================================================

    result = await provider.chat(
        messages=messages,
    )

    assistant_response = result["content"]


    # ==========================================================
    # 9. STORE ASSISTANT RESPONSE IN REDIS
    #
    # TTL resets again to 30 minutes
    # ==========================================================

    await session_service.add_message(
        session_id=session_id,
        user_id=request.user_id,
        role="assistant",
        content=assistant_response,
    )


    # ==========================================================
    # 10. RETURN RESPONSE
    # ==========================================================

    return AIChatResponse(
        session_id=session_id,
        response=assistant_response,
    )