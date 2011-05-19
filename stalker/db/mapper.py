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
    AssetType,
    Booking,
    Comment,
    Department,
    Entity,
    Group,
    ImageFormat,
    Link,
    LinkType,
    Note,
    Project,
    ProjectType,
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
    TaskType,
    TypeEntity,
    TypeTemplate,
    User,
    Version
)



#----------------------------------------------------------------------
def setup():
    """setups the mapping
    """
    
    # Entity_Type_IDs
    
    
    # SimpleEntity
    mapper(
        SimpleEntity,
        tables.SimpleEntities,
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
        },
        polymorphic_on=tables.SimpleEntities.c.db_entity_type,
        polymorphic_identity=SimpleEntity.entity_type
    )
    
    
    
    # Tag
    mapper(
        Tag,
        tables.Tags,
        inherits=Tag.__base__,
        polymorphic_identity=Tag.entity_type
    )
    
    
    
    # Entity
    mapper(
        Entity,
        tables.Entities,
        inherits=Entity.__base__,
        inherit_condition=tables.Entities.c.id==tables.SimpleEntities.c.id,
        polymorphic_identity=Entity.entity_type,
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
    
    
    
    # User
    mapper(
        User,
        tables.Users,
        inherits=User.__base__,
        inherit_condition=tables.Users.c.id==tables.Entities.c.id,
        polymorphic_identity=User.entity_type,
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
        },
    )
    
    
    
    # Department
    mapper(
        Department,
        tables.Departments,
        inherits=Department.__base__,
        inherit_condition=tables.Departments.c.id==tables.Entities.c.id,
        polymorphic_identity=Department.entity_type,
        properties={
            "_members": relationship(
                User,
                backref="_department",
                primaryjoin=\
                    tables.Departments.c.id==tables.Users.c.department_id,
            ),
            "members": synonym("_members")
        },
    )
    
    
    
    # Status
    mapper(
        Status,
        tables.Statuses,
        inherits=Status.__base__,
        inherit_condition=tables.Statuses.c.id==tables.Entities.c.id,
        polymorphic_identity=Status.entity_type,
    )
    
    
    
    # StatusList
    mapper(
        StatusList,
        tables.StatusLists,
        inherits=StatusList.__base__,
        inherit_condition=tables.StatusLists.c.id==tables.Entities.c.id,
        polymorphic_identity=StatusList.entity_type,
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
    
    
    
    # Repository
    mapper(
        Repository,
        tables.Repositories,
        inherits=Repository.__base__,
        inherit_condition=tables.Repositories.c.id==tables.Entities.c.id,
        polymorphic_identity=Repository.entity_type,
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
    
    
    
    # ImageFormat
    mapper(
        ImageFormat,
        tables.ImageFormats,
        inherits=ImageFormat.__base__,
        inherit_condition=tables.ImageFormats.c.id==tables.Entities.c.id,
        polymorphic_identity=ImageFormat.entity_type,
        properties={
            "_width": tables.ImageFormats.c.width,
            "width": synonym("_width"),
            "_height": tables.ImageFormats.c.height,
            "height": synonym("_height"),
            "_pixel_aspect": tables.ImageFormats.c.pixel_aspect,
            "pixel_aspect": synonym("_pixel_aspect"),
            "_print_resolution": tables.ImageFormats.c.print_resolution,
            "print_resolution": synonym("print_resolution")
        },
        exclude_properties=["device_aspect"]
    )
    
    
    
    # TypeEntity
    mapper(
        TypeEntity,
        tables.TypeEntities,
        inherits=TypeEntity.__base__,
        inherit_condition=tables.TypeEntities.c.id==tables.Entities.c.id,
        polymorphic_identity=TypeEntity.entity_type,
    )
    
    
    
    # AssetType
    mapper(
        AssetType,
        tables.AssetTypes,
        inherits=AssetType.__base__,
        inherit_condition=tables.AssetTypes.c.id==tables.TypeEntities.c.id,
        polymorphic_identity=AssetType.entity_type,
        properties={
            "_task_types": relationship(
                TaskType,
                secondary=tables.AssetType_TaskTypes
                ),
            "task_types": synonym("_task_types")
        }
    )
    
    
    
    # LinkType
    mapper(
        LinkType,
        tables.LinkTypes,
        inherits=LinkType.__base__,
        inherit_condition=tables.LinkTypes.c.id==tables.TypeEntities.c.id,
        polymorphic_identity=LinkType.entity_type,
    )
    
    
    
    # ProjectType
    mapper(
        ProjectType,
        tables.ProjectTypes,
        inherits=ProjectType.__base__,
        inherit_condition=tables.ProjectTypes.c.id==tables.TypeEntities.c.id,
        polymorphic_identity=ProjectType.entity_type,
    )
    
    
    
    # TaskType
    mapper(
        TaskType,
        tables.TaskTypes,
        inherits=TaskType.__base__,
        inherit_condition=tables.TaskTypes.c.id==tables.Entities.c.id,
        polymorphic_identity=TaskType.entity_type,
    )
    
    
    
    # TypeTemplate
    mapper(
        TypeTemplate,
        tables.TypeTemplates,
        inherits=TypeTemplate.__base__,
        inherit_condition=tables.TypeTemplates.c.id==tables.Entities.c.id,
        polymorphic_identity=TypeTemplate.entity_type,
        properties={
            "_path_code": tables.TypeTemplates.c.path_code,
            "path_code": synonym("_path_code"),
            "_file_code": tables.TypeTemplates.c.file_code,
            "file_code": synonym("_file_code"),
            "_type": relationship(
                TypeEntity,
                primaryjoin=\
                    tables.TypeTemplates.c.type_id==tables.TypeEntities.c.id
                ),
            "type": synonym("_type"),
        },
    )
    
    
    
    # Structure
    mapper(
        Structure,
        tables.Structures,
        inherits=Structure.__base__,
        inherit_condition=tables.Structures.c.id==tables.Entities.c.id,
        polymorphic_identity=Structure.entity_type,
        properties={
            "_project_template": tables.Structures.c.project_template,
            "project_template": synonym("_project_template"),
            "_asset_templates": relationship(
                TypeTemplate,
                secondary=tables.Structure_AssetTemplates,
                primaryjoin=\
                    tables.Structures.c.id==\
                    tables.Structure_AssetTemplates.c.structure_id,
                secondaryjoin=
                    tables.Structure_AssetTemplates.c.typeTemplate_id==\
                    tables.TypeTemplates.c.id
            ),
            "asset_templates": synonym("_asset_templates"),
            "_reference_templates": relationship(
                TypeTemplate,
                secondary=tables.Structure_ReferenceTemplates,
                primaryjoin=\
                    tables.Structures.c.id==\
                    tables.Structure_ReferenceTemplates.c.structure_id,
                secondaryjoin=
                    tables.Structure_ReferenceTemplates.c.typeTemplate_id==\
                    tables.TypeTemplates.c.id
            ),
            "reference_templates": synonym("_reference_templates"),
        },
    )
    
    
    
    # Links
    mapper(
        Link,
        tables.Links,
        inherits=Link.__base__,
        inherit_condition=tables.Links.c.id==tables.Entities.c.id,
        polymorphic_identity=Link.entity_type,
        properties={
            "_path": tables.Links.c.path,
            "path": synonym("_path"),
            "_filename": tables.Links.c.filename,
            "filename": synonym("_filename"),
            "_type": relationship(
                LinkType,
                primaryjoin=\
                    tables.Links.c.type_id==tables.LinkTypes.c.id
            ),
            "type": synonym("_type"),
        },
    )
    
    
    
    
    # Notes
    mapper(
        Note,
        tables.Notes,
        inherits=Note.__base__,
        inherit_condition=tables.Notes.c.id==tables.SimpleEntities.c.id,
        polymorphic_identity=Note.entity_type,
        properties={
            "_content": tables.Notes.c.content,
            "content": synonym("_content"),
        }
    )
    
    
    
    # Project - also the first implemented class using the mixins
    project_mapper_arguments = dict(
        inherits=Project.__base__,
        polymorphic_identity=Project.entity_type,
        inherit_condition=tables.Projects.c.id==tables.Entities.c.id,
        properties={
            "_lead": relationship(
                User,
                primaryjoin=tables.Projects.c.lead_id==tables.Users.c.id,
            ),
            "lead": synonym("_lead"),
            "_repository": relationship(
                Repository,
                primaryjoin=tables.Projects.c.repository_id==\
                            tables.Repositories.c.id
            ),
            "repository": synonym("repository"),
            "_type": relationship(
                ProjectType,
                primaryjoin=tables.Projects.c.type_id==tables.ProjectTypes.c.id
            ),
            "type": synonym("_type"),
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
    
    
    
    # Task
    # WARNING: Not finished, it is a temporary implementation, created to be
    # able to test other classes
    
    task_mapper_arguments = dict(
        inherits=Task.__base__,
        polymorphic_identity=Task.entity_type,
        inherit_condition=tables.Tasks.c.id==tables.Entities.c.id
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
    
    
    
    # Asset
    asset_mapper_arguments = dict(
        inherits=Asset.__base__,
        polymorphic_identity=Asset.entity_type,
        inherit_condition=tables.Assets.c.id==tables.Entities.c.id,
        properties={
            "_type": relationship(
                AssetType,
                primaryjoin=\
                    tables.Assets.c.type_id==tables.AssetTypes.c.id
            ),
            "type": synonym("_type"),
            "_project": relationship(
                Project,
                primaryjoin=\
                    tables.Assets.c.project_id==tables.Projects.c.id
            ),
            "project": synonym("_project"),
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
    
    
    
    # Shot
    shot_mapper_arguments = dict(
        inherits=Shot.__base__,
        inherit_condition=tables.Shots.c.id==tables.Entities.c.id,
        polymorphic_identity=Shot.entity_type,
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
            "_cut_duration": tables.Shots.c.cut_duration,
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
    
    
    
    # Sequence
    sequence_mapper_arguments = dict(
        inherits=Sequence.__base__,
        polymorphic_identity=Sequence.entity_type,
        inherit_condition=tables.Sequences.c.id==tables.Entities.c.id,
        properties={
            "_project": relationship(
                Project,
                primaryjoin=tables.Sequences.c.project_id==\
                    tables.Projects.c.id
            ),
            "project": synonym("project"),
            "_shots": relationship(
                Shot,
                primaryjoin=tables.Shots.c.sequence_id==\
                    tables.Sequences.c.id,
                uselist=True,
            )
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
    

