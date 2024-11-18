"""Rename depends_to to depends_on

Revision ID: 019378697b5b
Revises: feca9bac7d5a
Create Date: 2024-11-01 13:59:11.513575
"""

from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "019378697b5b"
down_revision = "feca9bac7d5a"


def upgrade():
    """Upgrade the tables."""
    op.alter_column(
        "Task_Dependencies", "depends_to_id", new_column_name="depends_on_id"
    )


def downgrade():
    """Downgrade the tables."""
    op.alter_column(
        "Task_Dependencies", "depends_on_id", new_column_name="depends_to_id"
    )
