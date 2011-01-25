#-*- coding: utf-8 -*-
"""This module contains the database mappers and tables for Mixins.

See examples/extending/great_entity.py for an example.
"""


from sqlalchemy.orm import relationship, synonym
from sqlalchemy import (
    Table,
    Column,
    Integer,
    ForeignKey,
)
from stalker import db
from stalker.db import tables
from stalker.core.models import link



#----------------------------------------------------------------------
def setup(class_, class_table):
    """creates the tables for the given mixed in class
    """
    
    
    class_name = class_.__name__
    
    # ReferenceMixin Columns
    columns = []
    
    # ReferenceMixin Properties
    properties = {}
    
    # ReferenceMixin Options
    options = {}
    
    # there is no extra columns in the base table so we don't need to update
    # the given class_table
    
    # use the given class_name and the table_name
    secondary_table = Table(
        class_name.lower() + "_references", db.metadata,
        Column(
            class_name.lower() + "_id",
            Integer,
            ForeignKey(class_table.c.id),
            primary_key=True,
        ),
        
        Column(
            "reference_id",
            Integer,
            ForeignKey(tables.links.c.id),
            primary_key=True,
        )
    )
    
    
    properties = {
        "_references": relationship(
            link.Link,
            secondary=secondary_table,
            primaryjoin=\
                class_table.c.id==\
                eval("secondary_table.c." + class_name.lower() + "_id"),
            secondaryjoin=\
                secondary_table.c.reference_id==\
                tables.links.c.id,
        ),
        "references": synonym("_references"),
    }
    
    
    class ReturnData(object):
        pass
    
    data = ReturnData()
    
    data.properties = properties
    data.options = options
    
    return data









