# -*- coding: utf-8 -*-

import unittest

import pytest

from stalker.testing import UnitTestDBBase


class DailyTestBase(unittest.TestCase):
    """Tests the stalker.models.review.Daily class
    """

    def setUp(self):
        super(DailyTestBase, self).setUp()

        from stalker import Status, StatusList
        self.status_new = Status(name='Mew', code='NEW')
        self.status_wfd = Status(name='Waiting For Dependency', code='WFD')
        self.status_rts = Status(name='Ready To Start', code='RTS')
        self.status_wip = Status(name='Work In Progress', code='WIP')
        self.status_prev = Status(name='Pending Review', code='PREV')
        self.status_hrev = Status(name='Has Revision', code='HREV')
        self.status_drev = Status(name='Dependency Has Revision', code='DREV')
        self.status_cmpl = Status(name='Completed', code='CMPL')

        self.status_open = Status(name='Open', code='OPEN')
        self.status_cls = Status(name='Closed', code='CLS')

        self.daily_status_list = StatusList(
            name='Daily Statuses',
            statuses=[self.status_open, self.status_cls],
            target_entity_type='Daily'
        )

        self.task_status_list = StatusList(
            name='Task Statuses',
            statuses=[self.status_wfd, self.status_rts, self.status_wip,
                      self.status_prev, self.status_hrev, self.status_drev,
                      self.status_cmpl],
            target_entity_type='Task'
        )

        self.test_project_status_list = StatusList(
            name='Project Statuses',
            target_entity_type='Project',
            statuses=[self.status_new, self.status_wip, self.status_cmpl]
        )

        from stalker import Repository, Project
        self.test_repo = Repository(name='Test Repository', code='TR')

        self.test_project = Project(
            name='Test Project',
            code='TP',
            repository=self.test_repo,
            status_list=self.test_project_status_list
        )

        from stalker import Task
        self.test_task1 = Task(
            name='Test Task 1',
            project=self.test_project,
            status_list=self.task_status_list
        )
        self.test_task2 = Task(
            name='Test Task 2',
            project=self.test_project,
            status_list=self.task_status_list
        )
        self.test_task3 = Task(
            name='Test Task 3',
            project=self.test_project,
            status_list=self.task_status_list
        )

        from stalker import Version
        self.test_version1 = Version(task=self.test_task1)
        self.test_version2 = Version(task=self.test_task1)
        self.test_version3 = Version(task=self.test_task1)
        self.test_version4 = Version(task=self.test_task2)

        from stalker import Link
        self.test_link1 = Link(original_filename='test_render1.jpg')
        self.test_link2 = Link(original_filename='test_render2.jpg')
        self.test_link3 = Link(original_filename='test_render3.jpg')
        self.test_link4 = Link(original_filename='test_render4.jpg')

        self.test_version1.outputs = [
            self.test_link1,
            self.test_link2,
            self.test_link3
        ]
        self.test_version4.outputs = [
            self.test_link4
        ]


class DailyTestCase(DailyTestBase):
    """Tests the stalker.models.review.Daily class
    """

    def test_daily_instance_creation(self):
        """testing if it is possible to create a Daily without a problem
        """
        from stalker import Daily
        daily = Daily(
            name='Test Daily',
            project=self.test_project,
            status_list=self.daily_status_list
        )
        assert isinstance(daily, Daily)

    def test_links_argument_is_skipped(self):
        """testing if the links attribute will be an empty list if the links
        argument is skipped
        """
        from stalker import Daily
        daily = Daily(
            name='Test Daily',
            project=self.test_project,
            status_list=self.daily_status_list
        )
        assert daily.links == []

    def test_links_argument_is_none(self):
        """testing if the links attribute will be an empty list when the links
        argument is None
        """
        from stalker import Daily
        daily = Daily(
            name='Test Daily',
            links=None,
            project=self.test_project,
            status_list=self.daily_status_list
        )
        assert daily.links == []

    def test_links_attribute_is_set_to_none(self):
        """testing if a TypeError will be raised when the links attribute is
        set to None
        """
        from stalker import Daily
        daily = Daily(
            name='Test Daily',
            project=self.test_project,
            status_list=self.daily_status_list
        )
        with pytest.raises(TypeError):
            daily.links = None

    def test_links_argument_is_not_a_list_instance(self):
        """testing if a TypeError will be raised when the links argument is not
        a list
        """
        from stalker import Daily
        with pytest.raises(TypeError) as cm:
            Daily(
                name='Test Daily',
                links='not a list of Daily instances',
                project=self.test_project,
                status_list=self.daily_status_list
            )

        assert str(cm.value) == \
            'DailyLink.link should be an instance of ' \
            'stalker.models.link.Link instance, not str'

    def test_links_argument_is_not_a_list_of_link_instances(self):
        """testing if a TypeError will be raised when the links argument is not
        a list of Link instances
        """
        from stalker import Daily
        with pytest.raises(TypeError) as cm:
            Daily(
                name='Test Daily',
                links=['not', 1, 'list', 'of', Daily, 'instances'],
                project=self.test_project,
                status_list=self.daily_status_list
            )

        assert str(cm.value) == \
            'DailyLink.link should be an instance of ' \
            'stalker.models.link.Link instance, not str'

    def test_links_argument_is_working_properly(self):
        """testing if the links argument value is correctly passed to the links
        attribute
        """
        test_value = [self.test_link1, self.test_link2]
        from stalker import Daily
        daily = Daily(
            name='Test Daily',
            links=test_value,
            project=self.test_project,
            status_list=self.daily_status_list
        )
        assert daily.links == test_value

    def test_links_attribute_is_working_properly(self):
        """testing if the links attribute is working properly
        """
        from stalker import Daily
        daily = Daily(
            name='Test Daily',
            project=self.test_project,
            status_list=self.daily_status_list
        )
        daily.links.append(self.test_link1)

        assert daily.links == [self.test_link1]

    def test_versions_attribute_is_read_only(self):
        """testing if versions attribute is a read only attribute
        """
        from stalker import Daily
        daily = Daily(
            name='Test Daily',
            project=self.test_project,
            status_list=self.daily_status_list
        )
        with pytest.raises(AttributeError):
            setattr(daily, 'versions', 10)


class DailyDBTestDBCase(UnitTestDBBase):

    def setUp(self):
        super(DailyDBTestDBCase, self).setUp()

        from stalker import Status, StatusList
        self.status_new = Status.query.filter_by(code='NEW').first()
        self.status_wfd = Status.query.filter_by(code='WFD').first()
        self.status_rts = Status.query.filter_by(code='RTS').first()
        self.status_wip = Status.query.filter_by(code='WIP').first()
        self.status_prev = Status.query.filter_by(code='PREV').first()
        self.status_hrev = Status.query.filter_by(code='HREV').first()
        self.status_drev = Status.query.filter_by(code='DREV').first()
        self.status_cmpl = Status.query.filter_by(code='CMPL').first()

        self.status_open = Status.query.filter_by(code='OPEN').first()
        self.status_cls = Status.query.filter_by(code='CLS').first()

        self.daily_status_list = \
            StatusList.query.filter_by(target_entity_type='Daily').first()

        self.task_status_list = \
            StatusList.query.filter_by(target_entity_type='Task').first()

        from stalker import Repository, Project
        self.test_repo = Repository(name='Test Repository', code='TR')
        from stalker.db.session import DBSession
        DBSession.add(self.test_repo)

        self.test_project = Project(
            name='Test Project',
            code='TP',
            repository=self.test_repo,
        )
        DBSession.add(self.test_project)

        from stalker import Task
        self.test_task1 = Task(
            name='Test Task 1',
            project=self.test_project,
            status_list=self.task_status_list
        )
        DBSession.add(self.test_task1)
        self.test_task2 = Task(
            name='Test Task 2',
            project=self.test_project,
            status_list=self.task_status_list
        )
        DBSession.add(self.test_task2)
        self.test_task3 = Task(
            name='Test Task 3',
            project=self.test_project,
            status_list=self.task_status_list
        )
        DBSession.add(self.test_task3)
        DBSession.commit()

        from stalker import Version
        self.test_version1 = Version(task=self.test_task1)
        DBSession.add(self.test_version1)
        DBSession.commit()
        self.test_version2 = Version(task=self.test_task1)
        DBSession.add(self.test_version2)
        DBSession.commit()
        self.test_version3 = Version(task=self.test_task1)
        DBSession.add(self.test_version3)
        DBSession.commit()
        self.test_version4 = Version(task=self.test_task2)
        DBSession.add(self.test_version4)
        DBSession.commit()

        from stalker import Link
        self.test_link1 = Link(original_filename='test_render1.jpg')
        self.test_link2 = Link(original_filename='test_render2.jpg')
        self.test_link3 = Link(original_filename='test_render3.jpg')
        self.test_link4 = Link(original_filename='test_render4.jpg')
        DBSession.add_all([
            self.test_link1, self.test_link2, self.test_link3, self.test_link4
        ])

        self.test_version1.outputs = [
            self.test_link1,
            self.test_link2,
            self.test_link3
        ]
        self.test_version4.outputs = [
            self.test_link4
        ]
        DBSession.commit()

    def test_tasks_attribute_will_return_a_list_of_tasks(self):
        """testing if the tasks attribute is a list of Task instances related
        to the given links
        """
        from stalker import Daily
        daily = Daily(
            name='Test Daily',
            project=self.test_project,
            status_list=self.daily_status_list
        )
        daily.links = [self.test_link1, self.test_link2]
        from stalker.db.session import DBSession
        DBSession.add(daily)
        DBSession.commit()
        assert daily.tasks == [self.test_task1]

    def test_versions_attribute_will_return_a_list_of_versions(self):
        """testing if the versions attribute is a list of Version instances
        related to the given links
        """
        from stalker import Daily
        daily = Daily(
            name='Test Daily',
            project=self.test_project,
            status_list=self.daily_status_list
        )
        daily.links = [self.test_link1, self.test_link2]
        from stalker.db.session import DBSession
        DBSession.add(daily)
        DBSession.commit()
        assert daily.versions == [self.test_version1]


class DailyLinkTestCase(DailyTestBase):
    """tests the DailyLink class
    """

    def test_rank_argument_is_skipped(self):
        """testing if rank attribute will use the default value is when skipped
        """
        from stalker import DailyLink
        dl = DailyLink()
        assert dl.rank == 0

    def test_daily_argument_is_not_a_daily_instance(self):
        """testing if a TypeError will be raised if the daily argument is not a
        Daily instance and not None
        """
        from stalker import DailyLink
        with pytest.raises(TypeError) as cm:
            DailyLink(daily='not a daily')

        assert str(cm.value) == \
            'DailyLink.daily should be an instance of ' \
            'stalker.models.review.Daily instance, not str'
