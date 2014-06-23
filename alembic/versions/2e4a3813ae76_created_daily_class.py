"""created Daily class and the "Daily Statuses" status list and the status Open

Revision ID: 2e4a3813ae76
Revises: 23dff41c95ff
Create Date: 2014-06-23 17:14:33.013543

"""

# revision identifiers, used by Alembic.
import stalker

revision = '2e4a3813ae76'
down_revision = '23dff41c95ff'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'Dailies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('status_id', sa.Integer(), nullable=False),
        sa.Column('status_list_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['id'], ['Entities.id'], ),
        sa.ForeignKeyConstraint(
            ['project_id'], ['Projects.id'], name='project_x_id',
            use_alter=True
        ),
        sa.ForeignKeyConstraint(['status_id'], ['Statuses.id'], ),
        sa.ForeignKeyConstraint(['status_list_id'], ['StatusLists.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'Daily_Links',
        sa.Column('daily_id', sa.Integer(), nullable=False),
        sa.Column('link_id', sa.Integer(), nullable=False),
        sa.Column('rank', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['daily_id'], ['Dailies.id'], ),
        sa.ForeignKeyConstraint(['link_id'], ['Links.id'], ),
        sa.PrimaryKeyConstraint('daily_id', 'link_id')
    )

    # create new Statuses
    #
    # 'Open', 'OPEN',

    def create_status(name, code):
        # Insert in to SimpleEntities
        op.execute(
            """INSERT INTO "SimpleEntities" (entity_type, name, description,
created_by_id, updated_by_id, date_created, date_updated, type_id,
thumbnail_id, html_style, html_class, stalker_version)
VALUES ('Status', '%(name)s', '', NULL, NULL,
(SELECT CAST(NOW() at time zone 'utc' AS timestamp)), (SELECT CAST(NOW() at time zone 'utc' AS timestamp)), NULL, NULL,
'', '', '%(stalker_version)s')""" %
            {
                'stalker_version': stalker.__version__,
                'name': name
            }
        )

        # insert in to Entities and Statuses
        op.execute(
            """INSERT INTO "Entities" (id)
            VALUES ((
              SELECT id
              FROM "SimpleEntities"
              WHERE "SimpleEntities".name = '%(name)s'
            ));
            INSERT INTO "Statuses" (id, code)
            VALUES ((
              SELECT id
              FROM "SimpleEntities"
              WHERE "SimpleEntities".name = '%(name)s'), '%(code)s');""" %
            {
                'name': name,
                'code': code
            }
        )

    create_status('Open', 'OPEN')

    # Create Review StatusList
    # Insert in to SimpleEntities
    op.execute(
        """INSERT INTO "SimpleEntities" (entity_type, name, description,
created_by_id, updated_by_id, date_created, date_updated, type_id,
thumbnail_id, html_style, html_class, stalker_version)
VALUES ('StatusList', 'Daily Statuses', '', NULL, NULL,
(SELECT CAST(NOW() at time zone 'utc' AS timestamp)),
(SELECT CAST(NOW() at time zone 'utc' AS timestamp)), NULL, NULL,
'', '', '%(stalker_version)s')""" %{
            'stalker_version': stalker.__version__
        })

    # insert in to Entities and StatusLists
    op.execute(
        """INSERT INTO "Entities" (id)
VALUES ((
  SELECT id
  FROM "SimpleEntities"
  WHERE "SimpleEntities".name = 'Daily Statuses'
));
INSERT INTO "StatusLists" (id, target_entity_type)
VALUES ((
  SELECT id
  FROM "SimpleEntities"
  WHERE "SimpleEntities".name = 'Daily Statuses'), 'Daily');""")

    # Add Review Statues To StatusList_Statuses
    # Add new Task statuses to StatusList
    op.execute("""INSERT INTO "StatusList_Statuses" (status_list_id, status_id)
VALUES
    ((SELECT id FROM "StatusLists" WHERE target_entity_type = 'Daily'),
    (SELECT id FROM "Statuses" WHERE code = 'OPEN')),
    ((SELECT id FROM "StatusLists" WHERE target_entity_type = 'Daily'),
    (SELECT id FROM "Statuses" WHERE code = 'CLS'))
""")


def downgrade():
    op.drop_table('Daily_Links')
    op.drop_table('Dailies')

    # Delete Open Status
    op.execute("""DELETE FROM "StatusList_Statuses" WHERE
    status_id IN (
    select id FROM "SimpleEntities" WHERE
    name = 'Open');
    DELETE FROM "Statuses" WHERE
      id IN (select id FROM "SimpleEntities" WHERE
    name = 'Open');
    DELETE FROM "Entities" WHERE
    id IN (select id FROM "SimpleEntities" WHERE
    name = 'Open');
    DELETE FROM "SimpleEntities" WHERE
    name = 'Open';
    """)

    # Delete Daily Statuses
    op.execute("""
    DELETE FROM "StatusList_Statuses"
    WHERE status_list_id=(SELECT id FROM "SimpleEntities" WHERE name='Daily Statuses');
    DELETE FROM "StatusLists"
    WHERE id=(SELECT id FROM "SimpleEntities" WHERE name='Daily Statuses');
    DELETE FROM "Entities"
    WHERE id=(SELECT id FROM "SimpleEntities" WHERE name='Daily Statuses');
    DELETE FROM "SimpleEntities" WHERE
    name = 'Daily Statuses';
    """)
