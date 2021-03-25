# -*- coding: utf-8 -*-
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
