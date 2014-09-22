"""Added Shot.source_in, Shot.source_out and Shot.record_in attributes

Revision ID: 5814290f49c7
Revises: 2e4a3813ae76
Create Date: 2014-09-22 15:25:29.618377

"""

# revision identifiers, used by Alembic.
revision = '5814290f49c7'
down_revision = '2e4a3813ae76'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'Shots',
        sa.Column('record_in', sa.Integer(), nullable=True)
    )
    op.add_column(
        'Shots',
        sa.Column('source_in', sa.Integer(), nullable=True)
    )
    op.add_column(
        'Shots',
        sa.Column('source_out', sa.Integer(), nullable=True)
    )


def downgrade():
    op.drop_column('Shots', 'source_out')
    op.drop_column('Shots', 'source_in')
    op.drop_column('Shots', 'record_in')
