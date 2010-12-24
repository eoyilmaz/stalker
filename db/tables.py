#-*- coding: utf-8 -*-
"""
this file contains the tags table
"""



from sqlalchemy import Table, Column, Integer, String, ForeignKey
from stalker.db import meta

#create the metadata
metadata = meta.metadata

# create tables

# SIMPLE ENTITY
simpleEntities = Table(
    'simpleEntities', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(256)),
    Column('description', String),
    Column('entity_type', String(128), nullable=False),
    )




# TAG
tags = Table(
    'tags', metadata,
    Column(
        'simpleEntity_id',
        ForeignKey('simpleEntities.id'),
        primary_key=True
        )
    )



