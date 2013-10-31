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

import logging

import warnings
from sqlalchemy import (Column, Integer, ForeignKey, Float, Boolean, Table)
from sqlalchemy.orm import relationship, validates

from stalker import User
from stalker import defaults
from stalker.db.session import DBSession
from stalker.db.declarative import Base
from stalker.models.entity import Entity
from stalker.models.mixins import (StatusMixin, ScheduleMixin, ReferenceMixin,
                                   CodeMixin)
from stalker.log import logging_level

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Project(Entity, ReferenceMixin, StatusMixin, ScheduleMixin, CodeMixin):
    """All the information about a Project in Stalker is hold in this class.

    Project is one of the main classes that will direct the others. A project
    in Stalker is a gathering point.

    It is mixed with :class:`~stalker.models.mixins.ReferenceMixin`,
    :class:`~stalker.models.mixins.StatusMixin`,
    :class:`~stalker.models.mixins.ScheduleMixin` and
    :class:`~stalker.models.mixins.CodeMixin` to give reference, status,
    schedule and code attribute. Please read the individual documentation of
    each of the mixins.

    **Project Users**

    The :attr:`~stalker.models.project.Project.users` attribute lists the users
    in this project. UIs like task creation for example will only list these
    users as available resources for this project.

    **TaskJuggler Integration**

    Stalker uses TaskJuggler for scheduling the project tasks. The
    :attr:`~stalker.models.project.Project.to_tjp` attribute generates a tjp
    compliant string which includes the project definition, the tasks of the
    project, the resources in the project including the vacation definitions
    and all the time logs recorded for the project.

    For custom attributes or directives that needs to be passed to TaskJuggler
    you can use the :attr:`~stalker.models.project.Project.custom_tjp`
    attribute which will be attached to the generated tjp file (inside the
    "project" directive).

    To manage all the studio projects at once (schedule them at once please use
    :class:`~stalker.models.studio.Studio`).

    :param lead: The lead of the project. Default value is None.

    :type lead: :class:`~stalker.User`

    :param image_format: The output image format of the project. Default
      value is None.

    :type image_format: :class:`~stalker.models.format.ImageFormat`

    :param float fps: The FPS of the project, it should be a integer or float
      number, or a string literal which can be correctly converted to a float.
      Default value is 25.0.

    :param type: The type of the project. Default value is None.

    :type type: :class:`~stalker.models.type.Type`

    :param structure: The structure of the project. Default value is None

    :type structure: :class:`~stalker.models.structure.Structure`

    :param repository: The repository that the project files are going to be
      stored in. You can not create a project without specifying the
      repository argument and passing a
      :class:`~stalker.models.repository.Repository` to it. Default value is
      None which raises a TypeError.

    :type repository: :class:`~stalker.models.repository.Repository`.

    :param bool is_stereoscopic: a bool value, showing if the project is going
      to be a stereo 3D project, anything given as the argument will be
      converted to True or False. Default value is False.

    :param users: A list of :class:`~stalker.models.auth.User`\ s holding the
      users in this project. This will create a reduced or grouped list of
      studio workers and will make it easier to define the resources for a Task
      related to this project. The default value is an empty list.
    """

    __auto_name__ = False
    __tablename__ = "Projects"
    project_id_local = Column("id", Integer, ForeignKey("Entities.id"),
                              primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "Project",
        "inherit_condition": project_id_local == Entity.entity_id
    }

    active = Column(Boolean, default=True)

    tasks = relationship(
        'Task',
        primaryjoin='Tasks.c.project_id==Projects.c.id',
        uselist=True,
        cascade="all, delete-orphan"
    )

    users = relationship(
        'User',
        secondary='Project_Users',
        back_populates='projects'
    )

    lead_id = Column(Integer, ForeignKey("Users.id"))
    lead = relationship(
        "User",
        primaryjoin="Projects.c.lead_id==Users.c.id",
        back_populates="projects_lead",
        doc="""The lead of the project.

        Should be an instance of :class:`~stalker.models.auth.User`,
        also can set to None.
        """
    )

    repository_id = Column(Integer, ForeignKey("Repositories.id"))
    repository = relationship(
        "Repository",
        primaryjoin="Project.repository_id==Repository.repository_id",
        doc="""The :class:`~stalker.models.repository.Repository` that this
        project should reside.

        Should be an instance of
        :class:`~stalker.models.repository.Repository`\ . It
        is a read-only attribute. So it is not possible to change the
        repository of one project.
        """
    )

    structure_id = Column(Integer, ForeignKey("Structures.id"))
    structure = relationship(
        "Structure",
        primaryjoin="Project.structure_id==Structure.structure_id",
        doc="""The structure of the project. Should be an instance of
        :class:`~stalker.models.structure.Structure` class"""
    )

    image_format_id = Column(Integer, ForeignKey("ImageFormats.id"))
    image_format = relationship(
        "ImageFormat",
        primaryjoin="Projects.c.image_format_id==ImageFormats.c.id",
        doc="""The :class:`~stalker.models.format.ImageFormat` of this
        project.

        This value defines the output image format of the project, should be an
        instance of :class:`~stalker.models.format.ImageFormat`.
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
                 lead=None,
                 repository=None,
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
        ScheduleMixin.__init__(self, **kwargs)
        #CodeMixin.__init__(self, **kwargs)

        self.lead = lead
        if users is None:
            users = []
        self.users = users
        self.repository = repository
        self.structure = structure

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

    @validates("fps")
    def _validate_fps(self, key, fps):
        """validates the given fps_in value
        """
        return float(fps)

    @validates("image_format")
    def _validate_image_format(self, key, image_format):
        """validates the given image format
        """
        from stalker.models.format import ImageFormat

        if image_format is not None and \
                not isinstance(image_format, ImageFormat):
            raise TypeError("%s.image_format should be an instance of "
                            "stalker.models.format.ImageFormat, not %s" %
                            (self.__class__.__name__,
                             image_format.__class__.__name__))
        return image_format

    @validates("lead")
    def _validate_lead(self, key, lead):
        """validates the given lead_in value
        """
        if lead is not None:
            if not isinstance(lead, User):
                raise TypeError("%s.lead should be an instance of "
                                "stalker.models.auth.User, not %s" %
                                (self.__class__.__name__,
                                 lead.__class__.__name__))
        return lead

    @validates("repository")
    def _validate_repository(self, key, repository):
        """validates the given repository_in value
        """
        from stalker.models.repository import Repository

        if not isinstance(repository, Repository):
            raise TypeError("%s.repository should be an instance of "
                            "stalker.models.repository.Repository, not %s" %
                            (self.__class__.__name__,
                             repository.__class__.__name__))
        return repository

    @validates("structure")
    def _validate_structure(self, key, structure_in):
        """validates the given structure_in value
        """
        from stalker.models.structure import Structure

        if structure_in is not None:
            if not isinstance(structure_in, Structure):
                raise TypeError("%s.structure should be an instance of "
                                "stalker.models.structure.Structure, not %s" %
                                (self.__class__.__name__,
                                 structure_in.__class__.__name__))
        return structure_in

    @validates('is_stereoscopic')
    def _validate_is_stereoscopic(self, key, is_stereoscopic_in):
        return bool(is_stereoscopic_in)

    @validates('users')
    def _validate_users(self, key, user_in):
        """validates the given users_in value
        """
        if not isinstance(user_in, User):
            raise TypeError('%s.users should be all stalker.models.auth.User '
                            'instances, not %s' %
                            (self.__class__.__name__,
                             user_in.__class__.__name__))
        return user_in

    @property
    def root_tasks(self):
        """returns a list of Tasks which have no parent
        """
        from stalker.models.task import Task

        return Task.query \
            .filter(Task._project == self) \
            .filter(Task.parent == None) \
            .all()

    @property
    def assets(self):
        """returns the assets related to this project
        """
        # use joins over the session.query
        from stalker.models.asset import Asset

        if DBSession is not None:
            return Asset.query \
                .join(Asset.project) \
                .filter(Project.name == self.name) \
                .all()
        else:
            warnings.warn("There is no database setup, the users can not "
                          "be queried from this state, please use "
                          "stalker.db.setup() to setup a database",
                          RuntimeWarning)
            return []

    @property
    def sequences(self):
        """returns the sequences related to this project
        """
        # sequences are tasks, use self.tasks
        from stalker.models.sequence import Sequence

        sequences = []
        for task in self.tasks:
            if isinstance(task, Sequence):
                sequences.append(task)
        return sequences

    @property
    def shots(self):
        """returns the shots related to this project
        """
        # shots are tasks, use self.tasks
        from stalker.models.shot import Shot

        shots = []
        for task in self.tasks:
            if isinstance(task, Shot):
                shots.append(task)
        return shots

    @property
    def to_tjp(self):
        """returns a TaskJuggler compatible string representing this project
        """
        from jinja2 import Template
        temp = Template(defaults.tjp_project_template)
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

        logger.debug('project.total_logged_seconds     : %s' % total_logged_seconds)

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

        logger.debug('project.schedule_seconds     : %s' % schedule_seconds)

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


# PROJECT_USERS
Project_Users = Table(
    'Project_Users', Base.metadata,
    Column('user_id', Integer, ForeignKey('Users.id'), primary_key=True),
    Column('project_id', Integer, ForeignKey('Projects.id'), primary_key=True)
)
