#-*- coding: utf-8 -*-
"""this is the default mapper to map the default models to the default tables

You can use your also use your own mappers. See the docs.
"""



from sqlalchemy.orm import mapper, relationship, backref, synonym
from stalker.db import tables
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
    
    # SimpleEntity
    mapper(
        entity.SimpleEntity,
        tables.simpleEntities,
        properties={
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
                uselist=False
            ),
            "created_by": synonym("_created_by"),
            "_updated_by": relationship(
                user.User,
                backref="_entities_updated",
                primaryjoin=tables.simpleEntities.c.updated_by_id== \
                            tables.users.c.id,
                post_update=True,
                uselist=False
            ),
            "updated_by": synonym("_updated_by"),
            "_date_created": tables.simpleEntities.c.date_created,
            "date_created": synonym("_date_created"),
            "_date_updated": tables.simpleEntities.c.date_updated,
            "date_updated": synonym("_date_updated")
        },
        polymorphic_on=tables.simpleEntities.c.entity_type,
        polymorphic_identity="SimpleEntity"
    )
    
    
    
    # Tag
    mapper(
        tag.Tag,
        tables.tags,
        inherits=entity.SimpleEntity,
        polymorphic_identity="Tag"
    )
    
    
    
    # Entity
    mapper(
        entity.Entity,
        tables.entities,
        inherits=entity.SimpleEntity,
        inherit_condition=tables.entities.c.id==tables.simpleEntities.c.id,
        polymorphic_identity="Entity",
        properties={
            "_tags": relationship(
                tag.Tag,
                secondary=tables.entity_tags,
                backref="_entities"
            ),
            "tags": synonym("_tags")
        }
    )
    
    
    
    # User
    mapper(
        user.User,
        tables.users,
        inherits=entity.Entity,
        inherit_condition=tables.users.c.id==tables.entities.c.id,
        polymorphic_identity="User",
        properties={
            "enitites_created": synonym("_entities_created"),
            "enitites_updated": synonym("_entities_updated"),
            "department": synonym("_department"),
            "_email": tables.users.c.email,
            "email": synonym("_email"),
            "_first_name": tables.users.c.first_name,
            "first_name": synonym("_first_name"),
            "_last_name": tables.users.c.last_name,
            "last_name": synonym("_last_name"),
            "_login_name": tables.users.c.login_name,
            "loing_name": synonym("_login_name"),
            "_password": tables.users.c.password,
            "password": synonym("_password"),
        },
    )
    
    
    
    # Department
    mapper(
        department.Department,
        tables.departments,
        inherits=entity.Entity,
        inherit_condition=tables.departments.c.id==tables.entities.c.id,
        polymorphic_identity="Department",
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
        inherits=entity.Entity,
        inherit_condition=tables.statuses.c.id==tables.entities.c.id,
        polymorphic_identity="Status",
        properties={
            "_short_name": tables.statuses.c.short_name,
            "short_name": synonym("_short_name")
        }
    )
    
    
    
    # StatusList
    mapper(
        status.StatusList,
        tables.statusLists,
        inherits=entity.Entity,
        inherit_condition=tables.statusLists.c.id==tables.entities.c.id,
        polymorphic_identity="StatusLists",
        properties={
            "_statuses": relationship(
                status.Status,
                secondary=tables.statusList_statuses
            ),
            "statuses": synonym("_statuses")
        }
    )
    
    
    
    # Repository
    mapper(
        repository.Repository,
        tables.repositories,
        inherits=entity.Entity,
        inherit_condition=tables.repositories.c.id==tables.entities.c.id,
        polymorphic_identity="Repository",
        properties={
            "_linux_path": tables.repositories.c.linux_path,
            "linux_path": synonym("_linux_path"),
            "_windows_path": tables.repositories.c.windows_path,
            "windows_path": synonym("_windows_path"),
            "_osx_path": tables.repositories.c.osx_path,
            "osx_path": synonym("_osx_path")
        },
        exclude_properties=["path"]
    )
    
    
    
    # ImageFormat
    mapper(
        imageFormat.ImageFormat,
        tables.imageFormats,
        inherits=entity.Entity,
        inherit_condition=tables.imageFormats.c.id==tables.entities.c.id,
        polymorphic_identity="ImageFormat",
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
        inherits=entity.Entity,
        inherit_condition=tables.typeEntities.c.id==tables.entities.c.id,
        polymorphic_identity="TypeEntity",
    )
    
    
    
    # AssetType
    mapper(
        types.AssetType,
        tables.assetTypes,
        inherits=entity.TypeEntity,
        inherit_condition=tables.assetTypes.c.id==tables.typeEntities.c.id,
        polymorphic_identity="AssetType",
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
        inherits=entity.TypeEntity,
        inherit_condition=tables.linkTypes.c.id==tables.typeEntities.c.id,
        polymorphic_identity="LinkType",
    )
    
    
    
    # ProjectType
    mapper(
        types.ProjectType,
        tables.projectTypes,
        inherits=entity.TypeEntity,
        inherit_condition=tables.projectTypes.c.id==tables.typeEntities.c.id,
        polymorphic_identity="ProjectType",
    )
    
    
    
    # PipelineStep
    mapper(
        pipelineStep.PipelineStep,
        tables.pipelineSteps,
        inherits=entity.Entity,
        inherit_condition=tables.pipelineSteps.c.id==tables.entities.c.id,
        polymorphic_identity="PipelineStep",
        properties={
            "_code": tables.pipelineSteps.c.code,
            "code": synonym("_code")
        }
    )
    
    
    
    # TypeTemplate
    mapper(
        types.TypeTemplate,
        tables.typeTemplates,
        inherits=entity.Entity,
        inherit_condition=tables.typeTemplates.c.id==tables.entities.c.id,
        polymorphic_identity="TypeTemplate",
        properties={
            "_path_code": tables.typeTemplates.c.path_code,
            "path_code": synonym("_path_code"),
            "_file_code": tables.typeTemplates.c.file_code,
            "file_code": synonym("file_code"),
            "_type": relationship(
                entity.TypeEntity,
                primaryjoin=\
                    tables.typeTemplates.c.type_id==tables.typeEntities.c.id
                ),
            "type_": synonym("_type"),
        },
    )
    
    
    
    # Structure
    mapper(
        structure.Structure,
        tables.structures,
        inherits=entity.Entity,
        inherit_condition=tables.structures.c.id==tables.entities.c.id,
        polymorphic_identity="Structure",
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
        inherits=entity.Entity,
        inherit_condition=tables.links.c.id==tables.entities.c.id,
        polymorphic_identity="Link",
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
            "type_": synonym("_type"),
        },
    )
    
    
    
    
    
    