"""Added ReferenceMixin to Task

Revision ID: 21b88ed3da95
Revises: 4664d72ce1e1
Create Date: 2013-05-31 12:08:59.425539

"""

# revision identifiers, used by Alembic.
revision = '21b88ed3da95'
down_revision = '4664d72ce1e1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    try:
        op.create_table(
            'Task_References',
            sa.Column('task_id', sa.Integer(), nullable=False),
            sa.Column('link_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['link_id'], ['Links.id'], ),
            sa.ForeignKeyConstraint(['task_id'], ['Tasks.id'], ),
            sa.PrimaryKeyConstraint('task_id', 'link_id')
        )
    except sa.exc.OperationalError:
        pass

    op.drop_table('Asset_References')
    op.drop_table('Shot_References')
    op.drop_table('Sequence_References')


def downgrade():
    op.create_table(
        'Sequence_References',
        sa.Column(
            'sequence_id', sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            'link_id', sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ['link_id'], ['Links.id'],
            name='Sequence_References_link_id_fkey'),
        sa.ForeignKeyConstraint(
            ['sequence_id'], ['Sequences.id'],
            name='Sequence_References_sequence_id_fkey'
        ),
        sa.PrimaryKeyConstraint(
            'sequence_id', 'link_id', name='Sequence_References_pkey'
        )
    )
    op.create_table('Shot_References',
                    sa.Column('shot_id', sa.INTEGER(), autoincrement=False,
                              nullable=False),
                    sa.Column('link_id', sa.INTEGER(), autoincrement=False,
                              nullable=False),
                    sa.ForeignKeyConstraint(['link_id'], ['Links.id'],
                                            name='Shot_References_link_id_fkey'),
                    sa.ForeignKeyConstraint(['shot_id'], ['Shots.id'],
                                            name='Shot_References_shot_id_fkey'),
                    sa.PrimaryKeyConstraint('shot_id', 'link_id',
                                            name='Shot_References_pkey')
    )
    op.create_table('Asset_References',
                    sa.Column('asset_id', sa.INTEGER(), autoincrement=False,
                              nullable=False),
                    sa.Column('link_id', sa.INTEGER(), autoincrement=False,
                              nullable=False),
                    sa.ForeignKeyConstraint(['asset_id'], ['Assets.id'],
                                            name='Asset_References_asset_id_fkey'),
                    sa.ForeignKeyConstraint(['link_id'], ['Links.id'],
                                            name='Asset_References_link_id_fkey'),
                    sa.PrimaryKeyConstraint('asset_id', 'link_id',
                                            name='Asset_References_pkey')
    )
    op.drop_table('Task_References')
