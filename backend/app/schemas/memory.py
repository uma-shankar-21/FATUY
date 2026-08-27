import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MemoryCreate(BaseModel):
    user_id: uuid.UUID
    key: str
    value: str


class MemoryUpdate(BaseModel):
    key: str | None = None
    value: str | None = None


class MemoryResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    key: str
    value: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )