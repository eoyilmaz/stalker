# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, validates
from stalker.db.declarative import Base
from stalker.models.entity import Entity
from stalker.models.mixins import TargetEntityTypeMixin

class Status(Entity):
    """Defines object statutes.
    
    No extra parameters, use the *code* attribute to give a short name for the
    status.
    
    A Status object can be compared with a string or unicode value and it will
    return if the lower case name or lower case code of the status matches the
    lower case form of the given string:
    
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
    """

    __tablename__ = "Statuses"
    __mapper_args__ = {"polymorphic_identity": "Status"}
    status_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
        )
    
    def __init__(self, **kwargs):
        super(Status, self).__init__(**kwargs)

    def __eq__(self, other):
        """the equality operator
        """

        if isinstance(other, (str, unicode)):
            return self.name.lower() == other.lower() or\
                   self.code.lower() == other.lower()
        else:
            return super(Status, self).__eq__(other) and\
                   isinstance(other, Status)


class StatusList(Entity, TargetEntityTypeMixin):
    """Type specific list of :class:`~stalker.models.status.Status` instances.
    
    Holds multiple :class:`~stalker.models.status.Status`\ es to be used as a
    choice list for several other classes.
    
    A StatusList can only be assigned to only one entity type. So a
    :class:`~stalker.models.project.Project` can only have a suitable
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
    
    :param statuses: this is a list of status objects, so you can prepare
      different StatusList objects for different kind of entities
    
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
