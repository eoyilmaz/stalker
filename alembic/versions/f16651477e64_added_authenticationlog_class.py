"""Added AuthenticationLog class

Revision ID: f16651477e64
Revises: 255ee1f9c7b3
Create Date: 2016-11-15 00:22:16.438000

"""

# revision identifiers, used by Alembic.
revision = "f16651477e64"
down_revision = "255ee1f9c7b3"

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table(
        "AuthenticationLogs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uid", sa.Integer(), nullable=False),
        sa.Column(
            "action",
            sa.Enum("login", "logout", name="AuthenticationActions"),
            nullable=False,
        ),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["SimpleEntities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["uid"],
            ["Users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_column("Users", "last_login")


def downgrade():
    op.add_column(
        "Users",
        sa.Column(
            "last_login", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
    )
    op.drop_table("AuthenticationLogs")
