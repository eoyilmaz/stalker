# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA


from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, validates

from stalker import defaults
from stalker.db.declarative import Base
from stalker.models.entity import Entity
from stalker.models.mixins import TargetEntityTypeMixin
from stalker.models.mixins import CodeMixin

from stalker.log import logging_level
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Status(Entity, CodeMixin):
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

    :param bg_color: A positive integer between 0-16777215 or 0x000000-0xffffff
      showing the background color of this status mainly used for UI stuff. If
      skipped or given as None the color will be set to the default background
      color (which is white).

    :param fg_color: A positive integer between 0-16777215 or 0x000000-0xffffff
      showing the foreground color of this status mainly used for UI stuff. If
      skipped or given as None the color will be set to the default foreground
      color (which is black).
    """
    __auto_name__ = False
    __tablename__ = "Statuses"
    __mapper_args__ = {"polymorphic_identity": "Status"}
    status_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    )
    bg_color = Column(Integer, default=0xffffff)
    fg_color = Column(Integer, default=0x000000)

    def __init__(self,
                 name=None,
                 code=None,
                 fg_color=None,
                 bg_color=None,
                 **kwargs):
        kwargs['name'] = name
        kwargs['code'] = code

        super(Status, self).__init__(**kwargs)
        #CodeMixin.__init__(self, **kwargs)

        self.code = code
        self.bg_color = bg_color
        self.fg_color = fg_color

    def __eq__(self, other):
        """the equality operator
        """
        if isinstance(other, (str, unicode)):
            return self.name.lower() == other.lower() or \
                   self.code.lower() == other.lower()
        else:
            return super(Status, self).__eq__(other) and \
                   isinstance(other, Status)

    @validates('bg_color')
    def _validate_bg_color(self, key, bg_color):
        """validates the given bg_color value
        """
        if bg_color is None:
            bg_color = defaults.status_bg_color

        if not isinstance(bg_color, int):
            raise TypeError('Status.bg_color should be an integer '
                            'not %s' % bg_color.__class__.__name__)

        bg_color = max(0, bg_color)
        bg_color = min(0xffffff, bg_color)

        return bg_color

    @validates('fg_color')
    def _validate_fg_color(self, key, fg_color):
        """validates the given fg_color value
        """
        if fg_color is None:
            fg_color = defaults.status_fg_color

        if not isinstance(fg_color, int):
            raise TypeError('Status.fg_color should be an integer '
                            'not %s' % fg_color.__class__.__name__)

        fg_color = max(0, fg_color)
        fg_color = min(0xffffff, fg_color)

        return fg_color


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
    >>> a_status_list["WIP"]
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
    __auto_name__ = True
    __tablename__ = "StatusLists"
    __mapper_args__ = {"polymorphic_identity": "StatusList"}

    __unique_target__ = True

    status_list_id = Column(
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
        return super(StatusList, self).__eq__(other) and \
               isinstance(other, StatusList) and \
               self.statuses == other.statuses and \
               self.target_entity_type == other.target_entity_type

    def __getitem__(self, key):
        """the indexing attributes for getting item
        """
        from stalker.db import DBSession

        with DBSession.no_autoflush:
            return_item = None
            if isinstance(key, (str, unicode)):
                for item in self.statuses:
                    if item == key:
                        return_item = item
            else:
                return_item = self.statuses[key]

        return return_item

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
        "status_list_id",
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

