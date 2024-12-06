"""Removed Version.variant_name attribute

Revision ID: 1875136a2bfc
Revises: a2007ad7f535
Create Date: 2024-11-28 10:18:56.634490
"""

from alembic import op

import sqlalchemy as sa

import stalker


# revision identifiers, used by Alembic.
revision = "1875136a2bfc"
down_revision = "a2007ad7f535"


def upgrade():
    """Upgrade the tables."""
    # create a new Variant task for all the Versions as their new parents.
    op.execute(
        f"""
        -- add temporary column to simple entities
        ALTER TABLE "SimpleEntities" ADD temp_variant_parent_id integer;

        -- insert a new Variant for each distinct Version.variant_name
        WITH sel1 as (
            SELECT
                subtable.task_id as task_id,
                'Variant' as entity_type,
                subtable.name as name,
                'Created by alembic revision: {revision}' as description,
                (SELECT CAST(NOW() at time zone 'utc' AS timestamp)) as date_created,
                (SELECT CAST(NOW() at time zone 'utc' AS timestamp)) as date_updated,
                '' as html_style,
                '' as html_class,
                '{stalker.__version__}' as stalker_version,
                subtable.project_id as project_id,
                false as is_milestone,
                subtable.allocation_strategy as allocation_strategy,
                subtable.persistent_allocation as persistent_allocation,
                500 as priority,
                10 as bid_timing,
                'min' as bid_unit,
                0 as schedule_seconds,
                0 as total_logged_seconds,
                0 as review_number,
                subtable.good_id as good_id,
                subtable.status_id as status_id,
                (SELECT id FROM "StatusLists" WHERE "StatusLists".target_entity_type = 'Variant') as status_list_id,
                subtable.start as start,
                subtable.duration as duration,
                subtable.computed_end as computed_end,
                subtable.computed_start as computed_start,
                subtable.end as end,
                subtable.schedule_timing as schedule_timing,
                subtable.schedule_unit as schedule_unit,
                subtable.schedule_constraint as schedule_constraint,
                subtable.schedule_model as schedule_model,
                subtable.parent_id as parent_id
            FROM (
                SELECT
                    (ARRAY_AGG(DISTINCT(COALESCE("Versions".task_id))))[1] as task_id,
                    (ARRAY_AGG(DISTINCT(COALESCE("Versions".variant_name))))[1] as name,
                    (ARRAY_AGG(DISTINCT(COALESCE("Version_Tasks".project_id))))[1] as project_id,
                    (ARRAY_AGG(DISTINCT(COALESCE("Version_Tasks".status_id))))[1] as status_id,
                    (ARRAY_AGG(DISTINCT(COALESCE("Version_Tasks".allocation_strategy))))[1] as allocation_strategy,
                    (ARRAY_AGG(DISTINCT(COALESCE("Version_Tasks".persistent_allocation))))[1] as persistent_allocation,
                    (ARRAY_AGG(DISTINCT(COALESCE("Version_Tasks".good_id))))[1] as good_id,
                    (ARRAY_AGG(DISTINCT(COALESCE("Version_Tasks".schedule_constraint))))[1] as schedule_constraint,
                    (ARRAY_AGG(DISTINCT(COALESCE("Version_Tasks".schedule_model))))[1] as schedule_model,
                    (ARRAY_AGG(DISTINCT(COALESCE("Version_Tasks".parent_id))))[1] as parent_id,
                    (ARRAY_AGG(DISTINCT(COALESCE("Version_Tasks".start))))[1] as start,
                    (ARRAY_AGG(DISTINCT(COALESCE("Version_Tasks".duration))))[1] as duration,
                    (ARRAY_AGG(DISTINCT(COALESCE("Version_Tasks".computed_end))))[1] as computed_end,
                    (ARRAY_AGG(DISTINCT(COALESCE("Version_Tasks".computed_start))))[1] as computed_start,
                    (ARRAY_AGG(DISTINCT(COALESCE("Version_Tasks".end))))[1] as end,
                    (ARRAY_AGG(DISTINCT(COALESCE("Version_Tasks".schedule_timing))))[1] as schedule_timing,
                    (ARRAY_AGG(DISTINCT(COALESCE("Version_Tasks".schedule_unit))))[1] as schedule_unit
                FROM "Versions"
                JOIN "SimpleEntities" AS "Version_SimpleEntities" ON "Versions".id = "Version_SimpleEntities".id
                JOIN "Tasks" AS "Version_Tasks" ON "Versions".task_id = "Version_Tasks".id
                JOIN "StatusLists" AS "Variant_StatusLists" ON "Variant_StatusLists".target_entity_type = 'Variant'
                GROUP BY
                    "Versions".task_id,
                    "Versions".variant_name
                ORDER BY
                    "Versions".task_id
            ) as subtable
        ),
        ins1 as (
            INSERT INTO "SimpleEntities" (
                entity_type,
                name,
                description,
                date_created,
                date_updated,
                html_style,
                html_class,
                stalker_version,
                temp_variant_parent_id
            ) (
                SELECT
                    sel1.entity_type,
                    sel1.name,
                    sel1.description,
                    sel1.date_created,
                    sel1.date_updated,
                    sel1.html_style,
                    sel1.html_class,
                    sel1.stalker_version,
                    sel1.task_id -- use task_id as parent_id
                FROM sel1
            )
            RETURNING id as variant_id, name as variant_name, temp_variant_parent_id as variant_parent_id
        ),
        ins2 as (
            INSERT INTO "Entities" (id) (SELECT ins1.variant_id FROM ins1)
        ), ins3 AS (
            INSERT INTO "Tasks" (
                id,
                project_id,
                is_milestone,
                allocation_strategy,
                persistent_allocation,
                priority,
                bid_timing,
                schedule_seconds,
                total_logged_seconds,
                review_number,
                good_id,
                status_id,
                status_list_id,
                start,
                duration,
                computed_end,
                computed_start,
                "end",
                schedule_timing,
                schedule_unit,
                schedule_constraint,
                schedule_model,
                parent_id
            )
            (
                SELECT
                    ins1.variant_id,
                    sel1.project_id,
                    sel1.is_milestone,
                    sel1.allocation_strategy,
                    sel1.persistent_allocation,
                    sel1.priority,
                    sel1.bid_timing,
                    sel1.schedule_seconds,
                    sel1.total_logged_seconds,
                    sel1.review_number,
                    sel1.good_id,
                    sel1.status_id,
                    sel1.status_list_id,
                    sel1.start,
                    sel1.duration,
                    sel1.computed_end,
                    sel1.computed_start,
                    sel1.end,
                    sel1.schedule_timing,
                    sel1.schedule_unit,
                    sel1.schedule_constraint,
                    sel1.schedule_model,
                    sel1.task_id -- use the original task as the parent of the new Variant
                FROM sel1, ins1
                WHERE sel1.name = ins1.variant_name AND sel1.task_id = ins1.variant_parent_id 
            )
        )
        INSERT INTO "Variants" (id) (SELECT ins1.variant_id FROM ins1);

        -- Update the Versions to use the new Variants as parents
        UPDATE "Versions"
        SET task_id = subtable.variant_id
        FROM (
            SELECT
                "Versions".id as version_id,
                "Versions".variant_name as version_variant_name,
                "Versions".task_id as version_task_id,
                "Tasks".id as task_id,
                "Variant_Tasks".parent_id as variant_parent_id,
                "Variant_Tasks".id as variant_id,
                "Variant_SimpleEntities".name as variant_name
            FROM "Versions"
            JOIN "Tasks" ON "Versions".task_id = "Tasks".id
            JOIN "Tasks" AS "Variant_Tasks" ON "Variant_Tasks".parent_id = "Tasks".id
            JOIN "SimpleEntities" AS "Variant_SimpleEntities" ON "Variant_Tasks".id = "Variant_SimpleEntities".id
            WHERE "Versions".variant_name = "Variant_SimpleEntities".name
            ORDER BY "Versions".id
        ) as subtable
        WHERE "Versions".id = subtable.version_id;


        -- Remove the temporary column
        ALTER TABLE "SimpleEntities" DROP COLUMN temp_variant_parent_id;

        -- And drop the Versions.variant_name column
        ALTER TABLE "Versions" DROP COLUMN variant_name;
        """
    )


def downgrade():
    """Downgrade the tables."""
    op.add_column(
        "Versions",
        sa.Column(
            "variant_name", sa.VARCHAR(length=256), autoincrement=False, nullable=True
        ),
    )

    op.execute(
        """
        -- Update Version.variant_name with parent names
        UPDATE "Versions" SET (variant_name, task_id) = (subtable.variant_name, subtable.task_id)
        FROM (
            SELECT
                "Versions".id as version_id,
                "Variant_SimpleEntities".name as variant_name,
                "Variant_Tasks".parent_id as task_id
            FROM "Versions"
            JOIN "SimpleEntities" as "Variant_SimpleEntities" on "Versions".task_id = "Variant_SimpleEntities".id
            JOIN "Tasks" as "Variant_Tasks" on "Versions".task_id = "Variant_Tasks".id
        ) as subtable
        WHERE subtable.version_id = "Versions".id;

        -- Remove all the variants that had a version before
        -- match by the Variant.name = Version.variant_name under the same parent task
        DELETE FROM "Variants"
        WHERE "Variants".id IN (
            SELECT
                DISTINCT("Variants".id) --,
                -- "Variant_SimpleEntities".name,
                -- "Variant_Tasks".parent_id,
                -- "Versions".variant_name,
                -- "Versions".task_id
            FROM "Variants"
            JOIN "Tasks" AS "Variant_Tasks" ON "Variants".id = "Variant_Tasks".id 
            JOIN "Versions" ON "Variant_Tasks".parent_id = "Versions".task_id
            JOIN "SimpleEntities" AS "Variant_SimpleEntities" ON "Variants".id = "Variant_SimpleEntities".id
            WHERE "Variant_SimpleEntities".name = "Versions".variant_name
        );
    """
    )
