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
        tables.simpleEntities,
        properties={
            "_code": tables.simpleEntities.c.code,
            "code": synonym("_code"),
            "_name": tables.simpleEntities.c.name,
            "name": synonym("_name"),
            "_description": tables.simpleEntities.c.description,
            "description": synonym("_description"),
            "_created_by": relationship(
                User,
                backref="_entities_created",
                primaryjoin=tables.simpleEntities.c.created_by_id== \
                            tables.users.c.id,
                post_update=True,
                #uselist=False
            ),
            "created_by": synonym("_created_by"),
            "_updated_by": relationship(
                User,
                backref="_entities_updated",
                primaryjoin=tables.simpleEntities.c.updated_by_id== \
                            tables.users.c.id,
                post_update=True,
                #uselist=False
            ),
            "updated_by": synonym("_updated_by"),
            "_date_created": tables.simpleEntities.c.date_created,
            "date_created": synonym("_date_created"),
            "_date_updated": tables.simpleEntities.c.date_updated,
            "date_updated": synonym("_date_updated"),
        },
        polymorphic_on=tables.simpleEntities.c.db_entity_type,
        polymorphic_identity=SimpleEntity.entity_type
    )
    
    
    
    # Tag
    mapper(
        Tag,
        tables.tags,
        inherits=Tag.__base__,
        polymorphic_identity=Tag.entity_type
    )
    
    
    
    # Entity
    mapper(
        Entity,
        tables.entities,
        inherits=Entity.__base__,
        inherit_condition=tables.entities.c.id==tables.simpleEntities.c.id,
        polymorphic_identity=Entity.entity_type,
        properties={
            "_tags": relationship(
                Tag,
                secondary=tables.entity_tags,
                backref="entities"
            ),
            "tags": synonym("_tags"),
            "_notes": relationship(
                Note,
                primaryjoin=tables.entities.c.id==tables.notes.c.entity_id,
                backref="entity",
            ),
            "notes": synonym("_notes"),
        }
    )
    
    
    
    # User
    mapper(
        User,
        tables.users,
        inherits=User.__base__,
        inherit_condition=tables.users.c.id==tables.entities.c.id,
        polymorphic_identity=User.entity_type,
        properties={
            "enitites_created": synonym("_entities_created"),
            "enitites_updated": synonym("_entities_updated"),
            "department": synonym("_department"),
            "_name": tables.simpleEntities.c.name,
            "name": synonym("_name"),
            "_first_name": tables.users.c.first_name,
            "first_name": synonym("_first_name"),
            "_last_name": tables.users.c.last_name,
            "last_name": synonym("_last_name"),
            "_initials": tables.users.c.initials,
            "initials": synonym("_initials"),
            "_email": tables.users.c.email,
            "email": synonym("_email"),
            "_password": tables.users.c.password,
            "password": synonym("_password"),
            "_last_login": tables.users.c.last_login,
            "last_login": synonym("_last_login"),
        },
    )
    
    
    
    # Department
    mapper(
        Department,
        tables.departments,
        inherits=Department.__base__,
        inherit_condition=tables.departments.c.id==tables.entities.c.id,
        polymorphic_identity=Department.entity_type,
        properties={
            "_members": relationship(
                User,
                backref="_department",
                primaryjoin=\
                    tables.departments.c.id==tables.users.c.department_id,
            ),
            "members": synonym("_members")
        },
    )
    
    
    
    # Status
    mapper(
        Status,
        tables.statuses,
        inherits=Status.__base__,
        inherit_condition=tables.statuses.c.id==tables.entities.c.id,
        polymorphic_identity=Status.entity_type,
    )
    
    
    
    # StatusList
    mapper(
        StatusList,
        tables.statusLists,
        inherits=StatusList.__base__,
        inherit_condition=tables.statusLists.c.id==tables.entities.c.id,
        polymorphic_identity=StatusList.entity_type,
        properties={
            "_statuses": relationship(
                Status,
                secondary=tables.statusList_statuses
            ),
            "statuses": synonym("_statuses"),
            "_target_entity_type": tables.statusLists.c.target_entity_type,
            "target_entity_type": synonym("_target_entity_type"),
        }
    )
    
    
    
    # Repository
    mapper(
        Repository,
        tables.repositories,
        inherits=Repository.__base__,
        inherit_condition=tables.repositories.c.id==tables.entities.c.id,
        polymorphic_identity=Repository.entity_type,
        properties={
            "_linux_path": tables.repositories.c.linux_path,
            "linux_path": synonym("_linux_path"),
            "_windows_path": tables.repositories.c.windows_path,
            "windows_path": synonym("_windows_path"),
            "_osx_path": tables.repositories.c.osx_path,
            "osx_path": synonym("_osx_path")
        },
        #exclude_properties=["path"]
    )
    
    
    
    # ImageFormat
    mapper(
        ImageFormat,
        tables.imageFormats,
        inherits=ImageFormat.__base__,
        inherit_condition=tables.imageFormats.c.id==tables.entities.c.id,
        polymorphic_identity=ImageFormat.entity_type,
        properties={
            "_width": tables.imageFormats.c.width,
            "width": synonym("_width"),
            "_height": tables.imageFormats.c.height,
            "height": synonym("_height"),
            "_pixel_aspect": tables.imageFormats.c.pixel_aspect,
            "pixel_aspect": synonym("_pixel_aspect"),
            "_print_resolution": tables.imageFormats.c.print_resolution,
            "print_resolution": synonym("print_resolution")
        },
        exclude_properties=["device_aspect"]
    )
    
    
    
    # TypeEntity
    mapper(
        TypeEntity,
        tables.typeEntities,
        inherits=TypeEntity.__base__,
        inherit_condition=tables.typeEntities.c.id==tables.entities.c.id,
        polymorphic_identity=TypeEntity.entity_type,
    )
    
    
    
    # AssetType
    mapper(
        AssetType,
        tables.assetTypes,
        inherits=AssetType.__base__,
        inherit_condition=tables.assetTypes.c.id==tables.typeEntities.c.id,
        polymorphic_identity=AssetType.entity_type,
        properties={
            "_task_types": relationship(
                TaskType,
                secondary=tables.assetType_taskTypes
                ),
            "task_types": synonym("_task_types")
        }
    )
    
    
    
    # LinkType
    mapper(
        LinkType,
        tables.linkTypes,
        inherits=LinkType.__base__,
        inherit_condition=tables.linkTypes.c.id==tables.typeEntities.c.id,
        polymorphic_identity=LinkType.entity_type,
    )
    
    
    
    # ProjectType
    mapper(
        ProjectType,
        tables.projectTypes,
        inherits=ProjectType.__base__,
        inherit_condition=tables.projectTypes.c.id==tables.typeEntities.c.id,
        polymorphic_identity=ProjectType.entity_type,
    )
    
    
    
    # TaskType
    mapper(
        TaskType,
        tables.taskTypes,
        inherits=TaskType.__base__,
        inherit_condition=tables.taskTypes.c.id==tables.entities.c.id,
        polymorphic_identity=TaskType.entity_type,
    )
    
    
    
    # TypeTemplate
    mapper(
        TypeTemplate,
        tables.typeTemplates,
        inherits=TypeTemplate.__base__,
        inherit_condition=tables.typeTemplates.c.id==tables.entities.c.id,
        polymorphic_identity=TypeTemplate.entity_type,
        properties={
            "_path_code": tables.typeTemplates.c.path_code,
            "path_code": synonym("_path_code"),
            "_file_code": tables.typeTemplates.c.file_code,
            "file_code": synonym("_file_code"),
            "_type": relationship(
                TypeEntity,
                primaryjoin=\
                    tables.typeTemplates.c.type_id==tables.typeEntities.c.id
                ),
            "type": synonym("_type"),
        },
    )
    
    
    
    # Structure
    mapper(
        Structure,
        tables.structures,
        inherits=Structure.__base__,
        inherit_condition=tables.structures.c.id==tables.entities.c.id,
        polymorphic_identity=Structure.entity_type,
        properties={
            "_project_template": tables.structures.c.project_template,
            "project_template": synonym("_project_template"),
            "_asset_templates": relationship(
                TypeTemplate,
                secondary=tables.structure_assetTemplates,
                primaryjoin=\
                    tables.structures.c.id==\
                    tables.structure_assetTemplates.c.structure_id,
                secondaryjoin=
                    tables.structure_assetTemplates.c.typeTemplate_id==\
                    tables.typeTemplates.c.id
            ),
            "asset_templates": synonym("_asset_templates"),
            "_reference_templates": relationship(
                TypeTemplate,
                secondary=tables.structure_referenceTemplates,
                primaryjoin=\
                    tables.structures.c.id==\
                    tables.structure_referenceTemplates.c.structure_id,
                secondaryjoin=
                    tables.structure_referenceTemplates.c.typeTemplate_id==\
                    tables.typeTemplates.c.id
            ),
            "reference_templates": synonym("_reference_templates"),
        },
    )
    
    
    
    # Links
    mapper(
        Link,
        tables.links,
        inherits=Link.__base__,
        inherit_condition=tables.links.c.id==tables.entities.c.id,
        polymorphic_identity=Link.entity_type,
        properties={
            "_path": tables.links.c.path,
            "path": synonym("_path"),
            "_filename": tables.links.c.filename,
            "filename": synonym("_filename"),
            "_type": relationship(
                LinkType,
                primaryjoin=\
                    tables.links.c.type_id==tables.linkTypes.c.id
            ),
            "type": synonym("_type"),
        },
    )
    
    
    
    
    # Notes
    mapper(
        Note,
        tables.notes,
        inherits=Note.__base__,
        inherit_condition=tables.notes.c.id==tables.simpleEntities.c.id,
        polymorphic_identity=Note.entity_type,
        properties={
            "_content": tables.notes.c.content,
            "content": synonym("_content"),
        }
    )
    
    
    
    # Project - also the first implemented class using the mixins
    project_mapper_arguments = dict(
        inherits=Project.__base__,
        polymorphic_identity=Project.entity_type,
        inherit_condition=tables.projects.c.id==tables.entities.c.id,
        properties={
            "_lead": relationship(
                User,
                primaryjoin=tables.projects.c.lead_id==tables.users.c.id,
            ),
            "lead": synonym("_lead"),
            "_repository": relationship(
                Repository,
                primaryjoin=tables.projects.c.repository_id==\
                            tables.repositories.c.id
            ),
            "repository": synonym("repository"),
            "_type": relationship(
                ProjectType,
                primaryjoin=tables.projects.c.type_id==tables.projectTypes.c.id
            ),
            "type": synonym("_type"),
            "_structure": relationship(
                Structure,
                primaryjoin=tables.projects.c.structure_id==\
                            tables.structures.c.id
            ),
            "structure": synonym("_structure"),
            "_image_format": relationship(
                ImageFormat,
                primaryjoin=tables.projects.c.image_format_id==\
                            tables.imageFormats.c.id
            ),
            "image_format": synonym("_image_format"),
            "_fps": tables.projects.c.fps,
            "fps": synonym("_fps"),
            "_is_stereoscopic": tables.projects.c.is_stereoscopic,
            "is_stereoscopic": synonym("_is_stereoscopic"),
            "_display_width": tables.projects.c.display_width,
            "display_width": synonym("_display_width"),
        }
    )
    
    # mix it with ReferenceMixin first
    ReferenceMixinDB.setup(Project, tables.projects, project_mapper_arguments)
    
    # then to the StatusMixin
    StatusMixinDB.setup(Project, tables.projects, project_mapper_arguments)
    
    # then to the ScheduleMixin
    ScheduleMixinDB.setup(Project, tables.projects, project_mapper_arguments)
    
    # then to the TaskMixin
    TaskMixinDB.setup(Project, tables.projects, project_mapper_arguments)
    
    mapper(
        Project,
        tables.projects,
        **project_mapper_arguments
    )
    
    
    
    # Task
    # WARNING: Not finished, it is a temporary implementation, created to be
    # able to test other classes
    
    task_mapper_arguments = dict(
        inherits=Task.__base__,
        polymorphic_identity=Task.entity_type,
        inherit_condition=tables.tasks.c.id==tables.entities.c.id
    )
    
    # mix it with StatusMixin
    StatusMixinDB.setup(Task, tables.tasks, task_mapper_arguments)
    
    # and then ScheduleMixin
    ScheduleMixinDB.setup(Task, tables.tasks, task_mapper_arguments)
    
    mapper(
        Task,
        tables.tasks,
        **task_mapper_arguments
    )
    
    
    
    # Asset
    # WARNING: Not completely implemented
    asset_mapper_arguments = dict(
        inherits=Asset.__base__,
        polymorphic_identity=Asset.entity_type,
        inherit_condition=tables.assets.c.id==tables.entities.c.id,
        properties={
            "_type": relationship(
                AssetType,
                primaryjoin=\
                    tables.assets.c.type_id==tables.assetTypes.c.id
            ),
            "type": synonym("_type"),
        }
    )
    
    
    # mix it with ReferenceMixin
    ReferenceMixinDB.setup(Asset, tables.assets, asset_mapper_arguments)
    
    # then with StatusMixin
    StatusMixinDB.setup(Asset, tables.assets, asset_mapper_arguments)
    
    # then with TaskMixin
    TaskMixinDB.setup(Asset, tables.assets, asset_mapper_arguments)
    
    # complete mapping
    mapper(Asset, tables.assets, **asset_mapper_arguments)
    
    
    
    # Shot
    shot_mapper_arguments = dict(
        inherits=Shot.__base__,
        inherit_condition=tables.shots.c.id==tables.entities.c.id,
        polymorphic_identity=Shot.entity_type,
        properties={
            "_assets": relationship(
                Asset,
                secondary=tables.shot_assets,
                primaryjoin=tables.shots.c.id==\
                    tables.shot_assets.c.shot_id,
                secondaryjoin=tables.shot_assets.c.asset_id==\
                    tables.assets.c.id
            ),
            "assets": synonym("_assets"),
            "_sequence": relationship(
                Sequence,
                primaryjoin=tables.shots.c.sequence_id==\
                    tables.sequences.c.id
            ),
            "sequence": synonym("_sequence"),
            "_cut_in": tables.shots.c.cut_in,
            "cut_in": synonym("_cut_in"),
            "_cut_duration": tables.shots.c.cut_duration,
            "cut_duration": synonym("_cut_duration"),
            "_code": tables.simpleEntities.c.code, # overloaded attribute
            "code": synonym("_code"), # overloaded property
        }
    )
    
    # mix it with ReferenceMixin
    ReferenceMixinDB.setup(Shot, tables.shots, shot_mapper_arguments)
    
    # then with StatusMixin
    StatusMixinDB.setup(Shot, tables.shots, shot_mapper_arguments)
    
    # then with TaskMixin
    TaskMixinDB.setup(Shot, tables.shots, shot_mapper_arguments)
    
    #print shot_mapper_arguments
    
    # complete mapping
    mapper(Shot, tables.shots, **shot_mapper_arguments)
    
    
    
    # Sequence
    sequence_mapper_arguments = dict(
        inherits=Sequence.__base__,
        polymorphic_identity=Sequence.entity_type,
        inherit_condition=tables.sequences.c.id==tables.entities.c.id,
        properties={
            "_project": relationship(
                Project,
                primaryjoin=tables.sequences.c.project_id==\
                    tables.projects.c.id
            ),
            "project": synonym("project"),
            "_shots": relationship(
                Shot,
                primaryjoin=tables.shots.c.sequence_id==\
                    tables.sequences.c.id,
                uselist=True,
            )
        }
    )
    
    # mix it with ReferenceMixin, StatusMixin and ScheduleMixin
    ReferenceMixinDB.setup(Sequence, tables.sequences,
                           sequence_mapper_arguments)
    
    StatusMixinDB.setup(Sequence, tables.sequences, sequence_mapper_arguments)
    
    ScheduleMixinDB.setup(Sequence, tables.sequences,
                          sequence_mapper_arguments)
    
    TaskMixinDB.setup(Sequence, tables.sequences, sequence_mapper_arguments)
    
    mapper(Sequence, tables.sequences, **sequence_mapper_arguments)
    

