from datetime import date
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


# ==========================================================
# CUSTOMER CREATE
# ==========================================================

class CustomerCreate(BaseModel):

    username: str = Field(
        min_length=1,
        max_length=150,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
    )

    first_name: str = Field(
        min_length=1,
        max_length=100,
    )

    last_name: str = Field(
        min_length=1,
        max_length=100,
    )

    phone: str = Field(
        min_length=1,
        max_length=20,
    )

    date_of_birth: date | None = None


# ==========================================================
# CUSTOMER RESPONSE
# ==========================================================

class CustomerResponse(BaseModel):

    id: UUID

    username: str

    email: EmailStr

    first_name: str

    last_name: str

    phone: str

    date_of_birth: date | None

    is_active: bool

    model_config = {
        "from_attributes": True,
    }


# ==========================================================
# LOGIN REQUEST
# ==========================================================

class CustomerLogin(BaseModel):

    identifier: str = Field(
        min_length=1,
    )

    password: str = Field(
        min_length=1,
    )

class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    customer: CustomerResponse