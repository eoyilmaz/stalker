"""Added "shot.fps".

Revision ID: a9319b19f7be
Revises: f16651477e64
Create Date: 2016-11-29 13:38:22.380000
"""
from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "a9319b19f7be"
down_revision = "f16651477e64"


def upgrade():
    op.add_column("Shots", sa.Column("fps", sa.Float(precision=3), nullable=True))


def downgrade():
    op.drop_column("Shots", "fps")
