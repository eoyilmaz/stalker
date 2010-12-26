#-*- coding: utf-8 -*-
"""this is the default mapper to map the default models to the default tables
"""

from sqlalchemy.orm import mapper, relationship, backref
from stalker.models import entity, tag, user, department
from stalker.db import tables



# SIMPLE ENTITY
mapper(
    entity.SimpleEntity,
    tables.simpleEntities,
    properties={
        '__name': tables.simpleEntities.c.name,
        '__description': tables.simpleEntities.c.description,
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



# TAGGED ENTITY
mapper(
    entity.TaggedEntity,
    tables.taggedEntities,
    inherits=entity.SimpleEntity,
    #inherit_condition=entity.TaggedEntity.id==entity.SimpleEntity.id,
    inherit_condition=tables.taggedEntities.c.id==tables.simpleEntities.c.id,
    polymorphic_identity='taggedEntity',
    properties={
        '__tags': relationship(
            tag.Tag,
            secondary=tables.taggedEntity_tags,
            backref='__entities'
        )
    }
)


print "started mapping AUDIT ENTITY"
# AUIDIT ENTITY - the many side of many-to-one for created_by and updated_by
mapper(
    entity.AuditEntity,
    tables.auditEntities,
    inherits=entity.TaggedEntity,
    #inherit_condition=entity.AuditEntity.id==entity.TaggedEntity.id,
    inherit_condition=tables.auditEntities.c.id==tables.taggedEntities.c.id,
    polymorphic_identity='auditEntity',
    properties={
        '__created_by': relationship(
            user.User,
            backref='__entities_created',
            primaryjoin=tables.auditEntities.c.id== \
                        tables.users.c.entities_created,
            #post_update=True,
            uselist=False
        ),
        '__updated_by': relationship(
            user.User,
            backref='__entities_updated',
            primaryjoin=tables.auditEntities.c.id== \
                        tables.users.c.entities_updated,
            #post_update=True,
            uselist=False
        )
    }
)
print "finished mapping AUDIT ENTITY"


print "started mapping USER ENTITY"
# USER - the one side of one-to-many for the entities_created and
# entities_updated
mapper(
    user.User,
    tables.users,
    inherits=entity.AuditEntity,
    inherit_condition=tables.users.c.id==tables.auditEntities.c.id,
    polymorphic_identity='user',
    properties={
        #'_entities_created': relationship(
            #entity.AuditEntity,
            #backref='_created_by',
            #primaryjoin=tables.users.c.id==tables.auditEntities.c.created_by,
        #),
        #'_entities_updated': relationship(
            #entity.AuditEntity,
            #backref='_updated_by',
            #primaryjoin=tables.users.c.id==tables.auditEntities.c.updated_by,
        #),
        #'_department': relationship(
            #department.Department,
            #backref='_members',
            #primaryjoin=tables.users.c.id==tables.departments.c.members,
            ##post_update=True,
        #),
    }
)
print "finished mapping USER ENTITY"



# DEPARTMENT - one side for the members one-to-many
mapper(
    department.Department,
    tables.departments,
    inherits=entity.AuditEntity,
    inherit_condition=tables.departments.c.id==tables.auditEntities.c.id,
    polymorphic_identity='department',
    properties={
        '__members': relationship(
            user.User,
            backref='__department',
            primaryjoin=tables.departments.c.members==tables.users.c.id,
            #post_update=True,
            #uselist=False
        )
    }
)



print "Done Mapping!!!"