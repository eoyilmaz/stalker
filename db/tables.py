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
    Column('id', Integer, primary_key=True),
    Column('name', String(256), unique=True, nullable=False),
    Column('description', String),
    
    Column(
        'created_by_id',
        Integer,
        ForeignKey('users.id', use_alter=True, name='x')
    ),
    
    Column(
        'updated_by_id',
        Integer,
        ForeignKey('users.id', use_alter=True, name='x')
    ),
    
    Column('date_created', DateTime),
    Column('date_updated', DateTime),
    Column('entity_type', String(128), nullable=False),
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


# ENTITY_TAGS
entity_tags = Table(
    'entity_tags', metadata,
    Column(
        'entity_id',
        Integer,
        ForeignKey('entities.id')
    ),
    
    Column(
        'tag_id',
        Integer,
        ForeignKey('tags.id')
    )
)



# ENTITY
entities = Table(
    'entities', metadata,
    Column(
        'id',
        ForeignKey('simpleEntities.id'),
        primary_key=True
    ),
)



# USER
users = Table(
    'users', metadata,
    Column(
        'id',
        Integer,
        ForeignKey('entities.id'),
        primary_key=True
    ),
    
    Column(
        'department_id',
        Integer,
        ForeignKey('departments.id')
    ),
    
    Column('email', String(256), nullable=False),
    Column('first_name', String(256), nullable=False),
    Column('last_name', String(256), nullable=True),
    Column('login_name', String(256), unique=True, nullable=False),
    Column('password', String(256), nullable=False),
    
    #Column('permission_groups_id',
           #Integer,
           #ForeignKey('groups.id')
    #),
)



## USER_PROJECTS
#user_projects = Table(
    #'user_projects', metadata,
    #Column(
        #'user_id',
        #Integer,
        #ForeignKey('users.id')
    #),
    
    #Column(
        #'project_id',
        #Integer,
        #ForeignKey('projects.id')
    #)
#)



## USER_TASKS
#user_tasks = Table(
    #'user_tasks', meta,
    #Column(
        #'user_id',
        #Integer,
        #ForeignKey('users.id')
    #),
    
    #Column(
        #'task_id',
        #Integer,
        #ForeignKey('tasks.id')
    #)
#)



# DEPARTMENT
departments = Table(
    'departments', metadata,
    Column(
        'id',
        Integer,
        ForeignKey('entities.id'),
        primary_key=True
    ),
    
    #Column(
        #'members',
        #Integer,
        #ForeignKey('users.id'),
    #)
)



## TASKS
#tasks = Table(
    #'tasks', metadata,
    #Column(
        #'id',


# STATUS
statuses = Table(
    'statuses', metadata,
    Column(
        'id',
        Integer,
        ForeignKey('entities.id'),
        primary_key=True
    ),
    Column('short_name', String(32))
)



# STATUSLIST_STATUSES
statusList_statuses = Table(
    'statusList_statuses', metadata,
    Column(
        'statusList_id',
        Integer,
        ForeignKey('statusLists.id'),
        primary_key=True
    ),
    Column(
        'status.id',
        Integer,
        ForeignKey('statuses.id'),
        primary_key=True
    )
)



# STATUSLIST
statusLists = Table(
    'statusLists', metadata,
    Column(
        'id',
        Integer,
        ForeignKey('entities.id'),
        primary_key=True
    ),
)


# REPOSITORY
repositories = Table(
    'repositories', metadata,
    Column(
        'id',
        Integer,
        ForeignKey('entities.id'),
        primary_key=True
    ),
    Column('linux_path', String(256)),
    Column('windows_path', String(256)),
    Column('osx_path', String(256)),
)


#print "Done Creating Tables!!!"