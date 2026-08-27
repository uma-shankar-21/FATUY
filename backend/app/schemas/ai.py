import uuid

from pydantic import BaseModel


class AIChatRequest(BaseModel):

    user_id: uuid.UUID

    message: str

    conversation_id: uuid.UUID | None = None

    provider: str = "ollama"


class AIChatResponse(BaseModel):

    conversation_id: uuid.UUID

    response: str