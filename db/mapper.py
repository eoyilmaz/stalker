#-*- coding: utf-8 -*-
"""this is the default mapper to map the default models to the default tables
"""

from sqlalchemy.orm import mapper, relationship, backref, synonym
from stalker.models import entity, tag, user, department
from stalker.db import tables



# SIMPLE ENTITY
mapper(
    entity.SimpleEntity,
    tables.simpleEntities,
    properties={
        '_name': tables.simpleEntities.c.name,
        'name': synonym('_name'),#, map_column=True),
        '_description': tables.simpleEntities.c.description,
        'description': synonym('_description')#, map_column=True)
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
        '_tags': relationship(
            tag.Tag,
            secondary=tables.taggedEntity_tags,
            backref='_entities'
        ),
        'tags': synonym('_tags')#, map_column=True)
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
        '_created_by': relationship(
            user.User,
            backref='_entities_created',
            primaryjoin=tables.auditEntities.c.created_by_id== \
                        tables.users.c.id,
            post_update=True,
            uselist=False
        ),
        'created_by': synonym('_created_by'),#, map_column=True),
        '_updated_by': relationship(
            user.User,
            backref='_entities_updated',
            primaryjoin=tables.auditEntities.c.updated_by_id== \
                        tables.users.c.id,
            post_update=True,
            uselist=False
        ),
        'updated_by': synonym('_updated_by')#, map_column=True)
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
        'enitites_created': synonym('_entities_created'),
        'enitites_updated': synonym('_entities_updated'),
        'department': synonym('_department'),
        '_email': tables.users.c.email,
        'email': synonym('_email'),
        '_first_name': tables.users.c.first_name,
        'first_name': synonym('_first_name'),
        '_last_name': tables.users.c.last_name,
        'last_name': synonym('_last_name'),
        '_login_name': tables.users.c.last_name,
        'loing_name': synonym('_login_name'),
        '_password': tables.users.c.password,
        'password': synonym('_password'),
        
        
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
        '_members': relationship(
            user.User,
            backref='_department',
            primaryjoin=tables.departments.c.id==tables.users.c.department_id,
            #post_update=True,
            #uselist=False
        ),
        'members': synonym('_members')#, map_column=True)
    }
)



print "Done Mapping!!!"