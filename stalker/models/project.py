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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
import copy
import datetime
import warnings

from sqlalchemy import (Column, Integer, ForeignKey, Float, Boolean,
                        PickleType, Table)
from sqlalchemy.orm import relationship, validates
from stalker import User
from stalker.conf import defaults
from stalker.db.session import DBSession
from stalker.db.declarative import Base
from stalker.models.entity import Entity
from stalker.models.mixins import (StatusMixin, ScheduleMixin, ReferenceMixin,
                                   CodeMixin)

from stalker.log import logging_level
import logging
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
    
    Project Users
    -------------
    
    The :attr:`~stalker.models.project.Project.users` attribute lists the users
    in this project. UIs like task creation for example will only list these
    users as available resources for this project.
    
    Root Task
    ---------
    
    Project instances will be created with a default Task with the same name of
    the project. This Task instance is stored in the ``root_task`` attribute of
    the project. Renaming the project will also renamed the root Task.
    
    The Root Task is used in Gantt Chart views as the starting point for the
    other Tasks. A new task can be created by passing the Project or by passing
    the Root Task to the Task class.
    
    Working Hours
    -------------
    
    Every Project in stalker has a working hour settings which defines the
    default working hours for that project. It helps the scheduler to schedule
    the tasks based on assigned resources and the working hours of that
    project.
    
    TaskJuggler Integration
    -----------------------
    
    Stalker uses TaskJuggler for scheduling the project tasks. The
    :attr:`~stalker.models.project.Project.to_tjp` attribute generates a tjp
    compliant string which includes the project definition, the tasks of the
    project, the resources in the project including the vacation definitions
    and all the bookings recorded for the project.
    
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
    
    :param working_hours: A :class:`~stalker.models.project.WorkingHours`
      instance showing the working hours settings for that project. This data
      is stored as a PickleType in the database.
    
    :param int daily_working_hours: An integer specifying the daily working
    hours for this project. It is another critical value attribute which
    TaskJuggler uses mainly converting working day values to working hours
    (1d = 10h kind of thing).
    
    :param users: A list of :class:`~stalker.models.auth.User`\ s holding the
      users in this project. This will create a reduced or grouped list of
      studio workers and will make it easier to define the resources for a Task
      related to this project. The default value is an empty list.
    """
    
    __auto_name__ = False
    #__strictly_typed__ = True
    __tablename__ = "Projects"
    project_id_local = Column("id", Integer, ForeignKey("Entities.id"),
                              primary_key=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "Project",
        "inherit_condition":
            project_id_local==Entity.entity_id
    }
    
    tasks = relationship(
        'Task',
        primaryjoin='Tasks.c.project_id==Projects.c.id',
        uselist=True
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
    
    working_hours = Column(PickleType)
    
    daily_working_hours = Column(Integer)
    
    tickets = relationship(
        'Ticket',
        primaryjoin='Tickets.c.project_id==Projects.c.id',
        uselist=True,
        
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
                 working_hours=None,
                 daily_working_hours=None,
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
        
        self.working_hours = working_hours
        self.daily_working_hours = daily_working_hours
        
        self.now = datetime.datetime.now()
    
    def __eq__(self, other):
        """the equality operator
        """
        return super(Project, self).__eq__(other) and\
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

        if image_format is not None and\
           not isinstance(image_format, ImageFormat):
            raise TypeError("the image_format should be an instance of "
                            "stalker.models.format.ImageFormat")
        return image_format
    
    @validates("lead")
    def _validate_lead(self, key, lead):
        """validates the given lead_in value
        """
        if lead is not None:
            if not isinstance(lead, User):
                raise TypeError("lead must be an instance of "
                                "stalker.models.auth.User")
        return lead
    
    @validates("repository")
    def _validate_repository(self, key, repository):
        """validates the given repository_in value
        """
        from stalker.models.repository import Repository
        
        if not isinstance(repository, Repository):
            raise TypeError("The stalker.models.project.Project instance "
                            "should be created with a "
                            "stalker.models.repository.Repository instance "
                            "passed through the 'repository' argument, the "
                            "current value is '%s'" % repository)
        return repository
    
    @validates("structure")
    def _validate_structure(self, key, structure_in):
        """validates the given structure_in value
        """
        from stalker.models.structure import Structure
        
        if structure_in is not None:
            if not isinstance(structure_in, Structure):
                raise TypeError("structure should be an instance of "
                                "stalker.models.structure.Structure")
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
    
    @validates('working_hours')
    def _validate_working_hours(self, key, wh):
        """validates the given working hours value
        """
        if wh is None:
            # use the default one
            wh = WorkingHours()
        return wh
    
    @validates('daily_working_hours')
    def _validate_daily_working_hours(self, key, dwh):
        """validates the given daily working hours value
        """
        if dwh is None:
            dwh = defaults.DAILY_WORKING_HOURS
        else:
            if not isinstance(dwh, int):
                raise TypeError('%s.daily_working_hours should be an integer, '
                                'not %s' % 
                                (self.__class__.__name__,
                                 dwh.__class__.__name__))
        return dwh
    
    @property
    def root_tasks(self):
        """returns a list of Tasks which have no parent
        """
        from stalker.models.task import Task
        return Task.query\
            .filter(Task._project==self)\
            .filter(Task.parent==None)\
            .all()
    
    @property
    def assets(self):
        """returns the assets related to this project
        """
        # use joins over the session.query
        from stalker.models.asset import Asset
        
        if DBSession is not None:
            return Asset.query\
                .join(Asset.project)\
                .filter(Project.name == self.name)\
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
        import datetime
        temp = Template(defaults.TJP_PROJECT_TEMPLATE)
        
        if not self.now:
            self.now = datetime.datetime.now()
        
        return temp.render({
            'project': self,
            'datetime': datetime,
            'now': self.round_time(self.now).strftime('%Y-%m-%d-%H:%M')
        })


class WorkingHours(object):
    """A helper class to manage Project working hours.
    
    Working hours is a data class to store the weekly working hours pattern of
    the studio. 
    
    The data stored as a dictionary with the short day names are used as the
    key and the value is a list of two integers showing the working hours
    interval as the minutes after midnight. This is done in that way to ease
    the data transfer to TaskJuggler. The default value is defined in
    :mod:`stalker.conf.defaults` ::
      
      wh = WorkingHours()
      wh.working_hours = {
          'mon': [[540, 720], [820, 1080]], # 9:00 - 12:00, 13:00 - 18:00
          'tue': [[540, 720], [820, 1080]], # 9:00 - 12:00, 13:00 - 18:00
          'wed': [[540, 720], [820, 1080]], # 9:00 - 12:00, 13:00 - 18:00
          'thu': [[540, 720], [820, 1080]], # 9:00 - 12:00, 13:00 - 18:00
          'fri': [[540, 720], [820, 1080]], # 9:00 - 12:00, 13:00 - 18:00
          'sat': [], # saturday off
          'sun': [], # sunday off
      }
    
    The default value is 9:30 - 18:30 from Monday to Friday and Saturday and
    Sunday are off.
    
    The working hours can be updated by the user supplied dictionary. If the
    user supplied dictionary doesn't have all the days then the default values
    will be used for those days.
    
    It is possible to use day index and day short names as a key value to reach
    the data::
      
      from stalker.conf import defaults
      wh = WorkingHours()
      
      # this is same by doing wh.working_hours['sun']
      assert wh['sun'] == defaults.WORKING_HOURS['sun']
      
      # you can reach the data using the weekday number as index
      assert wh[0] == defaults.WORKING_HOURS['sun']
      
      # working hours of sunday if defaults are used or any other day defined
      # by the stalker.conf.defaults.DAY_ORDER
      assert wh[0] == defaults.WORKING_HOURS[defaults.DAY_ORDER[0]]
    
    :param working_hours: The dictionary that shows the working hours. The keys
      of the dictionary should be one of ['mon', 'tue', 'wed', 'thu', 'fri',
      'sat', 'sun']. And the values should be a list of two integers like
      [[int, int], [int, int], ...] format, showing the minutes after midnight.
      For missing days the default value will be used. If skipped the default
      value is going to be used.
    """
    
    def __init__(self, working_hours=None, **kwargs):
        if working_hours is None:
            working_hours = defaults.WORKING_HOURS
        self._wh = None
        self.working_hours = self._validate_working_hours(working_hours)
    
    def __eq__(self, other):
        """equality test
        """
        return isinstance(other, WorkingHours) and \
               other.working_hours == self.working_hours
    
    def __str__(self):
        return super(object, WorkingHours).__str__(self)
    
    def __getitem__(self, item):
        if isinstance(item, int):
            return self._wh[defaults.DAY_ORDER[item]]
        elif isinstance(item, str):
            return self._wh[item]
    
    def __setitem__(self, key, value):
        self._validate_wh_value(value)
        if isinstance(key, int):
            self._wh[defaults.DAY_ORDER[key]] = value
        elif isinstance(key, str):
            # check if key is in
            if key not in defaults.DAY_ORDER:
                raise KeyError('%s accepts only %s as key, not %s' %
                               (self.__class__.__name__, defaults.DAY_ORDER,
                                key))
            self._wh[key] = value
    
    def _validate_working_hours(self, wh_in):
        """validates the given working hours
        """
        if not isinstance(wh_in, dict):
            raise TypeError('%s.working_hours should be a dictionary, not %s' % 
                            (self.__class__.__name__,
                             wh_in.__class__.__name__))
        
        for key in wh_in.keys():
            if not isinstance(wh_in[key], list):
                raise TypeError('%s.working_hours should be a dictionary with '
                                'keys "sun, mon, tue, wed, thu, fri, sat" '
                                'and the values should a list of lists of '
                                'two integers like [[540, 720], [800, 1080]], '
                                'not %s' % (self.__class__.__name__,
                                            wh_in[key].__class__.__name__))
            
            # validate item values
            self._validate_wh_value(wh_in[key])
        
        # update the default values with the supplied working_hour dictionary
        # copy the defaults
        wh_def = copy.copy(defaults.WORKING_HOURS)
        # update them
        wh_def.update(wh_in)
        
        return wh_def
    
    @property
    def working_hours(self):
        """the getter of _wh
        """
        return self._wh
    
    @working_hours.setter
    def working_hours(self, wh_in):
        """the setter of _wh
        """
        self._wh = self._validate_working_hours(wh_in)
    
    def is_working_hour(self, datetime):
        """checks if the given datetime is in working hours
        """
        pass
    
    def _validate_wh_value(self, value):
        """validates the working hour value
        """
        err = '%s.working_hours value should be a list of lists of two ' \
              'integers between and the range of integers should be 0-1440, ' \
              'not %s'
        
        if not isinstance(value, list):
            raise TypeError(err % (self.__class__.__name__,
                                   value.__class__.__name__))
        
        for i in value:
            if not isinstance(i, list):
                raise TypeError( err % (self.__class__.__name__,
                                        i.__class__.__name__))
            
            # check list length
            if len(i) != 2:
                raise RuntimeError( err %  (self.__class__.__name__, value))
            
            # check type
            if not isinstance(i[0], int) or not isinstance(i[1], int):
                raise TypeError(err % (self.__class__.__name__, value))
            
            # check range
            if i[0] < 0 or i[0] > 1440 or i[1] < 0 or i[1] > 1440:
                raise ValueError(err % (self.__class__.__name__, value))
        
        return value
    
    @property
    def to_tjp(self):
        """returns TaskJuggler representation of this object
        """
        # render the template
        from jinja2 import Template
        
        template = Template(defaults.TJP_WORKING_HOURS_TEMPLATE)
        return template.render({'workinghours': self})
    
    @property
    def weekly_working_hours(self):
        """returns the total working hours in a week
        """
        weekly_working_hours = 0
        for i in range(0, 7):
            for start, end in self[i]:
                weekly_working_hours += (end - start)
        return weekly_working_hours / 60.0




# PROJECT_USERS
Project_Users = Table(
    'Project_Users', Base.metadata,
    Column('user_id', Integer, ForeignKey('Users.id'), primary_key=True),
    Column('project_id', Integer, ForeignKey('Projects.id'), primary_key=True)
)
