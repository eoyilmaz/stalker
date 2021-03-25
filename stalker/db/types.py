# -*- coding: utf-8 -*-

from sqlalchemy.types import TypeDecorator, TEXT, JSON, DateTime
import json


class JSONEncodedDict(TypeDecorator):
    """Stores and retrieves JSON as TEXT.
    """

    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


GenericJSON = JSON().with_variant(JSONEncodedDict, 'sqlite')
"""A JSON variant that can be used both for PostgreSQL and SQLite3

It will be native JSON for PostgreSQL and JSONEncodedDict for SQLite3
"""


class DateTimeUTC(TypeDecorator):
    """Stores UTC internally without the timezone info and injects timezone
    info as the data comes back from db.
    """

    impl = DateTime

    def process_bind_param(self, value, dialect):
        if value is not None:
            # convert the datetime object to have UTC
            # and strip the datetime value out (which is automatic for SQLite3)
            import pytz
            value = value.astimezone(pytz.utc)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            # inject utc and then convert to local timezone
            import pytz
            import tzlocal
            local_tz = tzlocal.get_localzone()
            value = value.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return value

GenericDateTime = DateTime(timezone=True).with_variant(DateTimeUTC, 'sqlite')
"""A DateTime variant that can be used with both PostgreSQL and SQLite3 and
adds support to timezones in SQLite3.
"""