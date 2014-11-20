"""added Budget and BudgetEntry tables

Revision ID: 30c576f3691
Revises: 409d2d73ca30
Create Date: 2014-11-20 22:49:37.015323

"""

# revision identifiers, used by Alembic.
revision = '30c576f3691'
down_revision = '409d2d73ca30'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'Budgets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['id'], ['Entities.id'], ),
        sa.ForeignKeyConstraint(['project_id'], ['Projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'BudgetEntries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('budget_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['budget_id'], ['Budgets.id'], ),
        sa.ForeignKeyConstraint(['id'], ['Entities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('BudgetEntries')
    op.drop_table('Budgets')
