"""task review/status workflow

Revision ID: 433d9caaafab
Revises: 46775e4a3d96
Create Date: 2014-01-31 01:51:08.457109

"""

# revision identifiers, used by Alembic.
from sqlalchemy.exc import ProgrammingError, IntegrityError
import stalker

revision = '433d9caaafab'
down_revision = '46775e4a3d96'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    # Enum Types
    time_unit_enum = postgresql.ENUM(
        'min', 'h', 'd', 'w', 'm', 'y',
        name='TimeUnit',
        create_type=False
    )
    review_schedule_model_enum = postgresql.ENUM(
        'effort', 'length', 'duration',
        name='ReviewScheduleModel',
        create_type=False
    )

    task_dependency_target_enum = postgresql.ENUM(
        'onend', 'onstart',
        name='TaskDependencyTarget',
        create_type=False
    )

    task_dependency_gap_model = postgresql.ENUM(
        'length', 'duration',
        name='TaskDependencyGapModel',
        create_type=False
    )

    resource_allocation_strategy_enum = postgresql.ENUM(
        'minallocated', 'maxloaded', 'minloaded', 'order', 'random',
        name='ResourceAllocationStrategy',
        create_type=False
    )

    # Reviews
    op.create_table(
        'Reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('reviewer_id', sa.Integer(), nullable=False),
        sa.Column('review_number', sa.Integer(), nullable=True),
        sa.Column('schedule_timing', sa.Float(), nullable=True),
        sa.Column('schedule_unit', time_unit_enum, nullable=False),
        sa.Column('schedule_constraint', sa.Integer(),
                  nullable=False),
        sa.Column('schedule_model', review_schedule_model_enum,
                  nullable=False),
        sa.Column('status_id', sa.Integer(), nullable=False),
        sa.Column('status_list_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['SimpleEntities.id'], ),
        sa.ForeignKeyConstraint(['reviewer_id'], ['Users.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['Statuses.id'], ),
        sa.ForeignKeyConstraint(['status_list_id'],
                                ['StatusLists.id'], ),
        sa.ForeignKeyConstraint(['task_id'], ['Tasks.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Task_Responsible
    op.create_table(
        'Task_Responsible',
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('responsible_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['responsible_id'], ['Users.id']
        ),
        sa.ForeignKeyConstraint(['task_id'], ['Tasks.id']),
        sa.PrimaryKeyConstraint('task_id', 'responsible_id')
    )

    # Task_Alternative_Resources
    op.create_table(
        'Task_Alternative_Resources',
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('resource_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['resource_id'], ['Users.id'], ),
        sa.ForeignKeyConstraint(['task_id'], ['Tasks.id'], ),
        sa.PrimaryKeyConstraint('task_id', 'resource_id')
    )

    # Task Computed Resources
    op.create_table(
        'Task_Computed_Resources',
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('resource_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['resource_id'], ['Users.id'], ),
        sa.ForeignKeyConstraint(['task_id'], ['Tasks.id'], ),
        sa.PrimaryKeyConstraint('task_id', 'resource_id')
    )

    # EntityTypes
    op.add_column(
        'EntityTypes',
        sa.Column('dateable', sa.Boolean(), nullable=True)
    )

    # Projects
    op.drop_column('Projects', 'timing_resolution')

    # Studios
    op.add_column(
        'Studios',
        sa.Column('is_scheduling', sa.Boolean(), nullable=True)
    )
    op.add_column(
        'Studios',
        sa.Column('is_scheduling_by_id', sa.Integer(), nullable=True)
    )
    op.add_column(
        'Studios',
        sa.Column('last_schedule_message', sa.PickleType(), nullable=True)
    )
    op.add_column(
        'Studios',
        sa.Column('last_scheduled_at', sa.DateTime(), nullable=True)
    )
    op.add_column(
        'Studios',
        sa.Column('last_scheduled_by_id', sa.Integer(), nullable=True)
    )
    op.add_column(
        'Studios',
        sa.Column('scheduling_started_at', sa.DateTime(), nullable=True)
    )
    op.drop_column('Studios', 'daily_working_hours')

    # Task Dependencies

    # *************************************************************************
    # dependency_target - onend by default
    op.add_column(
        'Task_Dependencies',
        sa.Column(
            'dependency_target',
            task_dependency_target_enum,
            nullable=True
        )
    )
    # fill data
    op.execute("""
        UPDATE
           "Task_Dependencies"
        SET
            dependency_target = 'onend'
    """)

    # alter column to be nullable false
    op.alter_column(
        'Task_Dependencies',
        'dependency_target',
        existing_nullable=True,
        nullable=False
    )
    # *************************************************************************

    op.alter_column(
        'Task_Dependencies',
        'depends_to_task_id',
        new_column_name='depends_to_id'
    )

    # *************************************************************************
    # gap_constraint column - 0 by default
    op.add_column(
        'Task_Dependencies',
        sa.Column('gap_constraint', sa.Integer(), nullable=True)
    )
    # fill data
    op.execute("""
        UPDATE
           "Task_Dependencies"
        SET
            gap_constraint = 0
    """)

    # alter column to be nullable false
    op.alter_column(
        'Task_Dependencies',
        'gap_constraint',
        existing_nullable=True,
        nullable=False
    )
    # *************************************************************************

    # *************************************************************************
    # gap_model - length by default
    op.add_column(
        'Task_Dependencies',
        sa.Column(
            'gap_model', task_dependency_gap_model,
            nullable=True
        )
    )
    # fill data
    op.execute("""
        UPDATE
           "Task_Dependencies"
        SET
            gap_model = 'length'
    """)

    # alter column to be nullable false
    op.alter_column(
        'Task_Dependencies',
        'gap_model',
        existing_nullable=True,
        nullable=False
    )
    # *************************************************************************

    # *************************************************************************
    # gap_timing - 0 by default
    op.add_column(
        'Task_Dependencies',
        sa.Column('gap_timing', sa.Float(), nullable=True)
    )
    op.add_column(
        'Task_Dependencies',
        sa.Column(
            'gap_unit', time_unit_enum,
            nullable=True
        )
    )
    # fill data
    op.execute("""UPDATE "Task_Dependencies" SET gap_timing = 0""")

    # alter column to be nullable false
    op.alter_column(
        'Task_Dependencies',
        'gap_timing',
        existing_nullable=True,
        nullable=False
    )
    # *************************************************************************

    # Tasks
    op.add_column(
        'Tasks',
        sa.Column('review_number', sa.Integer(), nullable=True)
    )

    # *************************************************************************
    # allocation_strategy - minallocated by default
    op.add_column(
        'Tasks',
        sa.Column(
            'allocation_strategy',
            resource_allocation_strategy_enum,
            nullable=True
        )
    )
    # fill data
    op.execute("""UPDATE "Tasks" SET allocation_strategy = 'minallocated'""")

    # alter column to be nullable false
    op.alter_column(
        'Tasks',
        'allocation_strategy',
        existing_nullable=True,
        nullable=False
    )
    # *************************************************************************

    # *************************************************************************
    # persistent_allocation - True by default
    op.add_column(
        'Tasks',
        sa.Column('persistent_allocation', sa.Boolean(), nullable=True)
    )
    # fill data
    op.execute("""UPDATE "Tasks" SET persistent_allocation = TRUE""")

    # alter column to be nullable false
    op.alter_column(
        'Tasks',
        'persistent_allocation',
        existing_nullable=True,
        nullable=False
    )
    # *************************************************************************

    op.drop_column('Tasks', 'timing_resolution')

    op.drop_column('TimeLogs', 'timing_resolution')
    op.create_unique_constraint(None, 'Users', ['login'])

    op.drop_column('Vacations', 'timing_resolution')

    # before dropping responsible_id column from the Tasks table
    # move the data to the Task_Responsible table
    op.execute(
        'insert into "Task_Responsible" '
        '   select id, responsible_id '
        '   from "Tasks" where responsible_id is not NULL'
    )

    # now drop the data
    op.drop_column('Tasks', 'responsible_id')

    # create new Statuses
    #
    # 'Waiting For Dependency', 'WFD',
    # 'Dependency Has Revision','DREV',
    # 'On Hold',                'OH',
    # 'Stopped',                'STOP',

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

    create_status('Waiting For Dependency', 'WFD')
    create_status('Dependency Has Revision', 'DREV')
    create_status('On Hold', 'OH')
    create_status('Stopped', 'STOP')

    # Review Statuses
    create_status('Requested Revision', 'RREV')
    create_status('Approved', 'APP')

    # Add new Task statuses to StatusList
    def update_status_lists(entity_type, status_code):
        op.execute("""CREATE OR REPLACE FUNCTION add_status_to_status_list(status_list_id INT, status_id INT) RETURNS VOID AS $$
        BEGIN
            INSERT INTO "StatusList_Statuses" (status_list_id, status_id)
            VALUES (status_list_id, status_id);
        EXCEPTION WHEN OTHERS THEN
            -- do nothning
        END;
        $$
        LANGUAGE 'plpgsql';

        select NULL from add_status_to_status_list(
            (SELECT id FROM "StatusLists" WHERE target_entity_type = '%(entity_type)s'),
            (SELECT id FROM "Statuses" WHERE code = '%(status_code)s')
        );""" % {
            'entity_type': entity_type,
            'status_code': status_code
        })

    # Task
    for t in ['Task', 'Asset', 'Shot', 'Sequence']:
        for s in ['WFD', 'RTS', 'WIP', 'OH', 'STOP', 'PREV', 'HREV', 'DREV',
                  'CMPL']:
            update_status_lists(t, s)

    # drop function
    op.execute("drop function add_status_to_status_list(integer, integer);")

    # Remove NEW from Task, Asset, Shot and Sequence StatusList
    op.execute("""DELETE FROM "StatusList_Statuses"
WHERE status_list_id = (SELECT id FROM "StatusLists"
  WHERE target_entity_type = 'Task')
AND status_id = (SELECT id FROM "Statuses" WHERE "Statuses".code = 'NEW')
""")
    op.execute("""DELETE FROM "StatusList_Statuses"
WHERE status_list_id = (SELECT id FROM "StatusLists"
WHERE target_entity_type = 'Asset')
AND status_id = (SELECT id FROM "Statuses" WHERE "Statuses".code = 'NEW')
""")
    op.execute("""DELETE FROM "StatusList_Statuses"
WHERE status_list_id = (SELECT id FROM "StatusLists"
WHERE target_entity_type = 'Shot')
AND status_id = (SELECT id FROM "Statuses" WHERE "Statuses".code = 'NEW')
""")
    op.execute("""DELETE FROM "StatusList_Statuses"
WHERE status_list_id = (SELECT id FROM "StatusLists"
WHERE target_entity_type = 'Sequence')
AND status_id = (SELECT id FROM "Statuses" WHERE "Statuses".code = 'NEW')
""")

    # Create Review StatusList
    # Insert in to SimpleEntities
    op.execute(
        """INSERT INTO "SimpleEntities" (entity_type, name, description,
created_by_id, updated_by_id, date_created, date_updated, type_id,
thumbnail_id, html_style, html_class, stalker_version)
VALUES ('StatusList', 'Review Status List', '', NULL, NULL,
(SELECT CAST(NOW() at time zone 'utc' AS timestamp)),
(SELECT CAST(NOW() at time zone 'utc' AS timestamp)), NULL, NULL,
'', '', '%(stalker_version)s')""" %{ 'stalker_version': stalker.__version__})

    # insert in to Entities and StatusLists
    op.execute(
        """INSERT INTO "Entities" (id)
VALUES ((
  SELECT id
  FROM "SimpleEntities"
  WHERE "SimpleEntities".name = 'Review Status List'
));
INSERT INTO "StatusLists" (id, target_entity_type)
VALUES ((
  SELECT id
  FROM "SimpleEntities"
  WHERE "SimpleEntities".name = 'Review Status List'), 'Review');""")

    # Add Review Statues To StatusList_Statuses
    # Add new Task statuses to StatusList
    op.execute("""INSERT INTO "StatusList_Statuses" (status_list_id, status_id)
VALUES
    ((SELECT id FROM "StatusLists" WHERE target_entity_type = 'Review'),
    (SELECT id FROM "Statuses" WHERE code = 'NEW')),
    ((SELECT id FROM "StatusLists" WHERE target_entity_type = 'Review'),
    (SELECT id FROM "Statuses" WHERE code = 'RREV')),
    ((SELECT id FROM "StatusLists" WHERE target_entity_type = 'Review'),
    (SELECT id FROM "Statuses" WHERE code = 'APP'))
""")

    # Update all NEW Tasks to WFD
    op.execute("""update "Tasks"
set status_id = (select id from "Statuses" where code='WFD')
where status_id = (select id from "Statuses" where code='NEW')""")

    # Update all PREV Tasks to WIP
    op.execute("""update "Tasks"
set status_id = (select id from "Statuses" where code='WIP')
where status_id = (select id from "Statuses" where code='PREV')""")

    # delete any other status from Task, Asset, Shot and Sequence Status Lists
    map(lambda x:
        op.execute("""DELETE FROM "StatusList_Statuses"
        WHERE status_list_id=(
          SELECT id
          FROM "StatusLists"
          WHERE target_entity_type='%s')
          AND status_id in (
            SELECT id
            FROM "Statuses"
            WHERE code NOT IN
            ('WFD', 'RTS', 'WIP', 'OH', 'STOP', 'PREV', 'HREV', 'DREV', 'CMPL')
        );""" % x), ['Task', 'Asset', 'Shot', 'Sequence']
    )

    # Update Tasks.review_number to 0 for all tasks
    op.execute("""update "Tasks" set review_number = 0""")

    # Shots._cut_in -> Shots.cut_in
    op.alter_column(
        'Shots',
        '_cut_in',
        new_column_name='cut_in'
    )

    # Shots._cut_out -> Shots.cut_out
    op.alter_column(
        'Shots',
        '_cut_out',
        new_column_name='cut_out'
    )

    # Tasks._schedule_seconds -> Tasks.schedule_seconds
    op.alter_column(
        'Tasks',
        '_schedule_seconds',
        new_column_name='schedule_seconds'
    )

    # Tasks._total_logged_seconds -> Tasks.total_logged_seconds
    op.alter_column(
        'Tasks',
        '_total_logged_seconds',
        new_column_name='total_logged_seconds'
    )


def downgrade():
    """downgrade
    """
    op.add_column(
        'Vacations',
        sa.Column('timing_resolution', postgresql.INTERVAL(), nullable=True)
    )
    #op.drop_constraint(None, 'Users')
    op.add_column(
        'TimeLogs',
        sa.Column('timing_resolution', postgresql.INTERVAL(), nullable=True)
    )
    op.add_column(
        'Tasks',
        sa.Column('responsible_id', sa.INTEGER(), nullable=True)
    )

    # restore data
    op.execute("""
        UPDATE
           "Tasks"
        SET
            responsible_id = t2.responsible_id
        FROM (
            SELECT task_id, responsible_id
            FROM "Task_Responsible"
        ) as t2
        WHERE "Tasks".id = t2.task_id
    """)

    op.add_column(
        'Tasks',
        sa.Column('timing_resolution', postgresql.INTERVAL(), nullable=True)
    )
    op.drop_column('Tasks', 'persistent_allocation')
    op.drop_column('Tasks', 'allocation_strategy')
    op.drop_column('Tasks', 'review_number')
    op.alter_column(
        'Task_Dependencies',
        'depends_to_id',
        new_column_name='depends_to_task_id'
    )
    op.drop_column('Task_Dependencies', 'gap_unit')
    op.drop_column('Task_Dependencies', 'gap_timing')
    op.drop_column('Task_Dependencies', 'gap_model')
    op.drop_column('Task_Dependencies', 'gap_constraint')
    op.drop_column('Task_Dependencies', 'dependency_target')
    op.add_column(
        'Studios',
        sa.Column('daily_working_hours', sa.INTEGER(), nullable=True)
    )
    op.drop_column('Studios', 'scheduling_started_at')
    op.drop_column('Studios', 'last_scheduled_by_id')
    op.drop_column('Studios', 'last_scheduled_at')
    op.drop_column('Studios', 'last_schedule_message')
    op.drop_column('Studios', 'is_scheduling_by_id')
    op.drop_column('Studios', 'is_scheduling')
    op.add_column(
        'Projects',
        sa.Column('timing_resolution', postgresql.INTERVAL(), nullable=True)
    )
    op.drop_column('EntityTypes', 'dateable')
    op.drop_table('Task_Alternative_Resources')
    op.drop_table('Task_Computed_Resources')
    op.drop_table('Reviews')
    # will loose all the responsible data, change if you care!
    op.drop_table('Task_Responsible')

    # Update all WFD Tasks to NEW
    op.execute("""update "Tasks"
set status_id = (select id from "Statuses" where code='NEW')
where status_id = (select id from "Statuses" where code='WFD')""")

    # Update all OH Tasks to WIP
    op.execute("""update "Tasks"
set status_id = (select id from "Statuses" where code='WIP')
where status_id = (select id from "Statuses" where code='OH')""")

    # Update all STOP or DREV Tasks to CMPL
    op.execute("""update "Tasks"
set status_id = (select id from "Statuses" where code='WIP')
where status_id in (select id from "Statuses" where code in ('STOP', 'DREV'))""")

    op.execute("""update "Tasks"
set status_id = (select id from "Statuses" where code='WIP')
where status_id = (select id from "Statuses" where code='STOP')""")

    # Delete Statuses
    op.execute("""DELETE FROM "StatusList_Statuses" WHERE
    status_id IN (
    select id FROM "SimpleEntities" WHERE
    name IN ('Waiting For Dependency', 'Dependency Has Revision', 'On Hold',
    'Stopped', 'Requested Revision', 'Approved'));
    DELETE FROM "Statuses" WHERE
      id IN (select id FROM "SimpleEntities" WHERE
    name IN ('Waiting For Dependency', 'Dependency Has Revision', 'On Hold',
    'Stopped', 'Requested Revision', 'Approved'));
    DELETE FROM "Entities" WHERE
    id IN (select id FROM "SimpleEntities" WHERE
    name IN ('Waiting For Dependency', 'Dependency Has Revision', 'On Hold',
    'Stopped', 'Requested Revision', 'Approved'));
    DELETE FROM "SimpleEntities" WHERE
    name IN ('Waiting For Dependency', 'Dependency Has Revision', 'On Hold',
    'Stopped', 'Requested Revision', 'Approved');
    """)

    # Delete Review Status List
    op.execute("""
    DELETE FROM "StatusList_Statuses"
    WHERE status_list_id=(SELECT id FROM "SimpleEntities" WHERE name='Review Status List');
    DELETE FROM "StatusLists"
    WHERE id=(SELECT id FROM "SimpleEntities" WHERE name='Review Status List');
    DELETE FROM "Entities"
    WHERE id=(SELECT id FROM "SimpleEntities" WHERE name='Review Status List');
    DELETE FROM "SimpleEntities" WHERE
    name = 'Review Status List';
    """)

    # column name changes
    # Shots._cut_in -> Shots.cut_in
    op.alter_column(
        'Shots',
        'cut_in',
        new_column_name='_cut_in'
    )

    # Shots._cut_out -> Shots.cut_out
    op.alter_column(
        'Shots',
        'cut_out',
        new_column_name='_cut_out'
    )

    # Tasks._schedule_seconds -> Tasks.schedule_seconds
    op.alter_column(
        'Tasks',
        'schedule_seconds',
        new_column_name='_schedule_seconds'
    )

    # Tasks._total_logged_seconds -> Tasks.total_logged_seconds
    op.alter_column(
        'Tasks',
        'total_logged_seconds',
        new_column_name='_total_logged_seconds'
    )
