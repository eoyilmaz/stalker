"""removed Tasks.is_complete column

Revision ID: 23dff41c95ff
Revises: 5999269aad30
Create Date: 2014-06-11 14:00:00.559122

"""

# revision identifiers, used by Alembic.
revision = '23dff41c95ff'
down_revision = '5999269aad30'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('Tasks', 'is_complete')


def downgrade():
    op.add_column(
        'Tasks',
        sa.Column('is_complete', sa.BOOLEAN(), nullable=True)
    )
