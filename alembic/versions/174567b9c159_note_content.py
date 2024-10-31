"""'Note.content' is now a synonym of 'Note.description'.

Revision ID: 174567b9c159
Revises: a6598cde6b
Create Date: 2013-11-14 13:38:02.566201
"""
from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "174567b9c159"
down_revision = "a6598cde6b"


def upgrade():
    op.drop_column("Notes", "content")


def downgrade():
    op.add_column("Notes", sa.Column("content", sa.VARCHAR(), nullable=True))
