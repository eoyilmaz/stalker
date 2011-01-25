"""
In this example we are going to extend stalker with a new entity type, which
is also mixed in with a :mod:`~stalker.core.modelsmixin`.

To be able to use GreatEntity with the rest of the stalker.core.models in a
persistence environment, before calling anything from stalker call these in
your configuration scripts::

  from extending import great_entity
  from stalker.conf import defaults
  defaults.MAPPERS.append("extending.great_entity")
  defaults.CORE_MODEL_CLASSES.append("examples.extending.great_entity.GreatEntity")

Now Stalker nows how to extend the stalker.core.models with your class
"""

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import mapper, relationship, synonym
from stalker import db
from stalker.db import tables
from stalker.db.mixins import ReferenceMixin as ReferenceMixinDB
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
    
    
    # mix the table
    ReferenceMixinDB_data = ReferenceMixinDB.setup(GreatEntity,
                                                   great_entities_table)
    
    # setup the mapper with the supplied mixin properties
    mapper(
        GreatEntity,
        great_entities_table,
        inherits=GreatEntity.__base__,
        polymorphic_identity=GreatEntity.entity_type,
        
        # update the propreties with the one comming from mixin
        properties=ReferenceMixinDB_data.properties,
    )

