#-*- coding: utf-8 -*-



STUDIO_DATABASE_ENGINE= 'sqlite3'
STUDIO_DATABASE_NAME = 'stalker_studio.db'
PROJECT_DATABASE_ENGINE = 'sqlite3'
PROJECT_DATABASE_NAME = ''

# 
# these are for new projects
# after creating the project you can change them from the interface
# 
SUPERUSER_NAME = 'admin'
SUPERUSER_EMAIL = 'admin@admin.com'


# the keyword that is going to be used in password scrambling
KEY = "stalker_default_key"


# objects to tables list
OBJECT_TO_TABLE = [
    ("stalker.models.tag.Tag", "stalker.db.tables.tags_table"),
    ("stalker.models.entity.SimpleEntity", "stalker.db.tables.tags_table"),
]


