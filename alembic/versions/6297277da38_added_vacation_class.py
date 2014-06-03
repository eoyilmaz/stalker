"""Added Vacation class

Revision ID: 6297277da38
Revises: 21b88ed3da95
Create Date: 2013-06-07 16:03:08.412610

"""

# revision identifiers, used by Alembic.
revision = '6297277da38'
down_revision = '21b88ed3da95'

from alembic import op
import sqlalchemy as sa


def upgrade():
    try:
        op.drop_table('User_Vacations')
    except sa.exc.OperationalError:
        pass


def downgrade():
    op.create_table(
        'User_Vacations',
        sa.Column('user_id', sa.INTEGER(), autoincrement=False,
                  nullable=False),
        sa.Column('vacation_id', sa.INTEGER(),
                  autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['Users.id'],
                                name='User_Vacations_user_id_fkey'),
        sa.ForeignKeyConstraint(['vacation_id'], ['Vacations.id'],
                                name='User_Vacations_vacation_id_fkey'),
        sa.PrimaryKeyConstraint('user_id', 'vacation_id',
                                name='User_Vacations_pkey')
    )
