"""create EntityType.accepts_references

Revision ID: 4a836cf73bcf
Revises: None
Create Date: 2013-05-15 16:27:05.983849

"""

# revision identifiers, used by Alembic.
revision = '4a836cf73bcf'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    try:
        op.add_column('EntityTypes', sa.Column('accepts_references', sa.Boolean))
    except (sa.exc.OperationalError, sa.exc.ProgrammingError):
        # the column already exists
        pass

    try:
        op.add_column('Links', sa.Column('original_filename', sa.String(256)))
    except (sa.exc.OperationalError, sa.exc.ProgrammingError, sa.exc.InternalError):
        # the column already exists
        pass


def downgrade():
    # no drop column in SQLite so this will not work for SQLite databases
    op.drop_column('EntityTypes', 'accepts_references')
    op.drop_column('Links', 'original_filename')
