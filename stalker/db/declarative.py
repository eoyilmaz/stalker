# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
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

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.exc import UnmappedClassError

from stalker.models import make_plural


def query_property():
    """A ripped off version of the sqlalchemy.orm.ScopedSession.query_property
    """
    class query(object):
        def __get__(s, instance, owner):
            try:
                mapper = class_mapper(owner)
                if mapper:
                    # session's configured query class
                    from stalker import db
                    return db.session.query(mapper)
            except UnmappedClassError:
                return None
    return query()


class ORMClass(object):
    """The base of the Base class
    """

    query = query_property()

    @property
    def plural_class_name(self):
        """the plural name of this class
        """
        return make_plural(self.__class__.__name__)

Base = declarative_base(cls=ORMClass)
