#-*- coding: utf-8 -*-
"""This module contains the Mixins (ta taaa).

Mixins are, you know, things that we love. Ok I don't have anything to write,
just use and love them.

For SQLAlchemy part of the mixins (tables and mappers) refer to the
:mod:`~stalker.db.mixin`. There is a corresponding helper class for every mixin
implemented in this module. Also the documentation explains how to mixin tables
and mappers.
""" 



import datetime
from stalker.conf import defaults
from stalker.ext.validatedList import ValidatedList






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
    
    
    
    _references = ValidatedList([], "stalker.core.models.Entity")
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 references=ValidatedList([], "stalker.core.models.Entity"),
                 **kwargs):
        # pylint: disable=W0613
        
        self._references = self._validate_references(references)
    
    
    
    #----------------------------------------------------------------------
    def _validate_references(self, references_in):
        """validates the given references_in
        """
        
        # it should be an object supporting indexing, not necessarily a list
        if not (hasattr(references_in, "__setitem__") and \
                hasattr(references_in, "__getitem__")):
            raise TypeError("the references_in should support indexing")
        
        from stalker.core import models  # pylint: disable=W0404
        
        # all the elements should be instance of stalker.core.models.Link
        if not all([isinstance(element, models.Entity)
                    for element in references_in]):
            raise TypeError("all the elements should be instances of "
                             ":class:`stalker.core.models.Entity`")
        
        return ValidatedList(references_in, models.Entity)
    
    
    
    #----------------------------------------------------------------------
    @property
    def references(self):
        """References are lists containing :class:`~stalker.core.models.Entity` instances.
        """
        
        return self._references
    
    #----------------------------------------------------------------------
    @references.setter # pylint: disable=E1101
    def references(self, references_in):
        # pylint: disable=E0102, C0111
        self._references = self._validate_references(references_in)





########################################################################
class StatusMixin(object):
    """Adds statusabilities to the object.
    
    This mixin adds status and statusList variables to the list. Any object
    that needs a status and a corresponding status list can include this mixin.
    
    When mixed with a class which don't have an __init__ method, the mixin
    supplies one, and in this case the parameters below must be defined.
    
    :param status_list: this attribute holds a status list object, which shows
      the possible statuses that this entity could be in. This attribute can
      not be empty or None. Giving a StatusList object, the
      StatusList.target_entity_type should match the current class.
    
    :param status: an integer value which is the index of the status in the
      status_list attribute. So the value of this attribute couldn't be lower
      than 0 and higher than the length-1 of the status_list object and nothing
      other than an integer
    """
    
    
    
    _status_list = None
    _status = 0
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, status=0, status_list=None, **kwargs):
        # pylint: disable=W0613
        
        self._status_list = self._validate_status_list(status_list)
        self._status = self._validate_status(status)
    
    
    
    #----------------------------------------------------------------------
    def _validate_status_list(self, status_list_in):
        """validates the given status_list_in value
        """
        
        # raise TypeError when:
        from stalker.core import models # pylint: disable=W0404
        
        # it is not an instance of status_list
        if not isinstance(status_list_in, models.StatusList):
            raise TypeError("the status list should be an instance of "
                             "stalker.core.models.StatusList")
        
        # check if the entity_type matches to the StatusList.target_entity_type
        if self.entity_type != status_list_in.target_entity_type:
            raise TypeError("the given StatusLists' target_entity_type is %s, "
                            "whereas the entity_type of this object is %s" % \
                            (status_list_in.target_entity_type,
                             self.entity_type))
        
        return status_list_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_status(self, status_in):
        """validates the given status_in value
        """
        
        from stalker.core.models import StatusList # pylint: disable=W0404
        
        if not isinstance(self.status_list, StatusList):
            raise TypeError("please set the status_list attribute first")
        
        # it is set to None
        if status_in is None:
            raise TypeError("the status couldn't be None, set it to a "
                             "non-negative integer")
        
        # it is not an instance of int
        if not isinstance(status_in, int):
            raise TypeError("the status must be an instance of integer")
        
        # if it is not in the correct range:
        if status_in < 0:
            raise ValueError("the status must be a non-negative integer")
        
        if status_in >= len(self._status_list.statuses):
            raise ValueError("the status can not be bigger than the length of "
                             "the status_list")
        
        return status_in
    
    
    
    #----------------------------------------------------------------------
    @property
    def status(self):
        """The current status index of the object.
        
        This is an integer value and shows the index of the
        :class:`~stalker.core.models.Status` object in the
        :class:`~stalker.core.models.StatusList` of this object.
        """
        
        return self._status
    
    
    #----------------------------------------------------------------------
    @status.setter # pylint: disable=E1101
    def status(self, status_in):
        # pylint: disable=E0102, C0111
        self._status = self._validate_status(status_in)
    
    
    
    #----------------------------------------------------------------------
    @property
    def status_list(self):
        """The list of statuses that this object can have.
        """
        
        return self._status_list
    
    
    #----------------------------------------------------------------------
    @status_list.setter # pylint: disable=E1101
    def status_list(self, status_list_in):
        # pylint: disable=E0102, C0111
        self._status_list = self._validate_status_list(status_list_in)






########################################################################
class ScheduleMixin(object):
    """Adds schedule info to the mixed in class.
    
    Adds schedule information like ``start_date``, ``due_date`` and
    ``duration``. There are theree parameters to initialize a class with
    ScheduleMixin, which are, ``start_date``, ``due_date`` and ``duration``.
    Only two of them are enough to initialize the class. The preceeding order
    for the parameters is as follows::
      
      start_date > due_date > duration
    
    So if all of the parameters are given only the ``start_date`` and the
    ``due_date`` will be used and the ``duration`` will be calculated
    accordingly. In any other conditions the missing parameter will be
    calculated from the following table:
    
    +------------+----------+----------+----------------------------------------+
    | start_date | due_date | duration | DEFAULTS                               |
    +============+==========+==========+========================================+
    |            |          |          | start_date = datetime.date.today()     |
    |            |          |          |                                        |
    |            |          |          | duration = datetime.timedelta(days=10) |
    |            |          |          |                                        |
    |            |          |          | due_date = start_date + duration       |
    +------------+----------+----------+----------------------------------------+
    |     X      |          |          | duration = datetime.timedelta(days=10) |
    |            |          |          |                                        |
    |            |          |          | due_date = start_date + duration       |
    +------------+----------+----------+----------------------------------------+
    |     X      |    X     |          | duration = due_date - start_date       |
    +------------+----------+----------+----------------------------------------+
    |     X      |          |    X     | due_date = start_date + duration       |
    +------------+----------+----------+----------------------------------------+
    |     X      |    X     |    X     | duration = due_date - start_date       |
    +------------+----------+----------+----------------------------------------+
    |            |    X     |    X     | start_date = due_date - duration       |
    +------------+----------+----------+----------------------------------------+
    |            |    X     |          | duration = datetime.timedelta(days=10) |
    |            |          |          |                                        |
    |            |          |          | start_date = due_date - duration       |
    +------------+----------+----------+----------------------------------------+
    |            |          |    X     | start_date = datetime.date.today()     |
    |            |          |          |                                        |
    |            |          |          | due_date = start_date + duration       |
    +------------+----------+----------+----------------------------------------+
      
    The date attributes can be managed with timezones. Follow the Python idioms
    shown in the `documentation of datetime`_
    
    .. _documentation of datetime: http://docs.python.org/library/datetime.html
    
    :param start_date: the start date of the entity, should be a datetime.date
      instance, the start_date is the pin point for the date calculation. In
      any condition if the start_date is available then the value will be
      preserved. If start_date passes the due_date the due_date is also changed
      to a date to keep the timedelta between dates. The default value is
      datetime.date.today()
    
    :type start_date: :class:`datetime.datetime`
    
    :param due_date: the due_date of the entity, should be a datetime.date
      instance, when the start_date is changed to a date passing the due_date,
      then the due_date is also changed to a later date so the timedelta
      between the dates is kept.
    
    :type due_date: :class:`datetime.datetime` or :class:`datetime.timedelta`
    
    :param duration: The duration of the entity. It is a
      :class:`datetime.timedelta` instance. The default value is read from
      the :mod:`~stalker.conf.defaults` module. See the table above for the
      initialization rules.
    
    :type duration: :class:`datetime.timedelta`
    """
    
    
    _start_date = None
    _due_date = None
    _duration = None
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 start_date=None,
                 due_date=None,
                 duration=None,
                 **kwargs
                 ):
        # pylint: disable=W0613
        
        self._start_date = None
        self._due_date = None
        self._duration = None
        
        self._validate_dates(start_date, due_date, duration)
    
    
    
    #----------------------------------------------------------------------
    @property
    def due_date(self):
        """The date that the entity should be delivered.
        
        The due_date can be set to a datetime.timedelta and in this case it
        will be calculated as an offset from the start_date and converted to
        datetime.date again. Setting the start_date to a date passing the
        due_date will also set the due_date so the timedelta between them is
        preserved, default value is 10 days
        """
        
        return self._due_date
    
    #----------------------------------------------------------------------
    @due_date.setter # pylint: disable=E1101
    def due_date(self, due_date_in):
        # pylint: disable=E0102, C0111
        self._validate_dates(self.start_date, due_date_in, self.duration)
    
    
    
    #----------------------------------------------------------------------
    @property
    def start_date(self):
        """The date that this entity should start.
        
        Also effects the
        :attr:`~stalker.core.mixins.ScheduleMixin.due_date` attribute value in
        certain conditions, if the
        :attr:`~stalker.core.mixins.ScheduleMixin.start_date` is set to a time
        passing the :attr:`~stalker.core.mixins.ScheduleMixin.due_date` it will
        also offset the :attr:`~stalker.core.mixins.ScheduleMixin.due_date` to
        keep the :attr:`~stalker.core.mixins.ScheduleMixin.duration` value
        fixed. :attr:`~stalker.core.mixins.ScheduleMixin.start_date` should be
        an instance of class:`datetime.date` and the default value is
        :func:`datetime.date.today()`
        """
        return self._start_date
    
    #----------------------------------------------------------------------
    @start_date.setter # pylint: disable=E1101
    def start_date(self, start_date_in):
        # pylint: disable=E0102, C0111
        self._validate_dates(start_date_in, self.due_date, self.duration)
    
    
    
    #----------------------------------------------------------------------
    @property
    def duration(self):
        """Duration of the entity.
        
        It is a datetime.timedelta instance. Showing the difference of the
        :attr:`~stalker.core.mixins.ScheduleMixin.start_date` and the
        :attr:`~stalker.core.mixins.ScheduleMixin.due_date`. If edited it
        changes the :attr:`~stalker.core.mixins.ScheduleMixin.due_date`
        attribute value.
        """
        return self._duration
    
    #----------------------------------------------------------------------
    @duration.setter # pylint: disable=E1101
    def duration(self, duration_in):
        # pylint: disable=E0102, C0111
        
        if not duration_in is None:
            if isinstance(duration_in, datetime.timedelta):
                # set the due_date to None
                # to make it recalculated
                self._validate_dates(self.start_date, None, duration_in)
            else:
                self._validate_dates(self.start_date, self.due_date, duration_in)
        else:
            self._validate_dates(self.start_date, self.due_date, duration_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_dates(self, start_date, due_date, duration):
        """updates the date values
        """
        
        
        if not isinstance(start_date, datetime.date):
            start_date = None
        
        if not isinstance(due_date, datetime.date):
            due_date = None
        
        if not isinstance(duration, datetime.timedelta):
            duration = None
        
        
        # check start_date
        if start_date is None:
            # try to calculate the start_date from due_date and duration
            if due_date is None:
                
                # set the defaults
                start_date = datetime.date.today()
                
                if duration is None:
                    # set the defaults
                    duration = defaults.DEFAULT_TASK_DURATION
                
                due_date = start_date + duration
            else:
                
                if duration is None:
                    duration = defaults.DEFAULT_TASK_DURATION
                
                start_date = due_date - duration
        
        # check due_date
        if due_date is None:
            
            if duration is None:
                duration = defaults.DEFAULT_TASK_DURATION
            
            due_date = start_date + duration
        
        
        if due_date < start_date:
            
            # check duration
            if duration < datetime.timedelta(1):
                duration = datetime.timedelta(1)
            
            due_date = start_date + duration
        
        self._start_date = start_date
        self._due_date = due_date
        self._duration = self._due_date - self._start_date






########################################################################
class TaskMixin(object):
    """Gives the abilitiy to connect to a list of :class:`~stalker.core.models.Task`\ s to the mixed in object.
    
    TaskMixin lets the mixed object to have :class:`~stalker.core.model.Task`
    instances to be attached it self. And because
    :class:`~stalker.core.models.Task`\ s are related to
    :class:`~stalker.core.models.Project`\ s, it also adds ability to relate
    the object to a :class:`~stalker.core.models.Project` instance. So every
    object which is mixed with TaskMixin will have a
    :attr:`~stalker.core.mixins.TaskMixin.tasks` and a
    :attr:`~stalker.core.mixins.TaskMixin.project` attribute. Only the
    ``project`` argument needs to be initialized.
    
    :param project: A :class:`~stalker.core.models.Project` instance holding
      the project which this object is related to. It can not be None, or
      anything other than a :class:`~stalker.core.models.Project` instance.
    
    :type project: :class:`~stalker.core.models.Project`
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, project=None, **kwargs): # pylint: disable=W0613
        self._project = self._validate_project(project)
        self._tasks = ValidatedList(
            [],
            "stalker.core.models.Task",
            self.__task_item_validator__
        )
    
    
    
    #----------------------------------------------------------------------
    def _validate_tasks(self, tasks_in):
        """validates the given tasks_in value
        """
        
        if tasks_in is None:
            tasks_in = []
        
        if not isinstance(tasks_in, list):
            raise TypeError("tasks should be a list")
        
        from stalker.core.models import Task # pylint: disable=W0404
        
        for item in tasks_in:
            if not isinstance(item, Task):
                raise TypeError("tasks should be a list of "
                "stalker.core.models.Task instances")
        
        return ValidatedList(tasks_in, Task, self.__task_item_validator__)
    
    
    
    #----------------------------------------------------------------------
    def __task_item_validator__(self, tasks_added, tasks_removed):
        """a callable for more granular control over tasks list
        """
        # pylint: disable=E1003
        
        # add the current instance to tasks._task_of attribute
        for task in tasks_added:
            # remove it from the current owner
            try:
                # invoke no remove update by calling the supers (list) remove
                super(ValidatedList, task._task_of.tasks).remove(task)
            except ValueError: # there is no owner, probably it was
                pass           # initializing for the first time
            
            # set self to task_of of the Task
            task._task_of = self
        
        # removing tasks by removing it from the tasks list of a taskable
        # object is not allowed
        if len(tasks_removed) > 0:
            raise RuntimeError("tasks can not be removed in this way, please "
                               "assign the task to a new taskable object")
    
    
    
    #----------------------------------------------------------------------
    def _validate_project(self, project_in):
        """validates the given project value
        """
        
        if project_in is None:
            raise TypeError("project can not be None it must be an instance "
                            "of stalker.core.models.Project instance")
        
        from stalker.core.models import Project # pylint: disable=W0404
        
        if not isinstance(project_in, Project):
            raise TypeError("project must be an instance of "
                            "stalker.core.models.Project instance")
        
        return project_in
    
    
    
    #----------------------------------------------------------------------
    @property
    def project(self):
        """A :class:`~stalker.core.models.Project` instance showing the
        relation of this object to a Stalker
        :class:`~stalker.core.models.Project`. It is a read only attribute, so
        you can not change the Project of an already created object.
        """
        
        return self._project
    
    
    
    #----------------------------------------------------------------------
    @property
    def tasks(self):
        """The list of :class:`~stalker.core.models.Task` instances.
        
        Be careful that you can not remove any of the elements of the ``tasks``
        list. Trying to remove a :class:`~stalker.core.models.Task` by removing
        it from the list will raise a RunTimeError. This is because the
        :class:`~stalker.core.models.Task` will become an orphan task if it is
        removed by this way. To remove the
        :class:`~stalker.core.models.Task` from the list you should delete it
        or append it to another objects ``tasks`` attribute. This attribute is
        read-only so you can not set it to another list than it has, but you
        can change the elements inside, but again be careful about orphan
        tasks (though you will be warned by a RuntimeError).
        """
        
        return self._tasks






########################################################################
class ReviewMixin(object):
    """Adds the ability of being reviewed to the mixed in object.
    
    Adds the ``reviews`` attribute to the mixed in object. The ``reivews`` is a
    :class:`~satlker.ext.validatedList.ValidatedList` accepting
    :class:`~stalker.core.models.Comment` instances.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self):
        pass
    
    
    