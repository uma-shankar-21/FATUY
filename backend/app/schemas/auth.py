from uuid import UUID

from pydantic import BaseModel


# ==========================================================
# LOGIN REQUEST
# ==========================================================

class LoginRequest(BaseModel):

    identifier: str

    password: str


# ==========================================================
# CUSTOMER RESPONSE
# ==========================================================

class CustomerData(BaseModel):

    id: UUID

    username: str

    email: str

    first_name: str

    last_name: str

    phone: str

    is_active: bool


# ==========================================================
# LOGIN RESPONSE
# ==========================================================

class LoginResponse(BaseModel):

    message: str

    customer: CustomerData

    access: str

    refresh: str