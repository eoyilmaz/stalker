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
    
    
    
