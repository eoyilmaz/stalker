#-*- coding: utf-8 -*-
"""
this file contains the tags table
"""



from sqlalchemy import (
    Table,
    Column,
    Boolean,
    Integer,
    Float,
    String,
    ForeignKey,
    Date,
    DateTime,
    UniqueConstraint
)
#from stalker.db import meta
from stalker import db

#create the metadata
metadata = db.metadata

# create tables


# ENTITYTYPES
entity_types = Table(
    "entity_types", metadata,
    Column("id", Integer, primary_key=True),
    Column("entity_type", String(128), nullable=False),
)


# SIMPLE ENTITY
simpleEntities = Table(
    "simpleEntities", metadata,
    Column("id", Integer, primary_key=True),
    Column("code", String(256), nullable=False),
    Column("name", String(256), nullable=False),
    Column("description", String),
    
    Column(
        "created_by_id",
        Integer,
        ForeignKey("users.id", use_alter=True, name="x")
    ),
    
    Column(
        "updated_by_id",
        Integer,
        ForeignKey("users.id", use_alter=True, name="x")
    ),
    
    Column("date_created", DateTime),
    Column("date_updated", DateTime),
    Column("db_entity_type", String(128), nullable=False),
    UniqueConstraint("name", "db_entity_type")
)



# TAG
tags = Table(
    "tags", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("simpleEntities.id"),
        primary_key=True
    )
)


# ENTITY_TAGS
entity_tags = Table(
    "entity_tags", metadata,
    Column(
        "entity_id",
        Integer,
        ForeignKey("entities.id"),
        primary_key=True,
    ),
    
    Column(
        "tag_id",
        Integer,
        ForeignKey("tags.id"),
        primary_key=True,
    )
)



# ENTITY
entities = Table(
    "entities", metadata,
    Column(
        "id",
        ForeignKey("simpleEntities.id"),
        primary_key=True
    ),
)



# USER
users = Table(
    "users", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id"),
        primary_key=True
    ),
    
    Column(
        "department_id",
        Integer,
        ForeignKey("departments.id")
    ),
    
    Column("email", String(256), unique=True, nullable=False),
    Column("first_name", String(256), nullable=False),
    Column("last_name", String(256), nullable=True),
    Column("password", String(256), nullable=False),
    
    Column("last_login", DateTime),
    
    #Column("permission_groups_id",
           #Integer,
           #ForeignKey("groups.id")
    #),
    
    Column("initials", String(16)),
    
)



## USER_PROJECTS
#user_projects = Table(
    #"user_projects", metadata,
    #Column(
        #"user_id",
        #Integer,
        #ForeignKey("users.id")
    #),
    
    #Column(
        #"project_id",
        #Integer,
        #ForeignKey("projects.id")
    #)
#)



## USER_TASKS
#user_tasks = Table(
    #"user_tasks", meta,
    #Column(
        #"user_id",
        #Integer,
        #ForeignKey("users.id")
    #),
    
    #Column(
        #"task_id",
        #Integer,
        #ForeignKey("tasks.id")
    #)
#)



# DEPARTMENT
departments = Table(
    "departments", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id"),
        primary_key=True,
    ),
    
    #Column(
        #"members",
        #Integer,
        #ForeignKey("users.id"),
    #)
)



## TASKS
#tasks = Table(
    #"tasks", metadata,
    #Column(
        #"id",


# STATUS
statuses = Table(
    "statuses", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id"),
        primary_key=True,
    ),
)



# STATUSLIST_STATUSES
statusList_statuses = Table(
    "statusList_statuses", metadata,
    Column(
        "statusList_id",
        Integer,
        ForeignKey("statusLists.id"),
        primary_key=True
    ),
    Column(
        "status_id",
        Integer,
        ForeignKey("statuses.id"),
        primary_key=True
    )
)



# STATUSLIST
statusLists = Table(
    "statusLists", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id"),
        primary_key=True
    ),
    Column("target_entity_type", String(128), nullable=False, unique=True),
)



# REPOSITORY
repositories = Table(
    "repositories", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id"),
        primary_key=True,
    ),
    Column("linux_path", String(256)),
    Column("windows_path", String(256)),
    Column("osx_path", String(256))
)



# IMAGEFORMAT
imageFormats = Table(
    "imageFormats", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id"),
        primary_key=True,
    ),
    Column("width", Integer),
    Column("height", Integer),
    Column("pixel_aspect", Float),
    Column("print_resolution", Float)
)



# ASSETTYPE
assetTypes = Table(
    "assetTypes", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("typeEntities.id"),
        primary_key=True,
    ),
)


# ASSETTYPE_PIPELINE_STEPS
assetType_pipelineSteps = Table(
    "assetType_pipelineSteps", metadata,
    Column(
        "assetType_id",
        Integer,
        ForeignKey("assetTypes.id"),
        primary_key=True,
    ),
    
    Column(
        "pipelineStep_id",
        Integer,
        ForeignKey("pipelineSteps.id"),
        primary_key=True,
    ),
)


# PIPELINESTEPS
pipelineSteps = Table(
    "pipelineSteps", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id"),
        primary_key=True,
    ),
    #Column("code", String(32), unique=True),
)



# TYPETEMPLATES
typeTemplates = Table(
    "typeTemplates", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id"),
        primary_key=True,
    ),
    Column("path_code", String),
    Column("file_code", String),
    Column(
        "type_id",
        Integer,
        ForeignKey("typeEntities.id"),
    ),
)



# STRUCTURE
structures = Table(
    "structures", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id"),
        primary_key=True,
    ),
    Column("project_template", String),
)



# STRUCTURE_ASSETTEMPLATES
structure_assetTemplates = Table(
    "structure_assetTemplates", metadata,
    Column(
        "structure_id",
        Integer,
        ForeignKey("structures.id"),
        primary_key=True,
    ),
    Column(
        "typeTemplate_id",
        Integer,
        ForeignKey("typeTemplates.id"),
        primary_key=True,
    ),
)



# STRUCTURE_REFERENCETEMPLATES
structure_referenceTemplates = Table(
    "structure_referenceTemplates", metadata,
    Column(
        "structure_id",
        Integer,
        ForeignKey("structures.id"),
        primary_key=True,
    ),
    Column(
        "typeTemplate_id",
        Integer,
        ForeignKey("typeTemplates.id"),
        primary_key=True,
    ),
)



# TYPEENTITIES
typeEntities = Table(
    "typeEntities", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id"),
        primary_key=True,
    ),
)



# LINK
links = Table(
    "links", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id"),
        primary_key=True,
    ),
    Column("path", String),
    Column("filename", String),
    Column("type_id",
           Integer,
           ForeignKey("linkTypes.id"),
    ),
)



# LINKTYPES
linkTypes = Table(
    "linkTypes", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("typeEntities.id"),
        primary_key=True,
    ),
)



# PROJECTTYPES
projectTypes = Table(
    "projectTypes", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("typeEntities.id"),
        primary_key=True,
    ),
)



# NOTES
notes = Table(
    "notes", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("simpleEntities.id"),
        primary_key=True,
    ),
    Column(
        "entity_id",
        Integer,
        ForeignKey("entities.id"),
    ),
    Column("content", String),
)



# PROJECT_USERS
project_users = Table(
    "project_users", metadata,
    Column(
        "project_id",
        Integer,
        ForeignKey("projects.id"),
        primary_key=True,
    ),
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id"),
        primary_key=True,
    )
)



# PROJECT
projects = Table(
    "projects", metadata,
    Column("id", Integer, ForeignKey("entities.id"), primary_key=True),
    Column("lead_id", Integer, ForeignKey("users.id")),
    Column("repository_id", Integer, ForeignKey("repositories.id")),
    Column("type_id", Integer, ForeignKey("projectTypes.id")),
    Column("structure_id", Integer, ForeignKey("structures.id")),
    Column("image_format_id", Integer, ForeignKey("imageFormats.id")),
    Column("fps", Float(precision=3)),
    Column("is_stereoscopic", Boolean),
    Column("display_width", Float(precision=3)),
)



# TASK - WARNING: It is a temprorary table, will be completed later
tasks = Table(
    "tasks", metadata,
    Column("id", Integer, ForeignKey("entities.id"), primary_key=True),
)



# ASSETBASE_TASKS
assetBase_tasks = Table(
    "assetBase_tasks", metadata,
    Column(
        "assetBase_id",
        Integer,
        ForeignKey("assetBases.id"),
        primary_key=True
    ),
    Column(
        "task_id",
        Integer,
        ForeignKey("tasks.id"),
        primary_key=True
    )
)



# ASSETBASE
assetBases = Table(
    "assetBases", metadata,
    Column("id", Integer, ForeignKey("entities.id"), primary_key=True),
    Column("type_id", Integer, ForeignKey("assetTypes.id")),
)



# SHOT - WARNING: It is a temprorary table, will be completed later
shots = Table(
    "shots", metadata,
    Column("id", Integer, ForeignKey("entities.id"), primary_key=True),
    Column("sequence_id", Integer, ForeignKey("sequences.id")),
)



# SEQUENCES
sequences = Table(
    "sequences", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("entities.id"), primary_key=True
    ),
    Column(
        "project_id",
        Integer,
        ForeignKey("projects.id"),
    ),
    Column(
        "lead",
        Integer,
        ForeignKey("users.id"),
    ),
)