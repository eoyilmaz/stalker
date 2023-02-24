"""create EntityGroups table

Revision ID: 258985128aff
Revises: 39d3c16ff005
Create Date: 2016-05-16 16:06:39.389000

"""

# revision identifiers, used by Alembic.
revision = "258985128aff"
down_revision = "39d3c16ff005"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        "EntityGroups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["Entities.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "EntityGroup_Entities",
        sa.Column("entity_group_id", sa.Integer(), nullable=False),
        sa.Column("other_entity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["entity_group_id"],
            ["EntityGroups.id"],
        ),
        sa.ForeignKeyConstraint(
            ["other_entity_id"],
            ["SimpleEntities.id"],
        ),
        sa.PrimaryKeyConstraint("entity_group_id", "other_entity_id"),
    )


def downgrade():
    op.drop_table("EntityGroup_Entities")
    op.drop_table("EntityGroups")
