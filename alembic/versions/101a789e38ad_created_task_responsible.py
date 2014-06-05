"""Created Task.responsible attribute

Revision ID: 101a789e38ad
Revises: 59092d41175c
Create Date: 2013-06-24 12:32:04.852386

"""

# revision identifiers, used by Alembic.
revision = '101a789e38ad'
down_revision = '59092d41175c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    try:
        op.drop_column('Sequences', 'lead_id')
        op.add_column('Tasks',
                      sa.Column('responsible_id', sa.Integer(), nullable=True))
    except sa.exc.OperationalError:
        pass


def downgrade():
    try:
        op.drop_column('Tasks', 'responsible_id')
        op.add_column('Sequences',
                      sa.Column('lead_id', sa.INTEGER(), nullable=True))
    except sa.exc.OperationalError:
        pass
