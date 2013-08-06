"""Added Ticket.summary

Revision ID: 275bdc106fd5
Revises: 130a7697cd79
Create Date: 2013-08-07 00:19:39.414232

"""

# revision identifiers, used by Alembic.
revision = '275bdc106fd5'
down_revision = '130a7697cd79'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('Tickets', sa.Column('summary', sa.String(), nullable=True))

def downgrade():
    op.drop_column('Tickets', 'summary')
