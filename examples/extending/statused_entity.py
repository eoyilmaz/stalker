# -*- coding: utf-8 -*-
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
