"""Budget is now statusable.

Revision ID: 92257ba439e1
Revises: f2005d1fbadc
Create Date: 2016-07-28 13:20:27.397000
"""

from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "92257ba439e1"
down_revision = "f2005d1fbadc"


def upgrade():
    """Upgrade the tables."""
    op.add_column("Budgets", sa.Column("status_id", sa.Integer(), nullable=True))
    op.add_column("Budgets", sa.Column("status_list_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "Budgets", "Statuses", ["status_id"], ["id"])
    op.create_foreign_key(None, "Budgets", "StatusLists", ["status_list_id"], ["id"])

    # create a dummy status list for budgets
    op.execute(
        """insert into "SimpleEntities" (name, entity_type)
        values ('Dummy Budget StatusList', 'StatusList');
        insert into "Entities" (id)
          select
            "SimpleEntities".id
          from "SimpleEntities"
          where "SimpleEntities".entity_type = 'StatusList' and
            "SimpleEntities".name = 'Dummy Budget StatusList'
        ;
        insert into "StatusLists" (id, target_entity_type)
            select
              "SimpleEntities".id,
              'Budget'
            from "SimpleEntities"
            where "SimpleEntities".entity_type = 'StatusList' and
                  "SimpleEntities".name = 'Dummy Budget StatusList'
        ;
        insert into "StatusList_Statuses"
            select
                "SimpleEntities".id,
                "Statuses".id
            from "SimpleEntities", "Statuses"
            where "SimpleEntities".name = 'Dummy Budget StatusList'
            order by "Statuses".id
            limit 1
        ;
        update "Budgets"
          set status_id = (
            select "Statuses".id
            from "Statuses"
            order by "Statuses".id limit 1
          )
        ;
        update "Budgets"
          set status_list_id = (
            select "SimpleEntities".id
            from "SimpleEntities"
            where "SimpleEntities".name = 'Dummy Budget StatusList'
          )
        ;
        """
    )
    # now alter column to be non nullable
    op.alter_column("Budgets", "status_id", nullable=False)
    op.alter_column("Budgets", "status_list_id", nullable=False)


def downgrade():
    """Downgrade the tables."""
    op.execute(
        """
        ALTER TABLE public."Budgets" DROP CONSTRAINT "Budgets_status_id_fkey";
        ALTER TABLE public."Budgets" DROP CONSTRAINT "Budgets_status_list_id_fkey";
        ALTER TABLE public."Budgets" DROP COLUMN status_id;
        ALTER TABLE public."Budgets" DROP COLUMN status_list_id;
        """
    )

    # remove 'Dummy Budget StatusList' if it exists
    op.execute(
        """
          delete
          from "StatusList_Statuses"
          where "StatusList_Statuses".status_list_id = (
            select
              id
            from "SimpleEntities"
            where "SimpleEntities".name = 'Dummy Budget StatusList'
          )
          ;
          delete
          from "StatusLists"
          where "StatusLists".id = (
            select
              id
            from "SimpleEntities"
            where "SimpleEntities".name = 'Dummy Budget StatusList'
          )
          ;
          delete
          from "Entities"
          where "Entities".id = (
            select
              id
            from "SimpleEntities"
            where "SimpleEntities".name = 'Dummy Budget StatusList'
          )
          ;
          delete
          from "SimpleEntities"
          where "SimpleEntities".name = 'Dummy Budget StatusList'
          ;
        """
    )
