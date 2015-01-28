"""Multiple Repositories per Project

Revision ID: 2252e51506de
Revises: 1c9c9c28c102
Create Date: 2015-01-28 00:46:29.139946

"""

# revision identifiers, used by Alembic.
revision = '2252e51506de'
down_revision = '1c9c9c28c102'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'Project_Repositories',
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('repo_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['Projects.id']),
        sa.ForeignKeyConstraint(['repo_id'], ['Repositories.id']),
                    sa.PrimaryKeyConstraint('project_id', 'repo_id')
    )

    # before dropping repository column, carry all the data to the new table
    op.execute(
        'insert into "Project_Repositories"'
        '   select id, repository_id '
        '   from "Projects"'
    )

    with op.batch_alter_table('Projects', schema=None) as batch_op:
        batch_op.drop_column('repository_id')


def downgrade():
    with op.batch_alter_table('Projects', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('repository_id', sa.INTEGER(), autoincrement=False,
                      nullable=True))

    # before dropping Project_Repositories, carry all the data back,
    # note that only the first repository found per project will be
    # restored to the Project.repository_id column
    op.execute(
        'update "Projects" '
        '    set repository_id = ('
        '        select '
        '            repo_id'
        '        from "Project_Repositories" '
        '        where project_id = "Projects".id limit 1'
        '    )'
    )

    op.drop_table('Project_Repositories')
