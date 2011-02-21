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
    "stalker.core.models.Asset",
    "stalker.core.models.Booking",
    "stalker.core.models.Comment",
    "stalker.core.models.Department",
    "stalker.core.models.SimpleEntity",
    "stalker.core.models.Entity",
    "stalker.core.models.TypeEntity",
    "stalker.core.models.Group",
    "stalker.core.models.ImageFormat",
    "stalker.core.models.Link",
    "stalker.core.models.Message",
    "stalker.core.models.Note",
    "stalker.core.models.Project",
    "stalker.core.models.Repository",
    "stalker.core.models.Sequence",
    "stalker.core.models.Shot",
    "stalker.core.models.Status",
    "stalker.core.models.StatusList",
    "stalker.core.models.Structure",
    "stalker.core.models.Tag",
    "stalker.core.models.Task",
    "stalker.core.models.TaskType",
    "stalker.core.models.AssetType",
    "stalker.core.models.LinkType",
    "stalker.core.models.ProjectType",
    "stalker.core.models.TypeTemplate",
    "stalker.core.models.User",
    "stalker.core.models.Version",
]