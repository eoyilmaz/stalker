"""Added "User.efficiency" column.

Revision ID: 59bfe820c369
Revises: af869ddfdf9
Create Date: 2014-04-26 23:50:53.880274
"""

from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "59bfe820c369"
down_revision = "af869ddfdf9"


def upgrade():
    """Upgrade the tables."""
    op.add_column("Users", sa.Column("efficiency", sa.Float(), nullable=True))
    # set default value
    op.execute('update "Users" set efficiency = 1.0')


def downgrade():
    """Downgrade the tables."""
    op.drop_column("Users", "efficiency")
