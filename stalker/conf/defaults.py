# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import datetime

#
# The default settings for the database, see sqlalchemy.create_engine for
# possible parameters
# 
DATABASE_ENGINE_SETTINGS = {
    "sqlalchemy.url": "sqlite:///:memory:",
    "sqlalchemy.echo": False,
}

DATABASE_SESSION_SETTINGS = {}

STUDIO_DATABASE = "sqlite:///:memory:"
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
    "stalker.core.models.Department",
    "stalker.core.models.Entity",
    "stalker.core.models.FilenameTemplate",
    "stalker.core.models.ImageFormat",
    "stalker.core.models.Link",
    "stalker.core.models.Message",
    "stalker.core.models.Note",
    "stalker.core.models.PermissionGroup",
    "stalker.core.models.Project",
    "stalker.core.models.Repository",
    "stalker.core.models.Review",
    "stalker.core.models.Sequence",
    "stalker.core.models.Shot",
    "stalker.core.models.SimpleEntity",
    "stalker.core.models.Status",
    "stalker.core.models.StatusList",
    "stalker.core.models.Structure",
    "stalker.core.models.Tag",
    "stalker.core.models.Task",
    "stalker.core.models.Type",
    "stalker.core.models.User",
    "stalker.core.models.Version",
    ]

DEFAULT_TASK_DURATION = datetime.timedelta(days=10)
DEFAULT_TASK_PRIORITY = 500

DEFAULT_VERSION_TAKE_NAME = "MAIN"
