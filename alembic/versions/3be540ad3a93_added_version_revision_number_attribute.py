"""Added Version.revision_number attribute

Revision ID: 3be540ad3a93
Revises: 1875136a2bfc
Create Date: 2024-12-04 17:04:37.174269
"""

from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3be540ad3a93"
down_revision = "1875136a2bfc"


def upgrade():
    """Upgrade the tables."""
    op.execute(
        """ALTER TABLE "Versions" ADD revision_number integer NOT NULL DEFAULT 1;"""
    )


def downgrade():
    """Downgrade the tables."""
    # because we are removing the revision_number column,
    # add the 1000 * (revision_number - 1) to all the version numbers
    # to preserve the version sequences, intact...
    op.execute(
        """UPDATE "Versions" SET version_number = (1000 * (revision_number - 1) + version_number);"""
    )
    op.execute("""ALTER TABLE "Versions" DROP COLUMN revision_number;""")
