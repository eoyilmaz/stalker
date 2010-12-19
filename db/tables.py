#-*- coding: utf-8 -*-
"""
this file contains the tags table
"""



from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey


#create the metadata
metadata = MetaData()

# create tables

# TAG
tags_table = Table(
    'tags', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(128))
    )



# SIMPLE ENTITY
simpleEntity_table = Table(
    'simpleEntities', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(256)),
    Column('description', String),
    Column('tags', ForeignKey('tags.id'))
    )

