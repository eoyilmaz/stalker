# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import datetime
from sqlalchemy import (Table, Column, String, Integer, ForeignKey, Date,
                        Interval, Unicode)
from sqlalchemy.exc import UnboundExecutionError
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import synonym, relationship, validates
from stalker.conf import defaults
from stalker.db import Base
from stalker.db.session import DBSession

from stalker.log import logging_level
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)

def make_plural(name):
    """Returns the plural version of the given name argument.
    """
    plural_name = name + "s"
    
    if name[-1] == "y":
        plural_name = name[:-1] + "ies"
    elif name[-2:] == "ch":
        plural_name = name + "es"
    elif name[-1] == "f":
        plural_name = name[:-1] + "ves"
    elif name[-1] == "s":
        plural_name = name + "es"

    return plural_name

def create_secondary_table(
        primary_cls_name,
        secondary_cls_name,
        primary_cls_table_name,
        secondary_cls_table_name,
        secondary_table_name=None
    ):
    """creates any secondary table
    """
    
    plural_secondary_cls_name = make_plural(secondary_cls_name)
    
    # use the given class_name and the class_table
    if not secondary_table_name:
        secondary_table_name = \
            primary_cls_name + "_" + plural_secondary_cls_name
    
    # check if the table is already defined
    if secondary_table_name not in Base.metadata:
        secondary_table = Table(
            secondary_table_name, Base.metadata,
            Column(
                primary_cls_name.lower() + "_id",
                Integer,
                ForeignKey(primary_cls_table_name + ".id"),
                primary_key=True,
            ),
            
            Column(
                secondary_cls_name.lower() + "_id",
                Integer,
                ForeignKey(secondary_cls_table_name + ".id"),
                primary_key=True,
            )
        )
    else:
        secondary_table = Base.metadata.tables[secondary_table_name]
    
    return secondary_table

class TargetEntityTypeMixin(object):
    """Adds target_entity_type attribute to mixed in class.
    
    :param target_entity_type: The target entity type which this class is 
      designed for. Should be a class or a class name.
      
      For example::
        
        from stalker import SimpleEntity, TargetEntityTypeMixin, Project
        
        class A(SimpleEntity, TargetEntityTypeMixin):
            __tablename__ = "As"
            __mapper_args__ = {"polymorphic_identity": "A"}
            
            def __init__(self, **kwargs):
                super(A, self).__init__(**kwargs)
                TargetEntityTypeMixin.__init__(self, **kwargs)
        
        a_obj = A(target_entity_type=Project)
      
      The ``a_obj`` will only be accepted by
      :class:`~stalker.models.project.Project` instances. You can not assign it
      to any other class which accepts a :class:`~stalker.models.type.Type`
      instance.
    
    To control the mixed-in class behaviour add these class variables to the 
    mixed in class:
      
      __nullable_target__ : controls if the target_entity_type can be 
                            nullable or not. Default is False.
      
      __unique_target__ : controls if the target_entity_type should be 
                          unique, so there is only one object for one type.
                          Default is False.
    """
    
    __nullable_target__ = False
    __unique_target__ = False
    
    @declared_attr
    def _target_entity_type(cls):
        return Column(
            "target_entity_type",
            String(128),
            nullable=cls.__nullable_target__,
            unique=cls.__unique_target__
        )
    
    def __init__(self, target_entity_type=None, **kwargs):
        self._target_entity_type =\
            self._validate_target_entity_type(target_entity_type)

    def _validate_target_entity_type(self, target_entity_type_in):
        """validates the given target_entity_type value
        """
        # it can not be None
        if target_entity_type_in is None:
            raise TypeError("%s.target_entity_type can not be None" % 
                             self.__class__.__name__)

        if str(target_entity_type_in) == "":
            raise ValueError("%s.target_entity_type can not be empty" % 
                             self.__class__.__name__)

        # check if it is a class
        if isinstance(target_entity_type_in, type):
            target_entity_type_in = target_entity_type_in.__name__
        
        return str(target_entity_type_in)
    
    def _target_entity_type_getter(self):
        return self._target_entity_type
    
    @declared_attr
    def target_entity_type(cls):
        return synonym(
            "_target_entity_type",
            descriptor=property(
                fget=cls._target_entity_type_getter,
                doc="""The entity type which this object is valid for.
                
                Usually it is set to the TargetClass directly.
                """
            )
        )

class StatusMixin(object):
    """Makes the mixed in object statusable.
    
    This mixin adds status and status_list attributes to the mixed in class.
    Any object that needs a status and a corresponding status list can include
    this mixin.
    
    When mixed with a class which don't have an __init__ method, the mixin
    supplies one, and in this case the parameters below must be defined.
    
    :param status_list: this attribute holds a status list object, which shows
      the possible statuses that this entity could be in. This attribute can
      not be empty or None. Giving a StatusList object, the
      StatusList.target_entity_type should match the current class.
      
      .. versionadded:: 0.1.2.a4
      
        The status_list argument now can be skipped or can be None if there
        is an active database connection (stalker.models.DBSession is not
        None) and there is a suitable
        :class:`~stalker.models.status.StatusList` instance in the database
        whom :attr:`~stalker.models.status.StatusList.target_entity_type`
        attribute is set to the current mixed-in class name.
    
    :param status: It is a :class:`~stalker.models.status.Status` instance
      which shows the current status of the statusable object. Integer values
      are also accepted, which shows the index of the desired status in the
      ``status_list`` attribute of the current statusable object. If a
      :class:`~stalker.models.status.Status` instance is supplied, it should
      also be present in the ``status_list`` attribute. If set to None then the
      first :class:`~stalker.models.status.Status` instance in the
      ``status_list`` will be used.
      
      .. versionadded:: 0.2.0
        
        Status attribute as Status instance:
        
        It is now possible to set the status of the instance by a
        :class:`~stalker.models.status.Status` instance directly. And the
        :attr:`~stalker.models.mixins.StatusMixin.status` will return a proper
        :class:`~stalker.models.status.Status` instance.
    """
    
    def __init__(self, status=None, status_list=None, **kwargs):
        self.status_list = status_list
        self.status = status
        logger.debug('%s.status: %s' % (self.__class__.__name__, status))
    
    @declared_attr
    def status_id(cls):
        return Column(
            "status_id",
            Integer,
            ForeignKey('Statuses.id'),
            nullable=False
            # This is set to nullable=True but it is impossible to set the
            # status to None by using this Declarative approach.
            # 
            # This is done in that way cause SQLAlchemy was flushing the data
            # (AutoFlush) preliminarily while checking if the given Status was
            # in the related StatusList, and it was complaining about the
            # status can not be null
        )
    
    @declared_attr
    def status(cls):
        return relationship(
            'Status',
            primaryjoin=\
            "%s.status_id==Status.status_id" % cls.__name__,
            doc="""The current status of the object.
            
            It is a :class:`~stalker.models.status.Status` instance which
            is one of the Statuses stored in the ``status_list`` attribute
            of this object.
            """
        )
    
    @declared_attr
    def status_list_id(cls):
        return Column(
            "status_list_id",
            Integer,
            ForeignKey("StatusLists.id"), #, use_alter=True, name="x"),
            nullable=False
        )

    @declared_attr
    def status_list(cls):
        return relationship(
            "StatusList",
            primaryjoin=\
            "%s.status_list_id==StatusList.status_list_id" %
                cls.__name__,
        )
    
    @validates("status_list")
    def _validate_status_list(self, key, status_list):
        """validates the given status_list_in value
        """
        from stalker.models.status import StatusList
        
        if status_list is None:
            # check if there is a db setup and try to get the appropriate 
            # StatusList from the database
            
            # disable autoflush to prevent premature class initialization
            autoflush = DBSession.autoflush
            DBSession.autoflush = False
            try:
                # try to get a StatusList with the target_entity_type is 
                # matching the class name
                status_list = DBSession.query(StatusList)\
                    .filter_by(target_entity_type=self.__class__.__name__)\
                    .first()
            except UnboundExecutionError:
                # it is not mapped just skip it
                pass
            finally:
                # restore autoflush
                DBSession.autoflush = autoflush
        
        # if it is still None
        if status_list is None:
            # there is no db so raise an error because there is no way 
            # to get an appropriate StatusList
            raise TypeError(
                "'%s' instances can not be initialized without a "
                "stalker.models.status.StatusList instance, please pass a "
                "suitable StatusList (StatusList.target_entity_type=%s) "
                "with the 'status_list' argument" %
                (self.__class__.__name__, self.__class__.__name__)
            )
        else:
            # it is not an instance of status_list
            if not isinstance(status_list, StatusList):
                raise TypeError(
                    "%s.status_list should be an instance of "
                    "stalker.models.status.StatusList not %s" %
                    (self.__class__.__name__,
                     status_list.__class__.__name__)
                )
            
            # check if the entity_type matches to the StatusList.target_entity_type
            if self.__class__.__name__ != status_list.target_entity_type:
                raise TypeError(
                    "the given StatusLists' target_entity_type is %s, "
                    "whereas the entity_type of this object is %s" %\
                    (status_list.target_entity_type,
                     self.__class__.__name__))
        
        return status_list
    
    @validates('status')
    def _validate_status(self, key, status):
        """validates the given status value
        """
        from stalker.models.status import Status, StatusList
        
        if not isinstance(self.status_list, StatusList):
            raise TypeError("please set the %s.status_list attribute first" %
                self.__class__.__name__)
        
        # it is set to None
        if status is None:
            status = self.status_list.statuses[0]
        
        # it is not an instance of status or int
        if not isinstance(status, (Status, int)):
            raise TypeError("%s.status must be an instance of "
                            "stalker.models.status.Status or an integer "
                            "showing the index of the Status object in the "
                            "%s.status_list, not %s" % 
                            (self.__class__.__name__,
                             self.__class__.__name__,
                             status.__class__.__name__))
        
        if isinstance(status, int):
            # if it is not in the correct range:
            if status < 0:
                raise ValueError("%s.status must be a non-negative integer" %
                    self.__class__.__name__)
            
            if status >= len(self.status_list.statuses):
                raise ValueError("%s.status can not be bigger than the length "
                                 "of the status_list" % 
                                 self.__class__.__name__)
            # get the tatus instance out of the status_list instance
            status = self.status_list[status]
        
        # check if the given status is in the status_list
        logger.debug('self.status_list: %s' % self.status_list)
        logger.debug('given status: %s' % status)
        
        if status not in self.status_list:
            raise ValueError("The given Status instance for %s.status is not "
                             "in the %s.status_list, please supply a status "
                             "from that list." % 
                             (self.__class__.__name__, self.__class__.__name__)
            )
        
        return status


class ScheduleMixin(object):
    """Adds schedule info to the mixed in class.
    
    Adds schedule information like ``start_date``, ``end_date`` and
    ``duration``. There are theree parameters to initialize a class with
    ScheduleMixin, which are, ``start_date``, ``end_date`` and ``duration``.
    Only two of them are enough to initialize the class. The preceding order
    for the parameters is as follows::
      
      start_date > end_date > duration
    
    So if all of the parameters are given only the ``start_date`` and the
    ``end_date`` will be used and the ``duration`` will be calculated
    accordingly. In any other conditions the missing parameter will be
    calculated from the following table:
    
    +------------+----------+----------+----------------------------------------+
    | start_date | end_date | duration | DEFAULTS                               |
    +============+==========+==========+========================================+
    |            |          |          | start_date = datetime.date.today()     |
    |            |          |          |                                        |
    |            |          |          | duration = datetime.timedelta(days=10) |
    |            |          |          |                                        |
    |            |          |          | end_date = start_date + duration       |
    +------------+----------+----------+----------------------------------------+
    |     X      |          |          | duration = datetime.timedelta(days=10) |
    |            |          |          |                                        |
    |            |          |          | end_date = start_date + duration       |
    +------------+----------+----------+----------------------------------------+
    |     X      |    X     |          | duration = end_date - start_date       |
    +------------+----------+----------+----------------------------------------+
    |     X      |          |    X     | end_date = start_date + duration       |
    +------------+----------+----------+----------------------------------------+
    |     X      |    X     |    X     | duration = end_date - start_date       |
    +------------+----------+----------+----------------------------------------+
    |            |    X     |    X     | start_date = end_date - duration       |
    +------------+----------+----------+----------------------------------------+
    |            |    X     |          | duration = datetime.timedelta(days=10) |
    |            |          |          |                                        |
    |            |          |          | start_date = end_date - duration       |
    +------------+----------+----------+----------------------------------------+
    |            |          |    X     | start_date = datetime.date.today()     |
    |            |          |          |                                        |
    |            |          |          | end_date = start_date + duration       |
    +------------+----------+----------+----------------------------------------+
      
    The date attributes can be managed with timezones. Follow the Python idioms
    shown in the `documentation of datetime`_
    
    .. _documentation of datetime: http://docs.python.org/library/datetime.html
    
    :param start_date: the start date of the entity, should be a datetime.date
      instance, the start_date is the pin point for the date calculation. In
      any condition if the start_date is available then the value will be
      preserved. If start_date passes the end_date the end_date is also changed
      to a date to keep the timedelta between dates. The default value is
      datetime.date.today()
    
    :type start_date: :class:`datetime.datetime`
    
    :param end_date: the end_date of the entity, should be a datetime.date
      instance, when the start_date is changed to a date passing the end_date,
      then the end_date is also changed to a later date so the timedelta
      between the dates is kept.
    
    :type end_date: :class:`datetime.datetime` or :class:`datetime.timedelta`
    
    :param duration: The duration of the entity. It is a
      :class:`datetime.timedelta` instance. The default value is read from
      the :mod:`~stalker.conf.defaults` module. See the table above for the
      initialization rules.
    
    :type duration: :class:`datetime.timedelta`
    """
    
    #    # add this lines for Sphinx
    #    __tablename__ = "ScheduleMixins"
    
    def __init__(self,
                 start_date=None,
                 end_date=None,
                 duration=None,
                 **kwargs):
        self._validate_dates(start_date, end_date, duration)

    @declared_attr
    def _end_date(cls):
        return Column("end_date", Date)
    
    def _end_date_getter(self):
        """The date that the entity should be delivered.
        
        The end_date can be set to a datetime.timedelta and in this case it
        will be calculated as an offset from the start_date and converted to
        datetime.date again. Setting the start_date to a date passing the
        end_date will also set the end_date so the timedelta between them is
        preserved, default value is 10 days
        """
        return self._end_date

    def _end_date_setter(self, end_date_in):
        self._validate_dates(self.start_date, end_date_in, self.duration)
    
    @declared_attr
    def end_date(cls):
        return synonym(
            "_end_date",
            descriptor=property(
                cls._end_date_getter,
                cls._end_date_setter
            )
        )
    
    @declared_attr
    def _start_date(cls):
        return Column("start_date", Date)
    
    def _start_date_getter(self):
        """The date that this entity should start.
        
        Also effects the
        :attr:`~stalker.models.mixins.ScheduleMixin.end_date` attribute value
        in certain conditions, if the
        :attr:`~stalker.models.mixins.ScheduleMixin.start_date` is set to a
        time passing the :attr:`~stalker.models.mixins.ScheduleMixin.end_date`
        it will also offset the
        :attr:`~stalker.models.mixins.ScheduleMixin.end_date` to keep the
        :attr:`~stalker.models.mixins.ScheduleMixin.duration` value
        fixed. :attr:`~stalker.models.mixins.ScheduleMixin.start_date` should be
        an instance of class:`datetime.date` and the default value is
        :func:`datetime.date.today()`
        """
        return self._start_date
    
    def _start_date_setter(self, start_date_in):
        self._validate_dates(start_date_in, self.end_date, self.duration)
    
    @declared_attr
    def start_date(cls):
        return synonym(
            "_start_date",
            descriptor=property(
                cls._start_date_getter,
                cls._start_date_setter,
                )
        )
    
    @declared_attr
    def _duration(cls):
        return Column("duration", Interval)
    
    def _duration_getter(self):
        """Duration of the entity.
        
        It is a datetime.timedelta instance. Showing the difference of the
        :attr:`~stalker.models.mixins.ScheduleMixin.start_date` and the
        :attr:`~stalker.models.mixins.ScheduleMixin.end_date`. If edited it
        changes the :attr:`~stalker.models.mixins.ScheduleMixin.end_date`
        attribute value.
        """
        return self._duration
    
    def _duration_setter(self, duration_in):
        if duration_in is not None:
            if isinstance(duration_in, datetime.timedelta):
                # set the end_date to None
                # to make it recalculated
                self._validate_dates(self.start_date, None, duration_in)
            else:
                self._validate_dates(self.start_date, self.end_date,
                                     duration_in)
        else:
            self._validate_dates(self.start_date, self.end_date, duration_in)
    
    @declared_attr
    def duration(cls):
        return synonym(
            "_duration",
            descriptor=property(
                cls._duration_getter,
                cls._duration_setter
            )
        )
    
    def _validate_dates(self, start_date, end_date, duration):
        """updates the date values
        """
        if not isinstance(start_date, datetime.date):
            start_date = None
        
        if not isinstance(end_date, datetime.date):
            end_date = None
        
        if not isinstance(duration, datetime.timedelta):
            duration = None
        
        # check start_date
        if start_date is None:
            # try to calculate the start_date from end_date and duration
            if end_date is None:
                # set the defaults
                start_date = datetime.date.today()

                if duration is None:
                    # set the defaults
                    duration = defaults.DEFAULT_TASK_DURATION

                end_date = start_date + duration
            else:
                if duration is None:
                    duration = defaults.DEFAULT_TASK_DURATION

                start_date = end_date - duration

        # check end_date
        if end_date is None:
            if duration is None:
                duration = defaults.DEFAULT_TASK_DURATION

            end_date = start_date + duration

        if end_date < start_date:
            # check duration
            if duration < datetime.timedelta(1):
                duration = datetime.timedelta(1)

            end_date = start_date + duration

        self._start_date = start_date
        self._end_date = end_date
        self._duration = self._end_date - self._start_date

class ProjectMixin(object):
    """Gives the ability to connect to a :class:`~stalker.models.project.Project` to the mixed in object.
    
    :param project: A :class:`~stalker.models.project.Project` instance holding
      the project which this object is related to. It can not be None, or
      anything other than a :class:`~stalker.models.project.Project` instance.
    
    :type project: :class:`~stalker.models.project.Project`
    """

    #    # add this lines for Sphinx
    #    __tablename__ = "ProjectMixins"

    @declared_attr
    def project_id(cls):
        return Column(
            "project_id",
            Integer,
            ForeignKey("Projects.id", use_alter=True, name="project_x_id"),
            #ForeignKey("Projects.id"),
            # cannot use nullable cause a Project object needs
            # insert itself as the project and it needs post_update
            # thus nullable should be True
            #nullable=False,
        )

    @declared_attr
    def project(cls):
        backref = cls.__tablename__.lower()
        doc = """The :class:`~stalker.models.project.Project` instance that
        this object belongs to.
        """

        return relationship(
            "Project",
            primaryjoin=\
            cls.__tablename__ + ".c.project_id==Projects.c.id",
            post_update=True, # for project itself
            uselist=False,
            backref=backref,
            doc=doc
        )

    def __init__(self,
                 project=None,
                 **kwargs):
        self.project = project

    @validates("project")
    def _validate_project(self, key, project):
        """validates the given project value
        """
        
        from stalker.models.project import Project

        if project is None:
            raise TypeError("%s.project can not be None it must be an "
                            "instance of stalker.models.project.Project" %
                            self.__class__.__name__)

        if not isinstance(project, Project):
            raise TypeError("%s.project should be an instance of "
                            "stalker.models.project.Project instance not %s" %
                            (self.__class__.__name__,
                             project.__class__.__name__))
        return project

class ReferenceMixin(object):
    """Adds reference capabilities to the mixed in class.
    
    References are :class:`stalker.models.entity.Entity` instances or anything
    derived from it, which adds information to the attached objects. The aim of
    the References are generally to give more info to direct the evolution of
    the object.
    
    :param references: A list of :class:`~stalker.models.entity.Entity`
      objects.
    
    :type references: list of :class:`~stalker.models.entity.Entity` objects.
    """
    
    # add this lines for Sphinx
    #    __tablename__ = "ReferenceMixins"

    def __init__(self,
                 references=None,
                 **kwargs):
        if references is None:
            references = []
        
        self.references = references
    
    @declared_attr
    def references(cls):
        # TODO: there is something wrong here, the documentation and the implementation is not telling the same story
        # get secondary table
        secondary_table = create_secondary_table(
            cls.__name__,
            'Link',
            cls.__tablename__,
            'Links',
            cls.__name__ + "_References"
        )
        # return the relationship
        return relationship("Link", secondary=secondary_table)

    @validates("references")
    def _validate_references(self, key, reference):
        """validates the given reference
        """
        
        from stalker.models.entity import SimpleEntity
        
        # all the elements should be instance of stalker.models.entity.Entity
        if not isinstance(reference, SimpleEntity):
            raise TypeError("%s.references should be all instances of "
                            "stalker.models.entity.SimpleEntity not %s"
                            % (self.__class__.__name__,
                               reference.__class__.__name__))
        return reference

class ACLMixin(object):
    """A Mixin for adding ACLs to mixed in class.
    
    Access control lists or ACLs are used to determine if the given resource
    has the permission to access the given data. It is based on Pyramids
    Authorization system but organized to fit in Stalker style.
    
    The ACLMixin adds an attribute called ``permissions`` and a
    property called ``__acl__`` to be able to pass the permission data to
    Pyramid framework.
    """
    
    @declared_attr
    def permissions(cls):
        # get the secondary table
        secondary_table = create_secondary_table(
            cls.__name__, 'Permission', cls.__tablename__, 'Permissions'
        )
        #return the relationship
        return relationship('Permission', secondary=secondary_table)
    
    @validates('permissions')
    def _validate_permissions(self, key, permission):
        """validates the given permission value
        """
        
        from stalker.models.auth import Permission
        
        if not isinstance(permission, Permission):
            raise TypeError("%s.permissions should be all instances of "
                            "stalker.models.auth.Permission not %s" %
                (self.__class__.__name__, permission.__class__.__name__))
        
        return permission
    
    @property
    def __acl__(self):
        """Returns Pyramid friendly ACL list composed by the:
        
          * Permission.access (Ex: 'Allow' or 'Deny')
          * The Mixed in class name and the object name (Ex: 'User:eoyilmaz')
          * The Action and the target class name (Ex: 'Add_Project')
          
        Thus a list of tuple is returned as follows::
            
          __acl__ = [
              ('Allow', 'User:eoyilmaz', 'Add_Project'),
          ]
            
        For the last example user eoyilmaz can grant access to views requiring
        'Add_Project' permission.
        """
        return [(perm.access,
                 self.__class__.__name__ + ':' + self.name,
                 perm.action + '_' + perm.class_name)
                 for perm in self.permissions]

class CodeMixin(object):
    """Adds code info to the mixed in class.
    
    .. versionadded:: 0.2.0
      
      The code attribute of the SimpleEntity is now introduced as a separate
      mixin. To let it be used by the classes it is really needed. 
    
    The CodeMixin just adds a new field called ``code``. It is a very simple
    attribute and is used for simplifying long names (like Project.name etc.).
    
    Contrary to previous implementations the code attribute is not formatted in
    anyway, so care needs to be taken if the code attribute is going to be used
    in filesystem as file and directory names.
    
    :param str code: The code attribute is a string, can not be empty or can
      not be None.
    """
    
    def __init__(
            self,
            code=None,
            **kwargs):
        logger.debug('code: %s' % code)
        self.code = code

    @declared_attr
    def code(cls):
        return Column(
            'code',
            String(256),
            nullable=False,
            doc="""The code name of this object.
                
                It accepts strings. Can not be None."""
        )
    
    @validates('code')
    def _validate_code(self, key, code):
        """validates the given code attribute
        """
        logger.debug('validating code value of: %s' % code)
        if code is None:
            raise TypeError("%s.code cannot be None" % self.__class__.__name__)
        
        if not isinstance(code, (str, unicode)):
            raise TypeError('%s.code should be an instance of string or '
                            'unicode not %s' %
                            (self.__class__.__name__,
                             code.__class__.__name__)
            )
        
        if code == '':
            raise ValueError('%s.code can not be an empty string')
        
        return code
