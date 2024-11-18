"""Shot Sequence relation is now many-to-one

Revision ID: e25ec9930632
Revises: 4400871fa852
Create Date: 2024-11-16 00:27:54.060738
"""

from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e25ec9930632"
down_revision = "4400871fa852"


def upgrade():
    """Upgrade the tables."""
    # Add sequence_id column
    op.add_column("Shots", sa.Column("sequence_id", sa.Integer(), nullable=True))

    # Create foreign key constraint
    op.create_foreign_key(None, "Shots", "Sequences", ["sequence_id"], ["id"])

    # Migrate the data
    op.execute(
        """UPDATE "Shots" SET sequence_id = (
        SELECT sequence_id
            FROM "Shot_Sequences"
            WHERE "Shot_Sequences".shot_id = "Shots".id LIMIT 1
    )"""
    )

    # Drop Shot_Sequences Table
    op.execute("""DROP TABLE "Shot_Sequences" """)


def downgrade():
    """Downgrade the tables."""
    # Add Shot_Sequences Table
    op.create_table(
        "Shot_Sequences",
        sa.Column("shot_id", sa.Integer(), nullable=False),
        sa.Column("sequence_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["shot_id"],
            ["Shots.id"],
        ),
        sa.ForeignKeyConstraint(
            ["sequence_id"],
            ["Sequences.id"],
        ),
    )

    # Transfer Data
    op.execute(
        """
    UPDATE "Shot_Sequences" SET shot_id, sequence_id = (
        SELECT id, sequence_id FROM "Shots" WHERE "Shots".sequence_id != NULL
    )
    """
    )

    # Drop foreign key constraint
    op.drop_constraint("Shots_sequence_id_fkey", "Shots", type_="foreignkey")

    # drop Shots.sequence_id column
    op.drop_column("Shots", "sequence_id")
