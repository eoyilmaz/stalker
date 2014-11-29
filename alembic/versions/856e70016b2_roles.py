"""added Roles

Revision ID: 856e70016b2
Revises: 30c576f3691
Create Date: 2014-11-26 00:25:29.543411

"""

# revision identifiers, used by Alembic.
revision = '856e70016b2'
down_revision = '30c576f3691'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'Roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['Entities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'Client_Users',
        sa.Column('uid', sa.Integer(), nullable=False),
        sa.Column('cid', sa.Integer(), nullable=False),
        sa.Column('rid', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['cid'], ['Clients.id'], ),
        sa.ForeignKeyConstraint(['rid'], ['Roles.id'], ),
        sa.ForeignKeyConstraint(['uid'], ['Users.id'], ),
        sa.PrimaryKeyConstraint('uid', 'cid')
    )

    #
    # read Users.client_id and create Client_Users entries accordingly
    #

    op.rename_table('User_Groups', 'Group_Users')
    op.rename_table('User_Departments', 'Department_Users')

    op.add_column(
        u'Department_Users',
        sa.Column('rid', sa.Integer(), nullable=True)
    )
    op.add_column(
        u'Project_Users',
        sa.Column('rid', sa.Integer(), nullable=True)
    )

    op.drop_column(u'Departments', 'lead_id')
    op.drop_column(u'Projects', 'lead_id')
    op.drop_column(u'Users', 'company_id')


def downgrade():
    op.add_column(
        u'Projects',
        sa.Column('lead_id', sa.INTEGER(), nullable=True)
    )
    op.add_column(
        u'Departments',
        sa.Column('lead_id', sa.INTEGER(), nullable=True)
    )

    op.drop_column(u'Project_Users', 'rid')
    op.drop_column(u'Department_Users', 'rid')

    op.rename_table('Department_Users', 'User_Departments')
    op.rename_table('Group_Users', 'User_Groups')

    op.add_column(
        u'Users',
        sa.Column('company_id', sa.INTEGER(), nullable=True)
    )

    op.drop_table('Client_Users')

    op.drop_table('Roles')
