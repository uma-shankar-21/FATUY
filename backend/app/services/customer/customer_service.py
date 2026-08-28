from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)

from app.models.customer import Customer

from app.schemas.customer import (
    CustomerCreate,
)


class CustomerService:

    async def create_customer(
        self,
        db: AsyncSession,
        data: CustomerCreate,
    ) -> Customer:

        # ==========================================
        # CHECK USERNAME
        # ==========================================

        result = await db.execute(
            select(Customer).where(
                Customer.username == data.username
            )
        )

        existing_customer = (
            result.scalar_one_or_none()
        )

        if existing_customer is not None:

            raise ValueError(
                "Username already exists."
            )

        # ==========================================
        # CHECK EMAIL
        # ==========================================

        result = await db.execute(
            select(Customer).where(
                Customer.email == data.email
            )
        )

        existing_customer = (
            result.scalar_one_or_none()
        )

        if existing_customer is not None:

            raise ValueError(
                "Email already exists."
            )

        # ==========================================
        # CHECK PHONE
        # ==========================================

        result = await db.execute(
            select(Customer).where(
                Customer.phone == data.phone
            )
        )

        existing_customer = (
            result.scalar_one_or_none()
        )

        if existing_customer is not None:

            raise ValueError(
                "Phone number already exists."
            )

        # ==========================================
        # CREATE CUSTOMER
        # ==========================================

        customer = Customer(
            username=data.username,
            email=data.email,
            password_hash=hash_password(
                data.password
            ),
            first_name=data.first_name,
            last_name=data.last_name,
            phone=data.phone,
            date_of_birth=data.date_of_birth,
        )

        db.add(customer)

        await db.commit()

        await db.refresh(customer)

        return customer


    async def get_customer(
        self,
        db: AsyncSession,
        customer_id: UUID,
    ) -> Customer | None:

        result = await db.execute(
            select(Customer).where(
                Customer.id == customer_id
            )
        )

        return result.scalar_one_or_none()


    async def login_customer(
        self,
        db: AsyncSession,
        identifier: str,
        password: str,
    ) -> dict | None:

        # ==========================================
        # FIND BY USERNAME OR EMAIL
        # ==========================================

        result = await db.execute(
            select(Customer).where(
                or_(
                    Customer.username == identifier,
                    Customer.email == identifier,
                )
            )
        )

        customer = result.scalar_one_or_none()

        if customer is None:

            return None

        # ==========================================
        # CHECK ACTIVE STATUS
        # ==========================================

        if not customer.is_active:

            return None

        # ==========================================
        # VERIFY PASSWORD
        # ==========================================

        if not verify_password(
            password,
            customer.password_hash,
        ):

            return None

        # ==========================================
        # CREATE JWT TOKENS
        # ==========================================

        access_token = create_access_token(
            data={
                "user_id": str(customer.id),
            }
        )

        refresh_token = create_refresh_token(
            data={
                "user_id": str(customer.id),
            }
        )

        return {
            "customer": customer,
            "access": access_token,
            "refresh": refresh_token,
        }


customer_service = CustomerService()