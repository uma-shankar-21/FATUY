"""create outbox events table

Revision ID: <NEW_REVISION_ID>
Revises: f5c2fc4ef57d
Create Date: 2026-08-27

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers
revision: str = "<NEW_REVISION_ID>"
down_revision: Union[str, Sequence[str], None] = (
    "f5c2fc4ef57d"
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "outbox_events",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "topic",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "payload",
            postgresql.JSONB(
                astext_type=sa.Text()
            ),
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
            server_default="pending",
        ),

        sa.Column(
            "retry_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),

        sa.Column(
            "last_error",
            sa.Text(),
            nullable=True,
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

        sa.PrimaryKeyConstraint(
            "id"
        ),
    )

    op.create_index(
        "ix_outbox_events_status",
        "outbox_events",
        ["status"],
    )

    op.create_index(
        "ix_outbox_events_topic",
        "outbox_events",
        ["topic"],
    )


def downgrade() -> None:

    op.drop_index(
        "ix_outbox_events_topic",
        table_name="outbox_events",
    )

    op.drop_index(
        "ix_outbox_events_status",
        table_name="outbox_events",
    )

    op.drop_table(
        "outbox_events"
    )