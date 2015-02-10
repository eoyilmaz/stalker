"""Added position column to Project_Repositories table

Revision ID: eaed49db6d9
Revises: 583875229230
Create Date: 2015-02-10 16:08:03.449570

"""

# revision identifiers, used by Alembic.
revision = 'eaed49db6d9'
down_revision = '583875229230'

from alembic import op
import sqlalchemy as sa


def upgrade():
    with op.batch_alter_table('Project_Repositories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('position', sa.Integer(), nullable=True))
        batch_op.add_column(
            sa.Column('repository_id', sa.Integer(), nullable=False))
        batch_op.drop_column('repo_id')


def downgrade():
    with op.batch_alter_table('Project_Repositories', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('repo_id', sa.INTEGER(), autoincrement=False,
                      nullable=False))
        batch_op.drop_column('repository_id')
        batch_op.drop_column('position')
