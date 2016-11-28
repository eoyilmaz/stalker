"""added ProjectClients

Revision ID: f2005d1fbadc
Revises: 258985128aff
Create Date: 2016-06-27 14:33:10.642000

"""

# revision identifiers, used by Alembic.
revision = 'f2005d1fbadc'
down_revision = '745b210e6907'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table(
        'Project_Clients',
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('rid', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['client_id'], ['Clients.id'], ),
        sa.ForeignKeyConstraint(['project_id'], ['Projects.id'], ),
        sa.ForeignKeyConstraint(['rid'], ['Roles.id'], ),
        sa.PrimaryKeyConstraint('client_id', 'project_id')
    )

    # before doing anything store current project clients
    op.execute(
        """insert into "Project_Clients"
          select client_id, id, NULL
          from "Projects"
          where "Projects".client_id is not NULL
        """
    )

    # create missing constraints if any
    op.execute("""
    ALTER TABLE "BudgetEntries" DROP CONSTRAINT IF EXISTS "BudgetEntries_good_id_fkey";
    ALTER TABLE "BudgetEntries"
      ADD CONSTRAINT "BudgetEntries_good_id_fkey" FOREIGN KEY (good_id)
          REFERENCES public."Goods" (id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE NO ACTION;
    """)

    op.execute("""
    ALTER TABLE "Budgets" DROP CONSTRAINT IF EXISTS "Budgets_parent_id_fkey";
    ALTER TABLE public."Budgets"
      ADD CONSTRAINT "Budgets_parent_id_fkey" FOREIGN KEY (parent_id)
          REFERENCES public."Budgets" (id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE NO ACTION;
    """)

    op.execute("""
    ALTER TABLE "Dailies" DROP CONSTRAINT IF EXISTS "Dailies_project_id_fkey";
    ALTER TABLE public."Dailies"
      ADD CONSTRAINT "Dailies_project_id_fkey" FOREIGN KEY (project_id)
          REFERENCES public."Projects" (id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE NO ACTION;
    """)

    op.execute("""
    ALTER TABLE "Department_Users" DROP CONSTRAINT IF EXISTS "Department_Users_rid_fkey";
    ALTER TABLE public."Department_Users"
      ADD CONSTRAINT "Department_Users_rid_fkey" FOREIGN KEY (rid)
          REFERENCES public."Roles" (id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE NO ACTION;
    """)

    op.execute("""
    ALTER TABLE "Pages" DROP CONSTRAINT IF EXISTS "Pages_project_id_fkey";
    ALTER TABLE public."Pages"
      ADD CONSTRAINT "Pages_project_id_fkey" FOREIGN KEY (project_id)
          REFERENCES public."Projects" (id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE NO ACTION;
    """)

    op.execute("""
    ALTER TABLE "Project_Users" DROP CONSTRAINT IF EXISTS "Project_Users_rid_fkey";
    ALTER TABLE public."Project_Users"
      ADD CONSTRAINT "Project_Users_rid_fkey" FOREIGN KEY (rid)
          REFERENCES public."Roles" (id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE NO ACTION;
    """)

    op.drop_constraint(
        u'Projects_client_id_fkey',
        'Projects',
        type_='foreignkey'
    )
    op.drop_column(u'Projects', 'client_id')

    op.execute("""
    ALTER TABLE "Scenes" DROP CONSTRAINT IF EXISTS "Scenes_project_id_fkey";
    ALTER TABLE public."Scenes"
      ADD CONSTRAINT "Scenes_project_id_fkey" FOREIGN KEY (project_id)
          REFERENCES public."Projects" (id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE NO ACTION;
    """)

    op.execute("""
    ALTER TABLE "SimpleEntities" DROP CONSTRAINT IF EXISTS xu;
    ALTER TABLE "SimpleEntities"
      ADD CONSTRAINT xu FOREIGN KEY (updated_by_id)
          REFERENCES public."Users" (id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE NO ACTION;
    """)

    op.execute("""
    ALTER TABLE "SimpleEntities" DROP CONSTRAINT IF EXISTS z;
    ALTER TABLE public."SimpleEntities"
      ADD CONSTRAINT z FOREIGN KEY (thumbnail_id)
          REFERENCES public."Links" (id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE NO ACTION;
    """)

    op.execute("""
    ALTER TABLE "SimpleEntities" DROP CONSTRAINT IF EXISTS y;
    ALTER TABLE public."SimpleEntities"
      ADD CONSTRAINT y FOREIGN KEY (type_id)
          REFERENCES public."Types" (id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE NO ACTION;
    """)

    op.execute("""
    ALTER TABLE "Studios" DROP CONSTRAINT IF EXISTS "Studios_last_scheduled_by_id_fkey";
    ALTER TABLE "Studios"
      ADD CONSTRAINT "Studios_last_scheduled_by_id_fkey" FOREIGN KEY (last_scheduled_by_id)
          REFERENCES public."Users" (id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE NO ACTION;
    """)

    op.execute("""
    ALTER TABLE "Studios" DROP CONSTRAINT IF EXISTS "Studios_is_scheduling_by_id_fkey";
    ALTER TABLE "Studios"
      ADD CONSTRAINT "Studios_is_scheduling_by_id_fkey" FOREIGN KEY (is_scheduling_by_id)
          REFERENCES public."Users" (id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE NO ACTION;
    """)

    op.alter_column(
        u'Task_Dependencies',
        'gap_timing',
        existing_type=postgresql.DOUBLE_PRECISION(precision=53),
        nullable=True
    )

    op.alter_column(
        u'Task_Dependencies',
        'gap_unit',
        existing_type=postgresql.VARCHAR(length=256),
        nullable=True
    )

    op.execute("""
    ALTER TABLE "Tasks" DROP CONSTRAINT IF EXISTS "Tasks_good_id_fkey";
    ALTER TABLE public."Tasks"
      ADD CONSTRAINT "Tasks_good_id_fkey" FOREIGN KEY (good_id)
          REFERENCES public."Goods" (id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE NO ACTION;
    """)


def downgrade():
    op.execute('ALTER TABLE "Tasks" DROP CONSTRAINT "Tasks_good_id_fkey"')
    op.alter_column(
        u'Task_Dependencies',
        'gap_unit',
        existing_type=postgresql.VARCHAR(length=256),
        nullable=True
    )
    op.alter_column(
        u'Task_Dependencies',
        'gap_timing',
        existing_type=postgresql.DOUBLE_PRECISION(precision=53),
        nullable=True
    )

    op.add_column(
        u'Projects',
        sa.Column(
            'client_id',
            sa.INTEGER(),
            autoincrement=False,
            nullable=True
        )
    )
    op.create_foreign_key(
        u'Projects_client_id_fkey',
        'Projects',
        'Clients',
        ['client_id'],
        ['id']
    )

    # before dropping the Project_Clients, add the first client as the
    # Project.client_id
    op.execute(
        """
        update "Projects"
          set client_id = (
            select
              client_id
            from "Project_Clients"
            where project_id = "Projects".id limit 1
          )
        """
    )

    op.drop_table('Project_Clients')
