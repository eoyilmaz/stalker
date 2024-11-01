"""Added client_id column to Goods table.

Revision ID: 1181305d3001
Revises: 31b1e22b455e
Create Date: 2017-05-17 18:17:46.555000
"""

from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "1181305d3001"
down_revision = "31b1e22b455e"


def upgrade():
    """Upgrade the tables."""
    op.add_column("Goods", sa.Column("client_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "Goods", "Clients", ["client_id"], ["id"])


def downgrade():
    """Downgrade the tables."""
    op.drop_constraint(None, "Goods", type_="foreignkey")
    op.drop_column("Goods", "client_id")
