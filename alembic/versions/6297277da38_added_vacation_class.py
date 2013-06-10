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
        op.drop_table(u'User_Vacations')
    except sa.exc.OperationalError:
        pass


def downgrade():
    op.create_table(
        u'User_Vacations',
        sa.Column(u'user_id', sa.INTEGER(), autoincrement=False,
                  nullable=False),
        sa.Column(u'vacation_id', sa.INTEGER(),
                  autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], [u'Users.id'],
                                name=u'User_Vacations_user_id_fkey'),
        sa.ForeignKeyConstraint(['vacation_id'], [u'Vacations.id'],
                                name=u'User_Vacations_vacation_id_fkey'),
        sa.PrimaryKeyConstraint(u'user_id', u'vacation_id',
                                name=u'User_Vacations_pkey')
    )
