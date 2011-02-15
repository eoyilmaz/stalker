#-*- coding: utf-8 -*-
"""This module contains the Mixins (ta taaa).

Mixins are, you know, things that we love. Ok I don't have anything to write,
just use and love them.

For SQLAlchemy part of the mixins (tables and mappers) refer to the
:mod:`~stalker.db.mixin`. There is a corresponding type for every mixin
implemented in this module. Also the documentation explains how to mixin tables
and mappers.
"""



import datetime
from stalker.core.models import link, status
from stalker.ext.validatedList import ValidatedList





########################################################################
class ReferenceMixin(object):
    """Adds reference capabilities to the mixed in class.
    
    References are :class:`~stalker.core.models.link.Link` objects which adds
    outside information to the attached objects. The aim of the References are
    generally to give more info to direct the evolution of the objects,
    generally these objects are :class:`~stalker.core.models.asset.Asset`\ s.
    """
    
    
    
    _references = ValidatedList([], link.Link)
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 references=ValidatedList([], link.Link),
                 **kwargs):
        
        self._validate_references(references)
    
    
    
    #----------------------------------------------------------------------
    def _validate_references(self, references_in):
        """validates the given references_in
        """
        
        # it should be an object supporting indexing, not necessarily a list
        if not (hasattr(references_in, "__setitem__") and \
                hasattr(references_in, "__getitem__")):
            raise ValueError("the references_in should support indexing")
        
        # all the elements should be instance of stalker.core.models.link.Link
        if not all([isinstance(element, link.Link)
                    for element in references_in]):
            raise ValueError("all the elements should be instances of "
                             ":class:`~stalker.core.models.link.Link`")
        
        return ValidatedList(references_in, link.Link)
    
    
    
    #----------------------------------------------------------------------
    def references():
        
        def fget(self):
            return self._references
        
        def fset(self, references_in):
            self._references = self._validate_references(references_in)
        
        doc="""references are lists containing
        :class:`~stalker.core.models.link.Link` objects
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
      StatusList.target_type should match the current class.
    
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
        
        # it is not an instance of status_list
        if not isinstance(status_list_in, status.StatusList):
            raise ValueError("the status list should be an instance of "
                             "stalker.core.models.status.StatusList")
        
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
        
        if not isinstance(self.status_list, status.StatusList):
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
        :class:`~stalker.core.models.status.Status` object in the
        :class:`~stalker.core.models.status.StatusList` of this object.
        """
        
        return locals()
    
    status = property(**status())
        
    
    
    
    #----------------------------------------------------------------------
    def status_list():
        
        def fget(self):
            return self._status_list
        
        def fset(self, status_list_in):
            self._status_list = self._validate_status_list(status_list_in)
        
        doc = """The list of statuses that this object has.
        
        This is the property that sets and returns the status_list
        attribute
        """
        
        return locals()
    
    status_list = property(**status_list())






########################################################################
class ScheduleMixin(object):
    """Adds schedule info to the mixed in class.
    
    The schedule is the right mixin for entities which needs schedule
    information like ``start_date``, ``due_date`` and ``duration``
    
    The date attributes can be managed with timezones. Follow the Python idioms
    shown in the `documentation of datetime`_
    
    .. _documentation of datetime: http://docs.python.org/library/datetime.html
    
    :param start_date: the start date of the entity, should be a datetime.date
      instance, when given as None or tried to be set to None, it is to set to
      today, setting the start date also effects due date, if the new
      start_date passes the due_date the due_date is also changed to a date to
      keep the timedelta between dates. The default value is
      datetime.date.today()
    
    :type start_date: :class:`datetime.datetime`
    
    :param due_date: the due_date of the entity, should be a datetime.date or
      datetime.timedelta instance, if given as a datetime.timedelta, then it
      will be converted to date by adding the timedelta to the start_date
      attribute, when the start_date is changed to a date passing the due_date,
      then the due_date is also changed to a later date so the timedelta is
      kept between the dates. The default value is 10 days given as
      datetime.timedelta
    
    :type due_date: :class:`datetime.datetime` or :class:`datetime.timedelta`
    
    """
    
    
    _start_date = datetime.date.today()
    _due_date = _start_date + datetime.timedelta(days=10)
    _duration = _due_date - _start_date
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 start_date=datetime.date.today(),
                 due_date=datetime.timedelta(days=10),
                 **kwargs
                 ):
        
        self._start_date = self._validate_start_date(start_date)
        self._due_date = self._validate_due_date(due_date)
        self._duration = self.due_date - self.start_date
    
    
    
    #----------------------------------------------------------------------
    def _validate_due_date(self, due_date_in):
        """validates the given due_date_in value
        """
        
        if due_date_in is None:
            due_date_in = datetime.timedelta(days=10)
        
        if not isinstance(due_date_in, (datetime.date, datetime.timedelta)):
            raise ValueError("the due_date should be an instance of "
                             "datetime.date or datetime.timedelta")
        
        if isinstance(due_date_in, datetime.date) and \
           self.start_date > due_date_in:
            raise ValueError("the due_date should be set to a date passing "
                             "the start_date, or should be set to a "
                             "datetime.timedelta")
        
        if isinstance(due_date_in, datetime.timedelta):
            due_date_in = self._start_date + due_date_in
        
        return due_date_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_start_date(self, start_date_in):
        """validates the given start_date_in value
        """
        
        if start_date_in is None:
            start_date_in = datetime.date.today()
        
        if not isinstance(start_date_in, datetime.date):
            raise ValueError("start_date shouldbe an instance of "
                             "datetime.date")
        
        return start_date_in
    
    
    
    #----------------------------------------------------------------------
    def due_date():
        def fget(self):
            return self._due_date
        
        def fset(self, due_date_in):
            self._due_date = self._validate_due_date(due_date_in)
            
            # update the _project_duration
            self._duration = self._due_date - self._start_date
        
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
            self._start_date = self._validate_start_date(start_date_in)
            
            # check if start_date is passing due_date and offset due_date
            # accordingly
            if self._start_date > self._due_date:
                self._due_date = self._start_date + self._duration
            
            # update the project duration
            self._duration = self._due_date - self._start_date
        
        doc = """The date that this entity should start.
        
        Also effects the due_date in certain conditions, if the start_date is
        set to a time passing the due_date it will also offset the due_date to
        keep the time difference between the start_date and due_date.
        start_date should be an instance of datetime.date and the default value
        is datetime.date.today()"""
        
        return locals()
    
    start_date = property(**start_date())
    
    
    
    #----------------------------------------------------------------------
    def duration():
        def fget(self):
            return self._duration
        
        doc = """Duration of the project.
        
        The duration is calculated by subtracting start_date from the due_date,
        so it is a datetime.timedelta, for now it is read-only
        """
        
        return locals()
    
    duration = property(**duration())
    
    
    

