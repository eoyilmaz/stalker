"""Added Version.created_with

Revision ID: 59092d41175c
Revises: 5355b569237b
Create Date: 2013-06-19 15:31:53.547392

"""

# revision identifiers, used by Alembic.
revision = '59092d41175c'
down_revision = '5355b569237b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    try:
        op.add_column('Versions', sa.Column('created_with', sa.String(length=256), nullable=True))
    except sa.exc.OperationalError:
        pass

def downgrade():
    try:
        op.drop_column('Versions', 'created_with')
    except sa.exc.OperationalError:
        pass
