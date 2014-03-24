"""add Wiki Page

Revision ID: 2f55dc4f199f
Revises: 433d9caaafab
Create Date: 2014-03-24 16:52:45.127579

"""

# revision identifiers, used by Alembic.
revision = '2f55dc4f199f'
down_revision = '433d9caaafab'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'Pages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['id'], ['Entities.id']),
        sa.ForeignKeyConstraint(
            ['project_id'], ['Projects.id'],
            name='project_x_id',
            use_alter=True
        ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('Pages')
