"""Added exclude and check constraints to TimeLogs table

Revision ID: 31b1e22b455e
Revises: c5607b4cfb0a
Create Date: 2017-03-10 02:14:38.330000

"""

# revision identifiers, used by Alembic.
from sqlalchemy import CheckConstraint

revision = '31b1e22b455e'
down_revision = 'c5607b4cfb0a'

from alembic import op

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def upgrade():
    """adds CheckConstraint and an ExcludeConstraint for the TimeLogs table
    """
    # First cleanup TimeLogs table
    logger.info('Removing duplicate TimeLog entries')
    op.execute("""
-- first remove direct duplicates
with cte as (
    select
        row_number() over (partition by resource_id, start) as rn,
        id,
        start,
        "end",
        resource_id
    from "TimeLogs"
    where exists (
        select
            1
        from "TimeLogs" as tlogs
        where tlogs.start <= "TimeLogs".start
            and "TimeLogs".start < tlogs.end
            and tlogs.id != "TimeLogs".id
            and tlogs.resource_id = "TimeLogs".resource_id
    )
    order by start
) delete from "TimeLogs"
where "TimeLogs".id in (select id from cte where rn > 1);""")

    logger.info(
        'Removing contained TimeLog entries (TimeLogs surrounded by other '
        'TimeLogs'
    )
    op.execute("""
-- remove any contained (TimeLogs surrounded by other TimeLogs) TimeLogs
with cte as (
    select
        "TimeLogs".id,
        "TimeLogs".start,
        "TimeLogs".end,
        "TimeLogs".resource_id
    from "TimeLogs"
    join "TimeLogs" as tlogs on
        "TimeLogs".start > tlogs.start and "TimeLogs".start < tlogs.end
        and "TimeLogs".end > tlogs.start and "TimeLogs".end < tlogs.end
        and "TimeLogs".resource_id = tlogs.resource_id
) delete from "TimeLogs"
where "TimeLogs".id in (select id from cte);""")

    logger.info('Trimming residual overlapping TimeLog.end values')
    op.execute("""
-- then trim the end dates of the TimeLogs that are stil overlapping with others
update "TimeLogs"
set "end" = (
    select
        tlogs.start
    from "TimeLogs" as tlogs
    where "TimeLogs".start < tlogs.start and "TimeLogs".end > tlogs.start
        and "TimeLogs".resource_id = tlogs.resource_id
    limit 1
)
where "TimeLogs".end - "TimeLogs".start > interval '10 min'
    and exists(
        select
            1
        from "TimeLogs" as tlogs
        where "TimeLogs".start < tlogs.start and "TimeLogs".end > tlogs.start
            and "TimeLogs".resource_id = tlogs.resource_id
    );""")

    logger.info('Trimming residual overlapping TimeLog.start values')
    op.execute("""
-- then trim the start dates of the TimeLogs that are stil overlapping with
-- others (there may be 10 min TimeLogs left in the previous query)
update "TimeLogs"
set start = (
    select
        tlogs.end
    from "TimeLogs" as tlogs
    where "TimeLogs".start > tlogs.start and "TimeLogs".start < tlogs.end
        and "TimeLogs".resource_id = tlogs.resource_id
    limit 1
)
where "TimeLogs".end - "TimeLogs".start > interval '10 min'
    and exists(
        select
            1
        from "TimeLogs" as tlogs
        where "TimeLogs".start > tlogs.start and "TimeLogs".start < tlogs.end
            and "TimeLogs".resource_id = tlogs.resource_id
        limit 1
    );""")

    logger.info('Adding CheckConstraint(end > start) to TimeLogs table')
    with op.batch_alter_table(
            'TimeLogs',
            table_args=(CheckConstraint('"end" > start'))) as batch_op:
        pass

        logger.info('Adding ExcludeConstraint to TimeLogs table')
    from stalker.models.task import TimeLog, add_exclude_constraint
    conn = op.get_bind()
    add_exclude_constraint(TimeLog.__table__, conn)


def downgrade():
    # Drop ExcludeConstraint and functions
    # Sadly we can not reintroduce the deleted data in the upgrade() function
    logger.info('Dropping CheckConstraint(end > start)')
    op.execute("""ALTER TABLE "TimeLogs" DROP CONSTRAINT IF EXISTS TimeLogs_check;""")

    logger.info('Dropping "TimeLogs".overlapping_time_logs function')
    op.execute("""ALTER TABLE "TimeLogs" DROP CONSTRAINT IF EXISTS overlapping_time_logs;""")

    logger.info('Dropping ts_to_box function')
    op.execute("""DROP FUNCTION IF EXISTS ts_to_box(timestamp with time zone, timestamp with time zone);""")

    logger.info('Dropping btree_gist extension')
    op.execute("""DROP EXTENSION IF EXISTS btree_gist;""")
