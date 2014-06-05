"""derive Version from Link instead of Entity

Revision ID: 25b3eba6ffe7
Revises: 53d8127d8560
Create Date: 2013-05-22 16:51:53.136718

"""

# revision identifiers, used by Alembic.
revision = '25b3eba6ffe7'
down_revision = '53d8127d8560'

from alembic import op
import sqlalchemy as sa

from stalker import defaults

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def upgrade():
    try:
        op.drop_column('Versions', 'source_file_id')
    except (sa.exc.OperationalError, sa.exc.InternalError):
        # SQLite doesnt support it
        pass

    try:
        op.create_foreign_key(None, "Versions", "Links", ["id"], ["id"])
        #FOREIGN KEY ( id ) REFERENCES Entities ( id ) DEFERRABLE INITIALLY DEFERRED
        #FOREIGN KEY ( id ) REFERENCES Links ( id ) DEFERRABLE INITIALLY DEFERRED
    except NotImplementedError:
        # there is no way to create the foreign key in SQLite
        # and it is incredibly hard to upgrade it
        # so I opt to skip this part for SQLite and loose data

        # so create a new table with the name Versions_New and create columns
        # The DDL of the new table
        # + id INTEGER PRIMARY KEY NOT NULL,
        # + version_of_id INTEGER NOT NULL,
        # + take_name TEXT,
        # + version_number INTEGER NOT NULL,
        # + parent_id INTEGER,
        # + is_published TEXT,
        # + status_id INTEGER NOT NULL,
        # + status_list_id INTEGER NOT NULL,
        # + FOREIGN KEY ( status_list_id ) REFERENCES StatusLists ( id ) DEFERRABLE INITIALLY DEFERRED,
        # + FOREIGN KEY ( status_id ) REFERENCES Statuses ( id ) DEFERRABLE INITIALLY DEFERRED,
        # + FOREIGN KEY ( parent_id ) REFERENCES Versions ( id ) DEFERRABLE INITIALLY DEFERRED,
        # + FOREIGN KEY ( version_of_id ) REFERENCES Tasks ( id ) DEFERRABLE INITIALLY DEFERRED,
        # + FOREIGN KEY ( id ) REFERENCES Links ( id ) DEFERRABLE INITIALLY DEFERRED

        op.create_table(
            'Versions_New',
            sa.Column('id', sa.Integer, sa.ForeignKey('Links.id'), primary_key=True),
            sa.Column('version_of_id', sa.Integer, sa.ForeignKey('Tasks.id'), nullable=False),
            sa.Column('take_name', sa.String(256), default=defaults.version_take_name),
            sa.Column('version_number', sa.Integer, default=1, nullable=False),
            sa.Column('parent_id', sa.Integer, sa.ForeignKey('Versions.id')),
            sa.Column('is_published', sa.Boolean, default=False),
            sa.Column('status_id', sa.Integer, sa.ForeignKey('Statuses.id'), nullable=False),
            sa.Column('status_list_id', sa.Integer, sa.ForeignKey('StatusLists.id'), nullable=False)
        )

        # *********************************************************************
        # SKIP THIS PART
        # then copy the data from the original table to the new table
        # s = sa.sql.select(['Versions', 'Links']).where('Versions.c.source_link_id == Links.c.id')
        # result = op.execute(s)
        # 
        # if result:
        #     data = []
        #     for row in result:
        #        # get the source Link
        #        # data.append()
        # *********************************************************************

        # and then delete the original table
        op.drop_table('Versions')
        # and rename the new table to the old one
        op.rename_table('Versions_New', 'Versions')


def downgrade():
    op.add_column(
        'Versions', sa.Column('source_file_id', sa.INTEGER(), nullable=True)
    )
    op.create_foreign_key(None, "Versions", "Entities", ["id"], ["id"])

