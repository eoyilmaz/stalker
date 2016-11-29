"""updated version_inputs table

Revision ID: 0063f547dc2e
Revises: a9319b19f7be
Create Date: 2016-11-29 14:08:41.335000

"""

# revision identifiers, used by Alembic.
revision = '0063f547dc2e'
down_revision = 'a9319b19f7be'

from alembic import op


def upgrade():
    op.drop_constraint(u'Version_Inputs_link_id_fkey', 'Version_Inputs', type_='foreignkey')
    op.create_foreign_key(None, 'Version_Inputs', 'Links', ['link_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')


def downgrade():
    op.drop_constraint(None, 'Version_Inputs', type_='foreignkey')
    op.create_foreign_key(u'Version_Inputs_link_id_fkey', 'Version_Inputs', 'Links', ['link_id'], ['id'])
