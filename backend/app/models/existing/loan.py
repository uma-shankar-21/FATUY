import uuid

from sqlalchemy import String, Numeric, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    loan_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    principal_amount: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    outstanding_amount: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    interest_rate: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )

    monthly_emi: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    tenure_years: Mapped[int] = mapped_column(
        nullable=False,
    )

    next_due_date: Mapped[Date] = mapped_column(
        Date,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
    )