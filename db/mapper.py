#-*- coding: utf-8 -*-
"""this is the default mapper to map the default models to the default tables
"""

from sqlalchemy.orm import mapper, relationship, backref, synonym
from stalker.models import entity, tag, user, department
from stalker.db import tables



# SIMPLE ENTITY
print "started mapping SIMPLEENTITY"
mapper(
    entity.SimpleEntity,
    tables.simpleEntities,
    properties={
        '_name': tables.simpleEntities.c.name,
        'name': synonym('_name'),
        '_description': tables.simpleEntities.c.description,
        'description': synonym('_description'),
        '_created_by': relationship(
            user.User,
            backref='_entities_created',
            primaryjoin=tables.simpleEntities.c.created_by_id== \
                        tables.users.c.id,
            post_update=True,
            uselist=False
        ),
        'created_by': synonym('_created_by'),
        '_updated_by': relationship(
            user.User,
            backref='_entities_updated',
            primaryjoin=tables.simpleEntities.c.updated_by_id== \
                        tables.users.c.id,
            post_update=True,
            uselist=False
        ),
        'updated_by': synonym('_updated_by'),
        '_date_created': tables.simpleEntities.c.date_created,
        'date_created': synonym('_date_created'),
        '_date_updated': tables.simpleEntities.c.date_updated,
        'date_updated': synonym('_date_updated')
    },
    polymorphic_on=tables.simpleEntities.c.entity_type,
    polymorphic_identity='simpleEntity'
)
print "finished mapping SIMPLEENTITY"



# TAG
print "started mapping TAG"
mapper(
    tag.Tag,
    tables.tags,
    inherits=entity.SimpleEntity,
    polymorphic_identity='tag'
)
print "finished mapping TAG"



# ENTITY
print "started mapping ENTITY"
mapper(
    entity.Entity,
    tables.entities,
    inherits=entity.SimpleEntity,
    inherit_condition=tables.entities.c.id==tables.simpleEntities.c.id,
    polymorphic_identity='entity',
    properties={
        '_tags': relationship(
            tag.Tag,
            secondary=tables.entity_tags,
            backref='_entities'
        ),
        'tags': synonym('_tags')#, map_column=True)
    }
)
print "finished mapping ENTITY"



# USER
print "started mapping USER"
mapper(
    user.User,
    tables.users,
    inherits=entity.Entity,
    inherit_condition=tables.users.c.id==tables.entities.c.id,
    polymorphic_identity='user',
    properties={
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
    },
    exclude_properties=["projects", "projects_lead", "sequence_lead", "tasks",
                        "permission_groups"],
)
print "finished mapping USER"



# DEPARTMENT
print "started mapping DEPARTMENT"
mapper(
    department.Department,
    tables.departments,
    inherits=entity.Entity,
    inherit_condition=tables.departments.c.id==tables.entities.c.id,
    polymorphic_identity='department',
    properties={
        '_members': relationship(
            user.User,
            backref='_department',
            primaryjoin=tables.departments.c.id==tables.users.c.department_id,
        ),
        'members': synonym('_members')
    },
    exclude_properties=["lead"],
)
print "finished mapping DEPARTMENT"



print "Done Mapping!!!"