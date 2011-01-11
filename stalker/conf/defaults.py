#-*- coding: utf-8 -*-
import tempfile

#
# The default database addres
# 
DATABASE = 'sqlite:///:memory:'


#
# The default settings for the database, see sqlalchemy.create_engine for
# possible parameters
# 
DATABASE_ENGINE_SETTINGS = {
    'echo':False,
}


DATABASE_SESSION_SETTINGS ={}

STUDIO_DATABASE= 'sqlite:///:memory:'
PROJECT_DATABASE = 'sqlite:///:memory:'

#
# Tells Stalker to create an admin by default
#
AUTO_CREATE_ADMIN = True

# 
# these are for new projects
# after creating the project you can change them from the interface
# 
ADMIN_NAME = 'admin'
ADMIN_PASSWORD = 'admin'
ADMIN_EMAIL = 'admin@admin.com'
ADMIN_DEPARTMENT_NAME = 'admins'


# the default keyword which is going to be used in password scrambling
KEY = "stalker_default_key"


#
# The default mapper module, see docs for mappers for complete description of
# mappers
#
MAPPERS = [
'stalker.db.mapper'
]

