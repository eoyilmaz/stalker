# -*- coding: utf-8 -*-

import logging

from sqlalchemy.ext.declarative import declarative_base
from stalker.db.session import DBSession
from stalker import log
from stalker.models import make_plural

logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


class ORMClass(object):
    """The base of the Base class
    """

    query = DBSession.query_property()

    @property
    def plural_class_name(self):
        """the plural name of this class
        """
        return make_plural(self.__class__.__name__)

Base = declarative_base(cls=ORMClass)
