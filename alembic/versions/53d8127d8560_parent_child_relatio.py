"""parent child relation in Versions.

Revision ID: 53d8127d8560
Revises: 4a836cf73bcf
Create Date: 2013-05-22 12:44:05.626047
"""

from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "53d8127d8560"
down_revision = "4a836cf73bcf"


def upgrade():
    """Upgrade the tables."""
    try:
        op.add_column("Versions", sa.Column("parent_id", sa.Integer(), nullable=True))
    except (sa.exc.OperationalError, sa.exc.InternalError):
        pass


def downgrade():
    """Downgrade the tables."""
    op.drop_column("Versions", "parent_id")
