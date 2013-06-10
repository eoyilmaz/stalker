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

    op.drop_table(u'Asset_References')
    op.drop_table(u'Shot_References')
    op.drop_table(u'Sequence_References')

def downgrade():
    op.create_table(u'Sequence_References',
        sa.Column(u'sequence_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(u'link_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['link_id'], [u'Links.id'], name=u'Sequence_References_link_id_fkey'),
        sa.ForeignKeyConstraint(['sequence_id'], [u'Sequences.id'], name=u'Sequence_References_sequence_id_fkey'),
        sa.PrimaryKeyConstraint(u'sequence_id', u'link_id', name=u'Sequence_References_pkey')
    )
    op.create_table(u'Shot_References',
        sa.Column(u'shot_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(u'link_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['link_id'], [u'Links.id'], name=u'Shot_References_link_id_fkey'),
        sa.ForeignKeyConstraint(['shot_id'], [u'Shots.id'], name=u'Shot_References_shot_id_fkey'),
        sa.PrimaryKeyConstraint(u'shot_id', u'link_id', name=u'Shot_References_pkey')
    )
    op.create_table(u'Asset_References',
        sa.Column(u'asset_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(u'link_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['asset_id'], [u'Assets.id'], name=u'Asset_References_asset_id_fkey'),
        sa.ForeignKeyConstraint(['link_id'], [u'Links.id'], name=u'Asset_References_link_id_fkey'),
        sa.PrimaryKeyConstraint(u'asset_id', u'link_id', name=u'Asset_References_pkey')
    )
    op.drop_table('Task_References')
