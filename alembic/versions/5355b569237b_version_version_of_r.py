"""Version.version_of renamed to Version.task

Revision ID: 5355b569237b
Revises: 6297277da38
Create Date: 2013-06-10 11:47:28.984222

"""

# revision identifiers, used by Alembic.
revision = '5355b569237b'
down_revision = '6297277da38'

from alembic import op
import sqlalchemy as sa


def upgrade():
    try:
        op.alter_column('Versions', 'version_of_id', new_column_name='task_id')
    except sa.exc.OperationalError:
        # SQLite3
        # just create the new column
        # and copy data
        op.add_column(
            'Versions',
            'task_id',
            sa.Column(sa.Integer, sa.ForeignKey("Tasks.id"), nullable=False)
        )
        # copy data from Links.path to Links_Temp.full_path
        op.execute(
            'INSERT INTO "Versions".task_id '
            'SELECT "Versions".version_of_id '
            'FROM "Versions"'
        )

def downgrade():
    try:
        op.alter_column('Versions', 'task_id', new_column_name='version_of_id')
    except sa.exc.OperationalError:
        # SQLite3
        # just create the new column
        # and copy data
        op.add_column(
            'Versions',
            'version_of_id',
            sa.Column(sa.Integer, sa.ForeignKey("Tasks.id"), nullable=False)
        )
        op.execute(
            'INSERT INTO "Versions".version_of_id '
            'SELECT "Versions".task_id '
            'FROM "Versions"'
        )
