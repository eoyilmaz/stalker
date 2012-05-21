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


#PC Video (640, 480, 1.0)
#NTSC (720, 486, 0.91)
#NTSC 16:9 (720, 486, 1.21)
#PAL (720, 576, 1.067)
#PAL 16:9 (720, 576, 1.46)
#HD 720 (1280, 720, 1.0)
#HD 1080 (1920, 1080, 1.0)
#1K Super 35 (1024, 778, 1.0)
#2K Super 35 (2048, 1556, 1.0)
#4K Super 35 (4096, 3112, 1.0)
#A4 Portrait (2480, 3508, 1.0)
#A4 Landscape (3508, 2480, 1.0)
#A3 Portrait (3508, 4960, 1.0)
#A3 Landscape (4960, 3508, 1.0)
#A2 Portrait (4960, 7016, 1.0)
#A2 Landscape (7016, 4960, 1.0)
#50x70cm Poster Portrait (5905, 8268, 1.0)
#50x70cm Poster Landscape (8268, 5905, 1.0)
#70x100cm Poster Portrait (8268, 11810, 1.0)
#70x100cm Poster Landscape (11810, 8268, 1.0)
#1k Square (1024, 1024, 1.0)
#2K Square (2048, 2048, 1.0)
#3K Square (3072, 3072, 1.0)
#4K Square (4096, 4096, 1.0)
