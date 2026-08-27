"""replace conversation storage with expired conversations

Revision ID: f5c2fc4ef57d
Revises: f6b8da055c94
Create Date: 2026-08-27 10:46:15.590117
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "f5c2fc4ef57d"
down_revision: Union[str, Sequence[str], None] = "f6b8da055c94"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # ==========================================================
    # 1. CREATE EXPIRED CONVERSATIONS TABLE
    #
    # This stores the complete Redis conversation after
    # the session expires.
    #
    # Kafka will later process this record.
    # ==========================================================

    op.create_table(
        "expired_conversations",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "session_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "messages",
            postgresql.JSONB(),
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.Column(
            "processed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),

        sa.PrimaryKeyConstraint("id"),
    )


    # ==========================================================
    # INDEXES
    # ==========================================================

    op.create_index(
        "ix_expired_conversations_session_id",
        "expired_conversations",
        ["session_id"],
        unique=True,
    )

    op.create_index(
        "ix_expired_conversations_user_id",
        "expired_conversations",
        ["user_id"],
    )

    op.create_index(
        "ix_expired_conversations_status",
        "expired_conversations",
        ["status"],
    )


    # ==========================================================
    # 2. REMOVE OLD SHORT-TERM MEMORY TABLES
    #
    # conversations and messages are no longer needed.
    # Short-term memory will live in Redis.
    # ==========================================================

    op.drop_table("messages")

    op.drop_table("conversations")


    # ==========================================================
    # 3. REMOVE conversation_id FROM LONG-TERM MEMORY
    #
    # Long-term memory belongs to a user, not an active
    # conversation session.
    # ==========================================================

    op.drop_column(
        "memories",
        "conversation_id",
    )


def downgrade() -> None:

    # ==========================================================
    # RESTORE conversation_id IN MEMORIES
    # ==========================================================

    op.add_column(
        "memories",
        sa.Column(
            "conversation_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
    )


    # ==========================================================
    # RESTORE CONVERSATIONS TABLE
    # ==========================================================

    op.create_table(
        "conversations",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "title",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.PrimaryKeyConstraint("id"),
    )


    # ==========================================================
    # RESTORE MESSAGES TABLE
    # ==========================================================

    op.create_table(
        "messages",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "conversation_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "role",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["conversation_id"],
            ["conversations.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )


    # ==========================================================
    # REMOVE EXPIRED CONVERSATIONS TABLE
    # ==========================================================

    op.drop_index(
        "ix_expired_conversations_status",
        table_name="expired_conversations",
    )

    op.drop_index(
        "ix_expired_conversations_user_id",
        table_name="expired_conversations",
    )

    op.drop_index(
        "ix_expired_conversations_session_id",
        table_name="expired_conversations",
    )

    op.drop_table(
        "expired_conversations"
    )