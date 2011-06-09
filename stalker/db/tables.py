#-*- coding: utf-8 -*-



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
from stalker import db

#create the metadata
metadata = db.metadata



# create tables


# ENTITYTYPES
EntityTypes = Table(
    "EntityTypes", metadata,
    Column("id", Integer, primary_key=True),
    Column("entity_type", String(128), nullable=False),
)


# SIMPLEENTITY
SimpleEntities = Table(
    "SimpleEntities", metadata,
    Column("id", Integer, primary_key=True),
    Column("code", String(256), nullable=False),
    Column("name", String(256), nullable=False),
    Column("description", String),
    
    Column(
        "created_by_id",
        Integer,
        ForeignKey("Users.id", use_alter=True, name="x")
    ),
    
    Column(
        "updated_by_id",
        Integer,
        ForeignKey("Users.id", use_alter=True, name="x")
    ),
    
    Column("date_created", DateTime), Column("date_updated", DateTime),
    Column("db_entity_type", String(128), nullable=False),
    #Column("entity_type",String(128), nullable=False),
    Column(
        "type_id",
        Integer,
        ForeignKey("Types.id", use_alter=True, name="y")
    ),
    UniqueConstraint("name", "db_entity_type")
)



# TAG
Tags = Table(
    "Tags", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("SimpleEntities.id"),
        primary_key=True
    )
)


# ENTITY_TAGS
Entity_Tags = Table(
    "Entity_Tags", metadata,
    Column(
        "entity_id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    ),
    
    Column(
        "tag_id",
        Integer,
        ForeignKey("Tags.id"),
        primary_key=True,
    )
)



# ENTITY
Entities = Table(
    "Entities", metadata,
    Column(
        "id",
        ForeignKey("SimpleEntities.id"),
        primary_key=True
    ),
)



# USER
Users = Table(
    "Users", metadata,
    Column("id", Integer, ForeignKey("Entities.id"), primary_key=True),
    Column("department_id", Integer, ForeignKey("Departments.id")),
    Column("email", String(256), unique=True, nullable=False),
    Column("first_name", String(256), nullable=False),
    Column("last_name", String(256), nullable=True),
    Column("password", String(256), nullable=False),
    Column("last_login", DateTime),
    Column("initials", String(16)),
    #Column("permission_groups_id", Integer, ForeignKey("Groups.id")),
)



## USER_PROJECTS
#User_Projects = Table(
    #"User_Projects", metadata,
    #Column(
        #"user_id",
        #Integer,
        #ForeignKey("Users.id")
    #),
    
    #Column(
        #"project_id",
        #Integer,
        #ForeignKey("Projects.id")
    #)
#)



## USER_TASKS
#User_Tasks = Table(
    #"User_Tasks", meta,
    #Column(
        #"user_id",
        #Integer,
        #ForeignKey("Users.id")
    #),
    
    #Column(
        #"task_id",
        #Integer,
        #ForeignKey("Tasks.id")
    #)
#)



# DEPARTMENT
Departments = Table(
    "Departments", metadata,
    Column("id", Integer, ForeignKey("Entities.id"), primary_key=True),
    Column("lead_id", Integer,
           ForeignKey("Users.id", use_alter=True, name="x")
    ),
)



## TASKS
#Tasks = Table(
    #"Tasks", metadata,
    #Column(
        #"id",


# STATUS
Statuses = Table(
    "Statuses", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    ),
)



# STATUSLIST_STATUSES
StatusList_Statuses = Table(
    "StatusList_Statuses", metadata,
    Column(
        "statusList_id",
        Integer,
        ForeignKey("StatusLists.id"),
        primary_key=True
    ),
    Column(
        "status_id",
        Integer,
        ForeignKey("Statuses.id"),
        primary_key=True
    )
)



# STATUSLIST
StatusLists = Table(
    "StatusLists", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True
    ),
    Column("target_entity_type", String(128), nullable=False, unique=True),
)



# REPOSITORY
Repositories = Table(
    "Repositories", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    ),
    Column("linux_path", String(256)),
    Column("windows_path", String(256)),
    Column("osx_path", String(256))
)



# IMAGEFORMAT
ImageFormats = Table(
    "ImageFormats", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    ),
    Column("width", Integer),
    Column("height", Integer),
    Column("pixel_aspect", Float),
    Column("print_resolution", Float)
)



# FILENAMETEMPLATES
FilenameTemplates = Table(
    "FilenameTemplates", metadata,
    Column("id", Integer, ForeignKey("Entities.id"), primary_key=True),
    Column("target_entity_type", String),
    Column("path_code", String),
    Column("file_code", String),
    Column("output_path_code", String),
    Column("output_file_code", String),
    Column("output_is_relative", Boolean),
)



# STRUCTURE
Structures = Table(
    "Structures", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    ),
    Column("custom_template", String),
)



# STRUCTURE_FILENAMETEMPLATES
Structure_FilenameTemplates = Table(
    "Structure_FilenameTemplates", metadata,
    Column("structure_id", Integer, ForeignKey("Structures.id")),
    Column("filenametemplate_id", Integer, ForeignKey("FilenameTemplates.id"))
)



# TYPES
Types = Table(
    "Types", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    ),
    Column("target_entity_type", String)
)



# LINKS
Links = Table(
    "Links", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    ),
    Column("path", String),
    Column("filename", String),
)



# NOTES
Notes = Table(
    "Notes", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("SimpleEntities.id"),
        primary_key=True,
    ),
    Column(
        "entity_id",
        Integer,
        ForeignKey("Entities.id"),
    ),
    Column("content", String),
)



# removed this table because the users are now gathered from the tasks
## PROJECT_USERS
#Project_Users = Table(
    #"Project_Users", metadata,
    #Column("project_id", Integer, ForeignKey("Projects.id"), primary_key=True),
    #Column("user_id", Integer, ForeignKey("Users.id"), primary_key=True),
#)



# PROJECT
Projects = Table(
    "Projects", metadata,
    Column("id", Integer, ForeignKey("Entities.id"), primary_key=True),
    Column("lead_id", Integer, ForeignKey("Users.id")),
    Column("repository_id", Integer, ForeignKey("Repositories.id")),
    Column("structure_id", Integer, ForeignKey("Structures.id")),
    Column("image_format_id", Integer, ForeignKey("ImageFormats.id")),
    Column("fps", Float(precision=3)),
    Column("is_stereoscopic", Boolean),
    Column("display_width", Float(precision=3)),
)



# TASK - WARNING: It is a temprorary table, will be completed later
Tasks = Table(
    "Tasks", metadata,
    Column("id", Integer, ForeignKey("Entities.id"), primary_key=True),
)



# ASSET
Assets = Table(
    "Assets", metadata,
    Column("id", Integer, ForeignKey("Entities.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("Projects.id")),
)

# SHOT ASSETS
Shot_Assets = Table(
    "Shot_Assets", metadata,
    Column("shot_id", Integer, ForeignKey("Shots.id"), primary_key=True),
    Column("asset_id", Integer, ForeignKey("Assets.id"), primary_key=True),
)


# SHOT
# the cut_out attribute is not going to be stored in the database, only
# the cut_in and cut_duration will be enough to calculate the cut_out
# 
Shots = Table(
    "Shots", metadata,
    Column("id", Integer, ForeignKey("Entities.id"), primary_key=True),
    Column("sequence_id", Integer, ForeignKey("Sequences.id")),
    Column("cut_in", Integer),
    Column("cut_duration", Integer),
)



# SEQUENCES
Sequences = Table(
    "Sequences", metadata,
    Column(
        "id",
        Integer,
        ForeignKey("Entities.id"), primary_key=True
    ),
    Column(
        "project_id",
        Integer,
        ForeignKey("Projects.id"),
    ),
    Column(
        "lead_id",
        Integer,
        ForeignKey("Users.id"),
    ),
)