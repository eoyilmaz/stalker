"""Added generic_text attribute on SimpleEntity

Revision ID: 5999269aad30
Revises: 182f44ce5f07
Create Date: 2014-06-02 15:17:27.961000

"""

# revision identifiers, used by Alembic.
revision = '5999269aad30'
down_revision = '182f44ce5f07'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'SimpleEntities',
        sa.Column('generic_text', sa.Text())
    )


def downgrade():
    op.drop_column('SimpleEntities', 'generic_text')
