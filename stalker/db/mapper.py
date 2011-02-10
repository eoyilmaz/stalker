#-*- coding: utf-8 -*-
"""this is the default mapper to map the default models to the default tables

You can use your also use your own mappers. See the docs.
"""



from sqlalchemy.orm import mapper, relationship, backref, synonym
from stalker.db import tables
from stalker.db.mixin import ReferenceMixinDB, StatusMixinDB
from stalker.core.models import (
    asset,
    assetBase,
    booking,
    comment,
    department,
    entity,
    group,
    imageFormat,
    pipelineStep,
    project,
    link,
    mixin,
    note,
    repository,
    sequence,
    shot,
    status,
    structure,
    tag,
    task,
    types,
    user,
    version
)



#----------------------------------------------------------------------
def setup():
    """setups the mapping
    """
    
    # Entity_Type_IDs
    
    
    # SimpleEntity
    mapper(
        entity.SimpleEntity,
        tables.simpleEntities,
        properties={
            "_code": tables.simpleEntities.c.code,
            "code": synonym("_code"),
            "_name": tables.simpleEntities.c.name,
            "name": synonym("_name"),
            "_description": tables.simpleEntities.c.description,
            "description": synonym("_description"),
            "_created_by": relationship(
                user.User,
                backref="_entities_created",
                primaryjoin=tables.simpleEntities.c.created_by_id== \
                            tables.users.c.id,
                post_update=True,
                #uselist=False
            ),
            "created_by": synonym("_created_by"),
            "_updated_by": relationship(
                user.User,
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
        polymorphic_identity=entity.SimpleEntity.entity_type
    )
    
    
    
    # Tag
    mapper(
        tag.Tag,
        tables.tags,
        inherits=tag.Tag.__base__,
        polymorphic_identity=tag.Tag.entity_type
    )
    
    
    
    # Entity
    mapper(
        entity.Entity,
        tables.entities,
        inherits=entity.Entity.__base__,
        inherit_condition=tables.entities.c.id==tables.simpleEntities.c.id,
        polymorphic_identity=entity.Entity.entity_type,
        properties={
            "_tags": relationship(
                tag.Tag,
                secondary=tables.entity_tags,
                backref="entities"
            ),
            "tags": synonym("_tags"),
            "_notes": relationship(
                note.Note,
                primaryjoin=tables.entities.c.id==tables.notes.c.entity_id,
                backref="entity",
            ),
            "notes": synonym("_notes"),
        }
    )
    
    
    
    # User
    mapper(
        user.User,
        tables.users,
        inherits=user.User.__base__,
        inherit_condition=tables.users.c.id==tables.entities.c.id,
        polymorphic_identity=user.User.entity_type,
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
            "last_login": synonym("last_login"),
        },
    )
    
    
    
    # Department
    mapper(
        department.Department,
        tables.departments,
        inherits=department.Department.__base__,
        inherit_condition=tables.departments.c.id==tables.entities.c.id,
        polymorphic_identity=department.Department.entity_type,
        properties={
            "_members": relationship(
                user.User,
                backref="_department",
                primaryjoin=\
                    tables.departments.c.id==tables.users.c.department_id,
            ),
            "members": synonym("_members")
        },
    )
    
    
    
    # Status
    mapper(
        status.Status,
        tables.statuses,
        inherits=status.Status.__base__,
        inherit_condition=tables.statuses.c.id==tables.entities.c.id,
        polymorphic_identity=status.Status.entity_type,
    )
    
    
    
    # StatusList
    mapper(
        status.StatusList,
        tables.statusLists,
        inherits=status.StatusList.__base__,
        inherit_condition=tables.statusLists.c.id==tables.entities.c.id,
        polymorphic_identity=status.StatusList.entity_type,
        properties={
            "_statuses": relationship(
                status.Status,
                secondary=tables.statusList_statuses
            ),
            "statuses": synonym("_statuses"),
            "_target_entity_type": tables.statusLists.c.target_entity_type,
            "target_entity_type": synonym("_target_entity_type"),
        }
    )
    
    
    
    # Repository
    mapper(
        repository.Repository,
        tables.repositories,
        inherits=repository.Repository.__base__,
        inherit_condition=tables.repositories.c.id==tables.entities.c.id,
        polymorphic_identity=repository.Repository.entity_type,
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
        imageFormat.ImageFormat,
        tables.imageFormats,
        inherits=imageFormat.ImageFormat.__base__,
        inherit_condition=tables.imageFormats.c.id==tables.entities.c.id,
        polymorphic_identity=imageFormat.ImageFormat.entity_type,
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
        entity.TypeEntity,
        tables.typeEntities,
        inherits=entity.TypeEntity.__base__,
        inherit_condition=tables.typeEntities.c.id==tables.entities.c.id,
        polymorphic_identity=entity.TypeEntity.entity_type,
    )
    
    
    
    # AssetType
    mapper(
        types.AssetType,
        tables.assetTypes,
        inherits=types.AssetType.__base__,
        inherit_condition=tables.assetTypes.c.id==tables.typeEntities.c.id,
        polymorphic_identity=types.AssetType.entity_type,
        properties={
            "_steps": relationship(
                pipelineStep.PipelineStep,
                secondary=tables.assetType_pipelineSteps
                ),
            "steps": synonym("_steps")
        }
    )
    
    
    
    # LinkType
    mapper(
        types.LinkType,
        tables.linkTypes,
        inherits=types.LinkType.__base__,
        inherit_condition=tables.linkTypes.c.id==tables.typeEntities.c.id,
        polymorphic_identity=types.LinkType.entity_type,
    )
    
    
    
    # ProjectType
    mapper(
        types.ProjectType,
        tables.projectTypes,
        inherits=types.ProjectType.__base__,
        inherit_condition=tables.projectTypes.c.id==tables.typeEntities.c.id,
        polymorphic_identity=types.ProjectType.entity_type,
    )
    
    
    
    # PipelineStep
    mapper(
        pipelineStep.PipelineStep,
        tables.pipelineSteps,
        inherits=pipelineStep.PipelineStep.__base__,
        inherit_condition=tables.pipelineSteps.c.id==tables.entities.c.id,
        polymorphic_identity=pipelineStep.PipelineStep.entity_type,
        #properties={
            #"_code": tables.pipelineSteps.c.code,
            #"code": synonym("_code")
        #}
    )
    
    
    
    # TypeTemplate
    mapper(
        types.TypeTemplate,
        tables.typeTemplates,
        inherits=types.TypeTemplate.__base__,
        inherit_condition=tables.typeTemplates.c.id==tables.entities.c.id,
        polymorphic_identity=types.TypeTemplate.entity_type,
        properties={
            "_path_code": tables.typeTemplates.c.path_code,
            "path_code": synonym("_path_code"),
            "_file_code": tables.typeTemplates.c.file_code,
            "file_code": synonym("_file_code"),
            "_type": relationship(
                entity.TypeEntity,
                primaryjoin=\
                    tables.typeTemplates.c.type_id==tables.typeEntities.c.id
                ),
            "type": synonym("_type"),
        },
    )
    
    
    
    # Structure
    mapper(
        structure.Structure,
        tables.structures,
        inherits=structure.Structure.__base__,
        inherit_condition=tables.structures.c.id==tables.entities.c.id,
        polymorphic_identity=structure.Structure.entity_type,
        properties={
            "_project_template": tables.structures.c.project_template,
            "project_template": synonym("_project_template"),
            "_asset_templates": relationship(
                entity.TypeEntity,
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
                entity.TypeEntity,
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
        link.Link,
        tables.links,
        inherits=link.Link.__base__,
        inherit_condition=tables.links.c.id==tables.entities.c.id,
        polymorphic_identity=link.Link.entity_type,
        properties={
            "_path": tables.links.c.path,
            "path": synonym("_path"),
            "_filename": tables.links.c.filename,
            "filename": synonym("_filename"),
            "_type": relationship(
                types.LinkType,
                primaryjoin=\
                    tables.links.c.type_id==tables.linkTypes.c.id
            ),
            "type": synonym("_type"),
        },
    )
    
    
    
    
    # Notes
    mapper(
        note.Note,
        tables.notes,
        inherits=note.Note.__base__,
        inherit_condition=tables.notes.c.id==tables.simpleEntities.c.id,
        polymorphic_identity=note.Note.entity_type,
        properties={
            "_content": tables.notes.c.content,
            "content": synonym("_content"),
        }
    )
    
    
    
    # Project - also the first class uses the mixins
    project_mapper_arguments = {
        "inherits": project.Project.__base__,
        "polymorphic_identity": project.Project.entity_type,
        "properties": {
            "_start_date": tables.projects.c.start_date,
            "start_date": synonym("_start_date"),
            "_due_date": tables.projects.c.due_date,
            "due_date": synonym("_due_date"),
            "_lead": relationship(
                user.User,
                primaryjoin=tables.projects.c.lead_id==tables.users.c.id,
            ),
            "lead": synonym("_lead"),
            "_repository": relationship(
                repository.Repository,
                primaryjoin=tables.projects.c.repository_id==\
                            tables.repositories.c.id
            ),
            "repository": synonym("repository"),
            "_type": relationship(
                types.ProjectType,
                primaryjoin=tables.projects.c.type_id==tables.projectTypes.c.id
            ),
            "type": synonym("_type"),
            "_structure": relationship(
                structure.Structure,
                primaryjoin=tables.projects.c.structure_id==\
                            tables.structures.c.id
            ),
            "structure": synonym("_structure"),
            "_image_format": relationship(
                imageFormat.ImageFormat,
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
    }
    
    # give it to ReferenceMixin first
    ReferenceMixinDB.setup(project.Project, tables.projects, project_mapper_arguments)
    
    # then to the StatusMixin
    StatusMixinDB.setup(project.Project, tables.projects, project_mapper_arguments)
    
    mapper(
        project.Project,
        tables.projects,
        **project_mapper_arguments
    )