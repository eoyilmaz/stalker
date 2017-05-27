"""Added WorkingHours table

Revision ID: ed0167fff399
Revises: 1181305d3001
Create Date: 2017-05-20 14:32:48.388000

"""

# revision identifiers, used by Alembic.
revision = 'ed0167fff399'
down_revision = '1181305d3001'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table(
        'WorkingHours',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('working_hours', sa.JSON(), nullable=True),
        sa.Column('daily_working_hours', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['id'], ['Entities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.add_column(
        'Studios',
        sa.Column('working_hours_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        None, 'Studios', 'WorkingHours', ['working_hours_id'], ['id']
    )
    op.drop_column('Studios', 'working_hours')
    op.alter_column('Studios', 'last_schedule_message', type_=sa.Text)

    # warn the user to recreate the working hours
    # because of the nature of Pickle it is very hard to do it here
    print("Warning! Can not keep WorkingHours data of Studios.")
    print("Please, recreate the WorkingHours for all Studio instances!")


def downgrade():
    op.add_column(
        'Studios',
        sa.Column(
            'working_hours',
            postgresql.BYTEA(),
            autoincrement=False,
            nullable=True
        )
    )
    op.drop_constraint(
        'Studios_working_hours_id_fkey', 'Studios', type_='foreignkey'
    )
    op.drop_column('Studios', 'working_hours_id')
    op.drop_table('WorkingHours')
    op.execute(
        'ALTER TABLE "Studios"'
        'ALTER COLUMN last_schedule_message TYPE BYTEA '
        'USING last_schedule_message::bytea'
    )
    print("Warning! Can not keep WorkingHours instances.")
    print("Please, recreate the WorkingHours for all Studio instances!")
