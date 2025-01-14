# -*- coding: utf-8 -*-
"""Stalker specific data types are situated here."""
import datetime
import json
from typing import Any, Dict, TYPE_CHECKING, Union

import pytz

from sqlalchemy.types import DateTime, JSON, TEXT, TypeDecorator

import tzlocal

if TYPE_CHECKING:  # pragma: no cover
    from sqlalchemy.engine.interfaces import Dialect


class JSONEncodedDict(TypeDecorator):
    """Stores and retrieves JSON as TEXT."""

    impl = TEXT

    def process_bind_param(self, value: Union[None, Any], dialect: "Dialect") -> str:
        """Process bind param.

        Args:
            value (Union[None, Any]): The object to convert to JSON.
            dialect (sqlalchemy.engine.interface.Dialect): The dialect.

        Returns:
            str: The str representation of the JSON data.
        """
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(
        self, value: Union[None, str], dialect: "Dialect"
    ) -> Union[None, Dict[str, Any]]:
        """Process result value.

        Args:
            value (Union[None, Any]): The str representation of the JSON data.
            dialect (sqlalchemy.engine.interface.Dialect): The dialect.

        Returns:
            dict: The dict representation of the JSON data.
        """
        return_value: Union[None, Dict[str, Any]] = None
        if value is not None:
            return_value = json.loads(value)
        return return_value


GenericJSON = JSON().with_variant(JSONEncodedDict, "sqlite")
"""A JSON variant that can be used both for PostgreSQL and SQLite3

It will be native JSON for PostgreSQL and JSONEncodedDict for SQLite3
"""


class DateTimeUTC(TypeDecorator):
    """Store UTC internally without the timezone info.

    Inject timezone info as the data comes back from db.
    """

    impl = DateTime

    def process_bind_param(self, value: Any, dialect: str) -> datetime.datetime:
        """Process bind param.

        Args:
            value (Any): The value.
            dialect (str): The dialect.

        Returns:
            datetime.datetime: The datetime value with UTC timezone.
        """
        if value is not None:
            # convert the datetime object to have UTC
            # and strip the datetime value out (which is automatic for SQLite3)
            value = value.astimezone(pytz.utc)
        return value

    def process_result_value(self, value: Any, dialect: str) -> datetime.datetime:
        """Process result value.

        Args:
            value (Any): The value.
            dialect (str): The dialect.

        Returns:
            datetime.datetime: The datetime value with UTC timezone.
        """
        if value is not None:
            # inject utc and then convert to local timezone
            local_tz = tzlocal.get_localzone()
            value = value.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return value


GenericDateTime = DateTime(timezone=True).with_variant(DateTimeUTC, "sqlite")
"""A DateTime variant that can be used with both PostgreSQL and SQLite3 and
adds support to timezones in SQLite3.
"""
