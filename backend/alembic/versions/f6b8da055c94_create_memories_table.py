"""create memories table

Revision ID: f6b8da055c94
Revises: 3eaf40fa3cc3
Create Date: 2026-08-27
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers
revision: str = "f6b8da055c94"
down_revision: Union[str, Sequence[str], None] = "3eaf40fa3cc3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "memories",

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
            "conversation_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),

        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "memory_type",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "importance",
            sa.Integer(),
            nullable=False,
            server_default="1",
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

    op.create_index(
        "ix_memories_user_id",
        "memories",
        ["user_id"],
    )


def downgrade() -> None:

    op.drop_index(
        "ix_memories_user_id",
        table_name="memories",
    )

    op.drop_table(
        "memories"
    )