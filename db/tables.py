#-*- coding: utf-8 -*-
"""
this file contains the tags table
"""



from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from stalker.db import meta

#create the metadata
metadata = meta.metadata

# create tables

# SIMPLE ENTITY
simpleEntities = Table(
    'simpleEntities', metadata,
    Column(
        'id',
        Integer,
        primary_key=True
    ),
    
    Column(
        'name',
        String(256)
    ),
    
    Column(
        'description',
        String
    ),
    
    Column(
        'entity_type',
        String(128),
        nullable=False
    ),
)



# TAG
tags = Table(
    'tags', metadata,
    Column(
        'id',
        Integer,
        ForeignKey('simpleEntities.id'),
        primary_key=True
    )
)


# TAGGED_ENTITY_TAGS
taggedEntity_tags = Table(
    'taggedEntity_tags', metadata,
    Column(
        'taggedEntity_id',
        Integer,
        ForeignKey('taggedEntities.id')
    ),
    
    Column(
        'tag_id',
        Integer,
        ForeignKey('tags.id')
    )
)



# TAGGED ENTITY
taggedEntities = Table(
    'taggedEntities', metadata,
    Column(
        'id',
        ForeignKey('simpleEntities.id'),
        primary_key=True
    ),
)



# AUIDIT ENTITY
auditEntities = Table(
    'auditEntities', metadata,
    Column(
        'id',
        Integer,
        ForeignKey(
            'taggedEntities.id'
        ),
        primary_key=True
    ),
    
    Column(
        'created_by',
        Integer,
        ForeignKey(
            'users.id',
            use_alter=True,
            name='alt1'
        )
    ),
    
    Column(
        'updated_by',
        Integer,
        ForeignKey(
            'users.id',
            use_alter=True,
            name='alt1'
        )
    ),
    
    Column(
        'date_updated',
        DateTime
    )
)



# USER
users = Table(
    'users', metadata,
    Column(
        'id',
        Integer,
        ForeignKey('auditEntities.id'),
        primary_key=True
    ),
    
    Column(
        'entities_created',
        Integer,
        ForeignKey('auditEntities.id')
    ),
    
    Column(
        'entities_updated',
        Integer,
        ForeignKey('auditEntities.id')
    ),
    Column(
        'department',
        Integer,
        ForeignKey(
            'departments.id',
            use_alter=True,
            name='x'
        )
    )
)



# DEPARTMENT
departments = Table(
    'departments', metadata,
    Column(
        'id',
        Integer,
        ForeignKey('auditEntities.id'),
        primary_key=True
    ),
    
    Column(
        'members',
        Integer,
        ForeignKey('users.id'),
    )
)



print "Done Creating Tables!!!"