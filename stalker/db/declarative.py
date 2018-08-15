# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2018 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# Stalker is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# Stalker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with Stalker.  If not, see <http://www.gnu.org/licenses/>
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
