# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
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

import logging

from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship, validates

from stalker import defaults
from stalker.db.declarative import Base
from stalker.models.entity import Entity
from stalker.models.mixins import (StatusMixin, DateRangeMixin, ReferenceMixin,
                                   CodeMixin)
from stalker.log import logging_level

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class ProjectRepository(Base):
    """The association object for Project to Repository instances
    """
    __tablename__ = 'Project_Repositories'

    project_id = Column(
        Integer,
        ForeignKey('Projects.id'),
        primary_key=True
    )

    project = relationship(
        'Project',
        back_populates='repositories_proxy',
        primaryjoin='Project.project_id==ProjectRepository.project_id',
    )

    repository_id = Column(
        Integer,
        ForeignKey('Repositories.id'),
        primary_key=True
    )

    repository = relationship(
        'Repository',
        primaryjoin=
        'ProjectRepository.repository_id==Repository.repository_id',
    )

    position = Column(Integer)

    def __init__(self, project=None, repository=None, position=None):
        self.project = project
        self.repository = repository
        self.position = position

    @validates('project')
    def _validate_project(self, key, project):
        """validates the given project value
        """
        return project

    @validates("repository")
    def _validate_repository(self, key, repository):
        """validates the given repository value
        """
        if repository is not None:
            from stalker.models.repository import Repository
            if not isinstance(repository, Repository):
                raise TypeError(
                    "%s.repositories should be a list of "
                    "stalker.models.repository.Repository instances or "
                    "derivatives, not %s" %
                    (self.__class__.__name__, repository.__class__.__name__)
                )

        return repository


class Project(Entity, ReferenceMixin, StatusMixin, DateRangeMixin, CodeMixin):
    """All the information about a Project in Stalker is hold in this class.

    Project is one of the main classes that will direct the others. A project
    in Stalker is a gathering point.

    It is mixed with :class:`.ReferenceMixin`, :class:`.StatusMixin`,
    :class:`.DateRangeMixin` and :class:`.CodeMixin` to give reference, status,
    schedule and code attribute. Please read the individual documentation of
    each of the mixins.

    **Project Users**

    The :attr:`.Project.users` attribute lists the users in this project. UIs
    like task creation for example will only list these users as available
    resources for this project.

    **TaskJuggler Integration**

    Stalker uses TaskJuggler for scheduling the project tasks. The
    :attr:`.Project.to_tjp` attribute generates a tjp compliant string which
    includes the project definition, the tasks of the project, the resources in
    the project including the vacation definitions and all the time logs
    recorded for the project.

    For custom attributes or directives that needs to be passed to TaskJuggler
    you can use the :attr:`.Project.custom_tjp` attribute which will be
    attached to the generated tjp file (inside the "project" directive).

    To manage all the studio projects at once (schedule them at once please use
    :class:`.Studio`).

    .. versionadded:: 0.2.13
       Multiple Repositories per Project

       Starting with v0.2.13 Project instances can have multiple Repositories,
       which allows the project files to be placed in more than one repository
       according to the need of the studio pipeline. One great advantage of
       having multiple repositories is to be able to place Published versions
       in to another repository which is placed on to a faster server.

       Also the :attr:`.repositories` attribute is not a read-only attribute
       anymore.

    :param client: The client which the project is affiliated with. Default
      value is None.

    :type client: :class:`.Client`

    :param image_format: The output image format of the project. Default
      value is None.

    :type image_format: :class:`.ImageFormat`

    :param float fps: The FPS of the project, it should be a integer or float
      number, or a string literal which can be correctly converted to a float.
      Default value is 25.0.

    :param type: The type of the project. Default value is None.

    :type type: :class:`.Type`

    :param structure: The structure of the project. Default value is None

    :type structure: :class:`.Structure`

    :param repositories: A list of :class:`.Repository` instances that the
      project files are going to be stored in. You can not create a project
      without specifying the repositories argument and passing a
      :class:`.Repository` to it. Default value is None which raises a
      TypeError.

    :type repository: :class:`.Repository`.

    :param bool is_stereoscopic: a bool value, showing if the project is going
      to be a stereo 3D project, anything given as the argument will be
      converted to True or False. Default value is False.

    :param users: A list of :class:`.User`\ s holding the users in this
      project. This will create a reduced or grouped list of studio workers and
      will make it easier to define the resources for a Task related to this
      project. The default value is an empty list.
    """

    __auto_name__ = False
    __tablename__ = "Projects"
    project_id = Column("id", Integer, ForeignKey("Entities.id"),
                        primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "Project",
        "inherit_condition": project_id == Entity.entity_id
    }

    active = Column(Boolean, default=True)

    client_id = Column(Integer, ForeignKey("Clients.id"))
    client = relationship(
        "Client",
        primaryjoin="Projects.c.client_id==Clients.c.id",
        back_populates="projects",
        uselist=False,
        doc="""The client company assigning the studio
        with the project.

        Should be an instance of :class:`.Client`,
        can also be set to None.
        """
    )

    tasks = relationship(
        'Task',
        primaryjoin='Tasks.c.project_id==Projects.c.id',
        uselist=True,
        cascade="all, delete-orphan"
    )

    users = association_proxy(
        'user_role',
        'user',
        creator=lambda n: ProjectUser(user=n)
    )

    user_role = relationship(
        'ProjectUser',
        back_populates='project',
        cascade='all, delete-orphan',
        cascade_backrefs=False,
        primaryjoin='Projects.c.id==Project_Users.c.project_id'
    )

    repositories_proxy = relationship(
        'ProjectRepository',
        back_populates='project',
        cascade='all, delete-orphan',
        cascade_backrefs=False,
        order_by='ProjectRepository.position',
        primaryjoin='Projects.c.id==Project_Repositories.c.project_id',
        collection_class=ordering_list('position'),
        doc="""The :class:`.Repository` that this project files should reside.

        Should be a list of :class:`.Repository`\ instances.
        """
    )

    repositories = association_proxy(
        'repositories_proxy',
        'repository',
        creator=lambda n: ProjectRepository(repository=n)
    )

    structure_id = Column(Integer, ForeignKey("Structures.id"))
    structure = relationship(
        "Structure",
        primaryjoin="Project.structure_id==Structure.structure_id",
        doc="""The structure of the project. Should be an instance of
        :class:`.Structure` class"""
    )

    image_format_id = Column(Integer, ForeignKey("ImageFormats.id"))
    image_format = relationship(
        "ImageFormat",
        primaryjoin="Projects.c.image_format_id==ImageFormats.c.id",
        doc="""The :class:`.ImageFormat` of this project.

        This value defines the output image format of the project, should be an
        instance of :class:`.ImageFormat`.
        """
    )

    fps = Column(
        Float(precision=3),
        doc="""The fps of the project.

        It is a float value, any other types will be converted to float. The
        default value is 25.0.
        """
    )

    is_stereoscopic = Column(
        Boolean,
        doc="""True if the project is a stereoscopic project"""
    )

    tickets = relationship(
        'Ticket',
        primaryjoin='Tickets.c.project_id==Projects.c.id',
        uselist=True,
        cascade="all, delete-orphan"
    )

    def __init__(self,
                 name=None,
                 code=None,
                 client=None,
                 repositories=None,
                 structure=None,
                 image_format=None,
                 fps=25.0,
                 is_stereoscopic=False,
                 users=None,
                 **kwargs):
        # a projects project should be self
        # initialize the project argument to self
        kwargs['project'] = self

        kwargs['name'] = name

        super(Project, self).__init__(**kwargs)
        # call the mixin __init__ methods
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        DateRangeMixin.__init__(self, **kwargs)

        if users is None:
            users = []
        self.users = users

        if repositories is None:
            repositories = []
        self.repositories = repositories

        self.structure = structure
        self.client = client

        self._sequences = []
        self._assets = []

        self.image_format = image_format
        self.fps = fps
        self.is_stereoscopic = bool(is_stereoscopic)
        self.code = code

        self.active = True

    def __eq__(self, other):
        """the equality operator
        """
        return super(Project, self).__eq__(other) and \
            isinstance(other, Project)

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(Project, self).__hash__()

    @validates("fps")
    def _validate_fps(self, key, fps):
        """validates the given fps_in value
        """
        fps = float(fps)
        if fps <= 0:
            raise ValueError(
                '%s.fps can not be 0 or a negative value' %
                self.__class__.__name__
            )
        return float(fps)

    @validates("image_format")
    def _validate_image_format(self, key, image_format):
        """validates the given image format
        """
        from stalker.models.format import ImageFormat

        if image_format is not None and \
           not isinstance(image_format, ImageFormat):
            raise TypeError(
                "%s.image_format should be an instance of "
                "stalker.models.format.ImageFormat, not %s" %
                (self.__class__.__name__, image_format.__class__.__name__)
            )
        return image_format

    @validates("client")
    def _validate_client(self, key, client):
        """validates the given client value
        """
        if client is not None:
            from stalker.models.client import Client
            if not isinstance(client, Client):
                raise TypeError(
                    "%s.client should be an instance of "
                    "stalker.models.auth.Client not %s" %
                    (self.__class__.__name__, client.__class__.__name__)
                )
        return client

    @validates("structure")
    def _validate_structure(self, key, structure_in):
        """validates the given structure_in value
        """
        from stalker.models.structure import Structure

        if structure_in is not None:
            if not isinstance(structure_in, Structure):
                raise TypeError(
                    "%s.structure should be an instance of "
                    "stalker.models.structure.Structure, not %s" %
                    (self.__class__.__name__, structure_in.__class__.__name__)
                )
        return structure_in

    @validates('is_stereoscopic')
    def _validate_is_stereoscopic(self, key, is_stereoscopic_in):
        return bool(is_stereoscopic_in)

    @validates('users')
    def _validate_users(self, key, user_in):
        """validates the given users_in value
        """
        from stalker.models.auth import User

        if not isinstance(user_in, User):
            raise TypeError(
                '%s.users should be all stalker.models.auth.User instances, '
                'not %s' %
                (self.__class__.__name__, user_in.__class__.__name__)
            )
        return user_in

    @property
    def root_tasks(self):
        """returns a list of Tasks which have no parent
        """
        from stalker import db, Task

        with db.DBSession.no_autoflush:
            return Task.query \
                .filter(Task.project == self) \
                .filter(Task.parent == None) \
                .all()

    @property
    def assets(self):
        """returns the assets related to this project
        """
        # use joins over the session.query
        from stalker.models.asset import Asset

        return Asset.query \
            .filter(Asset.project == self) \
            .all()

    @property
    def sequences(self):
        """returns the sequences related to this project
        """
        # sequences are tasks, use self.tasks
        from stalker.models.sequence import Sequence

        return Sequence.query \
            .filter(Sequence.project == self) \
            .all()

    @property
    def shots(self):
        """returns the shots related to this project
        """
        # shots are tasks, use self.tasks
        from stalker.models.shot import Shot

        return Shot.query \
            .filter(Shot.project == self) \
            .all()

    @property
    def to_tjp(self):
        """returns a TaskJuggler compatible string representing this project
        """
        from jinja2 import Template
        temp = Template(defaults.tjp_project_template, trim_blocks=True,
                        lstrip_blocks=True)
        return temp.render({'project': self})

    @property
    def is_active(self):
        """predicate for Project.active attribute
        """
        return self.active

    @property
    def total_logged_seconds(self):
        """returns an integer representing the total TimeLog seconds recorded
        in child tasks.
        """
        total_logged_seconds = 0
        for task in self.root_tasks:
            if task.total_logged_seconds is None:
                task.update_schedule_info()
            total_logged_seconds += task.total_logged_seconds

        logger.debug('project.total_logged_seconds: %s' % total_logged_seconds)

        return total_logged_seconds

    @property
    def schedule_seconds(self):
        """returns an integer showing the total amount of schedule timing of
        the in child tasks in seconds
        """
        schedule_seconds = 0
        for task in self.root_tasks:
            if task.schedule_seconds is None:
                task.update_schedule_info()
            schedule_seconds += task.schedule_seconds

        logger.debug('project.schedule_seconds: %s' % schedule_seconds)

        return schedule_seconds

    @property
    def percent_complete(self):
        """returns the percent_complete based on the total_logged_seconds and
        schedule_seconds of the root tasks.
        """
        total_logged_seconds = self.total_logged_seconds
        schedule_seconds = self.schedule_seconds
        if schedule_seconds > 0:
            return total_logged_seconds / schedule_seconds * 100
        else:
            return 0

    @property
    def open_tickets(self):
        """The list of open :class:`.Ticket`\ s in this project.

        returns a list of :class:`.Ticket` instances which has a status of
        `Open` and created in this project.
        """
        from stalker import Ticket, Status
        return Ticket.query \
            .join(Status, Ticket.status) \
            .filter(Ticket.project == self) \
            .filter(Status.code != 'CLS') \
            .all()

    @property
    def repository(self):
        """compatibility attribute for pre v0.2.13 systems. Returns the first
        repository instance in the project.repositories attribute if there is
        any or None
        """
        if self.repositories:
            return self.repositories[0]
        else:
            return None


# PROJECT_USERS
class ProjectUser(Base):
    """The association object used in User-to-Project relation
    """

    __tablename__ = 'Project_Users'

    user_id = Column(
        'user_id',
        Integer,
        ForeignKey('Users.id'),
        primary_key=True
    )

    user = relationship(
        'User',
        back_populates='project_role',
        cascade_backrefs=False,
        primaryjoin='ProjectUser.user_id==User.user_id'
    )

    project_id = Column(
        'project_id',
        Integer,
        ForeignKey('Projects.id'),
        primary_key=True
    )

    project = relationship(
        'Project',
        back_populates='user_role',
        cascade_backrefs=False,
        primaryjoin='ProjectUser.project_id==Project.project_id'
    )

    role_id = Column(
        'rid',
        Integer,
        ForeignKey('Roles.id'),
        nullable=True
    )

    role = relationship(
        'Role',
        cascade_backrefs=False,
        primaryjoin='ProjectUser.role_id==Role.role_id'
    )

    def __init__(self, project=None, user=None, role=None):
        self.user = user
        self.project = project
        self.role = role

    @validates("user")
    def _validate_user(self, key, user):
        """validates the given user value
        """
        if user is not None:
            from stalker.models.auth import User
            if not isinstance(user, User):
                raise TypeError(
                    "%s.user should be a stalker.models.auth.User instance, "
                    "not %s" %
                    (self.__class__.__name__, user.__class__.__name__)
                )
        return user

    @validates("project")
    def _validate_project(self, key, project):
        """validates the given project value
        """
        if project is not None:
            # check if it is instance of Project object
            if not isinstance(project, Project):
                raise TypeError(
                    "%s.project should be a "
                    "stalker.models.project.Project instance, not %s" %
                    (self.__class__.__name__, project.__class__.__name__)
                )
        return project

    @validates('role')
    def _validate_role(self, key, role):
        """validates the given role instance
        """
        if role is not None:
            from stalker import Role
            if not isinstance(role, Role):
                raise TypeError(
                    '%s.role should be a'
                    'stalker.models.auth.Role instance, not %s' %
                    (self.__class__.__name__, role.__class__.__name__)
                )
        return role
