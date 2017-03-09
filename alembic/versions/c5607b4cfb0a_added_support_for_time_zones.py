"""Added support for time zones

Revision ID: c5607b4cfb0a
Revises: 0063f547dc2e
Create Date: 2017-03-09 02:17:08.209000

"""

# revision identifiers, used by Alembic.
revision = 'c5607b4cfb0a'
down_revision = '0063f547dc2e'

from alembic import op
import sqlalchemy as sa

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

tables_to_update = {
    'AuthenticationLogs': ['date'],
    'Tasks': ['computed_start', 'computed_end', 'start', 'end'],
    'Studios': ['computed_start', 'computed_end', 'start', 'end',
                'scheduling_started_at', 'last_scheduled_at'],
    'SimpleEntities': ['date_created', 'date_updated'],
    'Projects': ['computed_start', 'computed_end', 'start', 'end'],
    'TimeLogs': ['computed_start', 'computed_end', 'start', 'end'],
    'Vacations': ['computed_start', 'computed_end', 'start', 'end'],
}


def upgrade():
    # Directly updating the columns will set the timezone of the datetime
    # fields to the timezone of the machine that is running this code.
    #
    # Because the data in the database is already in UTC we need to update the
    # data also to have their time values correctly shifted to UTC.
    for table_name in tables_to_update:
        logger.info('upgrading table: %s' % table_name)
        with op.batch_alter_table(table_name) as batch_op:
            for column_name in tables_to_update[table_name]:
                logger.info('altering column: %s' % column_name)
                batch_op.alter_column(
                    column_name, type_=sa.DateTime(timezone=True)
                )

        sql = """
        -- Add the time zone offset
        UPDATE
          "{table_name}"
        SET
        """.format(table_name=table_name)

        for i, column_name in enumerate(tables_to_update[table_name]):
            if i > 0:
                sql = "{sql},\n".format(sql=sql)

            # per column add
            sql = """{sql}
              "{column_name}" = (
                SELECT
                  aliased_table.{column_name}::timestamp at time zone 'utc'
                FROM "{table_name}" as aliased_table
                where aliased_table.id = "{table_name}".id
              )""".format(sql=sql, column_name=column_name,
                          table_name=table_name)

        op.execute(sql)
        logger.info('done upgrading table: %s' % table_name)


def downgrade():
    # Removing the timezone info will not shift the time values. So shift the
    # values by hand
    for table_name in tables_to_update:
        logger.info('downgrading table: %s' % table_name)
        sql = """
        -- Add the time zone offset
        UPDATE
          "{table_name}"
        SET
        """.format(table_name=table_name)

        for i, column_name in enumerate(tables_to_update[table_name]):
            if i > 0:
                sql = "{sql},\n".format(sql=sql)

            # per column add
            sql = """{sql}
              "{column_name}" = (
                SELECT
                  CAST(aliased_table.{column_name} at time zone 'utc' AS timestamp with time zone)
                FROM "{table_name}" as aliased_table
                where aliased_table.id = "{table_name}".id
              )""".format(sql=sql, column_name=column_name,
                          table_name=table_name)
        op.execute(sql)
        logger.info('raw sql completed for table: %s' % table_name)

        with op.batch_alter_table(table_name) as batch_op:
            for column_name in tables_to_update[table_name]:
                batch_op.alter_column(
                    column_name, type_=sa.DateTime(timezone=False)
                )

        logger.info('done downgrading table: %s' % table_name)
