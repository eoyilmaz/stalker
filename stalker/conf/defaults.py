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
ADMIN_NAME = 'Admin'
ADMIN_LOGIN = 'admin'
ADMIN_CODE = 'adm'
ADMIN_PASSWORD = 'admin'
ADMIN_EMAIL = 'admin@admin.com'
ADMIN_DEPARTMENT_NAME = 'admins'
ADMIN_GROUP_NAME = 'admins'


# the default keyword which is going to be used in password scrambling
KEY = "stalker_default_key"

VERSION_TAKE_NAME = "Main"

TICKET_LABEL = "Ticket"

ACTIONS = ['Add', 'View', 'Edit', 'Delete']

STATUS_BG_COLOR = 0xffffff
STATUS_FG_COLOR = 0x000000

# Task Management
TIME_RESOLUTION = datetime.timedelta(hours=1)
TASK_DURATION = datetime.timedelta(days=10)
TASK_PRIORITY = 500

WORKING_HOURS = {
  'mon': [[570, 1110]], # 9:30 - 18:30
  'tue': [[570, 1110]], # 9:30 - 18:30
  'wed': [[570, 1110]], # 9:30 - 18:30
  'thu': [[570, 1110]], # 9:30 - 18:30
  'fri': [[570, 1110]], # 9:30 - 18:30
  'sat': [], # saturday off
  'sun': [], # sunday off
}

DAY_ORDER = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']

DAILY_WORKING_HOURS = 8

