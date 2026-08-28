from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import (
    get_current_customer,
)

from app.core.database import get_db

from app.models.auth_user import AuthUser
from app.models.customer import Customer

from app.schemas.auth import (
    CustomerData,
    LoginRequest,
    LoginResponse,
)

from app.services.auth.auth_service import (
    auth_service,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ==========================================================
# LOGIN
# ==========================================================

@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(
        get_db
    ),
):

    result = await auth_service.login(
        db=db,
        identifier=data.identifier.strip(),
        password=data.password,
    )

    if result is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    customer = result["customer"]

    auth_user = result["auth_user"]

    return {
        "message": "Login successful.",

        "customer": {
            "id": customer.id,
            "username": auth_user.username,
            "email": auth_user.email,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "phone": customer.phone,
            "is_active": customer.is_active,
        },

        "access": result["access"],

        "refresh": result["refresh"],
    }


# ==========================================================
# CURRENT LOGGED-IN USER
# ==========================================================

@router.get(
    "/me",
    response_model=CustomerData,
)
async def get_me(
    customer: Customer = Depends(
        get_current_customer
    ),
    db: AsyncSession = Depends(
        get_db
    ),
):

    result = await db.execute(
        select(AuthUser).where(
            AuthUser.id == customer.user_id
        )
    )

    auth_user = result.scalar_one_or_none()

    if auth_user is None:

        raise HTTPException(
            status_code=404,
            detail="Authentication user not found.",
        )

    return {
        "id": customer.id,
        "username": auth_user.username,
        "email": auth_user.email,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "phone": customer.phone,
        "is_active": customer.is_active,
    }