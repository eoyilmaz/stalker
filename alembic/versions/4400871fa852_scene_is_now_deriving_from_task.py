"""Scene is now deriving from Task

Revision ID: 4400871fa852
Revises: ec1eb2151bb9
Create Date: 2024-11-15 13:16:53.885627
"""

from alembic import op

import stalker

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4400871fa852"
down_revision = "ec1eb2151bb9"


def upgrade():
    """Upgrade the tables."""
    # Update the Scenes.id to be a foreign key to Tasks.id
    op.drop_constraint("Scenes_id_fkey", "Scenes", type_="foreignkey")
    op.create_foreign_key("Scenes_id_fkey", "Scenes", "Tasks", "id", "id")

    # Create a StatusList for Scenes
    # Create a SimpleEntity for the StatusList
    op.execute(
        """
    INSERT INTO "SimpleEntities" (
        entity_type,
        name,
        description,
        created_by_id,
        updated_by_id,
        date_created,
        date_updated,
        generic_text,
        html_style,
        html_class,
        stalker_version
    ) VALUES (
        'StatusList',
        'Scene Statuses',
        '',
        3,
        3,
        (SELECT CAST(NOW() at time zone 'utc' AS timestamp)),
        (SELECT CAST(NOW() at time zone 'utc' AS timestamp)),
        '',
        '',
        '',
        '{stalker_version}'
    )""".format(
            stalker_version=stalker.__version__
        )
    )
    # Insert the same data to the Entities
    op.execute(
        """
    INSERT INTO "Entities" (id) VALUES (
        (SELECT "SimpleEntities".id FROM "SimpleEntities" WHERE "SimpleEntities".name = 'Scene Statuses')
    )
    """
    )
    # Insert the same to the StatusLists
    op.execute(
        """INSERT INTO "StatusLists" (id, target_entity_type) VALUES (
        (SELECT "SimpleEntities".id FROM "SimpleEntities" WHERE "SimpleEntities".name = 'Scene Statuses'),
        'Scene'
    )
    """
    )
    # Create the same StatusList -> Status relation of a Task
    op.execute(
        """INSERT INTO "StatusList_Statuses" (status_list_id, status_id)
    SELECT
        "SimpleEntities".id,
        "StatusList_Statuses".status_id
    FROM "SimpleEntities", "StatusList_Statuses"
    WHERE "SimpleEntities".name = 'Scene Statuses'
        AND "StatusList_Statuses".status_list_id = (
            SELECT "SimpleEntities".id FROM "SimpleEntities" WHERE "SimpleEntities".name = 'Task Statuses'
        )
    """
    )

    # Because Scene class is now deriving from Task
    # we need create a Task for each Scene in the database,
    # with the same id of the Scene
    # carry on the data: id, project_id
    op.execute(
        """
        INSERT INTO "Tasks" (
            id,
            project_id,
            allocation_strategy,
            persistent_allocation,
            status_id,
            status_list_id,
            schedule_model,
            schedule_constraint
        ) SELECT
            "Scenes".id,
            "Scenes".project_id,
            'minallocated',
            TRUE,
            (SELECT "Statuses".id FROM "Statuses" WHERE "Statuses".code = 'CMPL'),
            (SELECT "SimpleEntities".id FROM "SimpleEntities" WHERE "SimpleEntities".name = 'Scene Statuses'),
            'effort',
            0
        FROM "Scenes"
    """
    )

    # drop the project_id column in Scenes table
    with op.batch_alter_table("Scenes", schema=None) as batch_op:
        batch_op.drop_column("project_id")


def downgrade():
    """Downgrade the tables."""
    # Add the project_id column back to the Scenes table
    op.add_column("Scenes", sa.Column("project_id", sa.Integer(), nullable=False))
    # Add the project_id data back to the Scenes table
    op.execute(
        """UPDATE "Scenes" SET project_id = (
            SELECT "Tasks".project_id FROM "Tasks" WHERE "Tasks".id = (
                SELECT "Scenes".id FROM "Scenes"
            )
        )"""
    )
    # set the project_id column not nullable
    op.execute("""ALTER TABLE "Scenes" ALTER COLUMN project_id SET NOT NULL""")
    # Remove the scene entries from Tasks table
    op.execute("""DELETE FROM "Tasks" WHERE id IN (SELECT id  FROM "Scenes")""")
    # Remove the StatusList entries from StatusList_Statuses
    op.execute(
        """DELETE FROM "StatusList_Statuses" WHERE status_list_id = (
            SELECT id FROM "SimpleEntities"
            WHERE "SimpleEntities".name = 'Scene Statuses'
        )
        """
    )
    # Remove the StatusList from StatusLists Table
    op.execute("""DELETE FROM "StatusLists" WHERE target_entity_type = 'Scene'""")
    # Remove the StatusList from Entities Table
    op.execute(
        """DELETE FROM "Entities" WHERE id IN (
            SELECT
                "SimpleEntities".id
            FROM "SimpleEntities"
            WHERE "SimpleEntities".name = 'Scene Statuses'
        )
        """
    )
    # Remove the StatusList from SimpleEntities Table
    op.execute("""DELETE FROM "SimpleEntities" WHERE name = 'Scene Statuses'""")

    # Update the Scenes.id to be a foreign key to Entities.id
    op.drop_constraint("Scenes_id_fkey", "Scenes", type_="foreignkey")
    op.create_foreign_key("Scenes_id_fkey", "Scenes", "Entities", "id", "id")
