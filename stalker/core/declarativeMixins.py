#-*- coding: utf-8 -*-
"""This module contains the Mixins (ta taaa).

Mixins are, you know, things that we love. Ok I don't have anything to write,
just use and love them.
""" 



import datetime
from sqlalchemy import (
    Table,
    Column,
    Date,
    Interval,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import relationship, synonym, validates
from sqlalchemy.ext.declarative import declared_attr

from stalker.conf import defaults
from stalker.core.declarativeModels import Base






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
    
    
    
    #----------------------------------------------------------------------
    @classmethod
    def create_secondary_tables(cls):
        """creates any secondary table
        """
        
        class_name = cls.__name__
        
        # use the given class_name and the class_table
        secondary_table_name = class_name + "_References"
        secondary_table = None
        
        # check if the table is already defined
        if secondary_table_name not in Base.metadata:
            secondary_table = Table(
                secondary_table_name, Base.metadata,
                Column(
                    class_name.lower() + "_id",
                    Integer,
                    ForeignKey(cls.__tablename__ + ".id"),
                    primary_key=True,
                ),
                
                Column(
                    "reference_id",
                    Integer,
                    ForeignKey("Links.id"),
                    primary_key=True,
                )
            )
        else:
            secondary_table = Base.metadata.tables[secondary_table_name]
        
        return secondary_table
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def references(cls):
        
        class_name = cls.__name__
        
        # get secondary table
        secondary_table = cls.create_secondary_tables()
        
        # return the relationship
        return relationship("Link", secondary=secondary_table)
    
    
    
    #----------------------------------------------------------------------
    @validates("references")
    def _validate_references(self, key, reference):
        """validates the given reference
        """
        
        from stalker.core.declarativeModels import SimpleEntity
        
        # all the elements should be instance of stalker.core.models.Entity
        if not isinstance(reference, SimpleEntity):
            raise TypeError("all the elements should be instances of "
                             ":class:`stalker.core.models.Entity`")
        
        return reference






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
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, status=0, status_list=None, **kwargs):
        self.status_list = status_list
        self.status = status
    
    
    
    #----------------------------------------------------------------------
    @classmethod
    def create_secondary_tables(cls):
        """creates any secondary table
        """
        
        class_name = cls.__name__
        
        # use the given class_name and the class_table
        secondary_table_name = class_name + "_References"
        secondary_table = None
        
        # check if the table is already defined
        if secondary_table_name not in Base.metadata:
            secondary_table = Table(
                secondary_table_name, Base.metadata,
                Column(
                    class_name.lower() + "_id",
                    Integer,
                    ForeignKey(cls.__tablename__ + ".id"),
                    primary_key=True,
                ),
                
                Column(
                    "reference_id",
                    Integer,
                    ForeignKey("Links.id"),
                    primary_key=True,
                )
            )
        else:
            secondary_table = Base.metadata.tables[secondary_table_name]
        
        return secondary_table
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def status(cls):
        return Column("status", Integer, default=0)
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def status_list_id(cls):
        return Column(
            "status_list_id",
            Integer,
            ForeignKey("StatusLists.id"),
            nullable=False
        )
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def status_list(cls):
        return relationship(
            "StatusList",
            primaryjoin=\
                "%s.status_list_id==StatusList.statusList_id" % cls.__name__
        )
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def references(cls):
        
        class_name = cls.__name__
        
        # get secondary table
        secondary_table = cls.create_secondary_tables()
        
        # return the relationship
        return relationship("Link", secondary=secondary_table)
    
    
    
    #----------------------------------------------------------------------
    @validates("status_list")
    def _validate_status_list(self, key, status_list):
        """validates the given status_list_in value
        """
        
        # raise TypeError when:
        from stalker.core.declarativeModels import StatusList
        
        # it is not an instance of status_list
        if not isinstance(status_list, StatusList):
            raise TypeError("the status list should be an instance of "
                             "stalker.core.models.StatusList")
        
        # check if the entity_type matches to the StatusList.target_entity_type
        if self.__class__.__name__ != status_list.target_entity_type:
            raise TypeError("the given StatusLists' target_entity_type is %s, "
                            "whereas the entity_type of this object is %s" % \
                            (status_list.target_entity_type,
                             self.__class__.__name__))
        
        return status_list
    
    
    
    #----------------------------------------------------------------------
    @validates("status")
    def _validate_status(self, key, status):
        """validates the given status value
        """
        
        from stalker.core.declarativeModels import StatusList
        
        if not isinstance(self.status_list, StatusList):
            raise TypeError("please set the status_list attribute first")
        
        # it is set to None
        if status is None:
            raise TypeError("the status couldn't be None, set it to a "
                             "non-negative integer")
        
        # it is not an instance of int
        if not isinstance(status, int):
            raise TypeError("the status must be an instance of integer")
        
        # if it is not in the correct range:
        if status < 0:
            raise ValueError("the status must be a non-negative integer")
        
        if status >= len(self.status_list.statuses):
            raise ValueError("the status can not be bigger than the length of "
                             "the status_list")
        
        return status






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
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 start_date=None,
                 due_date=None,
                 duration=None,
                 **kwargs
                 ):
        
        self._validate_dates(start_date, due_date, duration)
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def _due_date(cls):
        return Column("due_date", Date)
    
    
    
    #----------------------------------------------------------------------
    def _due_date_getter(self):
        """The date that the entity should be delivered.
        
        The due_date can be set to a datetime.timedelta and in this case it
        will be calculated as an offset from the start_date and converted to
        datetime.date again. Setting the start_date to a date passing the
        due_date will also set the due_date so the timedelta between them is
        preserved, default value is 10 days
        """
        
        return self._due_date
    
    #----------------------------------------------------------------------
    def _due_date_setter(self, due_date_in):
        self._validate_dates(self.start_date, due_date_in, self.duration)
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def due_date(cls):
        return synonym(
            "_due_date",
            descriptor=property(
                cls._due_date_getter,
                cls._due_date_setter
            )
        )
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def _start_date(cls):
        return Column("start_date", Date)
    
    
    
    #----------------------------------------------------------------------
    def _start_date_getter(self):
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
    def _start_date_setter(self, start_date_in):
        self._validate_dates(start_date_in, self.due_date, self.duration)
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def start_date(cls):
        return synonym(
            "_start_date",
            descriptor=property(
                cls._start_date_getter,
                cls._start_date_setter,
            )
        )
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def _duration(cls):
        return Column("duration", Interval)
    
    
    
    #----------------------------------------------------------------------
    def _duration_getter(self):
        """Duration of the entity.
        
        It is a datetime.timedelta instance. Showing the difference of the
        :attr:`~stalker.core.mixins.ScheduleMixin.start_date` and the
        :attr:`~stalker.core.mixins.ScheduleMixin.due_date`. If edited it
        changes the :attr:`~stalker.core.mixins.ScheduleMixin.due_date`
        attribute value.
        """
        return self._duration
    
    #----------------------------------------------------------------------
    def _duration_setter(self, duration_in):
        
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
    @declared_attr
    def duration(cls):
        return synonym(
            "_duration",
            descriptor=property(
                cls._duration_getter,
                cls._duration_setter
            )
        )
    
    
    
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





