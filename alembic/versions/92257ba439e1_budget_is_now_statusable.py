"""empty message

Revision ID: 92257ba439e1
Revises: f2005d1fbadc
Create Date: 2016-07-28 13:20:27.397000

"""

# revision identifiers, used by Alembic.
revision = '92257ba439e1'
down_revision = 'f2005d1fbadc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'Budgets',
        sa.Column('status_id', sa.Integer(), nullable=False)
    )
    op.add_column(
        'Budgets',
        sa.Column('status_list_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        None, 'Budgets', 'Statuses', ['status_id'], ['id']
    )
    op.create_foreign_key(
        None, 'Budgets', 'StatusLists', ['status_list_id'], ['id']
    )


def downgrade():
    op.drop_constraint(None, 'Budgets', type_='foreignkey')
    op.drop_constraint(None, 'Budgets', type_='foreignkey')
    op.drop_column('Budgets', 'status_list_id')
    op.drop_column('Budgets', 'status_id')
