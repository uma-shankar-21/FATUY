from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.schemas.customer import (
    CustomerCreate,
    CustomerLogin,
    CustomerResponse,
    LoginResponse,
)

from app.services.customer.customer_service import (
    customer_service,
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


# ==========================================================
# CREATE CUSTOMER
# ==========================================================

@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer(
    data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
):

    try:

        customer = (
            await customer_service.create_customer(
                db=db,
                data=data,
            )
        )

        return customer

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


# ==========================================================
# GET CUSTOMER
# ==========================================================

@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
async def get_customer(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
):

    customer = (
        await customer_service.get_customer(
            db=db,
            customer_id=customer_id,
        )
    )

    if customer is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Customer not found",
                "customer_id": str(customer_id),
            },
        )

    return customer


# ==========================================================
# LOGIN CUSTOMER
# ==========================================================

@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login_customer(
    data: CustomerLogin,
    db: AsyncSession = Depends(get_db),
):

    result = (
        await customer_service.login_customer(
            db=db,
            identifier=data.identifier.strip(),
            password=data.password,
        )
    )

    if result is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    return {
        "message": "Login successful.",
        "customer": result["customer"],
        "access": result["access"],
        "refresh": result["refresh"],
    }