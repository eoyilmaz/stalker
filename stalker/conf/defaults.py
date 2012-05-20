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
ADMIN_GROUP_NAME = 'admins'


# the default keyword which is going to be used in password scrambling
KEY = "stalker_default_key"

DEFAULT_TASK_DURATION = datetime.timedelta(days=10)
DEFAULT_TASK_PRIORITY = 500

DEFAULT_VERSION_TAKE_NAME = "MAIN"

DEFAULT_TICKET_LABEL = "Ticket"

DEFAULT_ACTIONS = ['Add', 'View', 'Edit', 'Delete']

