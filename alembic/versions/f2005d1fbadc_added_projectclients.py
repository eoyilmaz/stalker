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

    # These were coming up in every revision, and I was cleaning them every
    # time, so I'm leaving them in this one now
    op.create_foreign_key(None, 'BudgetEntries', 'Goods', ['good_id'], ['id'])
    op.create_foreign_key(None, 'Budgets', 'Budgets', ['parent_id'], ['id'])
    op.create_foreign_key(None, 'Dailies', 'Projects', ['project_id'], ['id'])
    op.create_foreign_key(None, 'Department_Users', 'Roles', ['rid'], ['id'])
    op.create_foreign_key(None, 'Pages', 'Projects', ['project_id'], ['id'])
    op.create_foreign_key(None, 'Project_Users', 'Roles', ['rid'], ['id'])

    op.drop_constraint(
        u'Projects_client_id_fkey',
        'Projects',
        type_='foreignkey'
    )
    op.drop_column(u'Projects', 'client_id')

    op.create_foreign_key(None, 'Scenes', 'Projects', ['project_id'], ['id'])
    op.create_foreign_key(
        'xu',
        'SimpleEntities',
        'Users',
        ['updated_by_id'],
        ['id'],
        use_alter=True
    )
    op.create_foreign_key(
        'z',
        'SimpleEntities',
        'Links',
        ['thumbnail_id'],
        ['id'],
        use_alter=True
    )
    op.create_foreign_key(
        'y',
        'SimpleEntities',
        'Types',
        ['type_id'],
        ['id'],
        use_alter=True
    )
    op.create_foreign_key(
        None,
        'Studios',
        'Users',
        ['last_scheduled_by_id'],
        ['id']
    )
    op.create_foreign_key(
        None,
        'Studios',
        'Users',
        ['is_scheduling_by_id'],
        ['id']
    )
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
    op.create_foreign_key(
        None,
        'Tasks',
        'Goods',
        ['good_id'],
        ['id']
    )


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

    op.execute(
        'ALTER TABLE "Studios" '
        'DROP CONSTRAINT "Studios_is_scheduling_by_id_fkey"'
    )
    op.execute(
        'ALTER TABLE "Studios" '
        'DROP CONSTRAINT "Studios_last_scheduled_by_id_fkey"'
    )
    op.execute(
        'ALTER TABLE "SimpleEntities" DROP CONSTRAINT y'
    )
    op.execute(
        'ALTER TABLE "SimpleEntities" DROP CONSTRAINT z'
    )
    op.execute(
        'ALTER TABLE "SimpleEntities" DROP CONSTRAINT xu'
    )
    op.execute(
        'ALTER TABLE "Scenes" DROP CONSTRAINT "Scenes_project_id_fkey"'
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

    op.execute(
        'ALTER TABLE "Project_Users" DROP CONSTRAINT "Project_Users_rid_fkey"'
    )
    op.execute(
        'ALTER TABLE "Pages" DROP CONSTRAINT "Pages_project_id_fkey"'
    )
    op.execute(
        'ALTER TABLE "Department_Users" '
        'DROP CONSTRAINT "Department_Users_rid_fkey"'
    )
    op.execute(
        'ALTER TABLE "Dailies" DROP CONSTRAINT "Dailies_project_id_fkey"'
    )
    op.execute(
        'ALTER TABLE "Budgets" DROP CONSTRAINT "Budgets_parent_id_fkey"'
    )
    op.execute(
        'ALTER TABLE "BudgetEntries" '
        'DROP CONSTRAINT "BudgetEntries_good_id_fkey"'
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
