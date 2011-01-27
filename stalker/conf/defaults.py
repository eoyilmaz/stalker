#-*- coding: utf-8 -*-

#
# The default database addres
# 
DATABASE = "sqlite:///:memory:"


#
# The default settings for the database, see sqlalchemy.create_engine for
# possible parameters
# 
DATABASE_ENGINE_SETTINGS = {
    "echo": False
}


DATABASE_SESSION_SETTINGS ={}

STUDIO_DATABASE= "sqlite:///:memory:"
PROJECT_DATABASE = "sqlite:///:memory:"

#
# Tells Stalker to create an admin by default
#
AUTO_CREATE_ADMIN = True

# 
# these are for new projects
# after creating the project you can change them from the interface
# 
ADMIN_NAME = "admin"
ADMIN_PASSWORD = "admin"
ADMIN_EMAIL = "admin@admin.com"
ADMIN_DEPARTMENT_NAME = "admins"


# the default keyword which is going to be used in password scrambling
KEY = "stalker_default_key"


#
# The default mapper module, see docs for mappers for complete description of
# mappers
#
MAPPERS = [
    "stalker.db.mapper",
]


CORE_MODEL_CLASSES = [
    "stalker.core.models.asset.Asset",
    "stalker.core.models.assetBase.AssetBase",
    "stalker.core.models.booking.Booking",
    "stalker.core.models.comment.Comment",
    "stalker.core.models.department.Department",
    "stalker.core.models.entity.SimpleEntity",
    "stalker.core.models.entity.Entity",
    "stalker.core.models.entity.TypeEntity",
    "stalker.core.models.group.Group",
    "stalker.core.models.imageFormat.ImageFormat",
    "stalker.core.models.link.Link",
    "stalker.core.models.message.Message",
    "stalker.core.models.note.Note",
    "stalker.core.models.pipelineStep.PipelineStep",
    "stalker.core.models.project.Project",
    "stalker.core.models.repository.Repository",
    "stalker.core.models.sequence.Sequence",
    "stalker.core.models.shot.Shot",
    "stalker.core.models.status.Status",
    "stalker.core.models.status.StatusList",
    "stalker.core.models.structure.Structure",
    "stalker.core.models.tag.Tag",
    "stalker.core.models.task.Task",
    "stalker.core.models.types.AssetType",
    "stalker.core.models.types.LinkType",
    "stalker.core.models.types.ProjectType",
    "stalker.core.models.types.TypeTemplate",
    "stalker.core.models.user.User",
    "stalker.core.models.version.Version",
]