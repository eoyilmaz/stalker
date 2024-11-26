"""Added Review.version_id column

Revision ID: a2007ad7f535
Revises: 91ed52b72b82
Create Date: 2024-11-26 11:36:07.776169
"""

from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a2007ad7f535"
down_revision = "91ed52b72b82"


def upgrade():
    """Upgrade the tables."""
    op.add_column("Reviews", sa.Column("version_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "Reviews_version_id_fkey",
        "Reviews",
        "Versions",
        ["version_id"],
        ["id"],
    )


def downgrade():
    """Downgrade the tables."""
    op.drop_constraint("Reviews_version_id_fkey", "Reviews", type_="foreignkey")
    op.drop_column("Reviews", "version_id")
