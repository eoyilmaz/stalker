"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision}
Create Date: ${create_date}
"""

from alembic import op

import sqlalchemy as sa

${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}


def upgrade():
    """Upgrade the tables."""
    ${upgrades if upgrades else "pass"}


def downgrade():
    """Downgrade the tables."""
    ${downgrades if downgrades else "pass"}
