"""Added position column to Project_Repositories table.

Revision ID: eaed49db6d9
Revises: 583875229230
Create Date: 2015-02-10 16:08:03.449570
"""

from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "eaed49db6d9"
down_revision = "583875229230"


def upgrade():
    """Upgrade the tables."""
    with op.batch_alter_table("Project_Repositories", schema=None) as batch_op:
        batch_op.add_column(sa.Column("position", sa.Integer(), nullable=True))
        batch_op.alter_column("repo_id", new_column_name="repository_id")

    # insert zeros as the position value
    op.execute(
        """update "Project_Repositories"
        set position=0
        """
    )


def downgrade():
    """Downgrade the tables."""
    with op.batch_alter_table("Project_Repositories", schema=None) as batch_op:
        batch_op.alter_column("repository_id", new_column_name="repo_id")
        batch_op.drop_column("position")
