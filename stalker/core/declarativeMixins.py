#-*- coding: utf-8 -*-
"""This module contains the Mixins (ta taaa).

Mixins are, you know, things that we love. Ok I don't have anything to write,
just use and love them.
""" 



import datetime
from sqlalchemy import (
    Table,
    Column,
    Date,
    Interval,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import relationship, synonym, validates
from sqlalchemy.ext.declarative import declared_attr

from stalker.conf import defaults
from stalker.core.declarativeModels import Base





########################################################################
class ReferenceMixin(object):
    """Adds reference capabilities to the mixed in class.
    
    References are :class:`stalker.core.models.Entity` instances or anything
    derived from it, which adds information to the attached objects. The aim of
    the References are generally to give more info to direct the evolution of
    the object.
    
    :param references: A list of :class:`~stalker.core.models.Entity` objects.
    
    :type references: list of :class:`~stalker.core.models.Entity` objects.
    """
    
    
    
    #----------------------------------------------------------------------
    @classmethod
    def create_secondary_tables(cls):
        """creates any secondary table
        """
        
        class_name = cls.__name__
        
        # use the given class_name and the class_table
        secondary_table_name = class_name + "_References"
        secondary_table = None
        
        # check if the table is already defined
        if secondary_table_name not in Base.metadata:
            secondary_table = Table(
                secondary_table_name, Base.metadata,
                Column(
                    class_name.lower() + "_id",
                    Integer,
                    ForeignKey(cls.__tablename__ + ".id"),
                    primary_key=True,
                ),
                
                Column(
                    "reference_id",
                    Integer,
                    ForeignKey("Links.id"),
                    primary_key=True,
                )
            )
        else:
            secondary_table = Base.metadata.tables[secondary_table_name]
        
        return secondary_table
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def references(cls):
        
        class_name = cls.__name__
        
        # get secondary table
        secondary_table = cls.create_secondary_tables()
        
        # return the relationship
        return relationship("Link", secondary=secondary_table)
    
    
    
    #----------------------------------------------------------------------
    @validates("references")
    def _validate_references(self, key, reference):
        """validates the given reference
        """
        
        from stalker.core.declarativeModels import SimpleEntity
        
        # all the elements should be instance of stalker.core.models.Entity
        if not isinstance(reference, SimpleEntity):
            raise TypeError("all the elements should be instances of "
                             ":class:`stalker.core.models.Entity`")
        
        return reference






########################################################################
class StatusMixin(object):
    """Adds statusabilities to the object.
    
    This mixin adds status and statusList variables to the list. Any object
    that needs a status and a corresponding status list can include this mixin.
    
    When mixed with a class which don't have an __init__ method, the mixin
    supplies one, and in this case the parameters below must be defined.
    
    :param status_list: this attribute holds a status list object, which shows
      the possible statuses that this entity could be in. This attribute can
      not be empty or None. Giving a StatusList object, the
      StatusList.target_entity_type should match the current class.
    
    :param status: an integer value which is the index of the status in the
      status_list attribute. So the value of this attribute couldn't be lower
      than 0 and higher than the length-1 of the status_list object and nothing
      other than an integer
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, status=0, status_list=None, **kwargs):
        self.status_list = status_list
        self.status = status
    
    
    
    #----------------------------------------------------------------------
    @classmethod
    def create_secondary_tables(cls):
        """creates any secondary table
        """
        
        class_name = cls.__name__
        
        # use the given class_name and the class_table
        secondary_table_name = class_name + "_References"
        secondary_table = None
        
        # check if the table is already defined
        if secondary_table_name not in Base.metadata:
            secondary_table = Table(
                secondary_table_name, Base.metadata,
                Column(
                    class_name.lower() + "_id",
                    Integer,
                    ForeignKey(cls.__tablename__ + ".id"),
                    primary_key=True,
                ),
                
                Column(
                    "reference_id",
                    Integer,
                    ForeignKey("Links.id"),
                    primary_key=True,
                )
            )
        else:
            secondary_table = Base.metadata.tables[secondary_table_name]
        
        return secondary_table
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def status(cls):
        return Column("status", Integer, default=0)
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def status_list_id(cls):
        return Column(
            "status_list_id",
            Integer,
            ForeignKey("StatusLists.id"),
            nullable=False
        )
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def status_list(cls):
        return relationship(
            "StatusList",
            primaryjoin=\
                "%s.status_list_id==StatusList.statusList_id" % cls.__name__
        )
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def references(cls):
        
        class_name = cls.__name__
        
        # get secondary table
        secondary_table = cls.create_secondary_tables()
        
        # return the relationship
        return relationship("Link", secondary=secondary_table)
    
    
    
    #----------------------------------------------------------------------
    @validates("status_list")
    def _validate_status_list(self, key, status_list):
        """validates the given status_list_in value
        """
        
        # raise TypeError when:
        from stalker.core.declarativeModels import StatusList
        
        # it is not an instance of status_list
        if not isinstance(status_list, StatusList):
            raise TypeError("the status list should be an instance of "
                             "stalker.core.models.StatusList")
        
        # check if the entity_type matches to the StatusList.target_entity_type
        if self.__class__.__name__ != status_list.target_entity_type:
            raise TypeError("the given StatusLists' target_entity_type is %s, "
                            "whereas the entity_type of this object is %s" % \
                            (status_list.target_entity_type,
                             self.__class__.__name__))
        
        return status_list
    
    
    
    #----------------------------------------------------------------------
    @validates("status")
    def _validate_status(self, key, status):
        """validates the given status value
        """
        
        from stalker.core.declarativeModels import StatusList
        
        if not isinstance(self.status_list, StatusList):
            raise TypeError("please set the status_list attribute first")
        
        # it is set to None
        if status is None:
            raise TypeError("the status couldn't be None, set it to a "
                             "non-negative integer")
        
        # it is not an instance of int
        if not isinstance(status, int):
            raise TypeError("the status must be an instance of integer")
        
        # if it is not in the correct range:
        if status < 0:
            raise ValueError("the status must be a non-negative integer")
        
        if status >= len(self.status_list.statuses):
            raise ValueError("the status can not be bigger than the length of "
                             "the status_list")
        
        return status






