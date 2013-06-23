# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
""" store the declarative_base in this module
"""

from sqlalchemy.ext.declarative import declarative_base
from stalker.db.session import DBSession
from stalker.models import make_plural


class ORMClass(object):
    query = DBSession.query_property()
    
    @property
    def plural_class_name(self):
        """the plural name of this class
        """
        return make_plural(self.__class__.__name__)

Base = declarative_base(cls=ORMClass)
