#-*- coding: utf-8 -*-
"""this is the default mapper to map the default models to the default tables

You can use your also use your own mappers. See the docs.
"""



from sqlalchemy.orm import mapper, relationship, backref, synonym
from stalker.db import tables
from stalker.db.mixin import (ReferenceMixinDB, StatusMixinDB, ScheduleMixinDB,
                              TaskMixinDB)
from stalker.core.models import (
    Asset,
    Booking,
    Comment,
    Department,
    Entity,
    ImageFormat,
    Link,
    Note,
    PermissionGroup,
    Project,
    ReferenceMixin,
    Repository,
    ScheduleMixin,
    StatusMixin,
    Sequence,
    Shot,
    SimpleEntity,
    Status,
    StatusList,
    Structure,
    Tag,
    Task,
    Type,
    FilenameTemplate,
    User,
    Version
)



#----------------------------------------------------------------------
def setup():
    """setups the mapping
    """
    
    # Entity_Type_IDs
    
    # *******************************************************************
    # SimpleEntity
    mapper(
        SimpleEntity,
        tables.SimpleEntities,
        polymorphic_on=tables.SimpleEntities.c.db_entity_type,
        polymorphic_identity="SimpleEntity",
        properties={
            "_code": tables.SimpleEntities.c.code,
            "code": synonym("_code"),
            "_name": tables.SimpleEntities.c.name,
            "name": synonym("_name"),
            "_description": tables.SimpleEntities.c.description,
            "description": synonym("_description"),
            "_created_by": relationship(
                User,
                backref="_entities_created",
                primaryjoin=tables.SimpleEntities.c.created_by_id== \
                            tables.Users.c.id,
                post_update=True,
                #uselist=False
            ),
            "created_by": synonym("_created_by"),
            "_updated_by": relationship(
                User,
                backref="_entities_updated",
                primaryjoin=tables.SimpleEntities.c.updated_by_id== \
                            tables.Users.c.id,
                post_update=True,
                #uselist=False
            ),
            "updated_by": synonym("_updated_by"),
            "_date_created": tables.SimpleEntities.c.date_created,
            "date_created": synonym("_date_created"),
            "_date_updated": tables.SimpleEntities.c.date_updated,
            "date_updated": synonym("_date_updated"),
            "_type": relationship(
                Type,
                primaryjoin=tables.SimpleEntities.c.type_id==tables.Types.c.id
            ),
            "type": synonym("_type"),
        },
    )
    
    
    # *******************************************************************
    # Tag
    mapper(
        Tag,
        tables.Tags,
        inherits=Tag.__base__,
        polymorphic_identity="Tag"
    )
    
    
    # *******************************************************************
    # PermissionGroup
    mapper(
        PermissionGroup,
        tables.PermissionGroups,
        inherits=PermissionGroup.__base__,
        polymorphic_identity="PermissionGrou"
    )
    
    # *******************************************************************
    # Entity
    mapper(
        Entity,
        tables.Entities,
        inherits=Entity.__base__,
        inherit_condition=tables.Entities.c.id==tables.SimpleEntities.c.id,
        polymorphic_identity="Entity",
        properties={
            "_tags": relationship(
                Tag,
                secondary=tables.Entity_Tags,
                backref="entities"
            ),
            "tags": synonym("_tags"),
            "_notes": relationship(
                Note,
                primaryjoin=tables.Entities.c.id==tables.Notes.c.entity_id,
                backref="entity",
            ),
            "notes": synonym("_notes"),
        }
    )
    
    
    
    # *******************************************************************
    # User
    mapper(
        User,
        tables.Users,
        inherits=User.__base__,
        inherit_condition=tables.Users.c.id==tables.Entities.c.id,
        polymorphic_identity="User",
        properties={
            "enitites_created": synonym("_entities_created"),
            "enitites_updated": synonym("_entities_updated"),
            "department": synonym("_department"),
            "_name": tables.SimpleEntities.c.name,
            "name": synonym("_name"),
            "_first_name": tables.Users.c.first_name,
            "first_name": synonym("_first_name"),
            "_last_name": tables.Users.c.last_name,
            "last_name": synonym("_last_name"),
            "_initials": tables.Users.c.initials,
            "initials": synonym("_initials"),
            "_email": tables.Users.c.email,
            "email": synonym("_email"),
            "_password": tables.Users.c.password,
            "password": synonym("_password"),
            "_last_login": tables.Users.c.last_login,
            "last_login": synonym("_last_login"),
            "_permission_groups": relationship(
                PermissionGroup,
                secondary=tables.User_PermissionGroups,
                primaryjoin=\
                    tables.Users.c.id==tables.User_PermissionGroups.c.user_id,
                secondaryjoin=\
                    tables.User_PermissionGroups.c.permissionGroup_id==\
                    tables.PermissionGroups.c.id
            ),
            "permission_groups": synonym("_permission_groups"),
            "projects_lead": synonym("_projects_lead"),
            "sequences_lead": synonym("_sequences_lead"),
            "_tasks": relationship(
                Task,
                secondary=tables.User_Tasks,
                primaryjoin=tables.Users.c.id==tables.User_Tasks.c.user_id,
                secondaryjoin=tables.User_Tasks.c.task_id==tables.Tasks.c.id,
                backref="_resources",
            ),
            "tasks": synonym("_tasks"),
        },
    )
    
    
    
    # *******************************************************************
    # Department
    mapper(
        Department,
        tables.Departments,
        inherits=Department.__base__,
        inherit_condition=tables.Departments.c.id==tables.Entities.c.id,
        polymorphic_identity="Department",
        properties={
            "_members": relationship(
                User,
                backref="_department",
                primaryjoin=\
                    tables.Departments.c.id==tables.Users.c.department_id,
            ),
            "members": synonym("_members"),
            "_lead": relationship(
                User,
                uselist=False,
                primaryjoin=tables.Departments.c.lead_id==tables.Users.c.id,
                post_update=True
            ),
            "lead": synonym("_lead"),
        },
    )
    
    
    
    # *******************************************************************
    # Status
    mapper(
        Status,
        tables.Statuses,
        inherits=Status.__base__,
        inherit_condition=tables.Statuses.c.id==tables.Entities.c.id,
        polymorphic_identity="Status",
    )
    
    
    
    # *******************************************************************
    # StatusList
    mapper(
        StatusList,
        tables.StatusLists,
        inherits=StatusList.__base__,
        inherit_condition=tables.StatusLists.c.id==tables.Entities.c.id,
        polymorphic_identity="StatusList",
        properties={
            "_statuses": relationship(
                Status,
                secondary=tables.StatusList_Statuses
            ),
            "statuses": synonym("_statuses"),
            "_target_entity_type": tables.StatusLists.c.target_entity_type,
            "target_entity_type": synonym("_target_entity_type"),
        }
    )
    
    
    
    # *******************************************************************
    # Repository
    mapper(
        Repository,
        tables.Repositories,
        inherits=Repository.__base__,
        inherit_condition=tables.Repositories.c.id==tables.Entities.c.id,
        polymorphic_identity="Repository",
        properties={
            "_linux_path": tables.Repositories.c.linux_path,
            "linux_path": synonym("_linux_path"),
            "_windows_path": tables.Repositories.c.windows_path,
            "windows_path": synonym("_windows_path"),
            "_osx_path": tables.Repositories.c.osx_path,
            "osx_path": synonym("_osx_path")
        },
        #exclude_properties=["path"]
    )
    
    
    
    # *******************************************************************
    # ImageFormat
    mapper(
        ImageFormat,
        tables.ImageFormats,
        inherits=ImageFormat.__base__,
        inherit_condition=tables.ImageFormats.c.id==tables.Entities.c.id,
        polymorphic_identity="ImageFormat",
        properties={
            "_width": tables.ImageFormats.c.width,
            "width": synonym("_width"),
            "_height": tables.ImageFormats.c.height,
            "height": synonym("_height"),
            "_pixel_aspect": tables.ImageFormats.c.pixel_aspect,
            "pixel_aspect": synonym("_pixel_aspect"),
            "_print_resolution": tables.ImageFormats.c.print_resolution,
            "print_resolution": synonym("print_resolution"),
            "device_aspect": synonym("_device_aspect"),
        },
        #exclude_properties=["device_aspect"]
    )
    
    
    
    # *******************************************************************
    # Type
    mapper(
        Type,
        tables.Types,
        inherits=Type.__base__,
        inherit_condition=tables.Types.c.id==tables.Entities.c.id,
        polymorphic_identity="Type",
    )
    
    
    
    # *******************************************************************
    # FilenameTemplate
    mapper(
        FilenameTemplate,
        tables.FilenameTemplates,
        inherits=FilenameTemplate.__base__,
        inherit_condition=tables.FilenameTemplates.c.id==tables.Entities.c.id,
        polymorphic_identity="FilenameTemplate",
        properties={
            "_path_code": tables.FilenameTemplates.c.path_code,
            "path_code": synonym("_path_code"),
            "_file_code": tables.FilenameTemplates.c.file_code,
            "file_code": synonym("_file_code"),
            "_target_entity_type":\
                tables.FilenameTemplates.c.target_entity_type,
            "target_entity_type": synonym("_target_entity_type"),
            "_output_path_code": tables.FilenameTemplates.c.output_path_code,
            "output_path_code": synonym("_output_path_code"),
            "_output_file_code": tables.FilenameTemplates.c.output_file_code,
            "output_file_code": synonym("_output_file_code"),
            "_output_is_relative":\
                tables.FilenameTemplates.c.output_is_relative,
            "output_is_relative": synonym("_output_is_relative")
        },
    )
    
    
    
    # *******************************************************************
    # Structure
    mapper(
        Structure,
        tables.Structures,
        inherits=Structure.__base__,
        inherit_condition=tables.Structures.c.id==tables.Entities.c.id,
        polymorphic_identity="Structure",
        properties={
            "_templates": relationship(
                FilenameTemplate,
                secondary=tables.Structure_FilenameTemplates
            ),
            "templates": synonym("_templates"),
            "_custom_template": tables.Structures.c.custom_template,
            "custom_template": synonym("_custom_template"),
        },
    )
    
    
    
    # *******************************************************************
    # Links
    mapper(
        Link,
        tables.Links,
        inherits=Link.__base__,
        inherit_condition=tables.Links.c.id==tables.Entities.c.id,
        polymorphic_identity="Link",
        properties={
            "_path": tables.Links.c.path,
            "path": synonym("_path"),
        },
    )
    
    
    
    
    # *******************************************************************
    # Notes
    mapper(
        Note,
        tables.Notes,
        inherits=Note.__base__,
        inherit_condition=tables.Notes.c.id==tables.SimpleEntities.c.id,
        polymorphic_identity="Note",
        properties={
            "_content": tables.Notes.c.content,
            "content": synonym("_content"),
        }
    )
    
    
    
    # *******************************************************************
    # Project
    project_mapper_arguments = dict(
        inherits=Project.__base__,
        polymorphic_identity="Project",
        inherit_condition=tables.Projects.c.id==tables.Entities.c.id,
        properties={
            "_lead": relationship(
                User,
                backref="_projects_lead",
                primaryjoin=tables.Projects.c.lead_id==tables.Users.c.id,
            ),
            "lead": synonym("_lead"),
            "_repository": relationship(
                Repository,
                primaryjoin=tables.Projects.c.repository_id==\
                            tables.Repositories.c.id
            ),
            "repository": synonym("repository"),
            "_structure": relationship(
                Structure,
                primaryjoin=tables.Projects.c.structure_id==\
                            tables.Structures.c.id
            ),
            "structure": synonym("_structure"),
            "_image_format": relationship(
                ImageFormat,
                primaryjoin=tables.Projects.c.image_format_id==\
                            tables.ImageFormats.c.id
            ),
            "image_format": synonym("_image_format"),
            "_fps": tables.Projects.c.fps,
            "fps": synonym("_fps"),
            "_is_stereoscopic": tables.Projects.c.is_stereoscopic,
            "is_stereoscopic": synonym("_is_stereoscopic"),
            "_display_width": tables.Projects.c.display_width,
            "display_width": synonym("_display_width"),
            #"_users": relationship(
                #User,
                #secondary=tables.Project_Users,
                #primaryjoin=\
                    #tables.Projects.c.id==tables.Project_Users.c.project_id,
                #secondaryjoin=\
                    #tables.Project_Users.c.user_id==tables.Users.c.id,
            #),
            #"users": synonym("_users")
        }
    )
    
    # mix it with ReferenceMixin first
    ReferenceMixinDB.setup(Project, tables.Projects, project_mapper_arguments)
    
    # then to the StatusMixin
    StatusMixinDB.setup(Project, tables.Projects, project_mapper_arguments)
    
    # then to the ScheduleMixin
    ScheduleMixinDB.setup(Project, tables.Projects, project_mapper_arguments)
    
    # then to the TaskMixin
    TaskMixinDB.setup(Project, tables.Projects, project_mapper_arguments)
    
    mapper(
        Project,
        tables.Projects,
        **project_mapper_arguments
    )
    
    # ------------------------------------------------------------------------
    # NOTES:
    #
    # Because a Project instance is mixed with the TaskMixin it has a project
    # attribute. In SOM, the project instantly assigns itself to the project
    # attribute (in __init__). But this creates a weird position in database
    # table and mapper configuration where for the Project class the mapper
    # should configure the _project attribute with the post_update flag is set
    # to True, and this implies the project_id coloumn to be Null for a while,
    # at least SQLAlchemy does an UPDATE to assign the Project itself to the
    # project attribute, thus the project_id column shouldn't be nullable for
    # Project class, but it is not neccessary for the others.
    # 
    # And because SOM is also checking if the project attribute is None or Null
    # for the created instance, I consider doing this safe.
    # ------------------------------------------------------------------------
    
    
    
    # *******************************************************************
    # Task
    task_mapper_arguments = dict(
        inherits=Task.__base__,
        polymorphic_identity="Task",
        inherit_condition=tables.Tasks.c.id==tables.Entities.c.id,
        properties={
            "resources": synonym("_resources"),
            
        }
    )
    
    # mix it with StatusMixin
    StatusMixinDB.setup(Task, tables.Tasks, task_mapper_arguments)
    
    # and then ScheduleMixin
    ScheduleMixinDB.setup(Task, tables.Tasks, task_mapper_arguments)
    
    mapper(
        Task,
        tables.Tasks,
        **task_mapper_arguments
    )
    
    
    
    # *******************************************************************
    # Asset
    asset_mapper_arguments = dict(
        inherits=Asset.__base__,
        polymorphic_identity="Asset",
        inherit_condition=tables.Assets.c.id==tables.Entities.c.id,
        properties={
            "shots": synonym("_shots"),
        }
    )
    
    # mix it with ReferenceMixin
    ReferenceMixinDB.setup(Asset, tables.Assets, asset_mapper_arguments)
    
    # then with StatusMixin
    StatusMixinDB.setup(Asset, tables.Assets, asset_mapper_arguments)
    
    # then with TaskMixin
    TaskMixinDB.setup(Asset, tables.Assets, asset_mapper_arguments)
    
    # complete mapping
    mapper(Asset, tables.Assets, **asset_mapper_arguments)
    
    
    
    # *******************************************************************
    # Shot
    shot_mapper_arguments = dict(
        inherits=Shot.__base__,
        inherit_condition=tables.Shots.c.id==tables.Entities.c.id,
        polymorphic_identity="Shot",
        properties={
            "_assets": relationship(
                Asset,
                secondary=tables.Shot_Assets,
                primaryjoin=tables.Shots.c.id==\
                    tables.Shot_Assets.c.shot_id,
                secondaryjoin=tables.Shot_Assets.c.asset_id==\
                    tables.Assets.c.id,
                backref="_shots",
            ),
            "assets": synonym("_assets"),
            "_sequence": relationship(
                Sequence,
                primaryjoin=tables.Shots.c.sequence_id==\
                    tables.Sequences.c.id
            ),
            "sequence": synonym("_sequence"),
            "_cut_in": tables.Shots.c.cut_in,
            "cut_in": synonym("_cut_in"),
            #"_cut_duration": tables.Shots.c.cut_duration,
            #"cut_duration": synonym("_cut_duration"),
            #"cut_out": synonym("_cut_out"),
            "_cut_out": tables.Shots.c.cut_out,
            "cut_out": synonym("_cut_out"),
            "cut_duration": synonym("_cut_duration"),
            "_code": tables.SimpleEntities.c.code, # overloaded attribute
            "code": synonym("_code"), # overloaded property
        }
    )
    
    # mix it with ReferenceMixin
    ReferenceMixinDB.setup(Shot, tables.Shots, shot_mapper_arguments)
    
    # then with StatusMixin
    StatusMixinDB.setup(Shot, tables.Shots, shot_mapper_arguments)
    
    # then with TaskMixin
    TaskMixinDB.setup(Shot, tables.Shots, shot_mapper_arguments)
    
    #print shot_mapper_arguments
    
    # complete mapping
    mapper(Shot, tables.Shots, **shot_mapper_arguments)
    
    
    
    # *******************************************************************
    # Sequence
    sequence_mapper_arguments = dict(
        inherits=Sequence.__base__,
        polymorphic_identity="Sequence",
        inherit_condition=tables.Sequences.c.id==tables.Entities.c.id,
        properties={
            #"_project": relationship(
                #Project,
                #primaryjoin=tables.Sequences.c.project_id==\
                    #tables.Projects.c.id,
                #backref="_sequences"
            #),
            #"project": synonym("project"),
            "_shots": relationship(
                Shot,
                primaryjoin=tables.Shots.c.sequence_id==\
                    tables.Sequences.c.id,
                uselist=True,
            ),
            "shots": synonym("_shots"),
            "_lead": relationship(
                User,
                primaryjoin=tables.Sequences.c.lead_id==tables.Users.c.id,
                backref="_sequences_lead",
                post_update=True
            ),
            "lead": synonym("_lead")
        }
    )
    
    # mix it with ReferenceMixin, StatusMixin and ScheduleMixin
    ReferenceMixinDB.setup(Sequence, tables.Sequences,
                           sequence_mapper_arguments)
    
    StatusMixinDB.setup(Sequence, tables.Sequences, sequence_mapper_arguments)
    
    ScheduleMixinDB.setup(Sequence, tables.Sequences,
                          sequence_mapper_arguments)
    
    TaskMixinDB.setup(Sequence, tables.Sequences, sequence_mapper_arguments)
    
    mapper(Sequence, tables.Sequences, **sequence_mapper_arguments)
    

