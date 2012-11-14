# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from sqlalchemy import Table, Column, Integer, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship, validates, composite
from sqlalchemy.ext.mutable import MutableComposite

from stalker.conf import defaults
from stalker.db.declarative import Base
from stalker.models.entity import Entity
from stalker.models.mixins import TargetEntityTypeMixin

class Color(MutableComposite):
    """Stores color values as a composite value.
    
    :param int r: The red value, should be between 0-255
    
    :param int g: The green value, should be between 0-255
    
    :param int b: The blue value, should be between 0-255
    """
    
    def __init__(self, r=None, g=None, b=None):
        self._r = None
        self._g = None
        self._b = None
        
        self.r = r
        self.g = g
        self.b = b
    
    def __setattr__(self, key, value):
        # set the attribute
        object.__setattr__(self, key, value)
        
        # alert all parent to the change
        self.changed()
    
    def __composite_values__(self):
        return self.r, self.g, self.b
    
    def __repr__(self):
        return 'Color(%i, %i, %i)' % (self.r, self.g, self.b)
    
    def __eq__(self, other):
        return isinstance(other, Color) and \
            other.r == self.r and other.g == self.g and other.b == self.b
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def _validate_color(self, color, signature):
        """validates the given color value
        """
        if color is None:
           color = 0
        
        if not isinstance(color, int):
            raise TypeError('Color.%s should be an int, not %s' % 
                            (signature, color.__class__.__name__))
        
        if color < 0:
            color = 0
        
        if color > 255:
            color = 255
        
        return color
    
    def _r_getter(self):
        return self._r
    
    def _r_setter(self, r):
        self._r = self._validate_color(r, 'r')
    
    r = property(
        _r_getter,
        _r_setter,
        doc="""The red value of this color instance
        """
    )
    
    def _g_getter(self):
        return self._g
    
    def _g_setter(self, g):
        self._g = self._validate_color(g, 'g')
    
    g = property(
        _g_getter,
        _g_setter,
        doc="""The green value of this color instance
        """
    )
    
    def _b_getter(self):
        return self._b
    
    def _b_setter(self, b):
        self._b = self._validate_color(b, 'b')
    
    b = property(
        _b_getter,
        _b_setter,
        doc="""The blue value of this color instance
        """
    )
    

class Status(Entity):
    """Defines object statutes.
    
    No extra parameters, use the *code* attribute to give a short name for the
    status.
    
    A Status object can be compared with a string or unicode value and it will
    return if the lower case name or lower case code of the status matches the
    lower case form of the given string::
    
      >>> from stalker import Status
      >>> a_status = Status(name="On Hold", "OH")
      >>> a_status == "on hold"
      True
      >>> a_status != "complete"
      True
      >>> a_status == "oh"
      True
      >>> a_status == "another status"
      False
    
    :param name: The name long name of this Status.
    
    :param code: The code of this Status, its generally the short version of
      the name attribute.
    
    :param bg_color: A :class:`~stalker.models.status.Color` instance showing
      the background color of this status mainly used for UI stuff. If skipped
      or given as None the color will be set to the default background color
      (which is white).
    
    :param fg_color: A :class:`~stalker.mocels.status.Color` instance showing
      the foreground color of this status mainly used for UI stuff. If skipped
      or given as None the color will be set to the default foreground color
      (which is black).
    """

    __tablename__ = "Statuses"
    __mapper_args__ = {"polymorphic_identity": "Status"}
    status_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    )
    
    bg_color_r = Column(SmallInteger, default=255)
    bg_color_g = Column(SmallInteger, default=255)
    bg_color_b = Column(SmallInteger, default=255)
    _bg_color = composite(Color, bg_color_r, bg_color_g, bg_color_b)
    
    fg_color_r = Column(SmallInteger, default=0)
    fg_color_g = Column(SmallInteger, default=0)
    fg_color_b = Column(SmallInteger, default=0)
    _fg_color = composite(Color, fg_color_r, fg_color_g, fg_color_b)
    
    def __init__(self,
                 name=None,
                 code=None,
                 fg_color=None,
                 bg_color=None,
                 **kwargs):
        kwargs['name'] = name
        kwargs['code'] = code
        super(Status, self).__init__(**kwargs)
        
        self.bg_color = bg_color
        self.fg_color = fg_color

    def __eq__(self, other):
        """the equality operator
        """
        if isinstance(other, (str, unicode)):
            return self.name.lower() == other.lower() or\
                   self.code.lower() == other.lower()
        else:
            return super(Status, self).__eq__(other) and\
                   isinstance(other, Status)
    
    def _validate_bg_color(self, bg_color):
        """validates the given bg_color value
        """
        if bg_color is None:
            bg_color = Color(*defaults.DEFAULT_BG_COLOR)
        
        if not isinstance(bg_color, Color):
            raise TypeError('Status.bg_color should be an instance of '
                            'stalker.models.status.Color, not %s' %
                            bg_color.__class__.__name__)
        
        return bg_color
    
    def _bg_getter(self):
        return self._bg_color
    
    def _bg_setter(self, bg_color):
        self._bg_color = self._validate_bg_color(bg_color)
    
    bg_color = property(_bg_getter, _bg_setter)
    
    def _validate_fg_color(self, fg_color):
        """validates the given fg_color value
        """
        if fg_color is None:
            fg_color = Color(*defaults.DEFAULT_FG_COLOR)
        
        if not isinstance(fg_color, Color):
            raise TypeError('Status.fg_color should be an instance of '
                            'stalker.models.status.Color, not %s' %
                            fg_color.__class__.__name__)
        
        return fg_color
    
    def _fg_getter(self):
        return self._fg_color
    
    def _fg_setter(self, fg_color):
        self._fg_color = self._validate_fg_color(fg_color)
    
    fg_color = property(_fg_getter, _fg_setter)

class StatusList(Entity, TargetEntityTypeMixin):
    """Type specific list of :class:`~stalker.models.status.Status` instances.
    
    Holds multiple :class:`~stalker.models.status.Status`\ es to be used as a
    choice list for several other classes.
    
    A StatusList can only be assigned to only one entity type. So a
    :class:`~stalker.models.project.Project` can only have one suitable
    StatusList object which is designed for
    :class:`~stalker.models.project.Project` entities.
    
    The list of statuses in StatusList can be accessed by using a list like
    indexing and it also supports string indexes only for getting the item,
    you can not set an item with string indices:
    
    >>> from stalker import Status, StatusList
    >>> status1 = Status(name="Complete", code="CMPLT")
    >>> status2 = Status(name="Work in Progress", code="WIP")
    >>> status3 = Status(name="Pending Review", code="PRev")
    >>> a_status_list = StatusList(name="Asset Status List",
                                   statuses=[status1, status2, status3],
                                   target_entity_type="Asset")
    >>> a_status_list[0]
    <Status (Complete, CMPLT)>
    >>> a_status_list["complete"]
    <Status (Complete, CMPLT)>
    >>> a_status_list["wip"]
    <Status (Work in Progress, WIP)>
    
    :param statuses: This is a list of :class:`~stalker.models.status.Status`
      instances, so you can prepare
      different StatusLists for different kind of entities using the same pool
      of :class:`~stalker.models.status.Status`\ es.
    
    :param target_entity_type: use this parameter to specify the target entity
      type that this StatusList is designed for. It accepts classes or names
      of classes.
      
      For example::
        
        from stalker import Status, StatusList, Project
        
        status_list = [
            Status(name="Waiting To Start", code="WTS"),
            Status(name="On Hold", code="OH"),
            Status(name="In Progress", code="WIP"),
            Status(name="Waiting Review", code="WREV"),
            Status(name="Approved", code="APP"),
            Status(name="Completed", code="CMPLT"),
        ]
        
        project_status_list = StatusList(
            name="Project Status List",
            statuses=status_list,
            target_entity_type="Project"
        )
        
        # or
        project_status_list = StatusList(
            name="Project Status List",
            statuses=status_list,
            target_entity_type=Project
        )
      
      now with the code above you can not assign the ``project_status_list``
      object to any other class than a ``Project`` object.
      
      The StatusList instance can be empty, means it may not have anything in
      its :attr:`~stalker.models.status.StatusList.statuses`. But it is
      useless. The validation for empty statuses list is left to the SOM user.
    """

    __tablename__ = "StatusLists"
    __mapper_args__ = {"polymorphic_identity": "StatusList"}
    
    __unique_target__ = True
    
    statusList_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True
    )

    statuses = relationship(
        "Status",
        secondary="StatusList_Statuses",
        doc="""list of :class:`~stalker.models.status.Status` objects, showing the possible statuses"""
    )

    def __init__(self, statuses=None, target_entity_type=None, **kwargs):
        super(StatusList, self).__init__(**kwargs)
        TargetEntityTypeMixin.__init__(self, target_entity_type, **kwargs)
        
        if statuses is None:
            statuses = []
        
        self.statuses = statuses

    @validates("statuses")
    def _validate_statuses(self, key, status):
        """validates the given status
        """
        
        if not isinstance(status, Status):
            raise TypeError("all the elements in %s.statuses must be an "
                            "instance of stalker.models.status.Status not %s" %
                            (self.__class__.__name__,
                             status.__class__.__name__))

        return status

    def __eq__(self, other):
        """the equality operator
        """

        return super(StatusList, self).__eq__(other) and\
               isinstance(other, StatusList) and\
               self.statuses == other.statuses and\
               self.target_entity_type == other.target_entity_type

    def __getitem__(self, key):
        """the indexing attributes for getting item
        """
        if isinstance(key, (str, unicode)):
            for item in self.statuses:
                if item == key:
                    return item
        else:
            return self.statuses[key]

    def __setitem__(self, key, value):
        """the indexing attributes for setting item
        """

        self.statuses[key] = self._validate_status(value)

    def __delitem__(self, key):
        """the indexing attributes for deleting item
        """

        del self.statuses[key]

    def __len__(self):
        """the indexing attributes for getting the length
        """

        return len(self.statuses)


# STATUSLIST_STATUSES
StatusList_Statuses = Table(
    "StatusList_Statuses", Base.metadata,
    Column(
        "statusList_id",
        Integer,
        ForeignKey("StatusLists.id"),
        primary_key=True
    ),
    Column(
        "status_id",
        Integer,
        ForeignKey("Statuses.id"),
        primary_key=True
    )
)

