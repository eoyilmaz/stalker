"""Added Project_Users.rate

Revision ID: d8421de6a206
Revises: 92257ba439e1
Create Date: 2016-08-17 19:27:00.358000

"""

# revision identifiers, used by Alembic.
revision = "d8421de6a206"
down_revision = "92257ba439e1"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("Project_Users", sa.Column("rate", sa.Float(), nullable=True))


def downgrade():
    op.execute(
        """
      ALTER TABLE public."Project_Users" DROP COLUMN IF EXISTS rate;
    """
    )
