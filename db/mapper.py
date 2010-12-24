#-*- coding: utf-8 -*-
"""this is the default mapper to map the default models to the default tables
"""

from sqlalchemy.orm import mapper
from stalker.models import entity, tag
from stalker.db import tables



# SIMPLE ENTITY
mapper(
    entity.SimpleEntity,
    tables.simpleEntities,
    properties={
        '_name' : tables.simpleEntities.c.name,
        '_description' : tables.simpleEntities.c.description,
        },
    polymorphic_on=tables.simpleEntities.c.entity_type,
    polymorphic_identity='simpleEntity'
)



# TAG
mapper(
    tag.Tag,
    tables.tags,
    inherits=entity.SimpleEntity,
    polymorphic_identity='tag'
)



print "Done Mapping!!!"