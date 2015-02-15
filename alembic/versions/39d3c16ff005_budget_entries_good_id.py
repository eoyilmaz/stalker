"""Added BudgetEntries.good_id

Revision ID: 39d3c16ff005
Revises: eaed49db6d9
Create Date: 2015-02-15 02:29:26.301437

"""

# revision identifiers, used by Alembic.
revision = '39d3c16ff005'
down_revision = 'eaed49db6d9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    with op.batch_alter_table('BudgetEntries', schema=None) as batch_op:
        batch_op.add_column(sa.Column('good_id', sa.Integer(), nullable=True))


def downgrade():
    with op.batch_alter_table('BudgetEntries', schema=None) as batch_op:
        batch_op.drop_column('good_id')
