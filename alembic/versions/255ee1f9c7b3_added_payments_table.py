"""Added Payments table

Revision ID: 255ee1f9c7b3
Revises: ea28a39ba3f5
Create Date: 2016-08-18 03:19:22.301000

"""

# revision identifiers, used by Alembic.
revision = "255ee1f9c7b3"
down_revision = "ea28a39ba3f5"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        "Payments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("invoice_id", sa.Integer(), nullable=True),
        sa.Column("amount", sa.Float(), nullable=True),
        sa.Column("unit", sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(
            ["id"],
            ["Entities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["invoice_id"],
            ["Invoices.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("Payments")
