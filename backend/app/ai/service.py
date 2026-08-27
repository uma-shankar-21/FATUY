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

    # 1. Create or use conversation
    if request.conversation_id is None:

        conversation = await conversation_service.create_conversation(
            db=db,
            user_id=request.user_id,
        )

        conversation_id = conversation.id

    else:

        conversation_id = request.conversation_id


    # 2. Store user message
    await message_service.create_message(
        db=db,
        conversation_id=conversation_id,
        role="user",
        content=request.message,
    )


    # 3. Load conversation context
    messages = await context_service.get_context(
        db=db,
        conversation_id=conversation_id,
    )


    # 4. Get AI provider
    provider = get_provider(
        request.provider
    )


    # 5. Ask AI
    result = await provider.chat(
        messages=messages,
    )


    assistant_response = result["content"]


    # 6. Store assistant response
    await message_service.create_message(
        db=db,
        conversation_id=conversation_id,
        role="assistant",
        content=assistant_response,
    )


    # 7. Return response
    return AIChatResponse(
        conversation_id=conversation_id,
        response=assistant_response,
    )