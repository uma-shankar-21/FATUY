import uuid

from sqlalchemy import String, Numeric, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("bank_accounts.id"),
        nullable=False,
    )

    transaction_type: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    amount: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        default="INR",
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    merchant: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    transaction_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
    )