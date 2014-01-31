"""create enum types

Revision ID: 46775e4a3d96
Revises: 2aeab8b376dc
Create Date: 2014-01-31 03:08:36.445876

"""

# revision identifiers, used by Alembic.

revision = '46775e4a3d96'
down_revision = '2aeab8b376dc'

from alembic import op


def upgrade():
    # remove unnecessary types
    op.execute('DROP TYPE IF EXISTS "TaskBidUnit" CASCADE;')

    # rename types
    op.execute('ALTER TYPE "TaskScheduleUnit" RENAME TO "TimeUnit";')

    # create new types
    op.execute("""
        CREATE TYPE "ResourceAllocationStrategy" AS ENUM
            ('minallocated', 'maxloaded', 'minloaded', 'order', 'random');
        CREATE TYPE "TaskDependencyGapModel" AS ENUM ('length', 'duration');
        CREATE TYPE "TaskDependencyTarget" AS ENUM ('onend', 'onstart');
        CREATE TYPE "ReviewScheduleModel"
            AS ENUM ('effort', 'length', 'duration');
    """)


def downgrade():
    # add necessary types
    op.execute(
        """CREATE TYPE "TaskBidUnit" AS ENUM
        ('min', 'h', 'd', 'w', 'm', 'y');
    """)

    # rename types
    op.execute('ALTER TYPE "TimeUnit" RENAME TO "TaskScheduleUnit";')

    # create new types
    op.execute("""
        DROP TYPE IF EXISTS "ResourceAllocationStrategy" CASCADE;
        DROP TYPE IF EXISTS "TaskDependencyGapModel" CASCADE;
        DROP TYPE IF EXISTS "TaskDependencyTarget" CASCADE;
        DROP TYPE IF EXISTS "ReviewScheduleModel" CASCADE;
    """)

