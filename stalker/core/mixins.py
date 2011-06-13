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
    
    References are :class:`stalker.core.models.Link` objects which adds
    outside information to the attached objects. The aim of the References are
    generally to give more info to direct the evolution of the object.
    
    :param references: A list of :class:`~stalker.core.models.Link` objects.
      For more detail about references see the
      :class:`~stalker.core.models.Link` documentation.
    
    :type references: list of :class:`~stalker.core.models.Link` objects
    
    """
    
    
    
    _references = ValidatedList([], "stalker.core.models.Link")
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 references=ValidatedList([], "stalker.core.models.Link"),
                 **kwargs):
        
        self._references = self._validate_references(references)
    
    
    
    #----------------------------------------------------------------------
    def _validate_references(self, references_in):
        """validates the given references_in
        """
        
        # it should be an object supporting indexing, not necessarily a list
        if not (hasattr(references_in, "__setitem__") and \
                hasattr(references_in, "__getitem__")):
            raise ValueError("the references_in should support indexing")
        
        #from stalker.core.models import Link
        from stalker.core import models
        
        # all the elements should be instance of stalker.core.models.Link
        if not all([isinstance(element, models.Link)
                    for element in references_in]):
            raise ValueError("all the elements should be instances of "
                             ":class:`stalker.core.models.Link`")
        
        return ValidatedList(references_in, models.Link)
    
    
    
    #----------------------------------------------------------------------
    def references():
        
        def fget(self):
            return self._references
        
        def fset(self, references_in):
            self._references = self._validate_references(references_in)
        
        doc="""References are lists containing :class:`~stalker.core.models.Link` objects.
        """
        
        return locals()
    
    references = property(**references())






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
        
        self._status_list = self._validate_status_list(status_list)
        self._status = self._validate_status(status)
    
    
    
    #----------------------------------------------------------------------
    def _validate_status_list(self, status_list_in):
        """validates the given status_list_in value
        """
        
        # raise ValueError when:
        from stalker.core import models
        
        # it is not an instance of status_list
        if not isinstance(status_list_in, models.StatusList):
            raise ValueError("the status list should be an instance of "
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
        
        # raise ValueError when there is no status_list is not an instance of
        # StatusList
        
        from stalker.core.models import StatusList
        
        if not isinstance(self.status_list, StatusList):
            raise ValueError("please set the status_list attribute first")
        
        # it is set to None
        if status_in is None:
            raise ValueError("the status couldn't be None, set it to a "
                             "non-negative integer")
        
        # it is not an instance of int
        if not isinstance(status_in, int):
            raise ValueError("the status must be an instance of integer")
        
        # if it is not in the correct range:
        if status_in < 0:
            raise ValueError("the status must be a non-negative integer")
        
        if status_in >= len(self._status_list.statuses):
            raise ValueError("the status can not be bigger than the length of "
                             "the status_list")
        
        return status_in
    
    
    
    #----------------------------------------------------------------------
    def status():
        
        def fget(self):
            return self._status
        
        def fset(self, status_in):
            self._status = self._validate_status(status_in)
        
        doc = """The current status index of the object.
        
        This is an integer value and shows the index of the
        :class:`~stalker.core.models.Status` object in the
        :class:`~stalker.core.models.StatusList` of this object.
        """
        
        return locals()
    
    status = property(**status())
    
    
    
    #----------------------------------------------------------------------
    def status_list():
        
        def fget(self):
            return self._status_list
        
        def fset(self, status_list_in):
            self._status_list = self._validate_status_list(status_list_in)
        
        doc = """The list of statuses that this object can have.
        
        
        """
        
        return locals()
    
    status_list = property(**status_list())






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
        
        self._start_date = None
        self._due_date = None
        self._duration = None
        
        self._validate_dates(start_date, due_date, duration)
    
    
    
    #----------------------------------------------------------------------
    def due_date():
        def fget(self):
            return self._due_date
        
        def fset(self, due_date_in):
            #self._due_date = self._validate_due_date(due_date_in)
            
            # update the project duration
            #self.update_duration()
            
            self._validate_dates(self.start_date,
                                 due_date_in,
                                 self.duration)
        
        doc = """The date that the entity should be delivered.
        
        The due_date can be set to a datetime.timedelta and in this case it
        will be calculated as an offset from the start_date and converted to
        datetime.date again. Setting the start_date to a date passing the
        due_date will also set the due_date so the timedelta between them is
        preserved, default value is 10 days"""
        
        return locals()
    
    due_date = property(**due_date())
    
    
    
    #----------------------------------------------------------------------
    def start_date():
        def fget(self):
            return self._start_date
        
        def fset(self, start_date_in):
            #self._start_date = self._validate_start_date(start_date_in)
            
            # check if start_date is passing due_date and offset due_date
            # accordingly
            #if self._start_date > self._due_date:
                #self._due_date = self._start_date + self._duration
            
            # update the project duration
            #self.update_duration()
            
            self._validate_dates(start_date_in, self.due_date, self.duration)
        
        doc = """The date that this entity should start.
        
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
        
        return locals()

    start_date = property(**start_date())
    
    
    
    #----------------------------------------------------------------------
    def duration():
        def fget(self):
            return self._duration
        
        def fset(self, duration_in):
            
            if not duration_in is None:
                if isinstance(duration_in, datetime.timedelta):
                    # set the due_date to None
                    # to make it recalculated
                    self._validate_dates(self.start_date, None, duration_in)
                else:
                    self._validate_dates(self.start_date, self.due_date, duration_in)
            else:
                self._validate_dates(self.start_date, self.due_date, duration_in)
        
        doc = """Duration of the project.
        
        It is a datetime.timedelta instance. Showing the difference of the
        :attr:`~stalker.core.mixins.ScheduleMixin.start_date` and the
        :attr:`~stalker.core.mixins.ScheduleMixin.due_date`. If edited it
        changes the :attr:`~stalker.core.mixins.ScheduleMixin.due_date`
        attribute value.
        """
        
        return locals()
    
    duration = property(**duration())
    
    
    
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
    """Gives the abilitiy to connect to a list of taks to the mixed in object.
    
    :param list tasks: The list of :class:`~stalker.core.models.Task`\ s.
      Should be a list of :class:`~stalker.core.models.Task` instances. Default
      value is an empty list.
    """
    
    
    
    _tasks = ValidatedList([], "stalker.core.models.Task")
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, tasks=[], **kwargs):
        self._tasks = self._validate_tasks(tasks)
    
    
    
    #----------------------------------------------------------------------
    def _validate_tasks(self, tasks_in):
        """validates the given tasks_in value
        """
        
        if tasks_in is None:
            tasks_in = []
        
        if not isinstance(tasks_in, list):
            raise ValueError("tasks should be a list")
        
        from stalker.core.models import Task
        
        for item in tasks_in:
            if not isinstance(item, Task):
                raise ValueError("tasks should be a list of "
                "stalker.core.models.Task instances")
        
        return ValidatedList(tasks_in, Task)
    
    
    
    #----------------------------------------------------------------------
    def tasks():
        def fget(self):
            return self._tasks
        def fset(self, task_in):
            self._tasks = self._validate_tasks(task_in)
        
        doc = """The list of :class:`~stalker.core.models.Task` instances.
        """
        
        return locals()
    
    tasks = property(**tasks())






