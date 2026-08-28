from uuid import UUID

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_token

from app.models.customer import Customer


security = HTTPBearer()


async def get_current_customer(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: AsyncSession = Depends(
        get_db
    ),
) -> Customer:

    token = credentials.credentials

    try:

        payload = decode_token(
            token
        )

        user_id = payload.get(
            "user_id"
        )

        token_type = payload.get(
            "type"
        )

        if (
            user_id is None
            or token_type != "access"
        ):

            raise ValueError()

        customer_id = UUID(
            user_id
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
        )

    # ==========================================================
    # GET CUSTOMER
    # ==========================================================

    result = await db.execute(
        select(Customer).where(
            Customer.id == customer_id
        )
    )

    customer = result.scalar_one_or_none()

    if customer is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    if not customer.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive.",
        )

    return customer