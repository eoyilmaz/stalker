#-*- coding: utf-8 -*-


#DATABASE = 'sqlite:///:memory:'
DATABASE = 'sqlite:////home/ozgur/stalker_test.db'
STUDIO_DATABASE= 'sqlite:///:memory:'
PROJECT_DATABASE = 'sqlite:///:memory:'

# 
# these are for new projects
# after creating the project you can change them from the interface
# 
SUPERUSER_NAME = 'admin'
SUPERUSER_EMAIL = 'admin@admin.com'


# the default keyword which is going to be used in password scrambling
KEY = "stalker_default_key"


## objects to tables list
#OBJECT_TO_TABLE = [
    #("stalker.models.tag.Tag",
     #"stalker.db.tables.tags_table"
     #"properties={tags_table}"),
    #("stalker.models.entity.SimpleEntity", "stalker.db.tables.tags_table",""),
#]


MAPPERS = [
'stalker.db.mapper'
]