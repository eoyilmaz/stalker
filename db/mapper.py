#-*- coding: utf-8 -*-
"""this is the default mapper to map the default models to the default tables

You can use your also use your own mappers. See the docs.
"""



from sqlalchemy.orm import mapper, relationship, backref, synonym
from stalker.db import tables
from stalker.models import (
    asset,
    assetBase,
    booking,
    comment,
    department,
    entity,
    group,
    imageFormat,
    link,
    pipelineStep,
    project,
    repository,
    sequence,
    shot,
    status,
    structure,
    tag,
    task,
    template,
    user,
    version
)



#----------------------------------------------------------------------
def setup():
    """setups the mapping
    """
    
    # SimpleEntity
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
    
    
    
    # Tag
    mapper(
        tag.Tag,
        tables.tags,
        inherits=entity.SimpleEntity,
        polymorphic_identity='tag'
    )
    
    
    
    # Entity
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
            'tags': synonym('_tags')
        }
    )
    
    
    
    # User
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
            '_login_name': tables.users.c.login_name,
            'loing_name': synonym('_login_name'),
            '_password': tables.users.c.password,
            'password': synonym('_password'),
        },
    )
    
    
    
    # Department
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
    )
    
    
    
    # STATUS
    mapper(
        status.Status,
        tables.statuses,
        inherits=entity.Entity,
        inherit_condition=tables.statuses.c.id==tables.entities.c.id,
        polymorphic_identity='status',
        properties={
            '_short_name': tables.statuses.c.short_name,
            'short_name': synonym('_short_name')
        }
    )
    
    
    
    # STATUSLIST
    mapper(
        status.StatusList,
        tables.statusLists,
        inherits=entity.Entity,
        inherit_condition=tables.statusLists.c.id==tables.entities.c.id,
        polymorphic_identity='statusLists',
        properties={
            '_statuses': relationship(
                status.Status,
                secondary=tables.statusList_statuses
            ),
            'statuses': synonym('_statuses')
        }
    )
    
    
    
    # REPOSITORY
    mapper(
        repository.Repository,
        tables.repositories,
        inherits=entity.Entity,
        inherit_condition=tables.repositories.c.id==tables.entities.c.id,
        polymorphic_identity='repository',
        properties={
            '_linux_path': tables.repositories.c.linux_path,
            '_windows_path': tables.repositories.c.windows_path,
            '_osx_path': tables.repositories.c.osx_path
        },
        exclude_properties=['path']
    )
    
    
    
    