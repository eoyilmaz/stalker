"""Added Tasks.good_id column

Revision ID: 583875229230
Revises: 2252e51506de
Create Date: 2015-02-07 18:53:04.343928

"""

# revision identifiers, used by Alembic.
revision = '583875229230'
down_revision = '2252e51506de'

from alembic import op
import sqlalchemy as sa


def upgrade():
    with op.batch_alter_table('Tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('good_id', sa.Integer(), nullable=True))


def downgrade():
    with op.batch_alter_table('Tasks', schema=None) as batch_op:
        batch_op.drop_column('good_id')
