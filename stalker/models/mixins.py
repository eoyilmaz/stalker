# -*- coding: utf-8 -*-

import logging

import pytz
from sqlalchemy import (Table, Column, String, Integer, ForeignKey, Interval,
                        Float, Enum)
from sqlalchemy.exc import UnboundExecutionError, OperationalError
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import synonym, relationship, validates


from stalker.db.declarative import Base
from stalker.db.types import GenericDateTime
from stalker.log import logging_level

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


def create_secondary_table(
        primary_cls_name,
        secondary_cls_name,
        primary_cls_table_name,
        secondary_cls_table_name,
        secondary_table_name=None):
    """creates any secondary table
    """
    from stalker.models import make_plural
    plural_secondary_cls_name = make_plural(secondary_cls_name)

    # use the given class_name and the class_table
    if not secondary_table_name:
        secondary_table_name = '%s_%s' % (primary_cls_name,
                                          plural_secondary_cls_name)

    # check if the table is already defined
    if secondary_table_name not in Base.metadata:
        secondary_table = Table(
            secondary_table_name, Base.metadata,
            Column(
                '%s_id' % primary_cls_name.lower(),
                Integer,
                ForeignKey('%s.id' % primary_cls_table_name),
                primary_key=True,
            ),

            Column(
                '%s_id' % secondary_cls_name.lower(),
                Integer,
                ForeignKey('%s.id' % secondary_cls_table_name),
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
      :class:`.Project` instances. You can not assign it to any other class
      which accepts a :class:`.Type` instance.

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
        self._target_entity_type = \
            self._validate_target_entity_type(target_entity_type)

    def _validate_target_entity_type(self, target_entity_type_in):
        """validates the given target_entity_type value
        """
        # it can not be None
        if target_entity_type_in is None:
            raise TypeError(
                "%s.target_entity_type can not be None" %
                self.__class__.__name__
            )

        # check if it is a class
        if isinstance(target_entity_type_in, type):
            target_entity_type_in = target_entity_type_in.__name__

        if target_entity_type_in == "":
            raise ValueError(
                "%s.target_entity_type can not be empty" %
                self.__class__.__name__
            )

        return target_entity_type_in

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
        is an active database connection and there is a suitable
        :class:`.StatusList` instance in the database whom
        :attr:`.StatusList.target_entity_type` attribute is set to the current
        mixed-in class name.

    :param status: It is a :class:`.Status` instance which shows the current
      status of the statusable object. Integer values are also accepted, which
      shows the index of the desired status in the ``status_list`` attribute of
      the current statusable object. If a :class:`.Status` instance is
      supplied, it should also be present in the ``status_list`` attribute. If
      set to None then the first :class:`.Status` instance in the
      ``status_list`` will be used.

      .. versionadded:: 0.2.0

        Status attribute as Status instance:

        It is now possible to set the status of the instance by a
        :class:`.Status` instance directly. And the :attr:`.StatusMixin.status`
        will return a proper :class:`.Status` instance.
    """

    def __init__(self, status=None, status_list=None, **kwargs):
        self.status_list = status_list
        self.status = status

    @declared_attr
    def status_id(cls):
        return Column(
            'status_id',
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
            primaryjoin="%s.status_id==Status.status_id" % cls.__name__,
            doc="""The current status of the object.

            It is a :class:`.Status` instance which
            is one of the Statuses stored in the ``status_list`` attribute
            of this object.
            """
        )

    @declared_attr
    def status_list_id(cls):
        return Column(
            'status_list_id',
            Integer,
            ForeignKey('StatusLists.id'),
            nullable=False
        )

    @declared_attr
    def status_list(cls):
        return relationship(
            "StatusList",
            primaryjoin= \
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
            from stalker.db.session import DBSession
            with DBSession.no_autoflush:
                try:
                    # try to get a StatusList with the target_entity_type is
                    # matching the class name
                    status_list = StatusList.query\
                        .filter_by(target_entity_type=self.__class__.__name__)\
                        .first()
                except (UnboundExecutionError, OperationalError):
                    # it is not mapped just skip it
                    pass

        # if it is still None
        if status_list is None:
            # there is no db so raise an error because there is no way
            # to get an appropriate StatusList
            raise TypeError(
                "%s instances can not be initialized without a "
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
                    (self.__class__.__name__, status_list.__class__.__name__)
                )

            # check if the entity_type matches to the
            # StatusList.target_entity_type
            if self.__class__.__name__ != status_list.target_entity_type:
                raise TypeError(
                    "The given StatusLists' target_entity_type is %s, "
                    "whereas the entity_type of this object is %s" %
                    (status_list.target_entity_type, self.__class__.__name__)
                )

        return status_list

    @validates('status')
    def _validate_status(self, key, status):
        """validates the given status value
        """
        from stalker.models.status import Status
        from stalker.db.session import DBSession

        # it is set to None
        if status is None:
            with DBSession.no_autoflush:
                status = self.status_list.statuses[0]

        # it is not an instance of status or int
        if not isinstance(status, (Status, int)):
            raise TypeError(
                "%(class)s.status must be an instance of "
                "stalker.models.status.Status or an integer showing the index "
                "of the Status object in the %(class)s.status_list, not "
                "%(status)s" %
                {
                    'class': self.__class__.__name__,
                    'status': status.__class__.__name__
                }
            )

        if isinstance(status, int):
            # if it is not in the correct range:
            if status < 0:
                raise ValueError(
                    "%s.status must be a non-negative integer" %
                    self.__class__.__name__
                )

            if status >= len(self.status_list.statuses):
                raise ValueError(
                    "%s.status can not be bigger than the length of the "
                    "status_list" % self.__class__.__name__
                )
                # get the status instance out of the status_list instance
            status = self.status_list[status]

        # check if the given status is in the status_list
        # logger.debug('self.status_list: %s' % self.status_list)
        # logger.debug('given status: %s' % status)

        if status not in self.status_list:
            raise ValueError(
                "The given Status instance for %s.status is not in the "
                "%s.status_list, please supply a status from that list." %
                (self.__class__.__name__, self.__class__.__name__)
            )

        return status


class DateRangeMixin(object):
    """Adds date range info to the mixed in class.

    Adds date range information like ``start``, ``end`` and ``duration``. These
    attributes will be used in TaskJuggler. Because ``effort`` is only
    meaningful if there are some ``resources`` this attribute has been left
    special for :class:`.Task` class. The ``length`` has not been implemented
    because of its rare use.

    The preceding order for the attributes is as follows::

      start > end > duration

    So if all of the parameters are given only the ``start`` and the ``end``
    will be used and the ``duration`` will be calculated accordingly. In any
    other conditions the missing parameter will be calculated from the
    following table:

    +-------+-----+----------+----------------------------------------+
    | start | end | duration | DEFAULTS                               |
    +=======+=====+==========+========================================+
    |       |     |          | start = datetime.datetime.now(pytz.utc)|
    |       |     |          |                                        |
    |       |     |          | duration = datetime.timedelta(days=10) |
    |       |     |          |                                        |
    |       |     |          | end = start + duration                 |
    +-------+-----+----------+----------------------------------------+
    |   X   |     |          | duration = datetime.timedelta(days=10) |
    |       |     |          |                                        |
    |       |     |          | end = start + duration                 |
    +-------+-----+----------+----------------------------------------+
    |   X   |  X  |          | duration = end - start                 |
    +-------+-----+----------+----------------------------------------+
    |   X   |     |    X     | end = start + duration                 |
    +-------+-----+----------+----------------------------------------+
    |   X   |  X  |    X     | duration = end - start                 |
    +-------+-----+----------+----------------------------------------+
    |       |  X  |    X     | start = end - duration                 |
    +-------+-----+----------+----------------------------------------+
    |       |  X  |          | duration = datetime.timedelta(days=10) |
    |       |     |          |                                        |
    |       |     |          | start = end - duration                 |
    +-------+-----+----------+----------------------------------------+
    |       |     |    X     | start = datetime.datetime.now(pytz.utc)|
    |       |     |          |                                        |
    |       |     |          | end = start + duration                 |
    +-------+-----+----------+----------------------------------------+

    Only the ``start``, ``end`` will be stored. The ``duration`` attribute is
    the direct difference of the the ``start`` and ``end`` attributes, so there
    is no need to store it. But if will be used in calculation of the start and
    end values.

    The start and end attributes have a ``computed`` companion. Which are the
    return values from TaskJuggler. so for ``start`` there is the
    ``computed_start`` and for ``end`` there is the ``computed_end``
    attributes.

    The date attributes can be managed with timezones. Follow the Python idioms
    shown in the `documentation of datetime`_

    .. _documentation of datetime: https://docs.python.org/library/datetime.html

    :param start: the start date of the entity, should be a datetime.datetime
      instance, the start is the pin point for the date calculation. In
      any condition if the start is available then the value will be
      preserved. If start passes the end the end is also changed
      to a date to keep the timedelta between dates. The default value is
      datetime.datetime.now(pytz.utc)

    :type start: :class:`datetime.datetime`

    :param end: the end of the entity, should be a datetime.datetime instance,
      when the start is changed to a date passing the end, then the end is also
      changed to a later date so the timedelta between the dates is kept.

    :type end: :class:`datetime.datetime` or :class:`datetime.timedelta`

    :param duration: The duration of the entity. It is a
      :class:`datetime.timedelta` instance. The default value is read from
      the :class:`.Config` class. See the table above for the initialization
      rules.

    :type duration: :class:`datetime.timedelta`
    """

    def __init__(
            self,
            start=None,
            end=None,
            duration=None,
            **kwargs
    ):
        self._start, self._end, self._duration = self._validate_dates(start, end, duration)

    @declared_attr
    def _end(cls):
        return Column("end", GenericDateTime)

    def _end_getter(self):
        """The date that the entity should be delivered.

        The end can be set to a datetime.timedelta and in this case it will be
        calculated as an offset from the start and converted to
        datetime.datetime again. Setting the start to a date passing the end
        will also set the end, so the timedelta between them is preserved,
        default value is 10 days
        """
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            return self._end

    def _end_setter(self, end_in):
        self._start, self._end, self._duration = \
            self._validate_dates(self.start, end_in, self.duration)

    @declared_attr
    def end(cls):
        return synonym(
            "_end",
            descriptor=property(
                cls._end_getter,
                cls._end_setter
            )
        )

    @declared_attr
    def _start(cls):
        return Column("start", GenericDateTime)

    def _start_getter(self):
        """The date that this entity should start.

        Also effects the :attr:`.DateRangeMixin.end` attribute value in certain
        conditions, if the :attr:`.DateRangeMixin.start` is set to a time
        passing the :attr:`.DateRangeMixin.end` it will also offset the
        :attr:`.DateRangeMixin.end` to keep the
        :attr:`.DateRangeMixin.duration` value fixed.
        :attr:`.DateRangeMixin.start` should be an instance of
        class:`datetime.datetime` and the default value is
        :func:`datetime.datetime.now(pytz.utc)`
        """
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            return self._start

    def _start_setter(self, start_in):
        self._start, self._end, self._duration = \
            self._validate_dates(start_in, self.end, self.duration)

    @declared_attr
    def start(cls):
        return synonym(
            "_start",
            descriptor=property(
                cls._start_getter,
                cls._start_setter,
            )
        )

    @declared_attr
    def _duration(cls):
        return Column('duration', Interval)

    def _duration_getter(self):
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            return self._duration

    def _duration_setter(self, duration_in):
        if duration_in is not None:
            import datetime
            if isinstance(duration_in, datetime.timedelta):
                # set the end to None
                # to make it recalculated
                self._start, self._end, self._duration = \
                    self._validate_dates(self.start, None, duration_in)
            else:
                # use the end
                self._start, self._end, self._duration = \
                    self._validate_dates(self.start, self.end, duration_in)
        else:
            self._start, self._end, self._duration = \
                self._validate_dates(self.start, self.end, duration_in)

    @declared_attr
    def duration(self):
        return synonym(
            '_duration',
            descriptor=property(
                self._duration_getter,
                self._duration_setter,
                doc="""Duration of the entity.

                It is a datetime.timedelta instance. Showing the difference of
                the :attr:`.start` and the :attr:`.end`. If edited it changes
                the :attr:`.end` attribute value."""
            )
        )

    def _validate_dates(self, start, end, duration):
        """updates the date values
        """
        # logger.debug('start    : %s' % start)
        # logger.debug('end      : %s' % end)
        # logger.debug('duration : %s' % duration)

        from stalker import defaults
        import datetime
        if not isinstance(start, datetime.datetime):
            start = None

        if not isinstance(end, datetime.datetime):
            end = None

        if not isinstance(duration, datetime.timedelta):
            duration = None

        # check start
        if start is None:
            # try to calculate the start from end and duration
            if end is None:
                # set the defaults
                start = datetime.datetime.now(pytz.utc)

                if duration is None:
                    # set the defaults
                    duration = defaults.timing_resolution

                end = start + duration
            else:
                if duration is None:
                    duration = defaults.timing_resolution

                # try:
                start = end - duration
                # except OverflowError: # end is datetime.datetime.min
                #     start = end

        # check end
        if end is None:
            if duration is None:
                duration = defaults.timing_resolution

            end = start + duration

        if end < start:
            # check duration
            if duration is None or duration < datetime.timedelta(1):
                duration = datetime.timedelta(1)

            # try:
            end = start + duration
            # except OverflowError: # start is datetime.datetime.max
            #     end = start

        # round the dates to the timing_resolution
        rounded_start = self.round_time(start)
        rounded_end = self.round_time(end)
        rounded_duration = rounded_end - rounded_start

        if rounded_duration < defaults.timing_resolution:
            rounded_duration = defaults.timing_resolution
            rounded_end = rounded_start + rounded_duration

        return rounded_start, rounded_end, rounded_duration

    @declared_attr
    def computed_start(cls):
        return Column('computed_start', GenericDateTime)

    @declared_attr
    def computed_end(cls):
        return Column('computed_end', GenericDateTime)

    @property
    def computed_duration(self):
        """returns the computed_duration as the difference of computed_start
        and computed_end if there are computed_start and computed_end otherwise
        returns None
        """
        return self.computed_end - self.computed_start if self.computed_end and self.computed_start else None

    @classmethod
    def round_time(cls, dt):
        """Round the given datetime object to the defaults.timing_resolution.

        Uses :class:`stalker.defaults.timing_resolution` as the closest number
        of seconds to round to.

        :param dt: datetime.datetime object, defaults to now.

        :type dt: datetime.datetime

        Based on Thierry Husson's answer in `Stackoverflow`_

        _`Stackoverflow` : https://stackoverflow.com/a/10854034/1431079
        """
        # to be compatible with python 2.6 use the following instead of
        # total_seconds()
        from stalker import defaults
        timing_resolution = defaults.timing_resolution
        trs = timing_resolution.days * 86400 + timing_resolution.seconds

        # convert to seconds
        import datetime
        import pytz
        epoch = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)

        diff = dt - epoch
        diff_in_seconds = diff.days * 86400 + diff.seconds
        return epoch + datetime.timedelta(
            seconds=(diff_in_seconds + trs * 0.5) // trs * trs
        )

    @property
    def total_seconds(self):
        """returns the duration as seconds
        """
        return self.duration.days * 86400 + self.duration.seconds

    @property
    def computed_total_seconds(self):
        """returns the duration as seconds
        """
        return self.computed_duration.days * 86400 + self.computed_duration.seconds


class ProjectMixin(object):
    """Allows connecting a :class:`.Project` to the mixed in object.

    This also forces a ``all, delete-orphan`` cascade, so when a
    :class:``.Project`` instance is deleted then all the class instances that
    are inherited from ``ProjectMixin`` will also be deleted. Meaning that, a
    class which also derives from ``ProjectMixin`` will not be able to exists
    without a project (``delete-orphan`` case).

    :param project: A :class:`.Project` instance holding the project which this
      object is related to. It can not be None, or anything other than a
      :class:`.Project` instance.

    :type project: :class:`.Project`
    """
    #    # add this lines for Sphinx
    #    __tablename__ = "ProjectMixins"

    @declared_attr
    def project_id(cls):
        return Column(
            "project_id",
            Integer,
            ForeignKey("Projects.id"),
            # cannot use nullable cause a Project object needs
            # insert itself as the project and it needs post_update
            # thus nullable should be True
        )

    @declared_attr
    def project(cls):
        from sqlalchemy.orm import backref
        backref_table_name = cls.__tablename__.lower()
        doc = """The :class:`.Project` instance that
        this object belongs to.
        """

        return relationship(
            "Project",
            primaryjoin="%s.c.project_id==Projects.c.id" % cls.__tablename__,
            post_update=True,  # for project itself
            uselist=False,
            backref=backref(
                backref_table_name,
                cascade='all, delete-orphan'
            ),
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
            raise TypeError(
                "%s.project can not be None it must be an instance of "
                "stalker.models.project.Project" % self.__class__.__name__
            )

        if not isinstance(project, Project):
            raise TypeError(
                "%s.project should be an instance of "
                "stalker.models.project.Project instance not %s" %
                (self.__class__.__name__, project.__class__.__name__)
            )
        return project


class ReferenceMixin(object):
    """Adds reference capabilities to the mixed in class.

    References are :class:`stalker.models.link.Link` instances or anything
    derived from it, which adds information to the attached objects. The aim of
    the References are generally to give more info to direct the evolution of
    the object.

    :param references: A list of :class:`.Link` instances.

    :type references: list of :class:`.Link` instances.
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
        # get secondary table
        secondary_table = create_secondary_table(
            cls.__name__,
            'Link',
            cls.__tablename__,
            'Links',
            "%s_References" % cls.__name__
        )
        # return the relationship
        return relationship(
            "Link",
            secondary=secondary_table,
            doc="""A list of :class:`.Link` instances given as a reference for
            this entity.
            """
        )

    @validates("references")
    def _validate_references(self, key, reference):
        """validates the given reference
        """
        from stalker.models.link import Link

        # all the elements should be instance of stalker.models.entity.Entity
        if not isinstance(reference, Link):
            raise TypeError(
                'All the elements in the %s.references should be '
                'stalker.models.link.Link instances not %s' %
                (self.__class__.__name__, reference.__class__.__name__)
            )
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
        return relationship('Permission', secondary=secondary_table)

    @validates('permissions')
    def _validate_permissions(self, key, permission):
        """validates the given permission value
        """
        from stalker.models.auth import Permission
        if not isinstance(permission, Permission):
            raise TypeError(
                "%s.permissions should be all instances of "
                "stalker.models.auth.Permission not %s" %
                (self.__class__.__name__, permission.__class__.__name__)
            )

        return permission

    @property
    def __acl__(self):
        """Returns Pyramid friendly ACL list composed by the:

          * Permission.access (Ex: 'Allow' or 'Deny')
          * The Mixed in class name and the object name (Ex: 'User:eoyilmaz')
          * The Action and the target class name (Ex: 'Create_Asset')

        Thus a list of tuple is returned as follows::

          __acl__ = [
              ('Allow', 'User:eoyilmaz', 'Create_Asset'),
          ]

        For the last example user eoyilmaz can grant access to views requiring
        'Add_Project' permission.
        """
        return [(perm.access,
                 '%s:%s' % (self.__class__.__name__, self.name),
                 '%s_%s' % (perm.action, perm.class_name))
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

    def __init__(self, code=None, **kwargs):
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

        from stalker import __string_types__
        if not isinstance(code, __string_types__):
            raise TypeError(
                '%s.code should be a string not %s' %
                (self.__class__.__name__, code.__class__.__name__)
            )

        if code == '':
            raise ValueError(
                '%s.code can not be an empty string' % self.__class__.__name__
            )

        return code


class WorkingHoursMixin(object):
    """Sets working hours for the mixed in class.

    Generally is meaningful for users, departments and studio.

    :param working_hours: A :class:`.WorkingHours` instance showing the working
      hours settings.
    """

    def __init__(self, working_hours=None, **kwargs):
        self.working_hours = working_hours

    @declared_attr
    def working_hours_id(cls):
        """the id of the related working hours
        """
        return Column(
            'working_hours_id',
            Integer,
            ForeignKey('WorkingHours.id')
        )

    @declared_attr
    def working_hours(cls):
        return relationship(
            'WorkingHours',
            primaryjoin='%s.working_hours_id==WorkingHours.working_hours_id' %
                        cls.__name__
        )

    @validates('working_hours')
    def _validate_working_hours(self, key, wh):
        """validates the given working hours value
        """
        from stalker import WorkingHours
        if wh is None:
            wh = WorkingHours()  # without any argument this will use the
                                 # default.working_hours settings
        elif not isinstance(wh, WorkingHours):
            raise TypeError(
                '%s.working_hours should be a '
                'stalker.models.studio.WorkingHours instance, not %s' % (
                    self.__class__.__name__, wh.__class__.__name__
                )
            )

        return wh


class ScheduleMixin(object):
    """Adds schedule info to the mixed in class.

    Adds attributes like schedule_timing, schedule_unit and schedule_model
    attributes to the mixed in class.

    Use the ``__default_schedule_attr_name__`` attribute to customize the
    column names.
    """

    # some default values that can be overridden in Mixed in classes
    from stalker import defaults
    __default_schedule_attr_name__ = 'schedule'
    __default_schedule_timing__ = defaults.timing_resolution.seconds / 60
    __default_schedule_unit__ = 'h'
    __default_schedule_models__ = defaults.task_schedule_models

    def __init__(
            self,
            schedule_timing=None,
            schedule_unit=None,
            schedule_model=None,
            schedule_constraint=0,
            **kwargs
    ):
        self.schedule_constraint = schedule_constraint
        self.schedule_model = schedule_model
        self.schedule_timing = schedule_timing
        self.schedule_unit = schedule_unit

    @declared_attr
    def schedule_timing(cls):
        return Column(
            '%s_timing' % cls.__default_schedule_attr_name__,
            Float, nullable=True, default=0,
            doc="""It is the value of the %(attr)s timing. It is a float
            value.

            The timing value can either be as Work Time or Calendar Time
            defined by the %(attr)s_model attribute. So when the %(attr)s_model
            is `duration` then the value of this attribute is in Calendar Time,
            and if the %(attr)s_model is either `length` or `effort` then the
            value is considered as Work Time.
            """ % {'attr': cls.__default_schedule_attr_name__}
        )

    @declared_attr
    def schedule_unit(cls):
        from stalker import defaults
        return Column(
            '%s_unit' % cls.__default_schedule_attr_name__,
            Enum(*defaults.datetime_units, name='TimeUnit'),
            nullable=True, default='h',
            doc="""It is the unit of the %(attr)s timing. It is a string
            value. And should be one of 'min', 'h', 'd', 'w', 'm', 'y'.""" %
                {'attr': cls.__default_schedule_attr_name__}
        )

    @declared_attr
    def schedule_model(cls):
        return Column(
            '%s_model' % cls.__default_schedule_attr_name__,
            Enum(*cls.__default_schedule_models__,
                 name='%(class)s%(attr)sModel' % {
                     'class': cls.__name__,
                     'attr': cls.__default_schedule_attr_name__.title()
                 }),
            default=cls.__default_schedule_models__[0], nullable=False,
            doc="""Defines the schedule model which is going to be used by
            **TaskJuggler** while scheduling this Task. It has three possible
            values; **effort**, **duration**, **length**. ``effort`` is the
            default value. Each value causes this task to be scheduled in
            different ways:

            ======== ==========================================================
            effort   If the :attr:`.schedule_model` attribute is set to
                     **"effort"** then the start and end date values are
                     calculated so that a resource should spent this much of
                     work time to complete a Task. For example, a task with
                     :attr:`.schedule_timing` of 4 days, needs 4 working days.
                     So it can take 4 working days to complete the Task, but it
                     doesn't mean that the task duration will be 4 days. If the
                     resource works overtime then the task will be finished
                     before 4 days or if the resource will not be available
                     (due to a vacation) then the task duration can be much
                     more.

            duration The duration of the task will exactly be equal to
                     :attr:`.schedule_timing` regardless of the resource
                     availability. So the difference between :attr:`.start`
                     and :attr:`.end` attribute values are equal to
                     :attr:`.schedule_timing`. Essentially making the task
                     duration in calendar days instead of working days.

            length   In this model the duration of the task will exactly be
                     equal to the given length value in working days regardless
                     of the resource availability. So a task with the
                     :attr:`.schedule_timing` is set to 4 days will be
                     completed in 4 working days. But again it will not be
                     always 4 calendar days due to the weekends or non working
                     days.
            ======== ==========================================================
            """
        )

    @declared_attr
    def schedule_constraint(cls):
        return Column(
            '%s_constraint' % cls.__default_schedule_attr_name__,
            Integer,
            default=0,
            nullable=False,
            doc="""An integer number showing the constraint schema for this
            task.

            Possible values are:

             ===== ===============
               0   Constrain None
               1   Constrain Start
               2   Constrain End
               3   Constrain Both
             ===== ===============

            For convenience use **stalker.models.task.CONSTRAIN_NONE**,
            **stalker.models.task.CONSTRAIN_START**,
            **stalker.models.task.CONSTRAIN_END**,
            **stalker.models.task.CONSTRAIN_BOTH**.

            This value is going to be used to constrain the start and end date
            values of this task. So if you want to pin the start of a task to a
            certain date. Set its :attr:`.schedule_constraint` value to
            **CONSTRAIN_START**. When the task is scheduled by **TaskJuggler**
            the start date will be pinned to the :attr:`start` attribute of
            this task.

            And if both of the date values (start and end) wanted to be pinned
            to certain dates (making the task effectively a ``duration`` task)
            set the desired :attr:`start` and :attr:`end` and then set the
            :attr:`schedule_constraint` to **CONSTRAIN_BOTH**.
            """
        )

    @validates('schedule_constraint')
    def _validate_schedule_constraint(self, key, schedule_constraint):
        """validates the given schedule_constraint value
        """
        if not schedule_constraint:
            schedule_constraint = 0

        if not isinstance(schedule_constraint, int):
            raise TypeError(
                '%(class)s.%(attr)s_constraint should be an integer '
                'between 0 and 3, not %(constraint_class)s' %
                {
                    'class': self.__class__.__name__,
                    'attr': self.__default_schedule_attr_name__,
                    'constraint_class':
                    schedule_constraint.__class__.__name__
                }
            )

        schedule_constraint = max(schedule_constraint, 0)
        schedule_constraint = min(schedule_constraint, 3)

        return schedule_constraint

    @validates('schedule_model')
    def _validate_schedule_model(self, key, schedule_model):
        """validates the given schedule_model value
        """
        if not schedule_model:
            schedule_model = self.__default_schedule_models__[0]

        error_message = \
            '%(class)s.%(attr)s_model should be one of %(defaults)s, not ' \
            '%(model_class)s' % {
                'class': self.__class__.__name__,
                'attr': self.__default_schedule_attr_name__,
                'defaults': self.__default_schedule_models__,
                'model_class': schedule_model.__class__.__name__
            }

        from stalker import __string_types__
        if not isinstance(schedule_model, __string_types__):
            raise TypeError(error_message)

        if schedule_model not in self.__default_schedule_models__:
            raise ValueError(error_message)

        return schedule_model

    @validates('schedule_unit')
    def _validate_schedule_unit(self, key, schedule_unit):
        """validates the given schedule_unit
        """
        from stalker import defaults
        if schedule_unit is None:
            schedule_unit = self.__default_schedule_unit__

        from stalker import __string_types__
        if not isinstance(schedule_unit, __string_types__):
            raise TypeError(
                '%(class)s.%(attr)s_unit should be a string value one of '
                '%(defaults)s showing the unit of the %(attr)s timing of this '
                '%(class)s, not %(unit_class)s' % {
                    'class': self.__class__.__name__,
                    'attr': self.__default_schedule_attr_name__,
                    'defaults': defaults.datetime_units,
                    'unit_class': schedule_unit.__class__.__name__
                }
            )

        if schedule_unit not in defaults.datetime_units:
            raise ValueError(
                '%(class)s.%(attr)s_unit should be a string value one of '
                '%(defaults)s showing the unit of the %(attr)s timing of '
                'this %(class)s, not %(unit_class)s' % {
                    'class': self.__class__.__name__,
                    'attr': self.__default_schedule_attr_name__,
                    'defaults': defaults.datetime_units,
                    'unit_class': schedule_unit.__class__.__name__
                }
            )

        return schedule_unit

    @validates('schedule_timing')
    def _validate_schedule_timing(self, key, schedule_timing):
        """validates the given schedule_timing
        """
        if schedule_timing is None:
            schedule_timing = self.__default_schedule_timing__
            self.schedule_unit = self.__default_schedule_unit__

        if not isinstance(schedule_timing, (int, float)):
            raise TypeError(
                '%(class)s.%(attr)s_timing should be an integer or float '
                'number showing the value of the %(attr)s timing of this '
                '%(class)s, not %(timing_class)s' % {
                    'class': self.__class__.__name__,
                    'attr': self.__default_schedule_attr_name__,
                    'timing_class': schedule_timing.__class__.__name__
                }
            )

        return schedule_timing

    @classmethod
    def least_meaningful_time_unit(cls, seconds, as_work_time=True):
        """returns the least meaningful timing unit that corresponds to the
        given seconds. So if:

          as_work_time == True
              seconds % (1 years work time as seconds) == 0 --> 'y' else:
              seconds % (1 month work time as seconds) == 0 --> 'm' else:
              seconds % (1 week work time as seconds) == 0 --> 'w' else:
              seconds % (1 day work time as seconds) == 0 --> 'd' else:
              seconds % (1 hour work time as seconds) == 0 --> 'h' else:
              seconds % (1 minutes work time as seconds) == 0 --> 'min' else:
              raise RuntimeError
          as_work_time == False
              seconds % (1 years as seconds) == 0 --> 'y' else:
              seconds % (1 month as seconds) == 0 --> 'm' else:
              seconds % (1 week as seconds) == 0 --> 'w' else:
              seconds % (1 day as seconds) == 0 --> 'd' else:
              seconds % (1 hour as seconds) == 0 --> 'h' else:
              seconds % (1 minutes as seconds) == 0 --> 'min' else:
              raise RuntimeError

        :param int seconds: An integer showing the total seconds to be
          converted.
        :param bool as_work_time: Should the input be considered as work time
          or calendar time.
        :returns int, string: Returns one integer and one string, showing the
          timing value and the unit.
        """
        from stalker import defaults
        minutes = 60
        hour = 3600
        day = 86400
        week = 604800
        month = 2419200
        year = 31536000

        day_wt = defaults.daily_working_hours * 3600
        week_wt = defaults.weekly_working_days * day_wt
        month_wt = 4 * week_wt
        year_wt = int(defaults.yearly_working_days) * day_wt

        if as_work_time:
            logger.debug('calculating in work time')
            if seconds % year_wt == 0:
                return seconds // year_wt, 'y'
            elif seconds % month_wt == 0:
                return seconds // month_wt, 'm'
            elif seconds % week_wt == 0:
                return seconds // week_wt, 'w'
            elif seconds % day_wt == 0:
                return seconds // day_wt, 'd'
        else:
            logger.debug('calculating in calendar time')
            if seconds % year == 0:
                return seconds // year, 'y'
            elif seconds % month == 0:
                return seconds // month, 'm'
            elif seconds % week == 0:
                return seconds // week, 'w'
            elif seconds % day == 0:
                return seconds // day, 'd'

        # in either case
        if seconds % hour == 0:
            return seconds // hour, 'h'

        # at this point we understand that it has a residual of less then one
        # minute so return in minutes
        return seconds // minutes, 'min'

    @classmethod
    def to_seconds(cls, timing, unit, model):
        """converts the schedule values to seconds, depending on to the
        schedule_model the value will differ. So if the schedule_model is
        'effort' or 'length' then the schedule_time and schedule_unit values
        are interpreted as work time, if the schedule_model is 'duration' then
        the schedule_time and schedule_unit values are considered as calendar
        time.
        """
        if not unit:
            return None

        lut = {
            'min': 60,
            'h': 3600,
            'd': 86400,
            'w': 604800,
            'm': 2419200,
            'y': 31536000
        }

        if model in ['effort', 'length']:
            from stalker import defaults
            day_wt = defaults.daily_working_hours * 3600
            week_wt = defaults.weekly_working_days * day_wt
            month_wt = 4 * week_wt
            year_wt = int(defaults.yearly_working_days) * day_wt

            lut = {
                'min': 60,
                'h': 3600,
                'd': day_wt,
                'w': week_wt,
                'm': month_wt,
                'y': year_wt
            }

        return timing * lut[unit]

    @property
    def schedule_seconds(self):
        """Returns the schedule values as seconds, depending on to the
        schedule_model the value will differ. So if the schedule_model is
        'effort' or 'length' then the schedule_time and schedule_unit values
        are interpreted as work time, if the schedule_model is 'duration' then
        the schedule_time and schedule_unit values are considered as calendar
        time.
        """
        return self.to_seconds(
            self.schedule_timing, self.schedule_unit, self.schedule_model
        )


class DAGMixin(object):
    """Creates a parent/child or a directed acyclic graph (DAG) relation on the
    mixed in class by introducing two new attributes called parent and
    children.

    Please set the ``__id_column__`` attribute to the id column of the mixed in
    class to be able to use this mixin::

      class MixedInClass(SomeBaseClass, DAGMixin):

          id = Column('id', Integer, primary_key=True)
          __id_column__ = id

    Use the :attr:``.__dag_cascade__`` to control the cascade behaviour.
    """

    __dag_cascade__ = 'all, delete'

    @declared_attr
    def parent_id(cls):
        return Column(
            'parent_id',
            Integer,
            ForeignKey('%s.id' % cls.__tablename__)
        )

    @declared_attr
    def parent(cls):
        return relationship(
            cls.__name__,
            remote_side=[getattr(cls, cls.__id_column__)],
            primaryjoin='%(ct)s.c.parent_id==%(ct)s.c.id' % {
                'ct': cls.__tablename__
            },
            back_populates='children',
            post_update=True,
            doc="""A :class:`%(c)s` instance which is the parent of this %(c)s.
            In Stalker it is possible to create a hierarchy of %(c)s.
            """ % {
                'c': cls.__name__
            }
        )

    @declared_attr
    def children(cls):
        return relationship(
            cls.__name__,
            primaryjoin='%(ct)s.c.id==%(ct)s.c.parent_id' % {
                'ct': cls.__tablename__
            },
            back_populates='parent',
            post_update=True,
            cascade=cls.__dag_cascade__,
            doc="""Other :class:`Budget` instances which are the children of this
            one. This attribute along with the :attr:`.parent` attribute is used in
            creating a DAG hierarchy of tasks.
            """
        )

    def __init__(self, parent=None, **kwargs):
        self.parent = parent

    @validates('parent')
    def _validate_parent(self, key, parent):
        """validates the given parent value
        """
        if parent is not None:
            if not isinstance(parent, self.__class__):
                raise TypeError(
                    '%(cls)s.parent should be an instance of %(cls)s class or '
                    'derivative, not %(parent_cls)s' % {
                        'cls': self.__class__.__name__,
                        'parent_cls': parent.__class__.__name__
                    }
                )

            from stalker.models import check_circular_dependency
            check_circular_dependency(self, parent, 'children')

        return parent

    @validates('children')
    def _validate_children(self, key, child):
        """validates the given child
        """
        if not isinstance(child, self.__class__):
            raise TypeError(
                '%(cls)s.children should be a list of %(cls)s (or '
                'derivative) instances, not %(child_cls)s' % {
                    'cls': self.__class__.__name__,
                    'child_cls': child.__class__.__name__
                }
            )

        return child

    @property
    def is_root(self):
        """Returns True if the Task has no parent
        """
        return not bool(self.parent)

    @property
    def is_container(self):
        """Returns True if the Task has children Tasks
        """
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            return bool(len(self.children))

    @property
    def is_leaf(self):
        """Returns True if the Task has no children Tasks
        """
        return not self.is_container

    @property
    def parents(self):
        """Returns all of the parents of this mixed in class starting from the
        root
        """
        parents = []
        entity = self.parent
        # TODO: make this a generator
        while entity:
            parents.append(entity)
            entity = entity.parent
        parents.reverse()
        return parents

    def walk_hierarchy(self, method=0):
        """Walks the hierarchy of this task.

        :param method: The walk method, 0: Depth First, 1: Breadth First
        """
        from stalker.models import walk_hierarchy
        for c in walk_hierarchy(self, 'children', method=method):
            yield c


class AmountMixin(object):
    """Adds ``amount`` attribute to the mixed in class.

    :param int float amount:
    """

    def __init__(self, amount=0, **kwargs):
        self.amount = amount

    @declared_attr
    def amount(cls):
        return Column(Float, default=0.0)

    @validates('amount')
    def _validate_amount(self, key, amount):
        """validates the given amount value
        """
        if amount is None:
            amount = 0.0

        if not isinstance(amount, (int, float)):
            raise TypeError(
                '%s.amount should be a number, not %s' % (
                    self.__class__.__name__, amount.__class__.__name__
                )
            )

        return float(amount)


class UnitMixin(object):
    """Adds ``unit`` attribute to the mixed in class.

    :param str unit:
    """

    def __init__(self, unit='', **kwargs):
        self.unit = unit

    @declared_attr
    def unit(cls):
        return Column(String(64))

    @validates('unit')
    def _validate_unit(self, key, unit):
        """validates the given unit value
        """
        if unit is None:
            unit = ''

        from stalker import __string_types__
        if not isinstance(unit, __string_types__):
            raise TypeError(
                '%s.unit should be a string, not %s' % (
                    self.__class__.__name__, unit.__class__.__name__
                )
            )

        return unit
