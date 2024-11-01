"""Added html_style and html_class columns to SimpleEntities.

Revision ID: 5168cc8552a3
Revises: 174567b9c159
Create Date: 2013-11-14 23:03:55.413681
"""

from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "5168cc8552a3"
down_revision = "174567b9c159"


def upgrade():
    """Upgrade the tables."""
    op.add_column("SimpleEntities", sa.Column("html_class", sa.String(), nullable=True))
    op.add_column("SimpleEntities", sa.Column("html_style", sa.String(), nullable=True))


def downgrade():
    """Downgrade the tables."""
    op.drop_column("SimpleEntities", "html_style")
    op.drop_column("SimpleEntities", "html_class")
