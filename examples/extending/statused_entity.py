#-*- coding: utf-8 -*-
"""
In this example we are going to extend stalker with a new entity type, which
is also mixed in with :class:`~stalker.core.models.mixin.StatusMixin`.

To be able to use NewStatusedEntity with the rest of the stalker.core.models in
a persistence environment, before calling anything from stalker call these in
your configuration scripts::

  from extending import statused_entity
  from stalker.conf import defaults
  defaults.MAPPERS.append("extending.statused_entity")
  defaults.CORE_MODEL_CLASSES.append("examples.extending.statused_entity.\
      NewStatusedEntity")

Now Stalker nows how to extend the stalker.core.models with your class
"""

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import mapper, relationship, synonym

from stalker import db
from stalker.db import tables
from stalker.db.mixin import StatusMixinDB
from stalker.core.models.mixin import StatusMixin
from stalker.core.models import entity



class NewStatusedEntity(entity.SimpleEntity, StatusMixin):
    """The new statused entity class, which is a new simpleEntity with status
    abilities
    """
    pass



def setup():
    """this is the setup function that stalker will call to setup our class
    """
    
    metadata = db.metadata
    
    # first create the table for our NewStatusedEntity, we don't need anything
    # other than an id column
    new_statused_entities_table = Table(
        "newStatusedEntities", metadata,
        Column(
            "id",
            Integer,
            ForeignKey(tables.simpleEntities.c.id),
            primary_key=True,
        ),
    )
    
    
    # to let the mixin adds its own columns and properties we call the
    # StatusMixinDB.setup
    
    # to mix the table
    mapper_arguments = StatusMixinDB.setup(NewStatusedEntity, new_statused_entities_table)
    #print "mapper_arguments", mapper_arguments
    
    # StatusMixinDB.setup returns the:
    #  * secondary_tables that it created for us
    #  * new properties for the mapper
    #  * new options for the mapper
    #
    # we don't need to use the secondary_tables but the properties and options
    # will be passed to the mapper of our class
    
    # update the mapper arguments with our variables
    mapper_arguments.update(
        dict(
            inherits=NewStatusedEntity.__base__,
            polymorphic_identity=NewStatusedEntity.entity_type
        )
    )
    
    # do the mapping
    mapper(
        NewStatusedEntity,
        new_statused_entities_table,
        **mapper_arguments
    )
    
    # voila now we have introduced a new type to the SOM and also mixed it
    # with a StatusMixin

