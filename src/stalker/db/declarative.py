# -*- coding: utf-8 -*-
"""The declarative base class is situated here."""
import logging
from typing import Any, Type

from sqlalchemy.orm import declarative_base

from stalker.db.session import DBSession
from stalker.log import get_logger
from stalker.utils import make_plural

logger: logging.Logger = get_logger(__name__)


class ORMClass(object):
    """The base of the Base class."""

    query = DBSession.query_property()

    @property
    def plural_class_name(self) -> str:
        """Return plural name of this class.

        Returns:
            str: The plural version of this class.
        """
        return make_plural(self.__class__.__name__)


Base: Type[Any] = declarative_base(cls=ORMClass)
