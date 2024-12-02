"""Created Variant class.

Revision ID: 91ed52b72b82
Revises: 644f5251fc0d
Create Date: 2024-11-22 07:57:46.848687
"""

from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "91ed52b72b82"
down_revision = "644f5251fc0d"


def upgrade():
    """Upgrade the tables."""
    op.create_table(
        "Variants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["Tasks.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.alter_column(
        "Projects",
        "fps",
        existing_type=sa.REAL(),
        type_=sa.Float(precision=3),
        existing_nullable=True,
    )
    op.alter_column(
        "Shots",
        "fps",
        existing_type=sa.REAL(),
        type_=sa.Float(precision=3),
        existing_nullable=True,
    )

    # create Variant Status Lists
    op.execute("""
        WITH ins1 AS (
            INSERT INTO "SimpleEntities" (
               entity_type,
               name,
               description,
               date_created,
               date_updated,
               html_style,
               html_class,
               stalker_version
            )
            VALUES (
                'StatusList',
                'Variant Statuses',
                'Created by alembic revision: 91ed52b72b82',
                (SELECT CAST(NOW() at time zone 'utc' AS timestamp)),
                (SELECT CAST(NOW() at time zone 'utc' AS timestamp)),
                '',
                '',
                '1.0.0.dev1'
            )
            RETURNING id as variant_status_list_id
        ),
        ins2 AS (
            INSERT INTO "Entities" (id) (SELECT ins1.variant_status_list_id FROM ins1)
        )
        INSERT INTO "StatusLists" (id, target_entity_type) (SELECT ins1.variant_status_list_id, 'Variant' FROM ins1);
    """)

    # Add the same statuses of Task StatusList to Variant StatusList
    op.execute(
        """
        INSERT INTO "StatusList_Statuses" (status_list_id, status_id) (
            SELECT
                (SELECT id FROM "StatusLists" WHERE target_entity_type = 'Variant') as status_list_id,
                "StatusList_Statuses".status_id
            FROM "StatusList_Statuses"
            WHERE "StatusList_Statuses".status_list_id = (
                SELECT id FROM "StatusLists" WHERE target_entity_type = 'Task'
            )
        )
        """
    )


def downgrade():
    """Downgrade the tables."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "Shots",
        "fps",
        existing_type=sa.Float(precision=3),
        type_=sa.REAL(),
        existing_nullable=True,
    )
    op.alter_column(
        "Projects",
        "fps",
        existing_type=sa.Float(precision=3),
        type_=sa.REAL(),
        existing_nullable=True,
    )
    # remove Variant Status List Statuses
    op.execute("""
        DELETE FROM "StatusList_Statuses"
        WHERE "StatusList_Statuses".status_list_id = (
            SELECT id FROM "StatusLists" WHERE "StatusLists".target_entity_type = 'Variant'
        )
    """)
    # remove Variant Status Lists
    op.execute("""
        WITH del1 AS (
            DELETE FROM "StatusLists"
               WHERE "StatusLists".target_entity_type = 'Variant'
               RETURNING "StatusLists".id as deleted_status_list_id
        ), del2 AS (
            DELETE FROM "Entities" WHERE "Entities".id = (SELECT del1.deleted_status_list_id FROM del1)
        )
        DELETE FROM "SimpleEntities" WHERE "SimpleEntities".id = (SELECT del1.deleted_status_list_id FROM del1)
    """)
    op.drop_table("Variants")
