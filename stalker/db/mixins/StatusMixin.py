#-*- coding: utf-8 -*-
"""This module contains the database mappers and tables for StatusMixin.

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
from stalker.core.models import status



#----------------------------------------------------------------------
def setup(class_, class_table, mapper_arguments={}):
    """creates the necessary tables and properties for the mappers for the
    mixed in class
    
    use the returning dictionary (mapper_arguments) in your mapper
    
    :param class_: the mixed in class, in other words the class which will be
      extended with the mixin functionalities
     
    :param class_table: the table holding the information about the class
    
    :param mapper_arguments: incoming mapper arugments for the
      SQLAlchemy.Orm.Mapper, it will be updated with the properties of the
      current mixin
    
    :returns: a dictionary holding the mapper_arguments
    """
    
    class_name = class_.__name__
    
    # update the given class table with new columns
    class_table.append_column(
        Column("status", Integer, default=0),
    )
    
    class_table.append_column(
        Column(
            "status_list_id",
            Integer,
            ForeignKey(tables.statusLists.c.id),
            nullable=False
        )
    )
    
    new_properties = {
        "_status": class_table.c.status,
        "status": synonym("_status"),
        "_status_list": relationship(
            status.StatusList,
            primaryjoin=\
            class_table.c.status_list_id==\
            tables.statusLists.c.id
        ),
        "status_list": synonym("_status_list"),
    }
    
    try:
        mapper_arguments["properties"].update(new_properties)
    except KeyError:
        mapper_arguments["properties"] = new_properties
    
    return mapper_arguments









