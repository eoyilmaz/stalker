"""Remove Project.active attribute

Revision ID: 644f5251fc0d
Revises: 5078390e5527
Create Date: 2024-11-18 12:47:09.673241
"""

from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "644f5251fc0d"
down_revision = "5078390e5527"


def upgrade():
    """Upgrade the tables."""
    # just remove the "active" column
    with op.batch_alter_table("Projects", schema=None) as batch_op:
        batch_op.drop_column("active")


def downgrade():
    """Downgrade the tables."""
    with op.batch_alter_table("Projects", schema=None) as batch_op:
        batch_op.add_column(sa.Column("active", sa.Boolean(), nullable=True))

    # restore the value by checking the status
    op.execute(
        """UPDATE "Projects" SET active = (
        SELECT
            (
                CASE WHEN "Projects".status_id = (
                    SELECT
                        "Statuses".id
                    FROM "Statuses"
                    WHERE "Statuses".code = 'WIP'
                )
                THEN true ELSE false END
            ) as active
        FROM "Projects"
    )
    """
    )
