"""Added "Repository.code" attribute.

Revision ID: bf67e6a234b4
Revises: ed0167fff399
Create Date: 2020-01-01 09:50:19.086342
"""

import logging

from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bf67e6a234b4"
down_revision = "ed0167fff399"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def upgrade():
    """Upgrade the tables."""
    # add the column
    logger.info("creating code column in Repositories table")
    op.add_column(
        "Repositories", sa.Column("code", sa.String(length=256), nullable=True)
    )

    # copy the name as code
    logger.info(
        "filling data to the code column in Repositories table from "
        "Repositories.name column"
    )
    op.execute(
        r"""UPDATE "Repositories"
        SET code = (
            SELECT REGEXP_REPLACE(name, '\s+', '')
            FROM "SimpleEntities" WHERE id="Repositories".id
        )"""
    )
    logger.info("set code column to not nullable")
    op.alter_column("Repositories", "code", nullable=False)


def downgrade():
    """Downgrade the tables."""
    logger.info("removing code column from Repositories table")
    op.drop_column("Repositories", "code")
