"""added Users.company and Projects.client columns and a new Clients table

Revision ID: 182f44ce5f07
Revises: 59bfe820c369
Create Date: 2014-05-29 11:33:02.313000

"""

# revision identifiers, used by Alembic.
revision = '182f44ce5f07'
down_revision = '59bfe820c369'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Create Clients table
    op.create_table('Clients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['Entities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Users table
    op.add_column(
        'Users',
        sa.Column('company_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        name=None,
        source='Users',
        referent='Clients',
        local_cols=['company_id'],
        remote_cols=['id']
    )

    # Projects table
    op.add_column(
        'Projects',
        sa.Column('client_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        name=None,
        source='Projects',
        referent='Clients',
        local_cols=['client_id'],
        remote_cols=['id']
    )


def downgrade():
    op.drop_column('Users', 'company_id')
    op.drop_column('Projects', 'client_id')
    op.drop_table('Clients')
