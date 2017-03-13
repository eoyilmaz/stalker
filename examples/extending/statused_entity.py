# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2017 Erkan Ozgur Yilmaz
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
In this example we are going to extend Stalker with a new entity type, which
is also mixed in with :class:`stalker.models.mixins.StatusMixin`.
"""

from sqlalchemy import Column, Integer, ForeignKey
from stalker import SimpleEntity, StatusMixin


class NewStatusedEntity(SimpleEntity, StatusMixin):
    """The new statused entity class, which is a new simpleEntity with status
    abilities.
    """

    __tablename__ = 'NewStatusedEntities'
    __mapper_args__ = {'polymorphic_identity': 'NewStatusedEntity'}

    new_statused_entity_id = Column('id', Integer,
                                    ForeignKey('SimpleEntities.id'),
                                    primary_key=True)

# voila now we have introduced a new type to the SOM and also mixed it with a
# StatusMixin
