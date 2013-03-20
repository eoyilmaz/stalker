# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
import copy

from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, validates
from stalker import User
from stalker.conf import defaults
from stalker.db.session import DBSession
from stalker.models.entity import Entity, SimpleEntity
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
    
    :param users: A list of :class:`~stalker.models.auth.User`\ s holding the
      users in this project. This will create a reduced or grouped list of
      studio workers and will make it easier to define the resources for a Task
      related to this project. The default value is an empty list.
    """
    
    # DELETED ARGUMENTS:
    #
    #:param float display_width: the width of the display that the output of the
    #  project is going to be displayed (very unnecessary if you are not using
    #  stereo 3D setup). Should be an int or float value, negative values
    #  converted to the positive values. Default value is 1.
    
    # ------------------------------------------------------------------------
    # NOTES:
    #
    # Because a Project instance is inherited from TaskableEntity and which is
    # mixed with the ProjectMixin it has a project attribute. In SOM, the
    # project instantly assigns itself to the project attribute (in __init__).
    # But this creates a weird position in database table and mapper
    # configuration where for the Project class the mapper should configure the
    # `project` attribute with the post_update flag is set to True, and this
    # implies the project_id column to be Null for a while, at least
    # SQLAlchemy does an UPDATE to assign the Project itself to the project
    # attribute, thus the project_id column shouldn't be nullable for Project
    # class, but it is not necessary for the others.
    # 
    # And because SOM is also checking if the project attribute is None or Null
    # for the created instance, I consider doing this safe.
    # ------------------------------------------------------------------------

    __auto_name__ = False
    #__strictly_typed__ = True
    __tablename__ = "Projects"
    project_id_local = Column("id", Integer, ForeignKey("TaskableEntities.id"),
                              primary_key=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "Project",
        "inherit_condition":
            project_id_local==Entity.entity_id
    }
    
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
    
    def __init__(self,
                 name=None,
                 code=None,
                 lead=None,
                 repository=None,
                 structure=None,
                 image_format=None,
                 fps=25.0,
                 is_stereoscopic=False,
                 #display_width=1.0,
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
        self._users = []
        self.repository = repository
        self.structure = structure
        self._sequences = []
        self._assets = []

        self.image_format = image_format
        self.fps = fps
        self.is_stereoscopic = bool(is_stereoscopic)
        self.code = code
    
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
    
    @validates("is_stereoscopic")
    def _validate_is_stereoscopic(self, key, is_stereoscopic_in):
        return bool(is_stereoscopic_in)
    
    @property
    def users(self):
        """returns the users related to this project
        """
        from stalker.models.auth import User
        from stalker.models.task import Task
        
        if DBSession is not None:
            return DBSession.query(User).\
            join(User.tasks).\
            join(Task.task_of).\
            join(TaskableEntity.project).\
            filter(Project.name == self.name).all()
        else:
            RuntimeWarning("There is no database setup, the users can not "
                           "be queried from this state, please use "
                           "stalker.db.setup() to setup a database")
            return []
    
    @property
    def assets(self):
        """returns the assets related to this project
        """
        # use joins over the session.query
        from stalker.models.asset import Asset
        
        if DBSession is not None:
            return DBSession.query(Asset).\
            join(Asset.project).\
            filter(Project.name == self.name).all()
        else:
            RuntimeWarning("There is no database setup, the users can not "
                           "be queried from this state, please use "
                           "stalker.db.setup() to setup a database")
            return []
    
    @property
    def sequences(self):
        """returns the sequences related to this project
        """
        # use joins over the session.query
        from stalker.models.sequence import Sequence
        
        if DBSession is not None:
            return Sequence.query\
                .join(Sequence.project)\
                .filter(Project.name == self.name).all()
        else:
            RuntimeWarning("There is no database setup, the sequences can not "
                           "be queried from this state, please use "
                           "stalker.db.setup() to setup a database")
            return []
    
    @property
    def project_tasks(self):
        """returns the Tasks which are direct or indirectly related to this
        Project
        """
        if DBSession is not None:
            from stalker import Task
            return Task.query\
                .join(Task.task_of)\
                .join(TaskableEntity.project)\
                .filter(Project.id == self.id)\
                .all()
        else:
            RuntimeWarning("There is no database setup, the tasks can not "
                           "be queried from this state, please use "
                           "stalker.db.setup() to setup a database")
            return []
     
    def __eq__(self, other):
        """the equality operator
        """
        return super(Project, self).__eq__(other) and\
               isinstance(other, Project)


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
    
    def working_hours_of_day(self, day):
        """returns the working hours of the given day
        
        :param day: if given an integer it will use it as the weekday number
           ([0(Sunday),6]), if it is a string then it is considered the lower
           case abbreviated weekday name (['sun', 'mon', 'tue', 'thu', 'fri',
           'sat', 'sun'])
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
