"""add PriceLists and Goods

Revision ID: 1c9c9c28c102
Revises: 856e70016b2
Create Date: 2015-01-26 13:05:50.050345

"""

# revision identifiers, used by Alembic.
revision = '1c9c9c28c102'
down_revision = '856e70016b2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'PriceLists',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['Entities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'Goods',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cost', sa.Float(), nullable=True),
        sa.Column('msrp', sa.Float(), nullable=True),
        sa.Column('unit', sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(['id'], ['Entities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'PriceList_Goods',
        sa.Column('price_list_id', sa.Integer(), nullable=False),
        sa.Column('good_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['good_id'], ['Goods.id'], ),
        sa.ForeignKeyConstraint(['price_list_id'], ['PriceLists.id'], ),
        sa.PrimaryKeyConstraint('price_list_id', 'good_id')
    )
    with op.batch_alter_table('BudgetEntries', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cost', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('msrp', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('price', sa.Float(), nullable=True))
        batch_op.add_column(
            sa.Column('realized_total', sa.Float(), nullable=True))
        batch_op.add_column(
            sa.Column('unit', sa.String(length=64), nullable=True))

    with op.batch_alter_table('Budgets', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('parent_id', sa.Integer(), nullable=True))


def downgrade():
    with op.batch_alter_table('Budgets', schema=None) as batch_op:
        batch_op.drop_column('parent_id')

    with op.batch_alter_table('BudgetEntries', schema=None) as batch_op:
        batch_op.drop_column('unit')
        batch_op.drop_column('realized_total')
        batch_op.drop_column('price')
        batch_op.drop_column('msrp')
        batch_op.drop_column('cost')

    op.drop_table('PriceList_Goods')
    op.drop_table('Goods')
    op.drop_table('PriceLists')
