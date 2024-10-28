"""Added Invoices table.

Revision ID: ea28a39ba3f5
Revises: 92257ba439e1
Create Date: 2016-08-17 19:21:40.428000
"""
from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "ea28a39ba3f5"
down_revision = "d8421de6a206"


def upgrade():
    op.create_table(
        "Invoices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("budget_id", sa.Integer(), nullable=True),
        sa.Column("client_id", sa.Integer(), nullable=True),
        sa.Column("amount", sa.Float(), nullable=True),
        sa.Column("unit", sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(
            ["budget_id"],
            ["Budgets.id"],
        ),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["Clients.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["Entities.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("Invoices")
