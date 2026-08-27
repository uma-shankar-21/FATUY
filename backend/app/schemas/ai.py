from uuid import UUID

from pydantic import BaseModel


class AIChatRequest(BaseModel):

    user_id: UUID

    message: str

    session_id: UUID | None = None

    provider: str | None = None


class AIChatResponse(BaseModel):

    session_id: UUID

    response: str