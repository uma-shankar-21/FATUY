from sqlalchemy import Boolean, DateTime, Integer, String

from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AuthUser(Base):
    __tablename__ = "auth_user"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    username: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(254),
        nullable=False,
    )

    password: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    is_staff: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    last_login: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    date_joined: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )