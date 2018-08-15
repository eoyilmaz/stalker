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
"""
In this example we are going to extend stalker with a new entity type, which
is also mixed in with a :class:`stalker.models.mixins.ReferenceMixin`.

To create your own data type, just derive it from a suitable SOM class.
"""

from sqlalchemy import Column, Integer, ForeignKey
from stalker import SimpleEntity, ReferenceMixin


class GreatEntity(SimpleEntity, ReferenceMixin):
    """The new great entity class, which is a new simpleEntity with
    ReferenceMixin
    """

    __tablename__ = 'GreatEntities'
    great_entity_id = Column('id', Integer, ForeignKey('SimpleEntities.c.id'),
                             primary_key=True)
