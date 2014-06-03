"""remove Statuses.bg_color and Statuses.fg_color columns

Revision ID: 2aeab8b376dc
Revises: 5168cc8552a3
Create Date: 2013-11-18 23:44:49.428028

"""

# revision identifiers, used by Alembic.
revision = '2aeab8b376dc'
down_revision = '5168cc8552a3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('Statuses', 'bg_color')
    op.drop_column('Statuses', 'fg_color')


def downgrade():
    op.add_column(
        'Statuses', sa.Column('fg_color', sa.INTEGER(), nullable=True)
    )
    op.add_column(
        'Statuses', sa.Column('bg_color', sa.INTEGER(), nullable=True)
    )
