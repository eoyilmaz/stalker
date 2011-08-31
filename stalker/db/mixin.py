#-*- coding: utf-8 -*-
"""contains helper classes which helps mixed in classes table and mapper setups
"""



from sqlalchemy.orm import relationship, synonym
from sqlalchemy import (
    Table,
    Column,
    Date,
    Interval,
    ForeignKey,
    Integer,
)
from stalker import db
from stalker.db import tables
from stalker.core.models import Link, Status, StatusList, Task, Project






########################################################################
class ReferenceMixinDB(object):
    """A helper class for ReferenceMixin table and mapper setup.
    
    Helps setting up tables and mappers for classes mixed in with
    :class:`stalker.core.models.ReferenceMixin`
    
    See examples/extending/great_entity.py for an example.
    """
    
    #----------------------------------------------------------------------
    @classmethod
    def setup(cls, class_, class_table, mapper_arguments=None):
        """Creates the necessary tables and properties for the mappers for the mixed in class.
        
        Use the returning dictionary (mapper_arguments) in your mapper.
        
        :param class\_: The mixed in class, in other words the class which will
          be extended with the mixin functionalities
         
        :param class_table: The table holding the information about the class
        
        :param mapper_arguments: Incoming mapper arugments for the
          SQLAlchemy.Orm.Mapper, it will be updated with the properties of the
          current mixin
        
        :type mapper_arguments: dict
        
        :returns: a dictionary holding the mapper_arguments
        """
        
        if mapper_arguments is None:
            mapper_arguments = {}
        
        class_name = class_.__name__
        
        # there is no extra columns in the base table so we don't need to
        # update the given class_table
        
        # use the given class_name and the class_table
        secondary_table_name = class_name + "_References"
        secondary_table = None
        
        # check if the table is already defined
        if secondary_table_name not in db.metadata:
            secondary_table = Table(
                secondary_table_name, db.metadata,
                Column(
                    class_name.lower() + "_id",
                    Integer,
                    ForeignKey(class_table.c.id),
                    primary_key=True,
                ),
                
                Column(
                    "reference_id",
                    Integer,
                    ForeignKey(tables.Links.c.id),
                    primary_key=True,
                )
            )
        else:
            secondary_table = db.metadata.tables[secondary_table_name]
        
        new_properties = {
            "_references": relationship(
                Link,
                secondary=secondary_table,
                primaryjoin=\
                    class_table.c.id==\
                    eval("secondary_table.c." + class_name.lower() + "_id"),
                secondaryjoin=\
                    secondary_table.c.reference_id==\
                    tables.Links.c.id,
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
    :class:`stalker.core.models.StatusMixin`
    
    See examples/extending/statused_entity.py for an example.
    """
    
    
    
    #----------------------------------------------------------------------
    @classmethod
    def setup(cls, class_, class_table, mapper_arguments=None):
        """Creates the necessary tables and properties for the mappers for the mixed in class.
        
        Use the returning dictionary (mapper_arguments) in your mapper.
        
        :param class\_: The mixed in class, in other words the class which will
          be extended with the mixin functionalities
         
        :param class_table: The table holding the information about the class
        
        :param mapper_arguments: Incoming mapper arugments for the
          SQLAlchemy.Orm.Mapper, it will be updated with the properties of the
          current mixin
        
        :type mapper_arguments: dict
        
        :returns: a dictionary holding the mapper_arguments
        """
        
        if mapper_arguments is None:
            mapper_arguments = {}
        
        #class_name = class_.__name__
        
        # update the given class table with new columns
        class_table.append_column(
            Column("status", Integer, default=0),
        )
        
        class_table.append_column(
            Column(
                "status_list_id",
                Integer,
                ForeignKey(tables.StatusLists.c.id),
                nullable=False
            )
        )
        
        new_properties = {
            "_status": class_table.c.status,
            "status": synonym("_status"),
            "_status_list": relationship(
                StatusList,
                primaryjoin=\
                class_table.c.status_list_id==\
                tables.StatusLists.c.id
            ),
            "status_list": synonym("_status_list"),
        }
        
        try:
            mapper_arguments["properties"].update(new_properties)
        except KeyError:
            mapper_arguments["properties"] = new_properties
        
        return mapper_arguments






########################################################################
class ScheduleMixinDB(object):
    """A helper class for ScheduleMixin table and mapper setup.
    
    Helps setting up tables and mappers for classes mixed in with
    :class:`stalker.core.models.ScheduleMixin`
    
    For now there is no exmaple for it, but it is pretty similiar to the other
    mixin classes.
    """
    
    
    
    #----------------------------------------------------------------------
    @classmethod
    def setup(cls, class_, class_table, mapper_arguments=None):
        """Creates the necessary tables and properties for the mappers for the mixed in class.
        
        Use the returning dictionary (mapper_arguments) in your mapper.
        
        :param class\_: The mixed in class, in other words the class which will
          be extended with the mixin functionalities
         
        :param class_table: The table holding the information about the class
        
        :param mapper_arguments: Incoming mapper arugments for the
          SQLAlchemy.Orm.Mapper, it will be updated with the properties of the
          current mixin
        
        :type mapper_arguments: dict
        
        :returns: a dictionary holding the mapper_arguments
        """
        
        if mapper_arguments is None:
            mapper_arguments = {}
        
        #class_name = class_.__name__
        
        # update the given class table with new columns
        class_table.append_column(
            Column("start_date", Date),
        )
        
        class_table.append_column(
            Column("due_date", Date),
        )
        
        class_table.append_column(
            Column("duration", Interval),
        )
        
        new_properties = {
            "_start_date": class_table.c.start_date,
            "start_date": synonym("_start_date"),
            "_due_date": class_table.c.due_date,
            "due_date": synonym("_due_date"),
            "_duration": class_table.c.duration,
            "duration": synonym("_duration"),
        }
        
        try:
            mapper_arguments["properties"].update(new_properties)
        except KeyError:
            mapper_arguments["properties"] = new_properties
        
        return mapper_arguments






########################################################################
class TaskMixinDB(object):
    """A helper class for TaskMixin table and mapper setup.
    
    Helps setting up tables and mappers for classes mixed in with
    :class:`stalker.core.models.TaskMixin`
    
    For now there is no exmaple for it, but it is pretty similiar to the other
    mixin classes.
    """
    
    
    
    #----------------------------------------------------------------------
    @classmethod
    def setup(cls, class_, class_table, mapper_arguments=None):
        """Creates the necessary tables and properties for the mappers for the mixed in class.
        
        Use the returning dictionary (mapper_arguments) in your mapper.
        
        :param class\_: The mixed in class, in other words the class which will
          be extended with the mixin functionalities
         
        :param class_table: The table holding the information about the class
        
        :param mapper_arguments: Incoming mapper arugments for the
          SQLAlchemy.Orm.Mapper, it will be updated with the properties of the
          current mixin
        
        :type mapper_arguments: dict
        
        :returns: a dictionary holding the mapper_arguments
        """
        
        if mapper_arguments is None:
            mapper_arguments = {}
        
        class_name = class_.__name__
        
        # update the given class table with new columns
        class_table.append_column(
            Column(
                "project_id",
                Integer,
                ForeignKey(tables.Projects.c.id),
                # cannot use nullable cause a Project object needs
                # insert itself as the project and it needs post_update
                # thus nullable should be True
                #nullable=False,
            )
        )
        
        # use the given class_name and the class_table
        secondary_table_name = class_name + "_Tasks"
        secondary_table = None
        
        # check if the table is already defined
        if secondary_table_name not in db.metadata:
            secondary_table = Table(
                secondary_table_name, db.metadata,
                Column(
                    class_name.lower() + "_id",
                    Integer,
                    ForeignKey(class_table.c.id),
                    primary_key=True,
                ),
                
                Column(
                    "task_id",
                    Integer,
                    ForeignKey(tables.Tasks.c.id),
                    primary_key=True,
                )
            )
        else:
            secondary_table = db.metadata.tables[secondary_table_name]
        
        new_properties = {
            "_project": relationship(
                Project,
                primaryjoin=\
                    class_table.c.project_id==tables.Projects.c.id,
                post_update=True, # for project itself
                uselist=False,
                #remote_side=[tables.Projects.c.id],
            ),
            "project": synonym("_project"),
            "_tasks": relationship(
                Task,
                secondary=secondary_table,
                primaryjoin=\
                    class_table.c.id==\
                    eval("secondary_table.c." + class_name.lower() + "_id"),
                secondaryjoin=\
                    secondary_table.c.task_id==\
                    tables.Tasks.c.id,
            ),
            "tasks": synonym("_tasks"),
        }
        
        try:
            mapper_arguments["properties"].update(new_properties)
        except KeyError:
            mapper_arguments["properties"] = new_properties
        
        return mapper_arguments


