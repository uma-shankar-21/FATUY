from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)

from app.models.auth_user import AuthUser
from app.models.customer import Customer


class AuthService:

    # ==========================================================
    # LOGIN
    # ==========================================================

    async def login(
        self,
        db: AsyncSession,
        identifier: str,
        password: str,
    ) -> dict | None:

        # ------------------------------------------------------
        # 1. FIND DJANGO USER BY USERNAME OR EMAIL
        # ------------------------------------------------------

        result = await db.execute(
            select(AuthUser).where(
                or_(
                    AuthUser.username == identifier,
                    AuthUser.email == identifier,
                )
            )
        )

        auth_user = result.scalar_one_or_none()

        if auth_user is None:

            return None

        # ------------------------------------------------------
        # 2. CHECK DJANGO USER ACTIVE
        # ------------------------------------------------------

        if not auth_user.is_active:

            return None

        # ------------------------------------------------------
        # 3. VERIFY DJANGO PASSWORD
        # ------------------------------------------------------

        if not verify_password(
            plain_password=password,
            hashed_password=auth_user.password,
        ):

            return None

        # ------------------------------------------------------
        # 4. GET CUSTOMER PROFILE
        # ------------------------------------------------------

        result = await db.execute(
            select(Customer).where(
                Customer.user_id == auth_user.id
            )
        )

        customer = result.scalar_one_or_none()

        if customer is None:

            return None

        if not customer.is_active:

            return None

        # ------------------------------------------------------
        # 5. CREATE JWT USING CUSTOMER UUID
        # ------------------------------------------------------

        access_token = create_access_token(
            data={
                "user_id": str(customer.id),
                "username": auth_user.username,
            }
        )

        refresh_token = create_refresh_token(
            data={
                "user_id": str(customer.id),
            }
        )

        # ------------------------------------------------------
        # 6. RETURN DATA
        # ------------------------------------------------------

        return {
            "customer": customer,
            "auth_user": auth_user,
            "access": access_token,
            "refresh": refresh_token,
        }


auth_service = AuthService()