"""renamed Link.path to Link.full_path

Revision ID: 4664d72ce1e1
Revises: 25b3eba6ffe7
Create Date: 2013-05-23 18:46:18.218662

"""

# revision identifiers, used by Alembic.
revision = '4664d72ce1e1'
down_revision = '25b3eba6ffe7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # create full_path column
    try:
        op.alter_column('Links', 'path', new_column_name='full_path')
    except sa.exc.OperationalError:
        # SQLite3
        # create new table
        op.create_table(
            'Links_Temp',
            sa.Column('id', sa.Integer, sa.ForeignKey("Entities.id"),
                      primary_key=True),
            sa.Column('original_filename', sa.String(256), nullable=True),
            sa.Column('full_path', sa.String)
        )

        links_temp = sa.sql.table(
            'Links_Temp',
            sa.Column('id', sa.Integer, sa.ForeignKey("Entities.id"),
                      primary_key=True),
            sa.Column('original_filename', sa.String(256), nullable=True),
            sa.Column('full_path', sa.String)
        )

        links = sa.sql.table(
            'Links',
            sa.Column('id', sa.Integer, sa.ForeignKey("Entities.id"),
                      primary_key=True),
            sa.Column('original_filename', sa.String(256), nullable=True),
            sa.Column('path', sa.String),
        )

        # copy data from Links.path to Links_Temp.full_path
        op.execute(
            'INSERT INTO "Links_Temp" '
            'SELECT "Links".id, "Links".original_filename, "Links".path '
            'FROM "Links"'
        )

        # drop the Links table and rename Links_Temp to Links
        op.drop_table('Links')
        op.rename_table('Links_Temp', 'Links')


def downgrade():
    try:
       op.alter_column('Links', 'path', new_column_name='full_path')
    except sa.exc.OperationalError:
        # SQLite3
        # create new table
        op.create_table(
            'Links_Temp',
            sa.Column('id', sa.Integer, sa.ForeignKey("Entities.id"),
                      primary_key=True),
            sa.Column('original_filename', sa.String(256), nullable=True),
            sa.Column('path', sa.String)
        )

        links_temp = sa.sql.table(
            'Links_Temp',
            sa.Column('id', sa.Integer, sa.ForeignKey("Entities.id"),
                      primary_key=True),
            sa.Column('original_filename', sa.String(256), nullable=True),
            sa.Column('path', sa.String),
        )

        links = sa.sql.table(
            'Links',
            sa.Column('id', sa.Integer, sa.ForeignKey("Entities.id"),
                      primary_key=True),
            sa.Column('original_filename', sa.String(256), nullable=True),
            sa.Column('full_path', sa.String)
        )

        # copy data from Links.path to Links_Temp.full_path
        op.execute(
            'INSERT INTO "Links_Temp" '
            'SELECT "Links".id, "Links".original_filename, "Links".full_path '
            'FROM "Links"'
        )

        # drop the Links table and rename Links_Temp to Links
        op.drop_table('Links')
        op.rename_table('Links_Temp', 'Links')
