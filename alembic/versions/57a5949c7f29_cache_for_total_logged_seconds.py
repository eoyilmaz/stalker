"""Created cache columns for total_logged_seconds and schedule_seconds
attributes

Revision ID: 57a5949c7f29
Revises: 101a789e38ad
Create Date: 2013-07-31 16:57:17.674995
"""

# revision identifiers, used by Alembic.
revision = '57a5949c7f29'
down_revision = '101a789e38ad'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('Tasks', sa.Column('_schedule_seconds', sa.Integer(), nullable=True))
    op.add_column('Tasks', sa.Column('_total_logged_seconds', sa.Integer(), nullable=True))

def downgrade():
    op.drop_column('Tasks', '_total_logged_seconds')
    op.drop_column('Tasks', '_schedule_seconds')
