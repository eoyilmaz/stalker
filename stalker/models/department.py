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

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, validates, synonym

from stalker import defaults
from stalker.models.auth import User
from stalker.models.entity import Entity

from stalker.log import logging_level
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Department(Entity):
    """The departments that forms the studio itself.

    The information that a Department object holds is like:

      * The members of the department
      * The lead of the department
      * and all the other things those are inherited from the AuditEntity class

    Two Department object considered the same if they have the same name, the
    the members list nor the lead info is important, a "Modeling" department
    should of course be the same with another department which has the name
    "Modeling" again.

    so creating a department object needs the following parameters:

    :param members: it can be an empty list, so one department can be created
      without any member in it. But this parameter should be a list of User
      objects.

    :param lead: this is a User object, that holds the lead information, a lead
      could be in this department but it is not forced to be also a member of
      the department. So another departments member can be a lead for another
      department. Lead attribute can not be empty or None.
    """
    __auto_name__ = False
    __tablename__ = "Departments"
    __mapper_args__ = {"polymorphic_identity": "Department"}
    department_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True
    )

    lead_id = Column(
        "lead_id",
        Integer,
        ForeignKey("Users.id", use_alter=True, name="x")
    )

    lead = relationship(
        "User",
        uselist=False,
        primaryjoin="Department.lead_id==User.user_id",
        post_update=True,
        doc="""The lead of this department, it is a User object""",
    )

    members = relationship(
        "User",
        secondary='User_Departments',
        back_populates="departments",
        doc="""List of users representing the members of this department.""",
    )
    
    users = synonym('members')

    def __init__(self, members=None, lead=None, **kwargs):
        super(Department, self).__init__(**kwargs)

        if members is None:
            members = []

        self.members = members
        self.lead = lead
    
    def __eq__(self, other):
        """the equality operator
        """
        return super(Department, self).__eq__(other) and\
               isinstance(other, Department) 
    
    @validates("members")
    def _validate_members(self, key, member):
        """validates the given member attribute
        """

        if not isinstance(member, User):
            raise TypeError("Every element in the %s.members list should be "
                            "an instance of stalker.models.auth.User class "
                            "not %s" %
                            (self.__class__.__name__,
                             member.__class__.__name__))
        return member

    @validates("lead")
    def _validate_lead(self, key, lead):
        """validates the given lead attribute
        """
        from stalker.models.auth import User
        if lead is not None:
            # the lead should be an instance of User class
            if not isinstance(lead, User):
                raise TypeError("%s.lead should be an instance of "
                                "stalker.models.auth.User not %s" %
                                (self.__class__.__name__,
                                 lead.__class__.__name__))
        return lead

    @property
    def to_tjp(self):
        """outputs a TaskJuggler compatible string
        """
        from jinja2 import Template
        temp = Template(defaults.tjp_department_template)
        return temp.render({'department': self})
