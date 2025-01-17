"""Link renamed to File

Revision ID: 9f9b88fef376
Revises: 3be540ad3a93
Create Date: 2025-01-14 15:37:15.746961
"""

from alembic import op

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

import stalker

# revision identifiers, used by Alembic.
revision = "9f9b88fef376"
down_revision = "3be540ad3a93"


def upgrade():
    """Upgrade the tables."""
    # -------------------------------------------------------------------------
    # Links -> Files
    op.rename_table("Links", "Files")

    # link_id_fkey
    op.drop_constraint("Links_id_fkey", table_name="Files", type_="foreignkey")
    op.create_foreign_key("Files_id_fkey", "Files", "Entities", ["id"], ["id"])
    # Links_pkey -> Files_pkey
    # This requires a lot of other constraints to be dropped first!!!
    op.drop_constraint("Daily_Links_link_id_fkey", "Daily_Links", type_="foreignkey")
    op.drop_constraint(
        "Project_References_link_id_fkey", "Project_References", type_="foreignkey"
    )
    op.drop_constraint(
        "Task_References_link_id_fkey", "Task_References", type_="foreignkey"
    )
    op.drop_constraint(
        "Version_Inputs_link_id_fkey", "Version_Inputs", type_="foreignkey"
    )
    op.drop_constraint(
        "Version_Outputs_link_id_fkey", "Version_Outputs", type_="foreignkey"
    )
    op.drop_constraint("Versions_id_fkey", "Versions", type_="foreignkey")
    op.drop_constraint("z", "SimpleEntities", type_="foreignkey")
    op.drop_constraint("Links_pkey", "Files", type_="primary")

    op.create_primary_key("Files_pkey", "Files", ["id"])

    # Update "SimpleEntities".entity_type to 'File'
    # and replace the 'Link_%' in the name with 'File_%'
    op.execute(
        """UPDATE "SimpleEntities"
        SET (entity_type, name) = ('File', REPLACE("SimpleEntities".name, 'Link_', 'File_'))
        WHERE "SimpleEntities".entity_type = 'Link'
        """
    )

    # Update "EntityTypes".name for 'Link' to 'File'
    op.execute(
        """UPDATE "EntityTypes"
        SET name = 'File'
        WHERE "EntityTypes".name = 'Link'
        """
    )

    # Update any Types where target_entity_type == 'Link' to 'File'
    op.execute(
        """UPDATE "Types"
        SET target_entity_type = 'File'
        WHERE target_entity_type = 'Link'
        """
    )

    # create "Files".created_with
    op.add_column(
        "Files",
        sa.Column("created_with", sa.String(length=256), nullable=True),
    )

    # migrate the created_with data from Versions to the Files table
    op.execute(
        """UPDATE "Files" SET created_with = "Versions".created_with
        FROM "Versions"
        WHERE "Versions".id = "Files".id
        """
    )

    # -------------------------------------------------------------------------
    # remove created_with from Versions table
    op.drop_column("Versions", "created_with")

    # -------------------------------------------------------------------------
    # Daily_Links -> Daily_Files
    op.rename_table("Daily_Links", "Daily_Files")

    # drop constraints
    # daily_id_fkey
    op.drop_constraint(
        "Daily_Links_daily_id_fkey", table_name="Daily_Files", type_="foreignkey"
    )
    # link_id_fkey
    # dropped already above!
    # pkey
    op.drop_constraint("Daily_Links_pkey", table_name="Daily_Files")

    # link_id -> file_id
    op.alter_column(
        table_name="Daily_Files",
        column_name="link_id",
        new_column_name="file_id",
    )

    # daily_id_fkey
    op.create_foreign_key(
        "Daily_Files_daily_id_fkey",
        "Daily_Files",
        "Dailies",
        ["daily_id"],
        ["id"],
    )

    # link_id_fkey -> file_id_fkey
    op.create_foreign_key(
        "Daily_Files_file_id_fkey",
        "Daily_Files",
        "Files",
        ["file_id"],
        ["id"],
    )

    # pkey
    op.create_primary_key("Daily_Files_pkey", "Daily_Files", ["daily_id", "file_id"])

    # -------------------------------------------------------------------------
    # Version_Outputs -> Version_Files (to preserve data)
    op.rename_table("Version_Outputs", "Version_Files")

    # Constraints
    # drop constraints
    # link_id_fkey
    # dropped already above!
    # version_id_fkey
    op.drop_constraint(
        "Version_Outputs_version_id_fkey", "Version_Files", type_="foreignkey"
    )
    # pkey
    op.drop_constraint(
        "Version_Outputs_pkey", table_name="Version_Files", type_="primary"
    )

    # link_id -> file_id
    op.alter_column("Version_Files", "link_id", new_column_name="file_id")

    # version_id_fkey
    op.create_foreign_key(
        "Version_Files_version_id_fkey",
        "Version_Files",
        "Versions",
        ["version_id"],
        ["id"],
    )

    # file_id_fkey
    op.create_foreign_key(
        "Version_Files_file_id_fkey",
        "Version_Files",
        "Files",
        ["file_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )

    # pkey
    op.create_primary_key(
        "Version_Files_pkey", "Version_Files", ["version_id", "file_id"]
    )

    # -------------------------------------------------------------------------
    # Rename Version_Inputs to File_References:
    #
    #   This table is storing which Version was referencing which other
    #   version.
    #
    #   Data needs to be migrated in tandem with the data moved to the
    #   Version_Files table.
    op.rename_table("Version_Inputs", "File_References")
    op.alter_column("File_References", "link_id", new_column_name="reference_id")
    op.alter_column("File_References", "version_id", new_column_name="file_id")

    # Version_Inputs_version_id_fkey -> File_References_file_id_fkey
    # Version_Inputs_link_id_fkey -> File_References_reference_id_fkey
    op.drop_constraint(
        "Version_Inputs_version_id_fkey",
        table_name="File_References",
        type_="foreignkey",
    )
    # "Version_Inputs_link_id_fkey" dropped already above!
    op.drop_constraint(
        "Version_Inputs_pkey",
        table_name="File_References",
        type_="primary",
    )

    # File_References_file_id_fkey
    op.create_foreign_key(
        "File_References_file_id_fkey",
        "File_References",
        "Files",
        ["file_id"],
        ["id"],
    )

    # File_References_reference_id_fkey
    op.create_foreign_key(
        "File_References_reference_id_fkey",
        "File_References",
        "Files",
        ["reference_id"],
        ["id"],
    )

    # File_References_pkey
    op.create_primary_key(
        "File_References_pkey",
        "File_References",
        ["file_id", "reference_id"],
    )

    # -------------------------------------------------------------------------
    # Project_References
    # link_id -> file_id
    # dropped already above!
    op.alter_column("Project_References", "link_id", new_column_name="reference_id")

    # Constraints
    # link_id_fkey -> reference_fkey
    op.create_foreign_key(
        "Project_References_reference_id_fkey",
        "Project_References",
        "Files",
        ["reference_id"],
        ["id"],
    )

    # -------------------------------------------------------------------------
    # Fix fkey names

    # SimpleEntities_thumbnail_id_fkey
    # dropped already above!
    op.create_foreign_key(
        "SimpleEntities_thumbnail_id_fkey",
        "SimpleEntities",
        "Files",
        ["thumbnail_id"],
        ["id"],
        use_alter=True,
    )

    # SimpleEntities_created_by_id_fkey
    op.drop_constraint("xc", "SimpleEntities", type_="foreignkey")
    op.create_foreign_key(
        "SimpleEntities_created_by_id_fkey",
        "SimpleEntities",
        "Users",
        ["created_by_id"],
        ["id"],
        use_alter=True,
    )

    # SimpleEntities_updated_by_id_fkey
    op.drop_constraint("xu", "SimpleEntities", type_="foreignkey")
    op.create_foreign_key(
        "SimpleEntities_updated_by_id_fkey",
        "SimpleEntities",
        "Users",
        ["updated_by_id"],
        ["id"],
        use_alter=True,
    )

    # SimpleEntities_type_id_fkey
    op.drop_constraint("y", "SimpleEntities", type_="foreignkey")
    op.create_foreign_key(
        "SimpleEntities_type_id_fkey",
        "SimpleEntities",
        "Types",
        ["type_id"],
        ["id"],
        use_alter=True,
    )

    # -------------------------------------------------------------------------
    # Task_References link_id -> reference_id
    # dropped already above!

    # rename the column: link_id -> reference_id
    op.alter_column("Task_References", "link_id", new_column_name="reference_id")

    # link_id_fkey -> file_id_fkey
    op.create_foreign_key(
        "Task_References_reference_id_fkey",
        "Task_References",
        "Files",
        ["reference_id"],
        ["id"],
    )

    # -------------------------------------------------------------------------
    # Versions is now deriving from Entities
    # dropped already above!
    op.create_foreign_key("Versions_id_fkey", "Versions", "Entities", ["id"], ["id"])

    # -------------------------------------------------------------------------
    # Migrate Files that were Versions before, to new entries...
    #   - Go back to Files tables
    #   - Search for Files that have the same ids with Versions
    #   - Create a new entry with the same data to Files, Entities and SimpleEntities
    #     tables.
    #   - Add them to the Version_Files tables, as they were previous versions
    #   - Delete the old files
    op.execute(
        f"""
        -- reshuffle names for entities that have autoname and that are clashing
        UPDATE "SimpleEntities"
            SET name = ("SimpleEntities".entity_type || '_' || gen_random_uuid())
        WHERE name in (
            SELECT
                name
            FROM "SimpleEntities"
            WHERE length(name) > 37 -- entity_type_uuid4
            GROUP BY name
            HAVING COUNT(*) > 1
            ORDER BY name
        );

        -- create temp storage for data coming from "Files" table
        ALTER TABLE "SimpleEntities"
            ADD original_filename character varying(256) COLLATE pg_catalog."default",
            ADD full_path text COLLATE pg_catalog."default",
            ADD created_from_version_id integer,
            ADD created_with character varying(256);

        -- create new entry for all Files that were originally Versions
        WITH sel1 as (
            SELECT
                "File_SimpleEntities".id,
                'File' as entity_type,
                REPLACE("File_SimpleEntities".name, 'Version_', 'File_') as entity_name,
                "File_SimpleEntities".description,
                "File_SimpleEntities".created_by_id,
                "File_SimpleEntities".updated_by_id,
                "File_SimpleEntities".date_created,
                "File_SimpleEntities".date_updated,
                "File_SimpleEntities".type_id,
                "File_SimpleEntities".generic_text,
                "File_SimpleEntities".thumbnail_id,
                "File_SimpleEntities".html_style,
                "File_SimpleEntities".html_class,
                "File_SimpleEntities".stalker_version,
                "Files".original_filename,
                "Files".full_path,
                "Files".created_with
            FROM "Files"
            JOIN "SimpleEntities" AS "File_SimpleEntities" ON "Files".id = "File_SimpleEntities".id
            WHERE "File_SimpleEntities".entity_type = 'Version'
            ORDER BY "File_SimpleEntities".id
        ), ins1 as (
            INSERT INTO "SimpleEntities" (
                entity_type,
                name,
                description,
                created_by_id,
                updated_by_id,
                date_created,
                date_updated,
                type_id,
                html_style,
                html_class,
                stalker_version,
                original_filename,
                full_path,
                created_with,
                created_from_version_id
            ) (
                SELECT
                    sel1.entity_type,
                    sel1.entity_name,
                    sel1.description,
                    sel1.created_by_id,
                    sel1.updated_by_id,
                    sel1.date_created,
                    sel1.date_updated,
                    sel1.type_id,
                    sel1.html_style,
                    sel1.html_class,
                    sel1.stalker_version,
                    sel1.original_filename,
                    sel1.full_path,
                    sel1.created_with,
                    sel1.id as created_from_version_id
                FROM sel1
            )
            RETURNING id as file_id, name as entity_name
        )
        INSERT INTO "Entities" (id) (SELECT ins1.file_id FROM ins1);

        -- Insert into Files
        INSERT INTO "Files" (id, original_filename, full_path, created_with)
        (
            SELECT
                "SimpleEntities".id,
                "SimpleEntities".original_filename,
                "SimpleEntities".full_path,
                "SimpleEntities".created_with
            FROM "SimpleEntities"
            WHERE "SimpleEntities".created_from_version_id IS NOT NULL
        );

        -- Insert into Version_Files
        INSERT INTO "Version_Files" (version_id, file_id)
        (
            SELECT
                "SimpleEntities".created_from_version_id as version_id,
                "SimpleEntities".id as file_id
            FROM "SimpleEntities"
            WHERE "SimpleEntities".created_from_version_id IS NOT NULL
        );

        -- Update File_References
        -- so that the newly created Files
        -- are referencing the newly create other Files and not the old versions

        -- Update the file_id column first
        UPDATE "File_References" SET file_id = sel1.file_id
        FROM (
            SELECT
                id as file_id,
                created_from_version_id
            FROM "SimpleEntities"
            WHERE created_from_version_id IS NOT NULL
        ) as sel1
        WHERE "File_References".file_id = sel1.created_from_version_id;

        -- then the reference_id column
        UPDATE "File_References" SET reference_id = sel1.file_id
        FROM (
            SELECT
                id as file_id,
                created_from_version_id
            FROM "SimpleEntities"
            WHERE created_from_version_id IS NOT NULL
        ) as sel1
        WHERE "File_References".reference_id = sel1.created_from_version_id;

        -- Drop all the Files that previously was a Version

        -- Remove constraints first (Otherwise it will be incredibly slow!)
        ALTER TABLE "SimpleEntities" DROP CONSTRAINT "SimpleEntities_thumbnail_id_fkey";
        ALTER TABLE "Daily_Files" DROP CONSTRAINT "Daily_Files_file_id_fkey";
        ALTER TABLE "Project_References" DROP CONSTRAINT "Project_References_reference_id_fkey";
        ALTER TABLE "Task_References" DROP CONSTRAINT "Task_References_reference_id_fkey";
        ALTER TABLE "File_References" DROP CONSTRAINT "File_References_file_id_fkey";
        ALTER TABLE "File_References" DROP CONSTRAINT "File_References_reference_id_fkey";
        ALTER TABLE "Version_Files" DROP CONSTRAINT "Version_Files_file_id_fkey";
        ALTER TABLE "Files" DROP CONSTRAINT "Files_id_fkey";

        -- Really delete data now
        DELETE FROM "Files"
        WHERE id in (
            SELECT
                id
            FROM "SimpleEntities"
            WHERE entity_type = 'Version'
        );

        -- Recreate constraints
        ALTER TABLE "SimpleEntities"
            ADD CONSTRAINT "SimpleEntities_thumbnail_id_fkey" FOREIGN KEY (thumbnail_id)
                REFERENCES public."Files" (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION;
        ALTER TABLE "Daily_Files"
            ADD CONSTRAINT "Daily_Files_file_id_fkey" FOREIGN KEY (file_id)
                REFERENCES public."Files" (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION;
        ALTER TABLE "Project_References"
            ADD CONSTRAINT "Project_References_reference_id_fkey" FOREIGN KEY (reference_id)
                REFERENCES public."Files" (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION;
        ALTER TABLE "Task_References"
            ADD CONSTRAINT "Task_References_reference_id_fkey" FOREIGN KEY (reference_id)
                REFERENCES public."Files" (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION;
        ALTER TABLE "File_References"
            ADD CONSTRAINT "File_References_file_id_fkey" FOREIGN KEY (file_id)
                REFERENCES public."Files" (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION,
            ADD CONSTRAINT "File_References_reference_id_fkey" FOREIGN KEY (reference_id)
                REFERENCES public."Files" (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION;
        ALTER TABLE "Version_Files"
            ADD CONSTRAINT "Version_Files_file_id_fkey" FOREIGN KEY (file_id)
                REFERENCES public."Files" (id) MATCH SIMPLE
                ON UPDATE CASCADE
                ON DELETE CASCADE;
        ALTER TABLE "Files"
            ADD CONSTRAINT "Files_id_fkey" FOREIGN KEY (id)
                REFERENCES public."Entities" (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION;

        -- delete temp data in "SimpleEntities"
        ALTER TABLE "SimpleEntities"
            DROP COLUMN original_filename,
            DROP COLUMN full_path,
            DROP COLUMN created_from_version_id,
            DROP COLUMN created_with;
        """
    )


def downgrade():
    """Downgrade the tables."""
    # drop constraints first
    op.drop_constraint("Daily_Files_pkey", "Daily_Files", type_="primary")
    op.drop_constraint("Daily_Files_file_id_fkey", "Daily_Files", type_="foreignkey")
    op.drop_constraint("Daily_Files_daily_id_fkey", "Daily_Files", type_="foreignkey")
    op.drop_constraint("File_References_pkey", "File_References", type_="primary")
    op.drop_constraint("File_References_file_id_fkey", "File_References", type_="foreignkey")
    op.drop_constraint("File_References_reference_id_fkey", "File_References", type_="foreignkey")
    op.drop_constraint("Files_pkey", "Files", type_="primary")
    op.drop_constraint("Files_id_fkey", "Files", type_="foreignkey")
    op.drop_constraint("Project_References_reference_id_fkey", "Project_References", type_="foreignkey")
    op.drop_constraint("SimpleEntities_created_by_id_fkey", "SimpleEntities", type_="foreignkey")
    op.drop_constraint("SimpleEntities_thumbnail_id_fkey", "SimpleEntities", type_="foreignkey")
    op.drop_constraint("SimpleEntities_updated_by_id_fkey", "SimpleEntities", type_="foreignkey")
    op.drop_constraint("SimpleEntities_type_id_fkey", "SimpleEntities", type_="foreignkey")
    op.drop_constraint("Task_References_reference_id_fkey", "Task_References", type_="foreignkey")
    op.drop_constraint("Version_Files_pkey", "Version_Files", type_="primary")
    op.drop_constraint("Version_Files_file_id_fkey", "Version_Files", type_="foreignkey")
    op.drop_constraint("Versions_id_fkey", "Versions", type_="foreignkey")

    # rename tables
    op.rename_table("Daily_Files", "Daily_Links")
    op.rename_table("Files", "Links")
    op.rename_table("File_References", "Version_Inputs")
    op.rename_table("Version_Files", "Version_Outputs")

    # rename columns
    op.alter_column("Daily_Links", "file_id", new_column_name="link_id")
    op.alter_column("Version_Outputs", "file_id", new_column_name="link_id")
    op.alter_column("Version_Inputs", "file_id", new_column_name="version_id")
    op.alter_column("Version_Inputs", "reference_id", new_column_name="link_id")
    op.alter_column("Project_References", "reference_id", new_column_name="link_id")
    op.alter_column("Task_References", "reference_id", new_column_name="link_id")

    # migrate the data as much as you can
    op.execute(
        """
        -- There are Versions where there are no corresponding input in the
        -- Links table anymore
        -- Update all the ids of the Links that are in the Version_Inputs with the
        -- id of the version, so that we have a corresponding links for all versions
        -- and then delete all the entries from the Entities and SimpleEntities tables
        -- for those links.

        UPDATE "Links" SET id = sel1.id FROM (
            SELECT
                link_id
            FROM "Version_Links"
        )

        """
    )

    # recreate constraints
    op.create_foreign_key("Daily_Links_daily_id_fkey", "Daily_Links", "Dailies", ["daily_id"], ["id"])
    op.create_foreign_key("Daily_Links_link_id_fkey", "Daily_Links", "Links", ["link_id"], ["id"])
    op.create_primary_key("Daily_Links_pkey", "Daily_Links", ["daily_id", "link_id"])
    op.create_primary_key("Links_pkey", "Links", ["id"])
    op.create_foreign_key("Link_id_fkey", "Links", "Entities", ["id"], ["id"])
    op.create_foreign_key("Project_References_link_id_fkey", "Project_References", ["link_id"], ["id"])
    op.create_foreign_key("Task_References_link_id_fkey", "Task_References", "Links", ["link_id"], ["id"])
    op.create_foreign_key("Version_Inputs_version_id_fkey", "Version_Inputs", "Versions", ["version_id"], ["id"])
    op.create_foreign_key("Version_Inputs_link_id_fkey", "Version_Inputs", "Links", ["link_id"], ["id"])
    op.create_primary_key("Version_Inputs_pkey", "Version_Inputs", ["version_id", "link_id"])
    op.create_primary_key("Version_Outputs_pkey", "Version_Outputs", ["version_id", "link_id"])
    op.create_foreign_key("Version_Outputs_link_id_fkey", "Versions_Outputs", "Links", ["link_id"], ["id"])
    op.create_foreign_key("Version_Outputs_version_id_fkey", "Version_Outputs", "Links", ["version_id"], ["id"])
    op.create_foreign_key("Versions_id_fkey", "Versions", "Links", ["id"], ["id"])
    op.create_foreign_key("xc", "SimpleEntities", "Users", ["created_by_id"], ["id"], use_alter=True)
    op.create_foreign_key("xu", "SimpleEntities", "Users", ["updated_by_id"], ["id"], use_alter=True)
    op.create_foreign_key("y", "SimpleEntities", "Types", ["type_id"], ["id"], use_alter=True)
    op.create_foreign_key("z", "SimpleEntities", "Links", ["thumbnail_id"], ["id"], use_alter=True)













    # pkey
    op.create_primary_key(
        "Daily_Files_pkey",
        "Daily_Files",
        ["daily_id", "file_id"],
    )




    # Rename tables
    op.rename_table("Files", "Links")
    op.rename_table("Daily_Files", "Daily_Links")



    # -------------------------------------------------------------------------
    # Versions should derive from Links again

    op.create_foreign_key("Versions_id_fkey", "Versions", "Entities", ["id"], ["id"])


    # Versions.created_with
    op.add_column(
        "Versions",
        sa.Column(
            "created_with", sa.VARCHAR(length=256), autoincrement=False, nullable=True
        ),
    )

    # Versions derive from Links
    op.drop_constraint(None, "Versions", type_="foreignkey")


    # -------------------------------------------------------------------------
    # Task_References reference_id -> link_id
    # dropped already above!

    # rename the column: link_id -> reference_id
    op.alter_column("Task_References", "link_id", new_column_name="reference_id")

    # link_id_fkey -> file_id_fkey
    op.create_foreign_key(
        "Task_References_reference_id_fkey",
        "Task_References",
        "Files",
        ["reference_id"],
        ["id"],
    )













    #
    op.create_foreign_key("Versions_id_fkey", "Versions", "Links", ["id"], ["id"])
    op.alter_column(
        "Tasks",
        "schedule_model",
        existing_type=stalker.models.enum.ScheduleModelDecorator(
            "effort", "duration", "length"
        ),
        type_=postgresql.ENUM("effort", "length", "duration", name="TaskScheduleModel"),
        existing_nullable=False,
    )
    op.add_column(
        "Task_References",
        sa.Column("link_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "Task_References", type_="foreignkey")
    op.create_foreign_key(
        "Task_References_link_id_fkey", "Task_References", "Links", ["link_id"], ["id"]
    )
    op.drop_column("Task_References", "reference_id")
    op.alter_column(
        "Task_Dependencies",
        "gap_model",
        existing_type=stalker.models.enum.ScheduleModelDecorator(
            "effort", "duration", "length"
        ),
        type_=postgresql.ENUM("length", "duration", name="TaskDependencyGapModel"),
        existing_nullable=False,
    )
    op.drop_constraint("z", "SimpleEntities", type_="foreignkey")
    op.create_foreign_key("z", "SimpleEntities", "Links", ["thumbnail_id"], ["id"])
    op.alter_column(
        "Shots",
        "fps",
        existing_type=sa.Float(precision=3),
        type_=sa.REAL(),
        existing_nullable=True,
    )
    op.alter_column(
        "Reviews",
        "schedule_model",
        existing_type=stalker.models.enum.ScheduleModelDecorator(
            "effort", "duration", "length"
        ),
        type_=postgresql.ENUM(
            "effort", "length", "duration", name="ReviewScheduleModel"
        ),
        existing_nullable=False,
    )
    op.alter_column(
        "Projects",
        "fps",
        existing_type=sa.Float(precision=3),
        type_=sa.REAL(),
        existing_nullable=True,
    )
    op.add_column(
        "Project_References",
        sa.Column("link_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "Project_References", type_="foreignkey")
    op.create_foreign_key(
        "Project_References_link_id_fkey",
        "Project_References",
        "Links",
        ["link_id"],
        ["id"],
    )
    op.drop_column("Project_References", "reference_id")
    op.create_table(
        "Links",
        sa.Column("id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "original_filename",
            sa.VARCHAR(length=256),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("full_path", sa.TEXT(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(["id"], ["Entities.id"], name="Links_id_fkey"),
        sa.PrimaryKeyConstraint("id", name="Links_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "Version_Inputs",
        sa.Column("version_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("link_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["link_id"],
            ["Links.id"],
            name="Version_Inputs_link_id_fkey",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["version_id"], ["Versions.id"], name="Version_Inputs_version_id_fkey"
        ),
        sa.PrimaryKeyConstraint("version_id", "link_id", name="Version_Inputs_pkey"),
    )
    op.create_table(
        "Version_Outputs",
        sa.Column("version_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("link_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["link_id"], ["Links.id"], name="Version_Outputs_link_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["version_id"], ["Versions.id"], name="Version_Outputs_version_id_fkey"
        ),
        sa.PrimaryKeyConstraint("version_id", "link_id", name="Version_Outputs_pkey"),
    )
    op.create_table(
        "Daily_Links",
        sa.Column("daily_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("link_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("rank", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["daily_id"], ["Dailies.id"], name="Daily_Links_daily_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["link_id"], ["Links.id"], name="Daily_Links_link_id_fkey"
        ),
        sa.PrimaryKeyConstraint("daily_id", "link_id", name="Daily_Links_pkey"),
    )
    op.drop_table("Version_Files")
    op.drop_table("Daily_Files")
    op.drop_table("File_References")
    op.drop_table("Files")
    # ### end Alembic commands ###
