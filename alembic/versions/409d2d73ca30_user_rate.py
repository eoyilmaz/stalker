"""added Users.rate

Revision ID: 409d2d73ca30
Revises: 5814290f49c7
Create Date: 2014-11-20 22:47:56.013644

"""

# revision identifiers, used by Alembic.
revision = '409d2d73ca30'
down_revision = '5814290f49c7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'Users', sa.Column('rate', sa.Float(), nullable=True)
    )


def downgrade():
    op.drop_column('Users', 'rate')
