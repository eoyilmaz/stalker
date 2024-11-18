"""Shot Scene relation is now many-to-one

Revision ID: 5078390e5527
Revises: e25ec9930632
Create Date: 2024-11-18 11:35:10.872216
"""

from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5078390e5527"
down_revision = "e25ec9930632"


def upgrade():
    """Upgrade the tables."""
    # Add scene_id column
    op.add_column("Shots", sa.Column("scene_id", sa.Integer(), nullable=True))

    # Create foreign key constraint
    op.create_foreign_key(None, "Shots", "Scenes", ["scene_id"], ["id"])

    # Migrate the data
    op.execute(
        """UPDATE "Shots" SET scene_id = (
            SELECT scene_id
                FROM "Shot_Scenes"
                WHERE "Shot_Scenes".shot_id = "Shots".id LIMIT 1
        )"""
    )

    # Drop Shot_Scenes Table
    op.execute("""DROP TABLE "Shot_Scenes" """)


def downgrade():
    """Downgrade the tables."""
    # Add Shot_Scenes Table
    op.create_table(
        "Shot_Scenes",
        sa.Column("shot_id", sa.Integer(), nullable=False),
        sa.Column("scene_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["shot_id"],
            ["Shots.id"],
        ),
        sa.ForeignKeyConstraint(
            ["scene_id"],
            ["Scenes.id"],
        ),
    )

    # Transfer Data
    op.execute(
        """
    UPDATE "Shot_Scenes" SET shot_id, scene_id = (
        SELECT id, scene_id FROM "Shots" WHERE "Shots".scene_id != NULL
    )
    """
    )

    # Drop foreign key constraint
    op.drop_constraint("Shots_scene_id_fkey", "Shots", type_="foreignkey")

    # drop Shots.scene_id column
    op.drop_column("Shots", "scene_id")
