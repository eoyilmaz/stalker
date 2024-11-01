"""Renamed OSX to macOS

Revision ID: feca9bac7d5a
Revises: bf67e6a234b4
Create Date: 2024-11-01 12:22:24.818481
"""

from alembic import op

import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = 'feca9bac7d5a'
down_revision = 'bf67e6a234b4'


def upgrade():
    """Upgrade the tables."""
    op.alter_column("Repositories", "osx_path", new_column_name="macos_path")


def downgrade():
    """Downgrade the tables."""
    op.alter_column("Repositories", "macos_path", new_column_name="osx_path")
