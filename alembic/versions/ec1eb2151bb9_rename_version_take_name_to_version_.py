"""Rename Version.take_name to Version.variant_name

Revision ID: ec1eb2151bb9
Revises: 019378697b5b
Create Date: 2024-11-01 16:37:18.048904
"""

from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ec1eb2151bb9"
down_revision = "019378697b5b"


def upgrade():
    """Upgrade the tables."""
    op.alter_column("Versions", "take_name", new_column_name="variant_name")


def downgrade():
    """Downgrade the tables."""
    op.alter_column("Versions", "variant_name", new_column_name="take_name")
