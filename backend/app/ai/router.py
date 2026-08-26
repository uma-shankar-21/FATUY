from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.service import ai_service


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


class AIChatRequest(BaseModel):

    user_id: UUID
    message: str


@router.post("/chat")
async def chat_with_ai(
    request: AIChatRequest,
):

    result = await ai_service.chat(
        user_id=str(request.user_id),
        message=request.message,
    )

    return result