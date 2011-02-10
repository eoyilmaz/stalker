#-*- coding: utf-8 -*-
"""contains helper classes which helps mixed in classes table and mapper setups
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
from stalker.core.models import link, status






########################################################################
class ReferenceMixinDB(object):
    """A helper class for ReferenceMixin table and mapper setup.
    
    Helps setting up tables and mappers for classes mixed in with
    :class:`~stalker.core.models.mixin.ReferenceMixin`
    
    See examples/extending/great_entity.py for an example.
    """
    
    #----------------------------------------------------------------------
    @classmethod
    def setup(cls, class_, class_table, mapper_arguments={}):
        """creates the necessary tables and properties for the mappers for the
        mixed in class
        
        use the returning dictionary (mapper_arguments) in your mapper
        
        :param class_: the mixed in class, in other words the class which will
          be extended with the mixin functionalities
         
        :param class_table: the table holding the information about the class
        
        :param mapper_arguments: incoming mapper arugments for the
          SQLAlchemy.Orm.Mapper, it will be updated with the properties of the
          current mixin
        
        :returns: a dictionary holding the mapper_arguments
        """
        
        class_name = class_.__name__
        
        # there is no extra columns in the base table so we don't need to update
        # the given class_table
        
        # use the given class_name and the class_table
        secondary_table_name = class_name.lower() + "_references"
        secondary_table = None
        
        # check if the table is already defined
        if secondary_table_name not in db.metadata:
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
        else:
            secondary_table = db.metadata.tables[secondary_table_name]
        
        new_properties = {
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
        
        try:
            mapper_arguments["properties"].update(new_properties)
        except KeyError:
            mapper_arguments["properties"] = new_properties
        
        return mapper_arguments






########################################################################
class StatusMixinDB(object):
    """A helper class for StatusMixin table and mapper setup.
    
    Helps setting up tables and mappers for classes mixed in with
    :class:`~stalker.core.models.mixin.StatusMixin`
    
    See examples/extending/statused_entity.py for an example.
    """
    
    
    
    #----------------------------------------------------------------------
    @classmethod
    def setup(cls, class_, class_table, mapper_arguments={}):
        """creates the necessary tables and properties for the mappers for the
        mixed in class
        
        use the returning dictionary (mapper_arguments) in your mapper
        
        :param class_: the mixed in class, in other words the class which will
          be extended with the mixin functionalities
         
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