# -*- coding: utf-8 -*-

import copy
import datetime

import pytest
import pytz

from stalker import TimeLog
from stalker.testing import UnitTestDBBase


class TimeLogDBTester(UnitTestDBBase):
    """tests the TimeLog class
    """

    def setUp(self):
        """setup the test
        """
        super(self.__class__, self).setUp()

        from stalker import Status
        self.status_wfd = Status.query.filter_by(code='WFD').first()
        self.status_rts = Status.query.filter_by(code='RTS').first()
        self.status_wip = Status.query.filter_by(code='WIP').first()
        self.status_prev = Status.query.filter_by(code='PREV').first()
        self.status_hrev = Status.query.filter_by(code='HREV').first()
        self.status_drev = Status.query.filter_by(code='DREV').first()
        self.status_oh = Status.query.filter_by(code='OH').first()
        self.status_stop = Status.query.filter_by(code='STOP').first()
        self.status_cmpl = Status.query.filter_by(code='CMPL').first()

        # create a resource
        from stalker.db.session import DBSession
        from stalker import User
        self.test_resource1 = User(
            name="User1",
            login="user1",
            email="user1@users.com",
            password="1234",
        )
        DBSession.add(self.test_resource1)

        self.test_resource2 = User(
            name="User2",
            login="user2",
            email="user2@users.com",
            password="1234"
        )
        DBSession.add(self.test_resource2)

        from stalker import Repository
        self.test_repo = Repository(name="test repository", code="tr")
        DBSession.add(self.test_repo)

        # create a Project
        self.test_status1 = Status(name="Status1", code="STS1")
        self.test_status2 = Status(name="Status2", code="STS2")
        self.test_status3 = Status(name="Status3", code="STS3")
        DBSession.add_all([
            self.test_status1, self.test_status2, self.test_status3
        ])

        from stalker import Project
        self.test_project = Project(
            name="test project",
            code='tp',
            repository=self.test_repo,
        )
        DBSession.add(self.test_project)

        # create Tasks
        from stalker import Task
        self.test_task1 = Task(
            name="test task 1",
            project=self.test_project,
            schedule_timing=10,
            schedule_unit='d',
            resources=[self.test_resource1]
        )
        DBSession.add(self.test_task1)

        self.test_task2 = Task(
            name="test task 2",
            project=self.test_project,
            schedule_timing=10,
            schedule_unit='d',
            resources=[self.test_resource1]
        )
        DBSession.add(self.test_task2)

        self.kwargs = {
            "task": self.test_task1,
            "resource": self.test_resource1,
            "start": datetime.datetime(2013, 3, 22, 1, 0, tzinfo=pytz.utc),
            "duration": datetime.timedelta(10)
        }

        # create a TimeLog
        # and test it
        self.test_time_log = TimeLog(**self.kwargs)
        DBSession.add(self.test_time_log)
        DBSession.commit()

    def test___auto_name__class_attribute_is_set_to_True(self):
        """testing if the __auto_name__ class attribute is set to True for
        TimeLog class
        """
        assert TimeLog.__auto_name__ is True

    def test_task_argument_is_skipped(self):
        """testing if a TypeError will be raised when the task argument is
        skipped
        """
        td = datetime.timedelta
        kwargs = copy.copy(self.kwargs)
        kwargs.pop("task")
        kwargs['start'] = kwargs['start'] - td(days=100)
        kwargs['duration'] = td(hours=10)
        with pytest.raises(TypeError) as cm:
            TimeLog(**kwargs)

        assert str(cm.value) == \
            'TimeLog.task should be an instance of stalker.models.task.Task ' \
            'not NoneType'

    def test_task_argument_is_None(self):
        """testing if a TypeError will be raised when the task argument is None
        """
        td = datetime.timedelta
        kwargs = copy.copy(self.kwargs)
        kwargs["task"] = None
        kwargs['start'] = kwargs['start'] - td(days=100)
        kwargs['duration'] = td(hours=10)
        with pytest.raises(TypeError) as cm:
            TimeLog(**kwargs)

        assert str(cm.value) == \
            'TimeLog.task should be an instance of stalker.models.task.Task ' \
            'not NoneType'

    def test_task_attribute_is_None(self):
        """testing if a TypeError will be raised when the task attribute i
        None
        """
        with pytest.raises(TypeError) as cm:
            self.test_time_log.task = None

        assert str(cm.value) == \
            'TimeLog.task should be an instance of stalker.models.task.Task ' \
            'not NoneType'

    def test_task_argument_is_not_a_Task_instance(self):
        """testing if a TypeError will be raised when the task argument is not
        a stalker.models.task.Task instance
        """
        td = datetime.timedelta
        kwargs = copy.copy(self.kwargs)
        kwargs["task"] = "this is a task"
        kwargs['start'] = kwargs['start'] - td(days=100)
        kwargs['duration'] = td(hours=10)
        with pytest.raises(TypeError) as cm:
            TimeLog(**kwargs)

        assert str(cm.value) == \
            'TimeLog.task should be an instance of stalker.models.task.Task ' \
            'not str'

    def test_task_attribute_is_not_a_Task_instance(self):
        """testing if a TypeError will be raised when the task attribute is not
        a stalker.models.task.Task instance
        """
        with pytest.raises(TypeError) as cm:
            self.test_time_log.task = "this is a task"

        assert str(cm.value) == \
            'TimeLog.task should be an instance of stalker.models.task.Task ' \
            'not str'

    def test_task_attribute_is_working_properly(self):
        """testing if the task attribute is working properly
        """
        from stalker import Task
        new_task = Task(
            name="Test task 2",
            project=self.test_project,
            resources=[self.test_resource1],
        )
        assert self.test_time_log.task != new_task
        self.test_time_log.task = new_task
        assert self.test_time_log.task == new_task

    def test_task_argument_updates_backref(self):
        """testing if the Task given with the task argument is updated
        correctly with the current TimeLog instance is listed in the time_logs
        attribute of the Task
        """
        from stalker import Task
        new_task = Task(
            name="Test Task 3",
            project=self.test_project,
            resources=[self.test_resource1],
        )

        # now create a new time_log for the new task
        kwargs = copy.copy(self.kwargs)
        kwargs["task"] = new_task
        kwargs["start"] = kwargs["start"] + kwargs["duration"] + \
                          datetime.timedelta(120)
        new_time_log = TimeLog(**kwargs)

        # now check if the new_time_log is in task.time_logs
        assert new_time_log in new_task.time_logs

    def test_task_attribute_updates_backref(self):
        """testing if the Task given with the task attribute is updated
        correctly with the current TimeLog instance is listed in the time_logs
        attribute of the Task
        """
        from stalker import Task
        new_task = Task(
            name="Test Task 3",
            project=self.test_project,
            resources=[self.test_resource1],
        )

        self.test_time_log.task = new_task
        assert self.test_time_log in new_task.time_logs

    def test_resource_argument_is_skipped(self):
        """testing if a TypeError will be raised when the resource argument is
        skipped
        """
        kwargs = copy.copy(self.kwargs)
        kwargs.pop("resource")
        kwargs['start'] -= datetime.timedelta(days=200)
        kwargs['end'] = kwargs['start'] + datetime.timedelta(days=10)
        with pytest.raises(TypeError) as cm:
            TimeLog(**kwargs)

        assert str(cm.value) == 'TimeLog.resource can not be None'

    def test_resource_argument_is_None(self):
        """testing if a TypeError will be raised when the resource argument is
        None
        """
        kwargs = copy.copy(self.kwargs)
        kwargs["resource"] = None
        with pytest.raises(TypeError) as cm:
            TimeLog(**kwargs)

        assert str(cm.value) == 'TimeLog.resource can not be None'

    def test_resource_attribute_is_None(self):
        """testing if a TypeError will be raised when the resource attribute is
        set to None
        """
        with pytest.raises(TypeError) as cm:
            self.test_time_log.resource = None

        assert str(cm.value) == 'TimeLog.resource can not be None'

    def test_resource_argument_is_not_a_User_instance(self):
        """testing if a TypeError will be raised when the resource argument is
        not a stalker.models.user.User instance
        """
        kwargs = copy.copy(self.kwargs)
        kwargs["resource"] = "This is a resource"
        with pytest.raises(TypeError) as cm:
            TimeLog(**kwargs)

        assert str(cm.value) == \
            'TimeLog.resource should be a stalker.models.auth.User instance ' \
            'not str'

    def test_resource_attribute_is_not_a_User_instance(self):
        """testing if a TypeError will be raised when the resource attribute is
        set to a value other than a stalker.models.user.User instance
        """
        with pytest.raises(TypeError) as cm:
            self.test_time_log.resource = "this is a resource"

        assert str(cm.value) == \
            'TimeLog.resource should be a stalker.models.auth.User instance ' \
            'not str'

    def test_resource_attribute_is_working_properly(self):
        """testing if the resource attribute is working properly
        """
        from stalker import User
        new_resource = User(
            name="Test Resource",
            login="test resource 2",
            email="test@resource2.com",
            password="1234",
        )

        assert self.test_time_log.resource != new_resource
        self.test_time_log.resource = new_resource
        assert self.test_time_log.resource == new_resource

    def test_resource_argument_updates_backref(self):
        """testing if the User instance given with the resource argument is
        updated with the current TimeLog is listed in the time_logs attribute
        of the User instance
        """
        from stalker import User
        new_resource = User(
            name="Test Resource",
            login="test resource 2",
            email="test@resource2.com",
            password="1234",
        )

        kwargs = copy.copy(self.kwargs)
        kwargs["resource"] = new_resource
        new_time_log = TimeLog(**kwargs)

        assert new_time_log.resource == new_resource

    def test_resource_attribute_updates_backref(self):
        """testing if the User instance given with the resource attribute is
        updated with the current TimeLog is listed in the time_logs attribute
        of the User instance
        """
        from stalker import User
        new_resource = User(
            name="Test Resource",
            login="test resource 2",
            email="test@resource2.com",
            password="1234",
        )

        assert self.test_time_log.resource != new_resource
        self.test_time_log.resource = new_resource
        assert self.test_time_log.resource == new_resource

    def test_ScheduleMixin_initialization(self):
        """testing if the DateRangeMixin part is initialized correctly
        """
        # it should have schedule attributes
        assert self.test_time_log.start == self.kwargs["start"]
        assert self.test_time_log.duration == self.kwargs["duration"]

        self.test_time_log.start = \
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
        self.test_time_log.end = \
            self.test_time_log.start + datetime.timedelta(10)
        assert self.test_time_log.duration == datetime.timedelta(10)

    def test_OverbookedError_1(self):
        """testing if a OverBookedError will be raised when the resource 
        is already booked for the given time period.

        Simple case diagram:
        #####
        #####
        """
        # time_log1
        import copy
        kwargs = copy.copy(self.kwargs)
        kwargs["resource"] = self.test_resource2
        kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc),
        kwargs["duration"] = datetime.timedelta(10)
        time_log1 = TimeLog(**kwargs)

        from stalker.db.session import DBSession
        DBSession.add(time_log1)
        DBSession.commit()

        from stalker.exceptions import OverBookedError
        with pytest.raises(OverBookedError) as cm:
            TimeLog(**kwargs)

        assert str(cm.value) == \
            'The resource has another TimeLog between %s and %s' % (
                time_log1.start, time_log1.end
            )

    def test_OverbookedError_2(self):
        """testing if a OverBookedError will be raised when the resource is
        already booked for the given time period.

        Simple case diagram:
        #######
        #####
        """
        # time_log1
        kwargs = copy.copy(self.kwargs)
        kwargs["resource"] = self.test_resource2
        kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
        kwargs["duration"] = datetime.timedelta(10)
        time_log1 = TimeLog(**kwargs)

        from stalker.db.session import DBSession
        DBSession.add(time_log1)
        DBSession.commit()

        # time_log2
        kwargs["duration"] = datetime.timedelta(8)
        from stalker.exceptions import OverBookedError
        with pytest.raises(OverBookedError) as cm:
            TimeLog(**kwargs)

        assert str(cm.value) == \
            'The resource has another TimeLog between %s and %s' % (
                time_log1.start, time_log1.end
            )

    def test_OverbookedError_3(self):
        """testing if a OverBookedError will be raised when the resource is
        already booked for the given time period.

        Simple case diagram:
        #####
        #######
        """
        # time_log1
        kwargs = copy.copy(self.kwargs)
        kwargs["resource"] = self.test_resource2
        kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
        kwargs["duration"] = datetime.timedelta(8)
        time_log1 = TimeLog(**kwargs)

        from stalker.db.session import DBSession
        DBSession.add(time_log1)
        DBSession.commit()

        # time_log2
        kwargs["duration"] = datetime.timedelta(10)
        from stalker.exceptions import OverBookedError
        with pytest.raises(OverBookedError) as cm:
            TimeLog(**kwargs)

        assert str(cm.value) == \
            'The resource has another TimeLog between %s and %s' % (
                time_log1.start, time_log1.end
            )

    def test_OverbookedError_4(self):
        """testing if a OverBookedError will be raised when the resource is
        already booked for the given time period.

        Simple case diagram:
        #######
          #####
        """
        # time_log1
        kwargs = copy.copy(self.kwargs)
        kwargs["resource"] = self.test_resource2
        kwargs["start"] = \
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc) \
            - datetime.timedelta(2)
        kwargs["duration"] = datetime.timedelta(12)
        time_log1 = TimeLog(**kwargs)

        from stalker.db.session import DBSession
        DBSession.add(time_log1)
        DBSession.commit()

        # time_log2
        kwargs["start"] = datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
        kwargs["duration"] = datetime.timedelta(10)

        from stalker.exceptions import OverBookedError
        with pytest.raises(OverBookedError) as cm:
            TimeLog(**kwargs)

        import tzlocal
        local_tz = tzlocal.get_localzone()
        assert str(cm.value) == \
            'The resource has another TimeLog between %s and %s' % (
                datetime.datetime(2013, 3, 20, 4, 0, tzinfo=pytz.utc)
                    .astimezone(local_tz),
                (datetime.datetime(2013, 3, 20, 4, 0, tzinfo=pytz.utc)
                    + datetime.timedelta(12)).astimezone(local_tz)
            )

    def test_OverbookedError_5(self):
        """testing if a OverBookedError will be raised when the resource is
        already booked for the given time period.

        Simple case diagram:
          #####
        #######
        """
        # time_log1
        kwargs = copy.copy(self.kwargs)
        kwargs["resource"] = self.test_resource2
        kwargs["start"] = \
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
        kwargs["duration"] = datetime.timedelta(10)

        time_log1 = TimeLog(**kwargs)

        from stalker.db.session import DBSession
        DBSession.add(time_log1)
        DBSession.commit()

        # time_log2
        kwargs["start"] = \
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc) \
            - datetime.timedelta(2)
        kwargs["duration"] = datetime.timedelta(12)

        from stalker.exceptions import OverBookedError
        with pytest.raises(OverBookedError) as cm:
            TimeLog(**kwargs)

        import tzlocal
        local_tz = tzlocal.get_localzone()
        assert str(cm.value) == \
            'The resource has another TimeLog between %s and %s' % (
                datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
                    .astimezone(local_tz),
                datetime.datetime(2013, 4, 1, 4, 0, tzinfo=pytz.utc)
                    .astimezone(local_tz)
            )

    def test_OverbookedError_6(self):
        """testing if a OverBookedError will be raised when the resource is
        already booked for the given time period.

        Simple case diagram:
          #######
        #######
        """
        # time_log1
        kwargs = copy.copy(self.kwargs)
        kwargs["resource"] = self.test_resource2
        kwargs["start"] = \
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
        kwargs["duration"] = datetime.timedelta(15)

        time_log1 = TimeLog(**kwargs)

        from stalker.db.session import DBSession
        DBSession.add(time_log1)
        DBSession.commit()

        # time_log2
        kwargs["start"] = \
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc) \
            - datetime.timedelta(5)
        kwargs["duration"] = datetime.timedelta(15)

        from stalker.exceptions import OverBookedError
        with pytest.raises(OverBookedError) as cm:
            TimeLog(**kwargs)

        import tzlocal
        local_tz = tzlocal.get_localzone()
        assert str(cm.value) == \
            'The resource has another TimeLog between %s and %s' % (
                datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
                    .astimezone(local_tz),
                datetime.datetime(2013, 4, 6, 4, 0, tzinfo=pytz.utc)
                    .astimezone(local_tz)
            )

    def test_OverbookedError_7(self):
        """testing if a OverBookedError will be raised when the resource is
        already booked for the given time period.

        Simple case diagram:
        #######
          #######
        """
        # time_log1
        kwargs = copy.copy(self.kwargs)
        kwargs["resource"] = self.test_resource2
        kwargs["start"] = \
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc) \
            - datetime.timedelta(5)
        kwargs["duration"] = datetime.timedelta(15)

        time_log1 = TimeLog(**kwargs)

        from stalker.db.session import DBSession
        DBSession.add(time_log1)
        DBSession.commit()

        # time_log2
        kwargs["start"] = \
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
        kwargs["duration"] = datetime.timedelta(15)

        from stalker.exceptions import OverBookedError
        with pytest.raises(OverBookedError) as cm:
            TimeLog(**kwargs)

        import tzlocal
        local_tz = tzlocal.get_localzone()
        assert str(cm.value) == \
            'The resource has another TimeLog between %s and %s' % (
                datetime.datetime(2013, 3, 17, 4, 0, tzinfo=pytz.utc)
                    .astimezone(local_tz),
                datetime.datetime(2013, 4, 1, 4, 0, tzinfo=pytz.utc)
                    .astimezone(local_tz),
            )

    def test_OverbookedError_8(self):
        """testing if no OverBookedError will be raised when the resource is
        not already booked for the given time period.

        Simple case diagram:
        #######
                 #######
        """
        # time_log1
        kwargs = copy.copy(self.kwargs)
        kwargs["resource"] = self.test_resource2
        kwargs["start"] = \
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
        kwargs["duration"] = datetime.timedelta(5)
        time_log1 = TimeLog(**kwargs)

        from stalker.db.session import DBSession
        DBSession.add(time_log1)
        DBSession.commit()

        # time_log2
        kwargs["start"] = \
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc) \
            + datetime.timedelta(20)
        # no warning
        time_log2 = TimeLog(**kwargs)
        DBSession.add(time_log2)
        DBSession.commit()

    def test_OverbookedError_9(self):
        """testing if no OverBookedError will be raised when the resource is
        not already booked for the given time period.

        Simple case diagram:
                 #######
        #######
        """
        # time_log1
        kwargs = copy.copy(self.kwargs)
        kwargs["resource"] = self.test_resource2
        kwargs["start"] =\
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc) \
            + datetime.timedelta(20)
        kwargs["duration"] = datetime.timedelta(5)
        time_log1 = TimeLog(**kwargs)

        from stalker.db.session import DBSession
        DBSession.add(time_log1)
        DBSession.commit()

        # time_log2
        kwargs["start"] = \
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)

        # no warning
        time_log2 = TimeLog(**kwargs)
        DBSession.add(time_log2)
        DBSession.commit()

    def test_OverbookedError_10(self):
        """testing if no OverBookedError will be raised for the same TimeLog
        instance
        """
        # time_log1
        kwargs = copy.copy(self.kwargs)
        kwargs['resource'] = self.test_resource2
        kwargs['start'] = \
            datetime.datetime(2013, 5, 6, 14, 0, tzinfo=pytz.utc)
        kwargs['duration'] = datetime.timedelta(20)
        time_log1 = TimeLog(**kwargs)

        # no warning
        self.test_resource2.time_logs.append(time_log1)

    def test_OverbookedError_11(self):
        """testing if a IntegrityError will be raised by the database backend
        when the resource is already booked for the given time period and it is
        not caught in Python side.

        Simple case diagram:
        #######
          #######
        """
        # time_log1
        kwargs = copy.copy(self.kwargs)
        kwargs["resource"] = self.test_resource2
        kwargs["start"] = \
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc) \
            - datetime.timedelta(5)
        kwargs["duration"] = datetime.timedelta(15)

        time_log1 = TimeLog(**kwargs)

        from stalker.db.session import DBSession
        DBSession.add(time_log1)

        # time_log2
        kwargs["start"] = \
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
        kwargs["duration"] = datetime.timedelta(15)

        time_log2 = TimeLog(**kwargs)
        DBSession.add(time_log2)

        # there should be an DatabaseError raised
        from sqlalchemy.exc import IntegrityError
        with pytest.raises(IntegrityError) as cm:
            DBSession.commit()

        assert '(psycopg2.errors.ExclusionViolation) conflicting key value ' \
            'violates exclusion constraint "overlapping_time_logs"' in \
            str(cm.value)

    def test_OverbookedError_12(self):
        """testing if a IntegrityError will be raised by the database backend
        when the resource is already booked for the given time period and it is
        not caught in Python side. But this one ensures that the error is
        raised even if the tasks are different.

        Simple case diagram:
        #######
          #######
        """
        # time_log1
        kwargs = copy.copy(self.kwargs)
        kwargs["resource"] = self.test_resource2
        kwargs["start"] = \
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc) \
            - datetime.timedelta(5)
        kwargs["duration"] = datetime.timedelta(15)
        kwargs['task'] = self.test_task1

        time_log1 = TimeLog(**kwargs)

        from stalker.db.session import DBSession
        DBSession.add(time_log1)

        # time_log2
        kwargs["start"] = \
            datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc)
        kwargs["duration"] = datetime.timedelta(15)
        kwargs['task'] = self.test_task2

        time_log2 = TimeLog(**kwargs)
        DBSession.add(time_log2)

        # there should be an DatabaseError raised
        from sqlalchemy.exc import IntegrityError
        with pytest.raises(IntegrityError) as cm:
            DBSession.commit()

        assert '(psycopg2.errors.ExclusionViolation) conflicting key value ' \
            'violates exclusion constraint "overlapping_time_logs"' in \
            str(cm.value)

    def test_timeLog_prevents_auto_flush_when_expanding_task_schedule_timing(self):
        """testing timeLog prevents auto flush when expanding task
        schedule_timing attribute
        """
        kwargs = copy.copy(self.kwargs)
        kwargs['start'] = kwargs['start'] - datetime.timedelta(days=100)
        tlog1 = TimeLog(**kwargs)

        from stalker.db.session import DBSession
        DBSession.add(tlog1)
        DBSession.commit()

        # create a new time log
        kwargs['start'] = kwargs['start'] + kwargs['duration']
        tlog2 = TimeLog(**kwargs)

    def test_timeLog_creation_for_a_child_task(self):
        """testing TimeLog creation for a child task which has a couple of
        parent tasks
        """
        dt = datetime.datetime
        td = datetime.timedelta

        from stalker import Task
        parent_task1 = Task(
            name="Parent Task 1",
            project=self.test_project,
        )

        parent_task2 = Task(
            name="Parent Task 2",
            project=self.test_project,
        )

        child_task1 = Task(
            name="Child Task 1",
            project=self.test_project,
            resources=[self.test_resource1]
        )

        child_task2 = Task(
            name="Child Task 1",
            project=self.test_project,
            resources=[self.test_resource2]
        )

        # Task hierarchy
        # +-> p1
        # |   |
        # |   +-> p2
        # |   |    |
        # |   |    +-> c1
        # |   |
        # |   +-> c2
        # |
        # +-> self.test_task1
        parent_task2.parent = parent_task1
        child_task2.parent = parent_task1
        child_task1.parent = parent_task2

        assert parent_task1.total_logged_seconds == 0
        assert parent_task2.total_logged_seconds == 0
        assert child_task1.total_logged_seconds == 0
        assert child_task2.total_logged_seconds == 0

        # now create a time log for child_task2
        tlog1 = TimeLog(
            task=child_task2,
            resource=child_task2.resources[0],
            start=dt(2013, 7, 31, 10, 0, tzinfo=pytz.utc),
            end=dt(2013, 7, 31, 19, 0, tzinfo=pytz.utc)
        )

        # before commit
        assert parent_task1.total_logged_seconds == 9 * 3600
        assert parent_task2.total_logged_seconds == 0
        assert child_task1.total_logged_seconds == 0
        assert child_task2.total_logged_seconds == 0

        # commit changes
        from stalker.db.session import DBSession
        DBSession.add(tlog1)
        DBSession.commit()

        # after commit it should not change
        assert parent_task1.total_logged_seconds == 9 * 3600
        assert parent_task2.total_logged_seconds == 0
        assert child_task1.total_logged_seconds == 0
        assert child_task2.total_logged_seconds == 9 * 3600

        # add a new tlog to child_task2 and commit it
        # now create a time log for child_task2
        tlog2 = TimeLog(
            task=child_task2,
            resource=child_task2.resources[0],
            start=dt(2013, 7, 31, 19, 0, tzinfo=pytz.utc),
            end=dt(2013, 7, 31, 22, 0, tzinfo=pytz.utc)
        )

        assert parent_task1.total_logged_seconds == 12 * 3600
        assert parent_task2.total_logged_seconds == 0
        assert child_task1.total_logged_seconds == 0
        assert child_task2.total_logged_seconds == 9 * 3600

        # commit changes
        DBSession.add(tlog2)
        DBSession.commit()

        assert parent_task1.total_logged_seconds == 12 * 3600
        assert parent_task2.total_logged_seconds == 0
        assert child_task1.total_logged_seconds == 0
        assert child_task2.total_logged_seconds == 12 * 3600

        # add a new time log to child_task1 and commit it
        tlog3 = TimeLog(
            task=child_task1,
            resource=child_task1.resources[0],
            start=dt(2013, 7, 31, 10, 0, tzinfo=pytz.utc),
            end=dt(2013, 7, 31, 19, 0, tzinfo=pytz.utc)
        )
        # commit changes
        DBSession.add(tlog3)
        DBSession.commit()

        assert parent_task1.total_logged_seconds == 21 * 3600
        assert parent_task2.total_logged_seconds == 9 * 3600
        assert child_task1.total_logged_seconds == 9 * 3600
        assert child_task2.total_logged_seconds == 12 * 3600

        # assert parent_task1.total_logged_seconds == 21 * 3600
        # assert parent_task2.total_logged_seconds == 9 * 3600
        # assert child_task1.total_logged_seconds == 9 * 3600
        # assert child_task2.total_logged_seconds == 12 * 3600

    def test_time_log_creation_for_a_WFD_leaf_task(self):
        """testing if a StatusError will be raised when a TimeLog instance
        wanted to be created for a WFD leaf task
        """
        from stalker import Task
        new_task = Task(
            name='Test Task 2',
            project=self.test_project
        )
        new_task.depends = [self.test_task1]
        kwargs = copy.copy(self.kwargs)
        kwargs['task'] = new_task
        from stalker.exceptions import StatusError
        with pytest.raises(StatusError) as cm:
            TimeLog(**kwargs)

        assert str(cm.value) == \
            'Test Task 2 is a WFD task, and it is not allowed to create ' \
            'TimeLogs for a WFD task, please supply a RTS, WIP, HREV or ' \
            'DREV task!'

    def test_time_log_creation_for_a_RTS_leaf_task(self):
        """testing if the status will be updated to WIP when a TimeLog instance
        is created for a RTS leaf task
        """
        kwargs = copy.copy(self.kwargs)
        task = kwargs['task']
        kwargs['start'] -= datetime.timedelta(days=100)
        task.status = self.status_rts
        assert task.status == self.status_rts
        TimeLog(**kwargs)
        assert task.status == self.status_wip

    def test_time_log_creation_for_a_WIP_leaf_task(self):
        """testing if the status will stay at WIP when a TimeLog instance is
        created for a WIP leaf task
        """
        kwargs = copy.copy(self.kwargs)
        task = kwargs['task']
        kwargs['start'] -= datetime.timedelta(days=10)
        task.status = self.status_wip
        assert task.status == self.status_wip
        TimeLog(**kwargs)

    def test_time_log_creation_for_a_PREV_leaf_task(self):
        """testing if the status will stay at PREV when a TimeLog instance is
        created for a PREV leaf task
        """
        kwargs = copy.copy(self.kwargs)
        task = kwargs['task']
        kwargs['start'] -= datetime.timedelta(days=100)
        task.status = self.status_prev
        assert task.status == self.status_prev
        TimeLog(**kwargs)
        assert task.status == self.status_prev

    def test_time_log_creation_for_a_HREV_leaf_task(self):
        """testing if the status will be updated to WIP when a TimeLog instance
        is created for a HREV leaf task
        """
        kwargs = copy.copy(self.kwargs)
        task = kwargs['task']
        kwargs['start'] -= datetime.timedelta(days=100)
        task.status = self.status_hrev
        assert task.status == self.status_hrev
        TimeLog(**kwargs)

    def test_time_log_creation_for_a_DREV_leaf_task(self):
        """testing if the status will stay at DREV when a TimeLog instance is
        created for a DREV leaf task
        """
        kwargs = copy.copy(self.kwargs)
        task = kwargs['task']
        kwargs['start'] -= datetime.timedelta(days=100)
        task.status = self.status_drev
        assert task.status == self.status_drev
        TimeLog(**kwargs)

    def test_time_log_creation_for_a_OH_leaf_task(self):
        """testing if a StatusError will be raised when a TimeLog instance is
        created for a OH leaf task
        """
        kwargs = copy.copy(self.kwargs)
        task = kwargs['task']
        task.status = self.status_oh
        assert task.status == self.status_oh
        from stalker.exceptions import StatusError
        with pytest.raises(StatusError) as cm:
            TimeLog(**kwargs)

        assert str(cm.value) == \
            'test task 1 is a OH task, and it is not allowed to create ' \
            'TimeLogs for a OH task, please supply a RTS, WIP, HREV or DREV ' \
            'task!'

    def test_time_log_creation_for_a_STOP_leaf_task(self):
        """testing if a StatusError will be raised when a TimeLog instance is
        created for a STOP leaf task
        """
        kwargs = copy.copy(self.kwargs)
        task = kwargs['task']
        task.status = self.status_stop
        assert task.status == self.status_stop
        from stalker.exceptions import StatusError
        with pytest.raises(StatusError) as cm:
            TimeLog(**kwargs)

        assert str(cm.value) == \
            'test task 1 is a STOP task, and it is not allowed to create ' \
            'TimeLogs for a STOP task, please supply a RTS, WIP, HREV or ' \
            'DREV task!'

    def test_time_log_creation_for_a_CMPL_leaf_task(self):
        """testing if a StatusError will be raised when a TimeLog instance is
        created for a CMPL leaf task
        """
        kwargs = copy.copy(self.kwargs)
        task = kwargs['task']
        task.status = self.status_cmpl
        assert task.status == self.status_cmpl
        from stalker.exceptions import StatusError
        with pytest.raises(StatusError) as cm:
            TimeLog(**kwargs)

        assert str(cm.value) == \
            'test task 1 is a CMPL task, and it is not allowed to create ' \
            'TimeLogs for a CMPL task, please supply a RTS, WIP, HREV or ' \
            'DREV task!'

    def test_time_log_creation_that_violates_dependency_condition_WIP_CMPL_onend(self):
        """testing if a DependencyViolationError will be raised when the entered
        TimeLog will violate the dependency relation of the task

            +--------+
            | Task 1 | ----+
            |  CMPL  |     |
            +--------+     |    +--------+
                           +--->| Task 2 |
                                |  WIP   |
                                +--------+
        """
        kwargs = copy.copy(self.kwargs)
        task = kwargs['task']
        task.status = self.status_cmpl
        task.start = datetime.datetime(2014, 3, 16, 10, 0, tzinfo=pytz.utc)
        task.end = datetime.datetime(2014, 3, 25, 19, 0, tzinfo=pytz.utc)

        from stalker import Task
        dep_task = Task(
            name="test task 2",
            project=self.test_project,
            schedule_timing=10,
            schedule_unit='d',
            depends=[task],
            resources=[self.test_resource2]
        )

        # set the dependency target to onend
        dep_task.task_depends_to[0].dependency_target = 'onend'

        # entering a time log to the dates before 2014-03-25-19-0 should raise
        # a ValueError
        from stalker.exceptions import DependencyViolationError
        with pytest.raises(DependencyViolationError) as cm:
            dep_task.create_time_log(
                self.test_resource2,
                datetime.datetime(2014, 3, 25, 18, 0, tzinfo=pytz.utc),
                datetime.datetime(2014, 3, 25, 19, 0, tzinfo=pytz.utc)
            )

        assert 'It is not possible to create a TimeLog before %s, which ' \
            'violates the dependency relation of "%s" to "%s"' % (
                datetime.datetime(2014, 3, 25, 19, 0, tzinfo=pytz.utc),
                dep_task.name,
                task.name
            ) == str(cm.value)

        # and creating a TimeLog after that is possible
        dep_task.create_time_log(
            self.test_resource2,
            datetime.datetime(2014, 3, 25, 19, 0, tzinfo=pytz.utc),
            datetime.datetime(2014, 3, 25, 20, 0, tzinfo=pytz.utc)
        )

    def test_time_log_creation_that_violates_dependency_condition_WIP_CMPL_onstart(self):
        """testing if a ValueError will be raised when the entered TimeLog will
        violate the dependency relation of the task

            +--------+
          +-| Task 1 |
          | |  CMPL  |
          | +--------+          +--------+
          +-------------------->| Task 2 |
                                |  WIP   |
                                +--------+
        """
        kwargs = copy.copy(self.kwargs)
        task = kwargs['task']
        task.status = self.status_cmpl
        task.start = datetime.datetime(2014, 3, 16, 10, 0, tzinfo=pytz.utc)
        task.end = datetime.datetime(2014, 3, 25, 19, 0, tzinfo=pytz.utc)

        from stalker import Task
        dep_task = Task(
            name="test task 2",
            project=self.test_project,
            schedule_timing=10,
            schedule_unit='d',
            depends=[task],
            resources=[self.test_resource2]
        )

        # set the dependency target to onstart
        dep_task.task_depends_to[0].dependency_target = 'onstart'

        # entering a time log to the dates before 2014-03-16-10-0 should raise
        # a ValueError
        from stalker.exceptions import DependencyViolationError
        with pytest.raises(DependencyViolationError) as cm:
            dep_task.create_time_log(
                self.test_resource2,
                datetime.datetime(2014, 3, 16, 9, 0, tzinfo=pytz.utc),
                datetime.datetime(2014, 3, 16, 10, 0, tzinfo=pytz.utc)
            )

        assert 'It is not possible to create a TimeLog before %s, which ' \
            'violates the dependency relation of "%s" to "%s"' % (
                datetime.datetime(2014, 3, 16, 10, 0, tzinfo=pytz.utc),
                dep_task.name, task.name) == str(cm.value)

        # and creating a TimeLog after that is possible
        dep_task.create_time_log(
            self.test_resource2,
            datetime.datetime(2014, 3, 16, 10, 0, tzinfo=pytz.utc),
            datetime.datetime(2014, 3, 16, 10, 0, tzinfo=pytz.utc)
        )

