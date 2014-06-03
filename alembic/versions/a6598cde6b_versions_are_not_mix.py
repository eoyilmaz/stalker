"""Versions are not mixed with StatusMixin anymore

Revision ID: a6598cde6b
Revises: 275bdc106fd5
Create Date: 2013-10-25 17:35:42.953516

"""

# revision identifiers, used by Alembic.
revision = 'a6598cde6b'
down_revision = '275bdc106fd5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('Versions', 'status_list_id')
    op.drop_column('Versions', 'status_id')


def downgrade():
    op.add_column(
        'Versions', sa.Column('status_id', sa.INTEGER(), nullable=False)
    )
    op.add_column(
        'Versions', sa.Column('status_list_id', sa.INTEGER(), nullable=False)
    )
