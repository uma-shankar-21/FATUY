from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import (
    get_current_customer,
)

from app.core.database import get_db

from app.models.auth_user import AuthUser
from app.models.existing.bank_account import BankAccount
from app.models.customer import Customer


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("")
async def get_dashboard(
    customer: Customer = Depends(
        get_current_customer
    ),
    db: AsyncSession = Depends(
        get_db
    ),
):

    # ==========================================================
    # GET AUTH USER
    # ==========================================================

    result = await db.execute(
        select(AuthUser).where(
            AuthUser.id == customer.user_id
        )
    )

    auth_user = result.scalar_one_or_none()

    # ==========================================================
    # GET BANK ACCOUNTS
    # ==========================================================

    result = await db.execute(
        select(BankAccount)
        .where(
            BankAccount.customer_id
            == customer.id
        )
        .order_by(
            BankAccount.created_at
        )
    )

    accounts = result.scalars().all()

    # ==========================================================
    # RETURN DASHBOARD
    # ==========================================================

    return {
        "customer": {
            "id": str(customer.id),

            "username": (
                auth_user.username
                if auth_user
                else None
            ),

            "email": (
                auth_user.email
                if auth_user
                else None
            ),

            "first_name": customer.first_name,

            "last_name": customer.last_name,

            "phone": customer.phone,

            "date_of_birth": (
                customer.date_of_birth
            ),
        },

        "accounts": [
            {
                "id": str(account.id),

                "account_number": (
                    account.account_number
                ),

                "account_type": (
                    account.account_type
                ),

                "currency": (
                    account.currency
                ),

                "balance": float(
                    account.balance
                ),

                "status": (
                    account.status
                ),
            }

            for account in accounts
        ],
    }