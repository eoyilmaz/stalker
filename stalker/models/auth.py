# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from sqlalchemy import Column, Integer, ForeignKey
from stalker.models.entity import SimpleEntity

class PermissionGroup(SimpleEntity):
    """Manages permission in the system.
    
    A PermissionGroup object maps permission for tasks like Create, Read,
    Update, Delete operations in the system to available classes in the system.
    
    It reads the :attr:`~stalker.conf.defaults.CORE_MODEL_CLASSES` list to get
    the list of available classes which can be created. It then stores a binary
    value for each of the class.
    
    A :class:`~stalker.models.user.User` can be in several
    :class:`~stalker.models.auth.PermissionGroup`\ s. The combined permission
    for an object is calculated with an ``OR`` (``^``) operation. So if one of
    the :class:`~stalker.models.auth.PermissionGroup`\ s of the
    :class:`~stalker.models.user.User` is allowing the action then the user is
    allowed to do the operation.
    
    The permissions are stored in a dictionary. The key is the class name and
    the value is a 4-bit binary integer value like 0b0001.
    
    +-------------------+--------+--------+--------+------+
    |        0b         |   0    |   0    |   0    |  0   |
    +-------------------+--------+--------+--------+------+
    | binary identifier | Delete | Update | Create | Read |
    |                   | Bit    | Bit    | Bit    | Bit  |
    +-------------------+--------+--------+--------+------+
    
    :param dict permissions: A Python dictionary showing the permissions. The
      key is the name of the Class and the value is the permission bit.
    
    
    NOTE TO DEVELOPERS: a Dictionary-Based Collections should be used in
    SQLAlchemy.
    """

    __tablename__ = "PermissionGroups"
    __mapper_args__ = {"polymorphic_identity": "PermissionGroup"}

    permissionGroup_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                                primary_key=True)
    
    def __init__(self, **kwargs):
        super(PermissionGroup, self).__init__(**kwargs)
