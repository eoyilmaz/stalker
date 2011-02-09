#-*- coding: utf-8 -*-
"""
In this example we are going to extend stalker with a new entity type, which
is also mixed in with a :mod:`~stalker.core.models.mixin.ReferenceMixin`.

To be able to use GreatEntity with the rest of the stalker.core.models in a
persistence environment, before calling anything from stalker call these in
your configuration scripts::

  from extending import great_entity
  from stalker.conf import defaults
  defaults.MAPPERS.append("extending.great_entity")
  defaults.CORE_MODEL_CLASSES.append("examples.extending.great_entity.\
      GreatEntity")

Now Stalker nows how to extend the stalker.core.models with your class
"""

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import mapper, relationship, synonym

from stalker import db
from stalker.db import tables
from stalker.db.mixin import ReferenceMixinDB
from stalker.core.models.mixin import ReferenceMixin
from stalker.core.models import entity



class GreatEntity(entity.SimpleEntity, ReferenceMixin):
    """The new great entity class, which is a new simpleEntity with
    ReferenceMixin
    """
    pass



def setup():
    
    metadata = db.metadata
    
    # first create the table for our GreatEntity
    great_entities_table = Table(
        "greatEntities", metadata,
        Column(
            "id",
            Integer,
            ForeignKey(tables.simpleEntities.c.id),
            primary_key=True,
        ),
    )
    
    
    # to let the mixin adds its own columns and properties we call the
    # ReferenceMixinDB.setup
    
    # create the mapper_arguments dictionary
    mapper_arguments= {
        "inherits": GreatEntity.__base__,
        "polymorphic_identity": GreatEntity.entity_type
    }
    
    # do the mixin database setup
    ReferenceMixinDB.setup(GreatEntity, great_entities_table, mapper_arguments)
    
    # setup the mapper with the updated mapper_arguments
    mapper(
        GreatEntity,
        great_entities_table,
        **mapper_arguments
    )
    
    # voila now we have introduced a new type to the SOM and also mixed it
    # with a StatusMixin


