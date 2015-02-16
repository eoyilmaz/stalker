# -*- coding: utf-8 -*-
# stalker
# Copyright (C) 2013 Erkan Ozgur Yilmaz
#
# This file is part of stalker.
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

import datetime
import tempfile
import unittest
from stalker.db import DBSession
from stalker import (db, User, Status, StatusList, Repository, Project, Task,
                     Type, TimeLog)
from stalker.exceptions import StatusError


class TaskStatusWorkflowTestCase(unittest.TestCase):
    """tests the Task Status Workflow
    """

    @classmethod
    def setUpClass(cls):
        """setup the test
        """
        db.setup({'sqlalchemy.url': 'sqlite:///:memory:'})
        db.init()

        # test users
        cls.test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@test.com',
            password='secret'
        )
        DBSession.add(cls.test_user1)

        cls.test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@test.com',
            password='secret'
        )
        DBSession.add(cls.test_user2)

        # create a couple of tasks
        cls.status_new = Status.query.filter_by(code='NEW').first()
        cls.status_wfd = Status.query.filter_by(code='WFD').first()
        cls.status_rts = Status.query.filter_by(code='RTS').first()
        cls.status_wip = Status.query.filter_by(code='WIP').first()
        cls.status_prev = Status.query.filter_by(code='PREV').first()
        cls.status_hrev = Status.query.filter_by(code='HREV').first()
        cls.status_drev = Status.query.filter_by(code='DREV').first()
        cls.status_oh = Status.query.filter_by(code='OH').first()
        cls.status_stop = Status.query.filter_by(code='STOP').first()
        cls.status_cmpl = Status.query.filter_by(code='CMPL').first()

        cls.status_rrev = Status.query.filter_by(code='RREV').first()
        cls.status_app = Status.query.filter_by(code='APP').first()

        cls.test_project_status_list = StatusList(
            name='Project Statuses',
            target_entity_type='Project',
            statuses=[cls.status_wfd, cls.status_wip,
                      cls.status_cmpl]
        )
        DBSession.add(cls.test_project_status_list)

        cls.test_task_statuses = StatusList.query\
            .filter_by(target_entity_type='Task').first()
        DBSession.add(cls.test_task_statuses)

        # repository
        tempdir = tempfile.mkdtemp()
        cls.test_repo = Repository(
            name='Test Repository',
            linux_path=tempdir,
            windows_path=tempdir,
            osx_path=tempdir
        )
        DBSession.add(cls.test_repo)

        # proj1
        cls.test_project1 = Project(
            name='Test Project 1',
            code='TProj1',
            status_list=cls.test_project_status_list,
            repository=cls.test_repo,
            start=datetime.datetime(2013, 6, 20, 0, 0, 0),
            end=datetime.datetime(2013, 6, 30, 0, 0, 0),
        )
        DBSession.add(cls.test_project1)

    def setUp(self):
        """set up before every test
        """
        # root tasks
        self.test_task1 = Task(
            name='Test Task 1',
            project=self.test_project1,
            responsible=[self.test_user1],
            status_list=self.test_task_statuses,
            start=datetime.datetime(2013, 6, 20, 0, 0),
            end=datetime.datetime(2013, 6, 30, 0, 0),
            schedule_timing=10,
            schedule_unit='d',
            schedule_model='effort',
        )
        DBSession.add(self.test_task1)

        self.test_task2 = Task(
            name='Test Task 2',
            project=self.test_project1,
            responsible=[self.test_user1],
            status_list=self.test_task_statuses,
            start=datetime.datetime(2013, 6, 20, 0, 0),
            end=datetime.datetime(2013, 6, 30, 0, 0),
            schedule_timing=10,
            schedule_unit='d',
            schedule_model='effort',
        )
        DBSession.add(self.test_task2)

        self.test_task3 = Task(
            name='Test Task 3',
            project=self.test_project1,
            status_list=self.test_task_statuses,
            resources=[self.test_user1, self.test_user2],
            responsible=[self.test_user1, self.test_user2],
            start=datetime.datetime(2013, 6, 20, 0, 0),
            end=datetime.datetime(2013, 6, 30, 0, 0),
            schedule_timing=10,
            schedule_unit='d',
            schedule_model='effort',
        )
        DBSession.add(self.test_task3)

        # children tasks

        # children of self.test_task1
        self.test_task4 = Task(
            name='Test Task 4',
            parent=self.test_task1,
            status=self.status_wfd,
            status_list=self.test_task_statuses,
            resources=[self.test_user1],
            depends=[self.test_task3],
            start=datetime.datetime(2013, 6, 20, 0, 0),
            end=datetime.datetime(2013, 6, 30, 0, 0),
            schedule_timing=10,
            schedule_unit='d',
            schedule_model='effort',
        )
        DBSession.add(self.test_task4)

        self.test_task5 = Task(
            name='Test Task 5',
            parent=self.test_task1,
            status_list=self.test_task_statuses,
            resources=[self.test_user1],
            depends=[self.test_task4],
            start=datetime.datetime(2013, 6, 20, 0, 0),
            end=datetime.datetime(2013, 6, 30, 0, 0),
            schedule_timing=10,
            schedule_unit='d',
            schedule_model='effort',
        )
        DBSession.add(self.test_task5)

        self.test_task6 = Task(
            name='Test Task 6',
            parent=self.test_task1,
            status_list=self.test_task_statuses,
            resources=[self.test_user1],
            start=datetime.datetime(2013, 6, 20, 0, 0),
            end=datetime.datetime(2013, 6, 30, 0, 0),
            schedule_timing=10,
            schedule_unit='d',
            schedule_model='effort',
        )
        DBSession.add(self.test_task6)

        # children of self.test_task2
        self.test_task7 = Task(
            name='Test Task 7',
            parent=self.test_task2,
            status_list=self.test_task_statuses,
            resources=[self.test_user2],
            start=datetime.datetime(2013, 6, 20, 0, 0),
            end=datetime.datetime(2013, 6, 30, 0, 0),
            schedule_timing=10,
            schedule_unit='d',
            schedule_model='effort',
        )
        DBSession.add(self.test_task7)

        self.test_task8 = Task(
            name='Test Task 8',
            parent=self.test_task2,
            status_list=self.test_task_statuses,
            resources=[self.test_user2],
            start=datetime.datetime(2013, 6, 20, 0, 0),
            end=datetime.datetime(2013, 6, 30, 0, 0),
            schedule_timing=10,
            schedule_unit='d',
            schedule_model='effort',
        )
        DBSession.add(self.test_task8)

        self.test_asset_status_list = StatusList.query\
            .filter_by(target_entity_type='Asset').first()
        DBSession.add(self.test_asset_status_list)

        # create an asset in between
        from stalker import Asset
        self.test_asset1 = Asset(
            name='Test Asset 1',
            code='TA1',
            parent=self.test_task7,
            type=Type(
                name='Character',
                code='Char',
                target_entity_type='Asset',
            ),
            status_list=self.test_asset_status_list
        )
        DBSession.add(self.test_asset1)

        # new task under asset
        self.test_task9 = Task(
            name='Test Task 9',
            parent=self.test_asset1,
            status_list=self.test_task_statuses,
            start=datetime.datetime(2013, 6, 20, 0, 0),
            end=datetime.datetime(2013, 6, 30, 0, 0),
            resources=[self.test_user2],
            schedule_timing=10,
            schedule_unit='d',
            schedule_model='effort',
        )
        DBSession.add(self.test_task9)
        DBSession.commit()

        # --------------
        # Task Hierarchy
        # --------------
        #
        # +-> Test Task 1
        # |   |
        # |   +-> Test Task 4
        # |   |
        # |   +-> Test Task 5
        # |   |
        # |   +-> Test Task 6
        # |
        # +-> Test Task 2
        # |   |
        # |   +-> Test Task 7
        # |   |   |
        # |   |   +-> Test Asset 1
        # |   |       |
        # |   |       +-> Test Task 9
        # |   |
        # |   +-> Test Task 8
        # |
        # +-> Test Task 3

        # no children for self.test_task3
        self.all_tasks = [
            self.test_task1, self.test_task2, self.test_task3,
            self.test_task4, self.test_task5, self.test_task6,
            self.test_task7, self.test_task8, self.test_task9,
            self.test_asset1
        ]

        self.data_created = [
            self.test_task1, self.test_task2, self.test_task3,
            self.test_task4, self.test_task5, self.test_task6,
            self.test_task7, self.test_task8, self.test_task9,
            self.test_asset1
        ]

    def tearDown(self):
        """run after every test and clean up
        """
        DBSession.commit()
        for data in self.data_created:
            if data in DBSession:
                DBSession.delete(data)
        DBSession.commit()

    @classmethod
    def tearDownClass(cls):
        """run only once
        """
        from stalker import defaults
        DBSession.remove()
        defaults.timing_resolution = datetime.timedelta(hours=1)

    def test_walk_hierarchy_is_working_properly(self):
        """testing if walk_hierarchy_is_working_properly
        """
        # this test should not be placed here
        visited_tasks = []
        expected_result = [
            self.test_task2, self.test_task7, self.test_task8,
            self.test_asset1, self.test_task9
        ]

        for task in self.test_task2.walk_hierarchy(method=1):
            visited_tasks.append(task)

        self.assertEqual(expected_result, visited_tasks)

    def test_walk_dependencies_is_working_properly(self):
        """testing if walk_dependencies is working properly
        """
        # this test should not be placed here
        visited_tasks = []
        expected_result = [
            self.test_task9, self.test_task6, self.test_task4, self.test_task5,
            self.test_task8, self.test_task3, self.test_task4, self.test_task8,
            self.test_task3
        ]

        # setup dependencies
        self.test_task9.depends = [self.test_task6]
        self.test_task6.depends = [self.test_task4, self.test_task5]
        self.test_task5.depends = [self.test_task4]
        self.test_task4.depends = [self.test_task8, self.test_task3]

        for task in self.test_task9.walk_dependencies():
            visited_tasks.append(task)

        self.assertEqual(expected_result, visited_tasks)

    # The following tests will test the status changes in dependency changes

    # Leaf Tasks - dependency relation changes
    # WFD
    def test_leaf_WFD_task_updated_to_have_a_dependency_of_WFD_task_task(self):
        """testing if it is possible to set a dependency between a task with
        WFD status to a task with WFD status and the status of the task will
        stay WFD
        """
        # create another dependency to make the task3 a WFD task
        self.test_task3.depends = []
        self.test_task9.status = self.status_wip
        self.assertEqual(self.test_task9.status, self.status_wip)
        self.test_task3.depends.append(self.test_task9)
        self.assertEqual(self.test_task3.status, self.status_wfd)
        # make a task with HREV status
        # create dependency
        self.test_task8.status = self.status_wfd
        self.assertEqual(self.test_task8.status, self.status_wfd)
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_leaf_WFD_task_updated_to_have_a_dependency_of_RTS_task(self):
        """testing if it is possible to set a dependency between a task with
        WFD status to a task with RTS status and the status of the task will
        stay WFD
        """
        # create another dependency to make the task3 a WFD task
        self.test_task3.depends = []
        self.test_task9.status = self.status_wip
        self.assertEqual(self.test_task9.status, self.status_wip)
        self.test_task3.depends.append(self.test_task9)
        self.assertEqual(self.test_task3.status, self.status_wfd)
        # make a task with HREV status
        # create dependency
        self.test_task8.status = self.status_rts
        self.assertEqual(self.test_task8.status, self.status_rts)
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_leaf_WFD_task_updated_to_have_a_dependency_of_WIP_task(self):
        """testing if it is possible to set a dependency between a task with
        WFD status to a task with WIP status and the status of the task will
        stay WFD
        """
        # create another dependency to make the task3 a WFD task
        self.test_task3.depends = []
        self.test_task9.status = self.status_wip
        self.assertEqual(self.test_task9.status, self.status_wip)
        self.test_task3.depends.append(self.test_task9)
        self.assertEqual(self.test_task3.status, self.status_wfd)
        # make a task with HREV status
        # create dependency
        self.test_task8.status = self.status_wip
        self.assertEqual(self.test_task8.status, self.status_wip)
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_leaf_WFD_task_updated_to_have_a_dependency_of_PREV_task(self):
        """testing if it is possible to set a dependency between a task with
        WFD status to a task with PREV status and the status of the task will
        stay WFD
        """
        # create another dependency to make the task3 a WFD task
        self.test_task3.depends = []
        self.test_task9.status = self.status_wip
        self.assertEqual(self.test_task9.status, self.status_wip)
        self.test_task3.depends.append(self.test_task9)
        self.assertEqual(self.test_task3.status, self.status_wfd)
        # make a task with HREV status
        # create dependency
        self.test_task8.status = self.status_prev
        self.assertEqual(self.test_task8.status, self.status_prev)
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_leaf_WFD_task_updated_to_have_a_dependency_of_HREV_task(self):
        """testing if it is possible to set a dependency between a task with
        WFD status to a task with HREV status and the status of the task will
        stay WFD
        """
        # create another dependency to make the task3 a WFD task
        self.test_task3.depends = []
        self.test_task9.status = self.status_wip
        self.assertEqual(self.test_task9.status, self.status_wip)
        self.test_task3.depends.append(self.test_task9)
        self.assertEqual(self.test_task3.status, self.status_wfd)
        # make a task with HREV status
        # create dependency
        self.test_task8.status = self.status_hrev
        self.assertEqual(self.test_task8.status, self.status_hrev)
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_leaf_WFD_task_updated_to_have_a_dependency_of_OH_task(self):
        """testing if it is possible to set a dependency between a task with
        WFD status to a task with OH status and the status of the task will
        stay WFD
        """
        # create another dependency to make the task3 a WFD task
        self.test_task3.depends = []
        self.test_task9.status = self.status_wip
        self.assertEqual(self.test_task9.status, self.status_wip)
        self.test_task3.depends.append(self.test_task9)
        self.assertEqual(self.test_task3.status, self.status_wfd)
        # make a task with HREV status
        # create dependency
        self.test_task8.status = self.status_oh
        self.assertEqual(self.test_task8.status, self.status_oh)
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_leaf_WFD_task_updated_to_have_a_dependency_of_STOP_task(self):
        """testing if it is possible to set a dependency between a task with
        WFD status to a task with STOP status and the status of the task status
        will stay WFD
        """
        # create another dependency to make the task3 a WFD task
        self.test_task3.depends = []
        self.test_task9.status = self.status_wip
        self.assertEqual(self.test_task9.status, self.status_wip)
        self.test_task3.depends.append(self.test_task9)
        self.assertEqual(self.test_task3.status, self.status_wfd)
        # make a task with HREV status
        # create dependency
        self.test_task8.status = self.status_stop
        self.assertEqual(self.test_task8.status, self.status_stop)
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_leaf_WFD_task_updated_to_have_a_dependency_of_CMPL_task(self):
        """testing if it is possible to set a dependency between a task with
        WFD status to a task with CMPL status and the status of the task status
        will stay to WFD
        """
        # create another dependency to make the task3 a WFD task
        self.test_task3.depends = []
        self.test_task9.status = self.status_wip
        self.assertEqual(self.test_task9.status, self.status_wip)
        self.test_task3.depends.append(self.test_task9)
        self.assertEqual(self.test_task3.status, self.status_wfd)
        # make a task with HREV status
        # create dependency
        self.test_task8.status = self.status_cmpl
        self.assertEqual(self.test_task8.status, self.status_cmpl)
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    # Leaf Tasks - dependency relation changes
    # RTS
    def test_leaf_RTS_task_updated_to_have_a_dependency_of_WFD_task_task(self):
        """testing if it is possible to set a dependency between a task with
        RTS status to a task with WFD status but the status of the task is
        updated from RTS to WFD
        """
        # find an RTS task
        self.test_task3.depends = []
        self.test_task3.status = self.status_rts
        self.assertEqual(self.test_task3.status, self.status_rts)
        # create dependency
        # make a task with WFD status
        self.test_task8.status = self.status_wfd
        self.assertEqual(self.test_task8.status, self.status_wfd)
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_leaf_RTS_task_updated_to_have_a_dependency_of_RTS_task(self):
        """testing if it is possible to set a dependency between a task with
        RTS status to a task with RTS status but the status of the task is
        updated from RTS to WFD
        """
        # find an RTS task
        self.test_task3.depends = []
        self.test_task3.status = self.status_rts
        self.assertEqual(self.test_task3.status, self.status_rts)
        # create dependency
        # make a task with RTS status
        self.test_task8.status = self.status_rts
        self.assertEqual(self.test_task8.status, self.status_rts)
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_leaf_RTS_task_updated_to_have_a_dependency_of_WIP_task(self):
        """testing if it is possible to set a dependency between a task with
        RTS status to a task with WIP status but the status of the task is
        updated from RTS to WFD
        """
        # find an RTS task
        self.test_task3.depends = []
        self.test_task3.status = self.status_rts
        self.assertEqual(self.test_task3.status, self.status_rts)
        # create dependency
        # make a task with WIP status
        self.test_task8.status = self.status_wip
        self.assertEqual(self.test_task8.status, self.status_wip)
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_leaf_RTS_task_updated_to_have_a_dependency_of_PREV_task(self):
        """testing if it is possible to set a dependency between a task with
        RTS status to a task with PREV status but the status of the task is
        updated from RTS to WFD
        """
        # find an RTS task
        self.test_task3.depends = []
        self.test_task3.status = self.status_rts
        self.assertEqual(self.test_task3.status, self.status_rts)
        # create dependency
        # make a task with PREV status
        self.test_task8.status = self.status_prev
        self.assertEqual(self.test_task8.status, self.status_prev)
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_leaf_RTS_task_updated_to_have_a_dependency_of_HREV_task(self):
        """testing if it is possible to set a dependency between a task with
        RTS status to a task with HREV status but the status of the task is
        updated from RTS to WFD
        """
        # find an RTS task
        self.test_task3.depends = []
        self.test_task3.status = self.status_rts
        self.assertEqual(self.test_task3.status, self.status_rts)
        # create dependency
        # make a task with HREV status
        self.test_task8.status = self.status_hrev
        self.assertEqual(self.test_task8.status, self.status_hrev)
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_leaf_RTS_task_updated_to_have_a_dependency_of_OH_task(self):
        """testing if it is possible to set a dependency between a task with
        RTS status to a task with OH status and the status of the task is
        updated from RTS to WFD
        """
        # find an RTS task
        self.test_task3.depends = []
        self.test_task3.status = self.status_rts
        self.assertEqual(self.test_task3.status, self.status_rts)
        # create dependency
        # make a task with OH status
        self.test_task8.status = self.status_oh
        self.assertEqual(self.test_task8.status, self.status_oh)
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_leaf_RTS_task_updated_to_have_a_dependency_of_STOP_task(self):
        """testing if it is possible to set a dependency between a task with
        RTS status to a task with STOP status and the status of the task will
        stay RTS as if the dependency is not there
        """
        # find an RTS task
        self.test_task3.depends = []
        self.test_task3.status = self.status_rts
        self.assertEqual(self.test_task3.status, self.status_rts)
        # create dependency
        # make a task with STOP status
        self.test_task8.status = self.status_stop
        self.assertEqual(self.test_task8.status, self.status_stop)
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_rts)

    def test_leaf_RTS_task_updated_to_have_a_dependency_of_CMPL_task(self):
        """testing if it is possible to set a dependency between a task with
        RTS status to a task with CMPL status and the status of the task will
        stay RTS
        """
        # find an RTS task
        self.assertEqual(self.test_task3.depends, [])
        self.test_task3.status = self.status_rts
        self.assertEqual(self.test_task3.status, self.status_rts)
        # create dependency
        # make a task with CMPL status
        self.test_task8.status = self.status_cmpl
        self.assertEqual(self.test_task8.status, self.status_cmpl)
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_rts)

    # Leaf Tasks - dependency changes
    # WIP - DREV - PREV - HREV - OH - STOP - CMPL
    def test_leaf_WIP_task_dependency_can_not_be_updated(self):
        """testing if it is not possible to update the dependencies of a WIP
        task
        """
        # find an WIP task
        self.test_task3.depends = []
        self.test_task3.status = self.status_wip
        self.assertEqual(self.test_task3.status, self.status_wip)
        # create dependency
        self.assertRaises(
            StatusError, self.test_task3.depends.append, self.test_task8
        )
        DBSession.rollback()

    def test_leaf_PREV_task_dependency_can_not_be_updated(self):
        """testing if it is not possible to update the dependencies of a PREV
        task
        """
        # find an PREV task
        self.test_task3.depends = []
        self.test_task3.status = self.status_prev
        self.assertEqual(self.test_task3.status, self.status_prev)
        # create dependency
        self.assertRaises(
            StatusError, self.test_task3.depends.append, self.test_task8
        )
        DBSession.rollback()

    def test_leaf_HREV_task_dependency_can_not_be_updated(self):
        """testing if it is not possible to update the dependencies of a HREV
        task
        """
        # find an HREV task
        self.test_task3.depends = []
        self.test_task3.status = self.status_hrev
        self.assertEqual(self.test_task3.status, self.status_hrev)
        # create dependency
        self.assertRaises(
            StatusError, self.test_task3.depends.append, self.test_task8
        )
        DBSession.rollback()

    def test_leaf_DREV_task_dependency_can_not_be_updated(self):
        """testing if it is not possible to update the dependencies of a DREV
        task
        """
        # find an DREV task
        self.test_task3.depends = []
        self.test_task3.status = self.status_drev
        self.assertEqual(self.test_task3.status, self.status_drev)
        # create dependency
        self.assertRaises(
            StatusError, self.test_task3.depends.append, self.test_task8
        )
        DBSession.rollback()

    def test_leaf_OH_task_dependency_can_not_be_updated(self):
        """testing if it is not possible to update the dependencies of a OH
        task
        """
        # find an OH task
        self.test_task3.depends = []
        self.test_task3.status = self.status_oh
        self.assertEqual(self.test_task3.status, self.status_oh)
        # create dependency
        self.assertRaises(
            StatusError, self.test_task3.depends.append, self.test_task8
        )
        DBSession.rollback()

    def test_leaf_STOP_task_dependency_can_not_be_updated(self):
        """testing if it is not possible to update the dependencies of a STOP
        task
        """
        # find an STOP task
        self.test_task3.depends = []
        self.test_task3.status = self.status_stop
        self.assertEqual(self.test_task3.status, self.status_stop)
        # create dependency
        self.assertRaises(
            StatusError, self.test_task3.depends.append, self.test_task8
        )
        DBSession.rollback()

    def test_leaf_CMPL_task_dependency_can_not_be_updated(self):
        """testing if it is not possible to update the dependencies of a CMPL
        task
        """
        # find an CMPL task
        self.test_task3.depends = []
        self.test_task3.status = self.status_cmpl
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        # create dependency
        self.assertRaises(
            StatusError, self.test_task3.depends.append, self.test_task8
        )
        DBSession.rollback()

    # dependencies of containers
    # container Tasks - dependency relation changes
    # RTS
    def test_container_RTS_task_updated_to_have_a_dependency_of_WFD_task_task(self):
        """testing if it is possible to set a dependency between an RTS
        container task to a WFD task but the status of the container task is
        updated from RTS to WFD
        """
        # make a task with WFD status
        self.test_task3.depends = []
        self.test_task8.status = self.status_wfd
        self.assertEqual(self.test_task8.status, self.status_wfd)
        # find a RTS container task
        self.test_task3.children.append(self.test_task2)
        self.test_task2.status = self.status_rts
        self.test_task3.status = self.status_rts
        self.assertEqual(self.test_task3.status, self.status_rts)
        # create dependency
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_container_RTS_task_updated_to_have_a_dependency_of_RTS_task(self):
        """testing if it is possible to set a dependency between an RTS
        container task to an RTS task but the status of the container task is
        updated from RTS to WFD
        """
        # make a task with WFD status
        self.test_task3.depends = []
        self.test_task8.status = self.status_rts
        self.assertEqual(self.test_task8.status, self.status_rts)
        # find a RTS container task
        self.test_task3.children.append(self.test_task2)
        self.test_task2.status = self.status_rts
        self.test_task3.status = self.status_rts
        self.assertEqual(self.test_task3.status, self.status_rts)
        # create dependency
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_container_RTS_task_updated_to_have_a_dependency_of_WIP_task(self):
        """testing if it is possible to set a dependency between an RTS
        container task to a WIP task but the status of the container task is
        updated from RTS to WFD
        """
        # make a task with WIP status
        self.test_task3.depends = []
        self.test_task8.status = self.status_wip
        self.assertEqual(self.test_task8.status, self.status_wip)
        # find a RTS container task
        self.test_task3.children.append(self.test_task2)
        self.test_task2.status = self.status_rts
        self.test_task3.status = self.status_rts
        self.assertEqual(self.test_task3.status, self.status_rts)
        # create dependency
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_container_RTS_task_updated_to_have_a_dependency_of_PREV_task(self):
        """testing if it is possible to set a dependency between an RTS
        container task to a PREV task but the status of the container task is
        updated from RTS to WFD
        """
        # make a task with PREV status
        self.test_task3.depends = []
        self.test_task8.status = self.status_prev
        self.assertEqual(self.test_task8.status, self.status_prev)
        # find a RTS container task
        self.test_task3.children.append(self.test_task2)
        self.test_task2.status = self.status_rts
        self.test_task3.status = self.status_rts
        self.assertEqual(self.test_task3.status, self.status_rts)
        # create dependency
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_container_RTS_task_updated_to_have_a_dependency_of_HREV_task(self):
        """testing if it is possible to set a dependency between an RTS
        container task to an HREV task but the status of the container task is
        updated from RTS to WFD
        """
        # make a task with HREV status
        self.test_task3.depends = []
        self.test_task8.status = self.status_hrev
        self.assertEqual(self.test_task8.status, self.status_hrev)
        # find a RTS container task
        self.test_task3.children.append(self.test_task2)
        self.test_task2.status = self.status_rts
        self.test_task3.status = self.status_rts
        self.assertEqual(self.test_task3.status, self.status_rts)
        # create dependency
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_container_RTS_task_updated_to_have_a_dependency_of_OH_task(self):
        """testing if it is possible to set a dependency between an RTS
        container task to an OH task but the status of the container task is
        updated from RTS to WFD
        """
        # make a task with OH status
        self.test_task3.depends = []
        self.test_task8.status = self.status_oh
        self.assertEqual(self.test_task8.status, self.status_oh)
        # find a RTS container task
        self.test_task3.children.append(self.test_task2)
        self.test_task2.status = self.status_rts
        self.test_task3.status = self.status_rts
        self.assertEqual(self.test_task3.status, self.status_rts)
        # create dependency
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_wfd)

    def test_container_RTS_task_updated_to_have_a_dependency_of_STOP_task(self):
        """testing if it is possible to set a dependency between an RTS
        container task to a STOP task and the status of the container task will
        stay RTS as if the dependency is not there
        """
        # make a task with STOP status
        self.test_task3.depends = []
        self.test_task8.status = self.status_stop
        self.assertEqual(self.test_task8.status, self.status_stop)
        # find a RTS container task
        self.test_task3.children.append(self.test_task2)
        self.test_task2.status = self.status_rts
        self.test_task3.status = self.status_rts
        self.assertEqual(self.test_task3.status, self.status_rts)
        # create dependency
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_rts)

    def test_container_RTS_task_updated_to_have_a_dependency_of_CMPL_task(self):
        """testing if it is possible to set a dependency between an RTS
        container task to a CMPL task and the status of the task will stay RTS
        """
        # make a task with CMPL status
        self.test_task3.depends = []
        self.test_task3.children.append(self.test_task6)

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()
        self.test_task8.create_time_log(
            resource=self.test_task8.resources[0],
            start=now,
            end=now + td(hours=1)
        )

        reviews = self.test_task8.request_review()
        for review in reviews:
            review.approve()

        self.assertEqual(self.test_task8.status, self.status_cmpl)

        # find a RTS container task
        self.assertEqual(self.test_task3.status, self.status_rts)

        # create dependency
        self.test_task3.depends.append(self.test_task8)
        self.assertEqual(self.test_task3.status, self.status_rts)

    # Container Tasks - dependency relation changes
    # WIP - DREV - PREV - HREV - OH - STOP - CMPL
    def test_container_WIP_task_dependency_can_not_be_updated(self):
        """testing if it is not possible to update the dependencies of a WIP
        container task
        """
        # find an WIP task
        self.test_task1.depends = []
        self.test_task1.status = self.status_wip
        self.assertEqual(self.test_task1.status, self.status_wip)
        # create dependency
        self.assertRaises(
            StatusError, self.test_task1.depends.append, self.test_task8
        )
        DBSession.rollback()

    def test_container_CMPL_task_dependency_can_not_be_updated(self):
        """testing if it is not possible to update the dependencies of a CMPL
        container task
        """
        # find an CMPL task
        self.test_task1.status = self.status_cmpl
        self.assertEqual(self.test_task1.status, self.status_cmpl)
        # create dependency
        with DBSession.no_autoflush:
            self.assertRaises(
                StatusError, self.test_task1.depends.append, self.test_task8
            )
        DBSession.rollback()

    #
    # Action Tests
    #

    # create_time_log
    # WFD
    def test_create_time_log_in_WFD_leaf_task(self):
        """testing if a StatusError will be raised when the the create_time_log
        actions is used in a WFD task
        """
        self.test_task3.status = self.status_wfd
        resource = self.test_task3.resources[0]
        start = datetime.datetime.now()
        end = datetime.datetime.now() + datetime.timedelta(hours=1)
        self.assertRaises(StatusError, self.test_task3.create_time_log,
                          resource, start, end)
        DBSession.rollback()

    # RTS: status updated to WIP
    def test_create_time_log_in_RTS_leaf_task_status_updated_to_WIP(self):
        """testing if the status of the RTS leaf task will be converted to WIP
        when create_time_log actions is used in an RTS task
        """
        self.test_task9.status = self.status_rts
        resource = self.test_task9.resources[0]
        start = datetime.datetime.now()
        end = datetime.datetime.now() + datetime.timedelta(hours=1)
        self.test_task9.create_time_log(resource, start, end)
        self.assertEqual(self.test_task9.status, self.status_wip)

    # RTS -> parent update
    def test_create_time_log_in_RTS_leaf_task_update_parent_status(self):
        """testing if the status of the parent of the RTS leaf task will be
        converted to WIP when create_time_log actions is used in an RTS task
        """
        self.test_task2.status = self.status_rts
        self.test_task8.status = self.status_rts

        self.assertEqual(
            self.test_task8.parent, self.test_task2
        )

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.test_task8.create_time_log(
            resource=self.test_task8.resources[0],
            start=now,
            end=now + td(hours=1)
        )

        self.assertEqual(self.test_task8.status, self.status_wip)
        self.assertEqual(self.test_task2.status, self.status_wip)

    # RTS -> root task no problem
    def test_create_time_log_in_RTS_root_task_no_parent_no_problem(self):
        """testing if RTS leaf task status will be converted to WIP when
        create_time_log actions is used in an RTS root task
        """
        self.test_task3.status = self.status_rts
        resource = self.test_task3.resources[0]
        start = datetime.datetime.now()
        end = datetime.datetime.now() + datetime.timedelta(hours=1)
        self.test_task3.create_time_log(resource, start, end)
        self.assertEqual(self.test_task3.status, self.status_wip)

    # WIP
    def test_create_time_log_in_WIP_leaf_task(self):
        """testing if there will be no problem when create_time_log is used
        in a WIP task, and the status will stay WIP
        """
        self.test_task9.status = self.status_wip
        resource = self.test_task9.resources[0]
        start = datetime.datetime.now()
        end = datetime.datetime.now() + datetime.timedelta(hours=1)
        self.test_task9.create_time_log(resource, start, end)
        self.assertEqual(self.test_task9.status, self.status_wip)

    # PREV
    def test_create_time_log_in_PREV_leaf_task(self):
        """testing if there will be no problem to call create_time_log for a
        PREV task and the status will stay PREV
        """
        self.test_task3.status = self.status_prev
        resource = self.test_task3.resources[0]
        start = datetime.datetime.now()
        end = datetime.datetime.now() + datetime.timedelta(hours=1)
        self.assertEqual(self.test_task3.status, self.status_prev)
        tlog = self.test_task3.create_time_log(resource, start, end)
        self.assertTrue(isinstance(tlog, TimeLog))
        self.assertEqual(self.test_task3.status, self.status_prev)

    # HREV
    def test_create_time_log_in_HREV_leaf_task(self):
        """testing if the status will be converted to WIP when create_time_log
        is used in a HREV task
        """
        self.test_task9.status = self.status_hrev
        resource = self.test_task9.resources[0]
        start = datetime.datetime.now()
        end = datetime.datetime.now() + datetime.timedelta(hours=1)
        self.test_task9.create_time_log(resource, start, end)
        self.assertEqual(self.test_task9.status, self.status_wip)

    # DREV
    def test_create_time_log_in_DREV_leaf_task(self):
        """testing if the status will stay DREV when create_time_log is used in
        a DREV task
        """
        self.test_task9.status = self.status_drev
        resource = self.test_task9.resources[0]
        start = datetime.datetime.now()
        end = datetime.datetime.now() + datetime.timedelta(hours=1)
        self.test_task9.create_time_log(resource, start, end)
        self.assertEqual(self.test_task9.status, self.status_drev)

    # OH
    def test_create_time_log_in_OH_leaf_task(self):
        """testing if a StatusError will be raised when the create_time_log
        actions is used in a OH task
        """
        self.test_task9.status = self.status_oh
        resource = self.test_task9.resources[0]
        start = datetime.datetime.now()
        end = datetime.datetime.now() + datetime.timedelta(hours=1)
        self.assertRaises(StatusError, self.test_task9.create_time_log,
                          resource, start, end)
        DBSession.rollback()

    # STOP
    def test_create_time_log_in_STOP_leaf_task(self):
        """testing if a StatusError will be raised when the create_time_log
        action is used in a STOP task
        """
        self.test_task9.status = self.status_stop
        resource = self.test_task9.resources[0]
        start = datetime.datetime.now()
        end = datetime.datetime.now() + datetime.timedelta(hours=1)
        self.assertRaises(StatusError, self.test_task9.create_time_log,
                          resource, start, end)
        DBSession.rollback()

    # CMPL
    def test_create_time_log_in_CMPL_leaf_task(self):
        """testing if a StatusError will be raised when the create_time_log
        action is used in a CMPL task
        """
        self.test_task9.status = self.status_cmpl
        resource = self.test_task9.resources[0]
        start = datetime.datetime.now()
        end = datetime.datetime.now() + datetime.timedelta(hours=1)
        with self.assertRaises(StatusError):
            self.test_task9.create_time_log(resource, start, end)
        DBSession.rollback()

    # On Container Task
    def test_create_time_log_on_container_task(self):
        """testing if a ValueError will be raised when the create_time_log
        action will be used in a container task
        """
        start = datetime.datetime.now()
        end = datetime.datetime.now() + datetime.timedelta(hours=1)
        self.assertRaises(ValueError, self.test_task2.create_time_log,
                          resource=None, start=start, end=end)

    def test_create_time_log_is_creating_time_logs(self):
        """testing if create_time_log action is really creating some time logs
        """
        # initial condition
        self.assertEqual(len(self.test_task3.time_logs), 0)

        now = datetime.datetime.now()
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now,
            end=now + datetime.timedelta(hours=1)
        )
        self.assertEqual(len(self.test_task3.time_logs), 1)
        self.assertEqual(self.test_task3.total_logged_seconds, 3600)

        now = datetime.datetime.now()
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now + datetime.timedelta(hours=1),
            end=now + datetime.timedelta(hours=2)
        )
        self.assertEqual(len(self.test_task3.time_logs), 2)
        self.assertEqual(self.test_task3.total_logged_seconds, 7200)

    def test_create_time_log_returns_time_log_instance(self):
        """testing if create_time_log returns a TimeLog instance
        """
        self.assertEqual(len(self.test_task3.time_logs), 0)

        now = datetime.datetime.now()
        tl = self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now,
            end=now + datetime.timedelta(hours=1)
        )
        self.assertTrue(isinstance(tl, TimeLog))

    # request_review
    # WFD
    def test_request_review_in_WFD_leaf_task(self):
        """testing if a StatusError will be raised when the request_review
        action is used in a WFD leaf task
        """
        self.test_task3.status = self.status_wfd
        self.assertRaises(StatusError, self.test_task3.request_review)
        DBSession.rollback()

    # RTS
    def test_request_review_in_RTS_leaf_task(self):
        """testing if a StatusError will be raised when the request_review
        action is used in a RTS leaf task
        """
        self.test_task3.status = self.status_rts
        self.assertRaises(StatusError, self.test_task3.request_review)
        DBSession.rollback()

    # WIP: status updated to PREV
    def test_request_review_in_WIP_leaf_task_status_updated_to_PREV(self):
        """testing if the status will be updated to PREV when the
        request_review action is used in a WIP leaf task
        """
        self.test_task3.status = self.status_wip
        self.test_task3.request_review()
        self.assertEqual(self.test_task3.status, self.status_prev)

    # WIP: review instances
    def test_request_review_in_WIP_leaf_task_review_instances(self):
        """testing if a review instance for each responsible will be returned
        when the request_review action is used in a WIP leaf task
        """
        from stalker import Review
        self.test_task3.responsible = [self.test_user1, self.test_user2]
        self.test_task3.status = self.status_wip
        reviews = self.test_task3.request_review()
        self.assertEqual(len(reviews), 2)
        self.assertTrue(isinstance(reviews[0], Review))
        self.assertTrue(isinstance(reviews[1], Review))

    # WIP: review instances review_number is correct
    def test_request_review_in_WIP_leaf_task_review_instances_review_number(self):
        """testing if the review_number attribute of the created Reviews are
        correctly set
        """
        self.test_task3.responsible = [self.test_user1, self.test_user2]
        self.test_task3.status = self.status_wip

        # request a review
        reviews = self.test_task3.request_review()
        review1 = reviews[0]
        review2 = reviews[1]
        self.assertEqual(review1.review_number, 1)
        self.assertEqual(review2.review_number, 1)

        # finalize reviews
        review1.approve()
        review2.approve()

        # request a revision
        review3 = self.test_task3.request_revision(
            reviewer=self.test_user1,
            description='some description',
            schedule_timing=1,
            schedule_unit='d'
        )

        # the new_review.revision number still should be 1
        self.assertEqual(
            review3.review_number, 2
        )

        # and then ask a review again
        self.test_task3.status = self.status_wip

        reviews = self.test_task3.request_review()
        self.assertEqual(reviews[0].review_number, 3)
        self.assertEqual(reviews[1].review_number, 3)

    # PREV
    def test_request_review_in_PREV_leaf_task(self):
        """testing if a StatusError will be raised when the request_review
        action is used in a PREV leaf task
        """
        self.test_task3.status = self.status_prev
        self.assertRaises(StatusError, self.test_task3.request_review)
        DBSession.rollback()

    # HREV
    def test_request_review_in_HREV_leaf_task(self):
        """testing if a StatusError will be raised when the request_review
        action is used in a HREV leaf task
        """
        self.test_task3.status = self.status_hrev
        self.assertRaises(StatusError, self.test_task3.request_review)
        DBSession.rollback()

    # DREV
    def test_request_review_in_DREV_leaf_task(self):
        """testing if a StatusError will be raised when the request_review
        action is used in a DREV leaf task
        """
        self.test_task3.status = self.status_drev
        self.assertRaises(StatusError, self.test_task3.request_review)
        DBSession.rollback()

    # OH
    def test_request_review_in_OH_leaf_task(self):
        """testing if a StatusError will be raised when the request_review
        action is used in a OH leaf task
        """
        self.test_task3.status = self.status_oh
        self.assertRaises(StatusError, self.test_task3.request_review)
        DBSession.rollback()

    # STOP
    def test_request_review_in_STOP_leaf_task(self):
        """testing if a StatusError will be raised when the request_review
        action is used in a STOP leaf task
        """
        self.test_task3.status = self.status_stop
        self.assertRaises(StatusError, self.test_task3.request_review)
        DBSession.rollback()

    # CMPL
    def test_request_review_in_CMPL_leaf_task(self):
        """testing if a StatusError will be raised when the request_review
        action is used in a CMPL leaf task
        """
        self.test_task3.status = self.status_cmpl
        self.assertRaises(StatusError, self.test_task3.request_review)
        DBSession.rollback()

    #request_revision
    #WFD
    def test_request_revision_in_WFD_leaf_task(self):
        """testing if a StatusError will be raised when the request_revision
        action is used in a WFD leaf task
        """
        self.test_task3.status = self.status_wfd
        self.assertRaises(StatusError, self.test_task3.request_revision)
        DBSession.rollback()

    #RTS
    def test_request_revision_in_RTS_leaf_task(self):
        """testing if a StatusError will be raised when the request_revision
        action is used in a RTS leaf task
        """
        self.test_task3.status = self.status_rts
        self.assertRaises(StatusError, self.test_task3.request_revision)
        DBSession.rollback()

    #WIP
    def test_request_revision_in_WIP_leaf_task(self):
        """testing if a StatusError will be raised when the request_revision
        action is used in a WIP leaf task
        """
        self.test_task3.status = self.status_wip
        self.assertRaises(StatusError, self.test_task3.request_revision)
        DBSession.rollback()

    #PREV: Status updated to HREV
    def test_request_revision_in_PREV_leaf_task_status_updated_to_HREV(self):
        """testing if a the status of the PREV leaf task will be converted to
        HREV when the request_revision action is used in a PREV leaf task
        """
        self.test_task3.status = self.status_prev

        reviewer=self.test_user1
        description = 'do something uleyn'
        schedule_timing = 4
        schedule_unit = 'h'

        self.test_task3.request_revision(
            reviewer=reviewer,
            description=description,
            schedule_timing=schedule_timing,
            schedule_unit=schedule_unit
        )
        self.assertEqual(self.test_task3.status, self.status_hrev)

    #PREV: Schedule info update
    def test_request_revision_in_PREV_leaf_task_timing_is_extended(self):
        """testing if the timing will be extended as stated in the action when
        the request_revision action is used in a PREV leaf task
        """
        self.test_task3.status = self.status_prev

        reviewer = self.test_user1
        description = 'do something uleyn'
        schedule_timing = 4
        schedule_unit = 'h'

        self.test_task3.request_revision(
            reviewer=reviewer,
            description=description,
            schedule_timing=schedule_timing,
            schedule_unit=schedule_unit
        )
        self.assertEqual(self.test_task3.schedule_timing, 10)
        self.assertEqual(self.test_task3.schedule_unit, 'd')

    #PREV: Schedule info update also consider RREV Reviews
    def test_request_revision_in_PREV_leaf_task_schedule_info_update_also_considers_other_RREV_reviews_with_same_review_number(self):
        """testing if the timing values are extended with the supplied values
        and also any RREV Review timings with the same revision number are
        included when the request_revision action is used in a PREV leaf task
        """
        # create a couple TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.test_task3.status = self.status_rts
        self.test_task3.responsible = [self.test_user1, self.test_user2]

        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now,
            end=now + td(hours=1)
        )
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        # check the status
        self.assertEqual(self.test_task3.status, self.status_wip)

        # first request a review
        reviews = self.test_task3.request_review()

        # only finalize the first review
        review1 = reviews[0]
        review2 = reviews[1]

        review1.request_revision(
            schedule_timing=6, schedule_unit='h', description=''
        )

        # now request_revision using the task
        review3 = self.test_task3.request_revision(
            reviewer=self.test_user1,
            description='do something uleyn',
            schedule_timing=4,
            schedule_unit='h'
        )
        self.assertEqual(
            len(self.test_task3.reviews), 2
        )

        # check if they are in the same review set
        self.assertEqual(
            review1.review_number, review3.review_number
        )

        # the final timing should be 12 hours
        self.assertEqual(self.test_task3.schedule_timing, 10)
        self.assertEqual(self.test_task3.schedule_unit, 'd')

    #PREV: Review instances statuses are updated
    def test_request_revision_in_PREV_leaf_task_review_instances_are_deleted(self):
        """testing if the NEW Review instances are deleted when the
        request_revision action is used in a PREV leaf task
        """
        self.test_task3.status = self.status_wip

        reviews = self.test_task3.request_review()
        review1 = reviews[0]
        review2 = reviews[1]

        self.assertEqual(review1.status, self.status_new)
        self.assertEqual(review2.status, self.status_new)

        review3 = self.test_task3.request_revision(
            reviewer=self.test_user2,
            description='some description',
            schedule_timing=4,
            schedule_unit='h'
        )

        # now check if the review instances are not in task3.reviews list
        # anymore
        self.assertFalse(review1 in self.test_task3.reviews)
        self.assertFalse(review2 in self.test_task3.reviews)
        self.assertTrue(review3 in self.test_task3.reviews)

    #PREV: Review instances statuses are updated
    def test_request_revision_in_PREV_leaf_task_new_review_instance_is_created(self):
        """testing if the statuses of review instances are correctly updated to
        RREV when the request_revision action is used in a PREV leaf task
        """
        self.test_task3.status = self.status_wip

        reviews = self.test_task3.request_review()
        new_review = self.test_task3.request_revision(
            reviewer=self.test_user2,
            description='some description',
            schedule_timing=1,
            schedule_unit='w'
        )
        from stalker import Review
        self.assertTrue(isinstance(new_review, Review))

    #HREV
    def test_request_revision_in_HREV_leaf_task(self):
        """testing if a StatusError will be raised when the request_revision
        action is used in a HREV leaf task
        """
        self.test_task3.status = self.status_hrev
        kw = {
            'reviewer': self.test_user1,
            'description': 'do something uleyn',
            'schedule_timing': 4,
            'schedule_unit': 'h'
        }
        self.assertRaises(StatusError, self.test_task3.request_revision, **kw)
        DBSession.rollback()

    #OH
    def test_request_revision_in_OH_leaf_task(self):
        """testing if a StatusError will be raised when the request_revision
        action is used in a OH leaf task
        """
        self.test_task3.status = self.status_oh
        kw = {
            'reviewer': self.test_user1,
            'description': 'do something uleyn',
            'schedule_timing': 4,
            'schedule_unit': 'h'
        }
        self.assertRaises(StatusError, self.test_task3.request_revision, **kw)
        DBSession.rollback()

    #STOP
    def test_request_revision_in_STOP_leaf_task(self):
        """testing if a StatusError will be raised when the request_revision
        action is used in a STOP leaf task
        """
        self.test_task3.status = self.status_stop
        kw = {
            'reviewer': self.test_user1,
            'description': 'do something uleyn',
            'schedule_timing': 4,
            'schedule_unit': 'h'
        }
        self.assertRaises(StatusError, self.test_task3.request_revision, **kw)
        DBSession.rollback()

    #CMPL: status update
    def test_request_revision_in_CMPL_leaf_task_status_updated_to_HREV(self):
        """testing if the status will be set to HREV and the timing values are
        extended with the supplied values when the request_revision action is
        used in a CMPL leaf task
        """
        self.test_task3.status = self.status_cmpl
        kw = {
            'reviewer': self.test_user1,
            'description': 'do something uleyn',
            'schedule_timing': 4,
            'schedule_unit': 'h'
        }
        review = self.test_task3.request_revision(**kw)
        self.assertEqual(self.test_task3.status, self.status_hrev)

    #CMPL: schedule info update
    def test_request_revision_in_CMPL_leaf_task_schedule_info_update(self):
        """testing if the timing values are extended with the supplied values
        when the request_revision action is used in a CMPL leaf task
        """
        # create a couple TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.test_task3.status = self.status_rts
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now,
            end=now + td(hours=1)
        )
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )
        self.assertEqual(self.test_task3.total_logged_seconds, 7200)

        reviews = self.test_task3.request_review()
        review1 = reviews[0]
        review2 = reviews[1]
        review1.approve()
        review2.approve()

        kw = {
            'reviewer': self.test_user1,
            'description': 'do something uleyn',
            'schedule_timing': 4,
            'schedule_unit': 'h'
        }
        self.test_task3.request_revision(**kw)
        self.assertEqual(self.test_task3.schedule_unit, 'h')
        self.assertEqual(self.test_task3.schedule_timing, 6)

    #CMPL: parent status update
    def test_request_revision_in_CMPL_leaf_task_parent_status_updated_to_WIP(self):
        """testing if the status of the parent will be set to WIP when the
        request_revision action is used in a CMPL leaf task
        """
        # create a couple TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.test_task9.status = self.status_rts
        TimeLog(
            task=self.test_task9,
            resource=self.test_task9.resources[0],
            start=now,
            end=now + td(hours=1)
        )
        TimeLog(
            task=self.test_task9,
            resource=self.test_task9.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        self.test_task9.status = self.status_cmpl
        self.test_asset1.status = self.status_cmpl

        kw = {
            'reviewer': self.test_user1,
            'description': 'do something uleyn',
            'schedule_timing': 4,
            'schedule_unit': 'h'
        }
        review = self.test_task9.request_revision(**kw)
        self.assertEqual(self.test_asset1.status, self.status_wip)

    #CMPL: dependent task status update RTS -> WFD
    def test_request_revision_in_CMPL_leaf_task_RTS_dependent_task_updated_to_WFD(self):
        """testing if the status of the dependent RTS task will be set to WFD
        when the request_revision action is used in a CMPL leaf task
        """
        # create a couple TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.test_task8.depends = [self.test_task9]
        self.test_task8.status = self.status_wfd

        self.test_task9.status = self.status_rts
        TimeLog(
            task=self.test_task9,
            resource=self.test_task9.resources[0],
            start=now,
            end=now + td(hours=1)
        )
        TimeLog(
            task=self.test_task9,
            resource=self.test_task9.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        self.test_task9.status = self.status_cmpl

        kw = {
            'reviewer': self.test_user1,
            'description': 'do something uleyn',
            'schedule_timing': 4,
            'schedule_unit': 'h',
        }
        review = self.test_task9.request_revision(**kw)
        self.assertEqual(self.test_task8.status, self.status_wfd)

    #CMPL: dependent task status update WIP -> DREV
    def test_request_revision_in_CMPL_leaf_task_WIP_dependent_task_updated_to_DREV(self):
        """testing if the status of the dependent WIP task will be set to DREV
        when the request_revision action is used in a CMPL leaf task
        """
        # create a couple TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.test_task8.depends = [self.test_task9]
        self.test_task8.status = self.status_wip

        self.test_task9.status = self.status_rts
        TimeLog(
            task=self.test_task9,
            resource=self.test_task9.resources[0],
            start=now,
            end=now + td(hours=1)
        )
        TimeLog(
            task=self.test_task9,
            resource=self.test_task9.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        self.test_task9.status = self.status_cmpl

        kw = {
            'reviewer': self.test_user1,
            'description': 'do something uleyn',
            'schedule_timing': 4,
            'schedule_unit': 'h'
        }
        review = self.test_task9.request_revision(**kw)
        self.assertEqual(self.test_task8.status, self.status_drev)

    #CMPL: dependent task status update CMPL -> DREV
    def test_request_revision_in_CMPL_leaf_task_CMPL_dependent_task_updated_to_DREV(self):
        """testing if the status of the dependent CMPL task will be set to DREV
        when the request_revision action is used in a CMPL leaf task
        """
        # create a couple TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.test_task8.depends = [self.test_task9]
        self.assertTrue(self.test_task9 in self.test_task8.depends)

        self.test_task9.status = self.status_rts
        self.test_task9.create_time_log(
            resource=self.test_task9.resources[0],
            start=now,
            end=now + td(hours=1)
        )
        self.test_task9.create_time_log(
            resource=self.test_task9.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        reviews = self.test_task9.request_review()
        for r in reviews:
            r.approve()
        self.assertEqual(self.test_task9.status, self.status_cmpl)
        self.assertEqual(self.test_task8.status, self.status_rts)

        self.test_task8.create_time_log(
            resource=self.test_task8.resources[0],
            start=now + td(hours=2),
            end=now + td(hours=3)
        )
        self.assertEqual(self.test_task8.status, self.status_wip)

        [r.approve() for r in self.test_task8.request_review()]
        self.assertEqual(self.test_task8.status, self.status_cmpl)

        kw = {
            'reviewer': self.test_user1,
            'description': 'do something uleyn',
            'schedule_timing': 4,
            'schedule_unit': 'h'
        }
        self.test_task9.request_revision(**kw)

        self.assertEqual(self.test_task9.status, self.status_hrev)
        self.assertEqual(self.test_task8.status, self.status_drev)

    #CMPL: dependent task dependency_target update CMPL -> DREV
    def test_request_revision_in_CMPL_leaf_task_CMPL_dependent_task_dependency_target_updated_to_onstart(self):
        """testing if the dependency_target attribute of the TaskDependency
        object between the revised task and the dependent CMPL task will be set
        to 'onstart' when the request_revision action is used in a CMPL leaf
        task
        """
        # create a couple of TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        # remove any TaskDependency instances
        from stalker import TaskDependency
        for i in TaskDependency.query.all():
            db.DBSession.delete(i)

        db.DBSession.commit()

        self.test_task3.depends = [self.test_task9]  # will be PREV
        self.test_task4.depends = [self.test_task9]  # will be HREV
        self.test_task5.depends = [self.test_task9]  # will be STOP
        self.test_task6.depends = [self.test_task9]  # will be OH
        self.test_task8.depends = [self.test_task9]  # will be DREV
        self.assertTrue(self.test_task9 in self.test_task5.depends)
        self.assertTrue(self.test_task9 in self.test_task6.depends)
        self.assertTrue(self.test_task9 in self.test_task8.depends)

        self.test_task9.status = self.status_rts
        self.test_task9.create_time_log(
            resource=self.test_task9.resources[0],
            start=now,
            end=now + td(hours=1)
        )
        self.test_task9.create_time_log(
            resource=self.test_task9.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        reviews = self.test_task9.request_review()
        for r in reviews:
            r.approve()
        self.assertEqual(self.test_task9.status, self.status_cmpl)
        self.assertEqual(self.test_task8.status, self.status_rts)

        self.test_task8.create_time_log(
            resource=self.test_task8.resources[0],
            start=now + td(hours=2),
            end=now + td(hours=3)
        )
        self.assertEqual(self.test_task8.status, self.status_wip)

        [r.approve() for r in self.test_task8.request_review()]
        self.assertEqual(self.test_task8.status, self.status_cmpl)

        # now work on task5
        self.test_task5.create_time_log(
            resource=self.test_task5.resources[0],
            start=now + td(hours=3),
            end=now + td(hours=4)
        )
        self.assertEqual(self.test_task5.status, self.status_wip)
        self.test_task5.hold()
        self.assertEqual(self.test_task5.status, self.status_oh)

        # now work on task6
        self.test_task6.create_time_log(
            resource=self.test_task6.resources[0],
            start=now + td(hours=4),
            end=now + td(hours=5)
        )
        self.assertEqual(self.test_task6.status, self.status_wip)
        self.test_task6.stop()
        self.assertEqual(self.test_task6.status, self.status_stop)

        # now work on task3
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now + td(hours=5),
            end=now + td(hours=6)
        )
        self.assertEqual(self.test_task3.status, self.status_wip)
        self.test_task3.request_review()
        self.assertEqual(self.test_task3.status, self.status_prev)

        # now work on task4
        self.test_task4.create_time_log(
            resource=self.test_task4.resources[0],
            start=now + td(hours=6),
            end=now + td(hours=7)
        )
        self.assertEqual(self.test_task4.status, self.status_wip)
        reviews = self.test_task4.request_review()
        DBSession.add_all(reviews)
        DBSession.commit()
        self.data_created.extend(reviews)

        self.assertEqual(self.test_task4.status, self.status_prev)
        for r in reviews:
            r.request_revision(
                schedule_timing=1,
                schedule_unit='h'
            )
        self.assertEqual(self.test_task4.status, self.status_hrev)

        kw = {
            'reviewer': self.test_user1,
            'description': 'do something uleyn',
            'schedule_timing': 4,
            'schedule_unit': 'h'
        }
        self.test_task9.request_revision(**kw)

        from stalker import TaskDependency
        tdep_t3 = TaskDependency.query\
            .filter_by(task=self.test_task3)\
            .filter_by(depends_to=self.test_task9)\
            .first()
        tdep_t4 = TaskDependency.query\
            .filter_by(task=self.test_task4)\
            .filter_by(depends_to=self.test_task9)\
            .first()
        tdep_t5 = TaskDependency.query\
            .filter_by(task=self.test_task5)\
            .filter_by(depends_to=self.test_task9)\
            .first()
        tdep_t6 = TaskDependency.query\
            .filter_by(task=self.test_task6)\
            .filter_by(depends_to=self.test_task9)\
            .first()
        tdep_t8 = TaskDependency.query\
            .filter_by(task=self.test_task8)\
            .filter_by(depends_to=self.test_task9)\
            .first()
        self.assertTrue(tdep_t3 is not None)
        self.assertTrue(tdep_t4 is not None)
        self.assertTrue(tdep_t5 is not None)
        self.assertTrue(tdep_t6 is not None)
        self.assertTrue(tdep_t8 is not None)
        self.assertEqual(tdep_t3.dependency_target, 'onstart')
        self.assertEqual(tdep_t4.dependency_target, 'onstart')
        self.assertEqual(tdep_t5.dependency_target, 'onstart')
        self.assertEqual(tdep_t6.dependency_target, 'onstart')
        self.assertEqual(tdep_t8.dependency_target, 'onstart')

    #CMPL: dependent task parent status updated to WIP
    def test_request_revision_in_CMPL_leaf_task_dependent_task_parent_status_updated_to_WIP(self):
        """testing if the status of the dependent task parent updated to WIP
        when the request_revision action is used in a CMPL leaf task
        """
        # create a couple TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.test_task9.depends = [self.test_task8]
        self.test_task9.status = self.status_wfd
        self.test_asset1.status = self.status_wfd
        self.test_task8.status = self.status_rts

        self.test_task8.create_time_log(
            resource=self.test_task8.resources[0],
            start=now,
            end=now + td(hours=1)
        )
        self.test_task8.create_time_log(
            resource=self.test_task8.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        self.test_task8.status = self.status_cmpl
        self.test_task9.status = self.status_cmpl
        self.test_asset1.status = self.status_cmpl
        self.test_task7.status = self.status_cmpl

        kw = {
            'reviewer': self.test_user1,
            'description': 'do something uleyn',
            'schedule_timing': 4,
            'schedule_unit': 'h'
        }
        review = self.test_task8.request_revision(**kw)

        self.assertEqual(self.test_task9.status, self.status_drev)
        self.assertEqual(self.test_asset1.status, self.status_wip)
        self.assertEqual(self.test_task7.status, self.status_wip)

    def test_request_revision_in_deeper_dependency_setup(self):
        """testing if all of the dependent task statuses are updated to DREV
        properly
        """
        # create a couple TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        # remove any TaskDependency instances
        from stalker import TaskDependency
        for i in TaskDependency.query.all():
            db.DBSession.delete(i)

        db.DBSession.commit()

        self.test_task5.depends = []
        self.test_task6.depends = [self.test_task5]
        self.test_task3.depends = [self.test_task6]
        self.test_task8.depends = [self.test_task3]
        self.test_task9.depends = [self.test_task8]

        self.test_task5.update_status_with_dependent_statuses()
        self.test_task6.update_status_with_dependent_statuses()
        self.test_task3.update_status_with_dependent_statuses()
        self.test_task8.update_status_with_dependent_statuses()
        self.test_task9.update_status_with_dependent_statuses()

        self.assertEqual(self.test_task5.status, self.status_rts)
        self.assertEqual(self.test_task6.status, self.status_wfd)
        self.assertEqual(self.test_task3.status, self.status_wfd)
        self.assertEqual(self.test_task3.status, self.status_wfd)
        self.assertEqual(self.test_task3.status, self.status_wfd)
        db.DBSession.commit()

        # complete each of them first
        # test_task5
        self.test_task5.create_time_log(
            self.test_task5.resources[0],
            now - td(hours=1),
            now
        )
        self.test_task5.schedule_timing = 1
        self.test_task5.schedule_unit = 'h'
        self.test_task5.status = self.status_cmpl

        # test_task6
        self.test_task6.status = self.status_rts
        self.test_task6.create_time_log(
            self.test_task6.resources[0],
            now,
            now + td(hours=1)
        )
        self.test_task6.schedule_timing = 1
        self.test_task6.schedule_unit = 'h'
        self.test_task6.status = self.status_cmpl

        # test_task3
        self.test_task3.status = self.status_rts
        self.test_task3.create_time_log(
            self.test_task3.resources[0],
            now + td(hours=1),
            now + td(hours=2)
        )
        self.test_task3.schedule_timing = 1
        self.test_task3.schedule_unit = 'h'
        self.test_task3.status = self.status_cmpl

        # test_task8
        self.test_task8.status = self.status_rts
        self.test_task8.create_time_log(
            self.test_task8.resources[0],
            now + td(hours=2),
            now + td(hours=3)
        )
        self.test_task8.schedule_timing = 1
        self.test_task8.schedule_unit = 'h'
        self.test_task8.status = self.status_cmpl

        # test_task9
        self.test_task9.status = self.status_rts
        self.test_task9.create_time_log(
            self.test_task9.resources[0],
            now + td(hours=3),
            now + td(hours=4)
        )
        self.test_task9.schedule_timing = 1
        self.test_task9.schedule_unit = 'h'
        self.test_task9.status = self.status_cmpl

        # now request a revision to the first task (test_task6)
        # and expect all of the task dependency targets to be turned
        # in to "onstart"
        self.test_task6.request_revision(
            self.test_user1
        )

        self.assertEqual(
            self.test_task6.task_depends_to[0].dependency_target, 'onend'
        )
        self.assertEqual(
            self.test_task3.task_depends_to[0].dependency_target, 'onstart'
        )
        self.assertEqual(
            self.test_task8.task_depends_to[0].dependency_target, 'onstart'
        )
        self.assertEqual(
            self.test_task9.task_depends_to[0].dependency_target, 'onstart'
        )


    # hold
    # WFD
    def test_hold_in_WFD_leaf_task(self):
        """testing if a StatusError will be raised when the hold action is used
        in a WFD leaf task
        """
        self.test_task3.status = self.status_wfd
        self.assertRaises(StatusError, self.test_task3.hold)

    # RTS
    def test_hold_in_RTS_leaf_task(self):
        """testing if a StatusError will be raised when the hold action is used
        in a RTS leaf task
        """
        self.test_task3.status = self.status_rts
        self.assertRaises(StatusError, self.test_task3.hold)
        DBSession.rollback()

    # WIP: Status updated to OH
    def test_hold_in_WIP_leaf_task_status(self):
        """testing if the status will be updated to OH when the hold action is
        used in a WIP leaf task
        """
        self.test_task3.status = self.status_wip
        self.test_task3.hold()
        self.assertEqual(self.test_task3.status, self.status_oh)

    # WIP: Schedule values are intact
    def test_hold_in_WIP_leaf_task_schedule_values(self):
        """testing if the schedule values will be intact when the hold action
        is used in a WIP leaf task
        """
        self.test_task3.status = self.status_wip
        self.test_task3.hold()
        self.assertEqual(self.test_task3.schedule_timing, 10)
        self.assertEqual(self.test_task3.schedule_unit, 'd')

    # WIP: Priority is set to 0
    def test_hold_in_WIP_leaf_task(self):
        """testing if the priority will be set to 0 when the hold action is
        used in a WIP leaf task
        """
        self.test_task3.status = self.status_wip
        self.test_task3.hold()
        self.assertEqual(self.test_task3.priority, 0)

    # PREV
    def test_hold_in_PREV_leaf_task(self):
        """testing if a StatusError will be raised when the hold action is used
        in a PREV leaf task
        """
        self.test_task3.status = self.status_prev
        self.assertRaises(StatusError, self.test_task3.hold)
        DBSession.rollback()

    # HREV
    def test_hold_in_HREV_leaf_task(self):
        """testing if a StatusError will be raised when the hold action is used
        in a HREV leaf task
        """
        self.test_task3.status = self.status_hrev
        self.assertRaises(StatusError, self.test_task3.hold)
        DBSession.rollback()

    # DREV: Status updated to OH
    def test_hold_in_DREV_leaf_task_status_updated_to_OH(self):
        """testing if the status will be updated to OH when the hold action is
        used in a DREV leaf task
        """
        self.test_task3.status = self.status_drev
        self.test_task3.hold()
        self.assertEqual(self.test_task3.status, self.status_oh)

    # DREV: Schedule values are intact
    def test_hold_in_DREV_leaf_task_schedule_values_are_intact(self):
        """testing if the schedule values will be intact when the hold action
        is used in a DREV leaf task
        """
        self.test_task3.status = self.status_drev
        self.test_task3.hold()
        self.assertEqual(self.test_task3.schedule_timing, 10)
        self.assertEqual(self.test_task3.schedule_unit, 'd')

    # DREV: Priority is set to 0
    def test_hold_in_DREV_leaf_task_priority_set_to_0(self):
        """testing if the priority will be set to 0 when the hold action is
        used in a DREV leaf task
        """
        self.test_task3.status = self.status_drev
        self.test_task3.hold()
        self.assertEqual(self.test_task3.priority, 0)

    # OH
    def test_hold_in_OH_leaf_task(self):
        """testing if the status will stay on OH when the hold action is used
        in a OH leaf task
        """
        self.test_task3.status = self.status_oh
        self.test_task3.hold()
        self.assertEqual(self.test_task3.status, self.status_oh)

    # STOP
    def test_hold_in_STOP_leaf_task(self):
        """testing if a StatusError will be raised when the hold action is used
        in a STOP leaf task
        """
        self.test_task3.status = self.status_stop
        self.assertRaises(StatusError, self.test_task3.hold)
        DBSession.rollback()

    # CMPL
    def test_hold_in_CMPL_leaf_task(self):
        """testing if a StatusError will be raised when the hold action is used
        in a CMPL leaf task
        """
        self.test_task3.status = self.status_cmpl
        self.assertRaises(StatusError, self.test_task3.hold)
        DBSession.rollback()

    # stop
    # WFD
    def test_stop_in_WFD_leaf_task(self):
        """testing if a StatusError will be raised when the stop action is used
        in a WFD leaf task
        """
        self.test_task3.status = self.status_wfd
        self.assertRaises(StatusError, self.test_task3.stop)
        DBSession.rollback()

    # RTS
    def test_stop_in_RTS_leaf_task(self):
        """testing if a StatusError will be raised when the stop action is used
        in a RTS leaf task
        """
        self.test_task3.status = self.status_rts
        self.assertRaises(StatusError, self.test_task3.stop)
        DBSession.rollback()

    # WIP: Status Test
    def test_stop_in_WIP_leaf_task_status_is_updated_to_STOP(self):
        """testing if a status will be updated to STOP when the stop action is
        used in a WIP leaf task
        """
        self.test_task3.status = self.status_wip
        self.test_task3.hold()
        self.assertEqual(self.test_task3.status, self.status_oh)

    # WIP: Schedule Timing Test
    def test_stop_in_WIP_leaf_task_schedule_values_clamped(self):
        """testing if the schedule values will be clamped to the current
        total_logged_seconds when the stop action is used in a WIP leaf task
        """
        # create a couple TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.test_task8.status = self.status_rts
        TimeLog(
            task=self.test_task8,
            resource=self.test_task8.resources[0],
            start=now,
            end=now + td(hours=1)
        )
        TimeLog(
            task=self.test_task8,
            resource=self.test_task8.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )
        self.test_task8.status = self.status_wip
        self.test_task8.stop()
        self.assertEqual(self.test_task8.schedule_timing, 2)
        self.assertEqual(self.test_task8.schedule_unit, 'h')

    # WIP: Dependency Status: WFD -> RTS
    def test_stop_in_WIP_leaf_task_dependent_task_status_updated_from_WFD_to_RTS(self):
        """testing if the dependent task status updated from WFD to RTS when
        the stop action is used in a WIP leaf task
        """
        # create a couple TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.test_task9.status = self.status_rts
        self.test_task8.status = self.status_rts

        self.test_task9.depends = [self.test_task8]

        TimeLog(
            task=self.test_task8,
            resource=self.test_task8.resources[0],
            start=now,
            end=now + td(hours=1)
        )
        TimeLog(
            task=self.test_task8,
            resource=self.test_task8.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )
        self.test_task8.status = self.status_wip
        self.test_task8.stop()
        self.assertEqual(self.test_task9.status, self.status_rts)

    # WIP: Dependency Status: DREV -> WIP
    def test_stop_in_WIP_leaf_task_status_from_DREV_to_HREV(self):
        """testing if the dependent task status updated from DREV to HREV when
        the stop action is used in a WIP leaf task
        """
        # create a couple TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.test_task9.status = self.status_rts
        self.test_task8.status = self.status_cmpl

        self.test_task9.depends = [self.test_task8]

        TimeLog(
            task=self.test_task9,
            resource=self.test_task9.resources[0],
            start=now,
            end=now + td(hours=1)
        )
        TimeLog(
            task=self.test_task9,
            resource=self.test_task9.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )
        self.test_task9.status = self.status_wip

        self.test_task8.status = self.status_hrev
        self.test_task9.status = self.status_drev

        TimeLog(
            task=self.test_task8,
            resource=self.test_task8.resources[0],
            start=now + td(hours=2),
            end=now + td(hours=3)
        )
        TimeLog(
            task=self.test_task8,
            resource=self.test_task8.resources[0],
            start=now + td(hours=4),
            end=now + td(hours=5)
        )

        self.test_task8.status = self.status_wip
        self.test_task8.stop()
        self.assertEqual(self.test_task9.status, self.status_hrev)

    # WIP: parent statuses
    def test_stop_in_DREV_leaf_task_check_parent_status(self):
        """testing if the parent status is updated correctly when the stop
        action is used in a DREV leaf task
        """
        # create a couple TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        TimeLog(
            task=self.test_task9,
            resource=self.test_task9.resources[0],
            start=now,
            end=now + td(hours=1)
        )
        TimeLog(
            task=self.test_task8,
            resource=self.test_task9.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        self.test_task9.status = self.status_drev
        self.test_task9.stop()
        self.assertEqual(self.test_task9.status, self.status_stop)
        self.assertEqual(self.test_asset1.status, self.status_cmpl)

    # PREV
    def test_stop_in_PREV_leaf_task(self):
        """testing if a StatusError will be raised when the stop action is used
        in a PREV leaf task
        """
        self.test_task3.status = self.status_prev
        self.assertRaises(StatusError, self.test_task3.stop)
        DBSession.rollback()

    # HREV
    def test_stop_in_HREV_leaf_task(self):
        """testing if a StatusError will be raised when the stop action is used
        in a HREV leaf task
        """
        self.test_task3.status = self.status_hrev
        self.assertRaises(StatusError, self.test_task3.stop)
        DBSession.rollback()

    # DREV: Status Test
    def test_stop_in_DREV_leaf_task_status_is_updated_to_STOP(self):
        """testing if the status will be set to STOP when the stop action is
        used in a DREV leaf task
        """
        self.test_task3.status = self.status_drev
        self.test_task3.stop()
        self.assertEquals(self.test_task3.status, self.status_stop)

    # DREV: Schedule Timing Test
    def test_stop_in_DREV_leaf_task_schedule_values_are_clamped(self):
        """testing if the schedule timing value will be clamped to the current
        time logs when the stop action is used in a DREV leaf task
        """
        # create a couple TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.test_task8.status = self.status_rts
        TimeLog(
            task=self.test_task8,
            resource=self.test_task8.resources[0],
            start=now,
            end=now + td(hours=2)
        )
        TimeLog(
            task=self.test_task8,
            resource=self.test_task8.resources[0],
            start=now + td(hours=2),
            end=now + td(hours=4)
        )
        self.test_task8.status = self.status_drev
        self.test_task8.stop()
        self.assertEqual(self.test_task8.schedule_timing, 4)
        self.assertEqual(self.test_task8.schedule_unit, 'h')

    # DREV: parent statuses
    def test_stop_in_DREV_leaf_task_parent_status(self):
        """testing if the parent status is updated correctly when the stop
        action is used in a DREV leaf task
        """
        # create a couple TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        TimeLog(
            task=self.test_task9,
            resource=self.test_task9.resources[0],
            start=now,
            end=now + td(hours=1)
        )
        TimeLog(
            task=self.test_task8,
            resource=self.test_task9.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        self.test_task9.status = self.status_wip
        self.test_task9.stop()
        self.assertEqual(self.test_task9.status, self.status_stop)
        self.assertEqual(self.test_asset1.status, self.status_cmpl)

    # DREV: Dependency Status: WFD -> RTS
    def test_stop_in_DREV_leaf_task_dependent_task_status_updated_from_WFD_to_RTS(self):
        """testing if the dependent task statuses are updated correctly when
        the stop action is used in a DREV leaf task
        """
        # create a couple TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.test_task9.status = self.status_rts
        self.test_task8.status = self.status_rts

        self.test_task9.depends = [self.test_task8]

        TimeLog(
            task=self.test_task8,
            resource=self.test_task8.resources[0],
            start=now,
            end=now + td(hours=1)
        )
        TimeLog(
            task=self.test_task8,
            resource=self.test_task8.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )
        self.test_task8.status = self.status_wip
        self.test_task8.stop()
        self.assertEqual(self.test_task9.status, self.status_rts)

    # DREV: Dependency Status: DREV -> WIP
    def test_stop_in_DREV_leaf_task_dependent_task_status_updated_from_DREV_to_HREV(self):
        """testing if the dependent task statuses are updated correctly when
        the stop action is used in a DREV leaf task
        """
        # create a couple TimeLogs
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        self.test_task9.status = self.status_rts
        self.test_task8.status = self.status_rts

        self.test_task9.depends = [self.test_task8]
        self.test_task9.status = self.status_drev  # this will be set by an
                                                   # action in normal run
        TimeLog(
            task=self.test_task8,
            resource=self.test_task8.resources[0],
            start=now,
            end=now + td(hours=1)
        )
        TimeLog(
            task=self.test_task8,
            resource=self.test_task8.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )
        self.test_task8.status = self.status_wip
        self.test_task8.stop()
        self.assertEqual(self.test_task9.status, self.status_hrev)

    # OH
    def test_stop_in_OH_leaf_task(self):
        """testing if a StatusError will be raised when the stop action is used
        in a OH leaf task
        """
        self.test_task3.status = self.status_oh
        self.assertRaises(StatusError, self.test_task3.stop)
        DBSession.rollback()

    # STOP
    def test_stop_in_STOP_leaf_task(self):
        """testing if the status will stay on STOP when the stop action is used
        in a STOP leaf task
        """
        self.test_task3.status = self.status_stop
        self.test_task3.stop()
        self.assertEquals(self.test_task3.status, self.status_stop)

    # CMPL
    def test_stop_in_CMPL_leaf_task(self):
        """testing if a StatusError will be raised when the stop action is used
        in a CMPL leaf task
        """
        self.test_task3.status = self.status_cmpl
        self.assertRaises(StatusError, self.test_task3.stop)
        DBSession.rollback()

    # resume
    # WFD
    def test_resume_in_WFD_leaf_task(self):
        """testing if a StatusError will be raised when the resume action is
        used in a WFD leaf task
        """
        self.test_task3.status = self.status_wfd
        self.assertRaises(StatusError, self.test_task3.resume)
        DBSession.rollback()

    # RTS
    def test_resume_in_RTS_leaf_task(self):
        """testing if a StatusError will be raised when the resume action is
        used in a RTS leaf task
        """
        self.test_task3.status = self.status_rts
        self.assertRaises(StatusError, self.test_task3.resume)
        DBSession.rollback()

    # WIP
    def test_resume_in_WIP_leaf_task(self):
        """testing if a StatusError will be raised when the resume action is
        used in a WIP leaf task
        """
        self.test_task3.status = self.status_wip
        self.assertRaises(StatusError, self.test_task3.resume)
        DBSession.rollback()

    # PREV
    def test_resume_in_PREV_leaf_task(self):
        """testing if a StatusError will be raised when the resume action is
        used in a PREV leaf task
        """
        self.test_task3.status = self.status_prev
        self.assertRaises(StatusError, self.test_task3.resume)
        DBSession.rollback()

    # HREV
    def test_resume_in_HREV_leaf_task(self):
        """testing if a StatusError will be raised when the resume action is
        used in a HREV leaf task
        """
        self.test_task3.status = self.status_hrev
        self.assertRaises(StatusError, self.test_task3.resume)
        DBSession.rollback()

    # DREV
    def test_resume_in_DREV_leaf_task(self):
        """testing if a StatusError will be raised when the resume action is
        used in a DREV leaf task
        """
        self.test_task3.status = self.status_drev
        self.assertRaises(StatusError, self.test_task3.resume)
        DBSession.rollback()

    # OH: no dependency -> WIP
    def test_resume_in_OH_leaf_task_with_no_dependencies(self):
        """testing if the status will be updated to WIP when the resume action
        is used in a OH leaf task with no dependencies
        """
        self.test_task3.status = self.status_oh
        self.test_task3.depends = []
        self.test_task3.resume()
        # no time logs so it will return back to rts
        # the test is wrong in the first place (no way to turn a task with no
        # time logs in to a OH task),
        # but checks a situation that the system needs to be more robust
        self.assertEqual(self.test_task3.status, self.status_rts)

    # OH: WIP dependencies -> DREV
    def test_resume_in_OH_leaf_task_with_WIP_dependencies(self):
        """testing if the status will be updated to DREV when the resume action
        is used in a OH leaf task with WIP dependencies
        """
        self.test_task3.status = self.status_rts
        self.test_task9.status = self.status_rts
        self.test_task9.depends = [self.test_task3]

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_rts)
        self.assertEqual(self.test_task9.status, self.status_wfd)

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        # start working on task3
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now,
            end=now + td(hours=1)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_wip)
        self.assertEqual(self.test_task9.status, self.status_wfd)

        # complete task3
        reviews = self.test_task3.request_review()
        for r in reviews:
            r.approve()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_rts)

        # start working on task9
        self.test_task9.create_time_log(
            resource=self.test_task9.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_wip)

        # hold task9
        self.test_task9.hold()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_oh)

        # request a revision to task3
        self.test_task3.request_revision(
            reviewer=self.test_user1
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_hrev)
        self.assertEqual(self.test_task9.status, self.status_oh)

        # now continue working on task3
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now + td(hours=2),
            end=now + td(hours=3)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_wip)
        self.assertEqual(self.test_task9.status, self.status_oh)

        # now resume task9
        self.test_task9.resume()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_wip)
        self.assertEqual(self.test_task9.status, self.status_drev)

    # OH: HREV dependencies -> DREV
    def test_resume_in_OH_leaf_task_with_HREV_dependencies(self):
        """testing if the status will be updated to DREV when the resume action
        is used in a OH leaf task with HREV dependencies
        """
        self.test_task3.status = self.status_rts
        self.test_task9.status = self.status_rts
        self.test_task9.depends = [self.test_task3]

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now,
            end=now + td(hours=1)
        )

        reviews = self.test_task3.request_review()
        for r in reviews:
            r.approve()

        # task3 should be cmpl
        self.assertEqual(self.test_task3.status, self.status_cmpl)

        # start working on task9
        self.test_task9.create_time_log(
            resource=self.test_task9.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        # now continue working on test_task3
        self.test_task3.request_revision(
            reviewer=self.test_task3.resources[0]
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_hrev)
        self.assertEqual(self.test_task9.status, self.status_drev)

        # hold task9
        self.test_task9.hold()
        self.assertEqual(self.test_task9.status, self.status_oh)

        # resume task9
        self.test_task9.resume()
        self.assertEqual(self.test_task9.status, self.status_drev)

    # OH: PREV dependencies -> DREV
    def test_resume_in_OH_leaf_task_with_PREV_dependencies(self):
        """testing if the status will be updated to DREV when the resume action
        is used in a OH leaf task with PREV dependencies
        """
        self.test_task3.status = self.status_rts
        self.test_task9.status = self.status_rts
        self.test_task9.depends = [self.test_task3]

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_rts)
        self.assertEqual(self.test_task9.status, self.status_wfd)

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        # start working on task3
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now,
            end=now + td(hours=1)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_wip)
        self.assertEqual(self.test_task9.status, self.status_wfd)

        # complete task3
        reviews = self.test_task3.request_review()
        for r in reviews:
            r.approve()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_rts)

        # start working on task9
        self.test_task9.create_time_log(
            resource=self.test_task9.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_wip)

        # hold task9
        self.test_task9.hold()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_oh)

        # request a revision to task3
        self.test_task3.request_revision(
            reviewer=self.test_user1
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_hrev)
        self.assertEqual(self.test_task9.status, self.status_oh)

        # now continue working on task3
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now + td(hours=2),
            end=now + td(hours=3)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_wip)
        self.assertEqual(self.test_task9.status, self.status_oh)

        # request a review for task3
        self.test_task3.request_review()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_prev)
        self.assertEqual(self.test_task9.status, self.status_oh)

        # now resume task9
        self.test_task9.resume()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_prev)
        self.assertEqual(self.test_task9.status, self.status_drev)

    # OH: DREV dependencies -> DREV
    def test_resume_in_OH_leaf_task_with_DREV_dependencies(self):
        """testing if the status will be updated to DREV when the resume action
        is used in a OH leaf task with DREV dependencies
        """
        self.test_task6.status = self.status_rts
        self.test_task3.status = self.status_rts
        self.test_task9.status = self.status_rts
        self.test_task9.depends = [self.test_task3]
        self.test_task3.depends = [self.test_task6]

        # check statuses
        self.assertEqual(self.test_task6.status, self.status_rts)
        self.assertEqual(self.test_task3.status, self.status_wfd)
        self.assertEqual(self.test_task9.status, self.status_wfd)

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()
        self.test_task6.create_time_log(
            resource=self.test_task6.resources[0],
            start=now,
            end=now + td(hours=1)
        )

        # approve task6
        reviews = self.test_task6.request_review()
        for r in reviews:
            r.approve()

        # check statuses
        self.assertEqual(self.test_task6.status, self.status_cmpl)
        self.assertEqual(self.test_task3.status, self.status_rts)
        self.assertEqual(self.test_task9.status, self.status_wfd)

        # start working on task3
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        # approve task3
        reviews = self.test_task3.request_review()
        for r in reviews:
            r.approve()

        # check statuses
        self.assertEqual(self.test_task6.status, self.status_cmpl)
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_rts)

        # start working on task9
        self.test_task9.create_time_log(
            resource=self.test_task9.resources[0],
            start=now + td(hours=2),
            end=now + td(hours=3)
        )

        # check statuses
        self.assertEqual(self.test_task6.status, self.status_cmpl)
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_wip)

        # hold task9
        self.test_task9.hold()

        # check statuses
        self.assertEqual(self.test_task6.status, self.status_cmpl)
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_oh)

        # request a revision to task6
        self.test_task6.request_revision(
            reviewer=self.test_user1
        )

        # check statuses
        self.assertEqual(self.test_task6.status, self.status_hrev)
        self.assertEqual(self.test_task3.status, self.status_drev)
        self.assertEqual(self.test_task9.status, self.status_oh)

        # resume task9
        self.test_task9.resume()

        # check statuses
        self.assertEqual(self.test_task6.status, self.status_hrev)
        self.assertEqual(self.test_task3.status, self.status_drev)
        self.assertEqual(self.test_task9.status, self.status_drev)

    # OH: OH dependencies -> DREV
    def test_resume_in_OH_leaf_task_with_OH_dependencies(self):
        """testing if the status will be updated to WIP when the resume action
        is used in a OH leaf task with OH dependencies
        """
        self.test_task3.status = self.status_rts
        self.test_task9.status = self.status_rts

        # finish task3 first
        now = datetime.datetime.now()
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now,
            end=now + datetime.timedelta(hours=1)
        )
        reviews = self.test_task3.request_review()
        for r in reviews:
            r.approve()

        self.test_task9.depends = [self.test_task3]

        # start working for task9
        self.test_task9.create_time_log(
            resource=self.test_task9.resources[0],
            start=now + datetime.timedelta(hours=1),
            end=now + datetime.timedelta(hours=2)
        )

        # now request a revision for task3
        self.test_task3.request_revision(reviewer=self.test_user1)
        self.assertEqual(self.test_task3.status, self.status_hrev)
        self.assertEqual(self.test_task9.status, self.status_drev)

        # enter a new time log for task3 to make it wip
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now + datetime.timedelta(hours=3),
            end=now + datetime.timedelta(hours=4),
        )

        # and hold task3 and task9
        self.test_task9.hold()
        self.test_task3.hold()

        self.assertEqual(self.test_task3.status, self.status_oh)
        self.assertEqual(self.test_task9.status, self.status_oh)

        self.test_task9.resume()
        self.assertEqual(self.test_task9.status, self.status_drev)

    # OH: STOP dependencies -> WIP
    def test_resume_in_OH_leaf_task_with_STOP_dependencies(self):
        """testing if the status will be updated to WIP when the resume action
        is used in a OH leaf task with STOP dependencies
        """
        self.test_task3.status = self.status_rts
        self.test_task9.status = self.status_rts
        self.test_task9.depends = [self.test_task3]

        self.test_task3.status = self.status_stop
        self.test_task9.status = self.status_oh

        self.test_task9.resume()
        self.assertEqual(self.test_task9.status, self.status_wip)

    # OH: CMPL dependencies -> WIP
    def test_resume_in_OH_leaf_task_with_CMPL_dependencies(self):
        """testing if the status will be updated to WIP when the resume action
        is used in a OH leaf task with CMPL dependencies
        """
        self.test_task3.status = self.status_rts
        self.test_task9.status = self.status_rts
        self.test_task9.depends = [self.test_task3]

        self.test_task3.status = self.status_cmpl
        self.test_task9.status = self.status_oh

        self.test_task9.resume()
        self.assertEqual(self.test_task9.status, self.status_wip)

    # STOP: no dependency -> WIP
    def test_resume_in_STOP_leaf_task_with_no_dependencies(self):
        """testing if the status will be updated to WIP when the resume action
        is used in a STOP leaf task with no dependencies
        """
        self.test_task3.status = self.status_stop
        self.test_task3.depends = []
        self.test_task3.resume()
        # no time logs so it will return back to rts
        # the test is wrong in the first place (no way to turn a task with no
        # time logs in to a OH task),
        # but checks a situation that the system needs to be more robust
        self.assertEqual(self.test_task3.status, self.status_rts)

    # STOP: WIP dependencies -> DREV
    def test_resume_in_STOP_leaf_task_with_WIP_dependencies(self):
        """testing if the status will be updated to DREV when the resume action
        is used in a STOP leaf task with WIP dependencies
        """
        self.test_task3.status = self.status_rts
        self.test_task9.status = self.status_rts
        self.test_task9.depends = [self.test_task3]

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_rts)
        self.assertEqual(self.test_task9.status, self.status_wfd)

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        # start working on task3
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now,
            end=now + td(hours=1)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_wip)
        self.assertEqual(self.test_task9.status, self.status_wfd)

        # complete task3
        reviews = self.test_task3.request_review()
        for r in reviews:
            r.approve()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_rts)

        # start working on task9
        self.test_task9.create_time_log(
            resource=self.test_task9.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_wip)

        # stop task9
        self.test_task9.stop()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # request a revision to task3
        self.test_task3.request_revision(
            reviewer=self.test_user1
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_hrev)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # now continue working on task3
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now + td(hours=2),
            end=now + td(hours=3)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_wip)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # now resume task9
        self.test_task9.resume()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_wip)
        self.assertEqual(self.test_task9.status, self.status_drev)

    # STOP: HREV dependencies -> DREV
    def test_resume_in_STOP_leaf_task_with_HREV_dependencies(self):
        """testing if the status will be updated to DREV when the resume action
        is used in a STOP leaf task with HREV dependencies
        """
        self.test_task3.status = self.status_rts
        self.test_task9.status = self.status_rts
        self.test_task9.depends = [self.test_task3]

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_rts)
        self.assertEqual(self.test_task9.status, self.status_wfd)

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        # start working on task3
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now,
            end=now + td(hours=1)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_wip)
        self.assertEqual(self.test_task9.status, self.status_wfd)

        # complete task3
        reviews = self.test_task3.request_review()
        for r in reviews:
            r.approve()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_rts)

        # start working on task9
        self.test_task9.create_time_log(
            resource=self.test_task9.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_wip)

        # stop task9
        self.test_task9.stop()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # request a revision to task3
        self.test_task3.request_revision(
            reviewer=self.test_user1
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_hrev)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # now continue working on task3
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now + td(hours=2),
            end=now + td(hours=3)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_wip)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # request a review for task3
        reviews = self.test_task3.request_review()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_prev)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # request revisions
        for r in reviews:
            r.request_revision()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_hrev)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # now resume task9
        self.test_task9.resume()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_hrev)
        self.assertEqual(self.test_task9.status, self.status_drev)

    # STOP: PREV dependencies -> DREV
    def test_resume_in_STOP_leaf_task_with_PREV_dependencies(self):
        """testing if the status will be updated to DREV when the resume action
        is used in a STOP leaf task with PREV dependencies
        """
        self.test_task3.status = self.status_rts
        self.test_task9.status = self.status_rts
        self.test_task9.depends = [self.test_task3]

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_rts)
        self.assertEqual(self.test_task9.status, self.status_wfd)

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        # start working on task3
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now,
            end=now + td(hours=1)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_wip)
        self.assertEqual(self.test_task9.status, self.status_wfd)

        # complete task3
        reviews = self.test_task3.request_review()
        for r in reviews:
            r.approve()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_rts)

        # start working on task9
        self.test_task9.create_time_log(
            resource=self.test_task9.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_wip)

        # stop task9
        self.test_task9.stop()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # request a revision to task3
        self.test_task3.request_revision(
            reviewer=self.test_user1
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_hrev)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # now continue working on task3
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now + td(hours=2),
            end=now + td(hours=3)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_wip)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # request a review for task3
        self.test_task3.request_review()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_prev)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # now resume task9
        self.test_task9.resume()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_prev)
        self.assertEqual(self.test_task9.status, self.status_drev)

    # STOP: DREV dependencies -> DREV
    def test_resume_in_STOP_leaf_task_with_DREV_dependencies(self):
        """testing if the status will be updated to DREV when the resume action
        is used in a STOP leaf task with DREV dependencies
        """
        self.test_task6.status = self.status_rts
        self.test_task3.status = self.status_rts
        self.test_task9.status = self.status_rts
        self.test_task9.depends = [self.test_task3]
        self.test_task3.depends = [self.test_task6]

        # check statuses
        self.assertEqual(self.test_task6.status, self.status_rts)
        self.assertEqual(self.test_task3.status, self.status_wfd)
        self.assertEqual(self.test_task9.status, self.status_wfd)

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()
        self.test_task6.create_time_log(
            resource=self.test_task6.resources[0],
            start=now,
            end=now + td(hours=1)
        )

        # approve task6
        reviews = self.test_task6.request_review()
        for r in reviews:
            r.approve()

        # check statuses
        self.assertEqual(self.test_task6.status, self.status_cmpl)
        self.assertEqual(self.test_task3.status, self.status_rts)
        self.assertEqual(self.test_task9.status, self.status_wfd)

        # start working on task3
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        # approve task3
        reviews = self.test_task3.request_review()
        for r in reviews:
            r.approve()

        # check statuses
        self.assertEqual(self.test_task6.status, self.status_cmpl)
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_rts)

        # start working on task9
        self.test_task9.create_time_log(
            resource=self.test_task9.resources[0],
            start=now + td(hours=2),
            end=now + td(hours=3)
        )

        # check statuses
        self.assertEqual(self.test_task6.status, self.status_cmpl)
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_wip)

        # stop task9
        self.test_task9.stop()

        # check statuses
        self.assertEqual(self.test_task6.status, self.status_cmpl)
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # request a revision to task6
        self.test_task6.request_revision(
            reviewer=self.test_user1
        )

        # check statuses
        self.assertEqual(self.test_task6.status, self.status_hrev)
        self.assertEqual(self.test_task3.status, self.status_drev)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # resume task9
        self.test_task9.resume()

        # check statuses
        self.assertEqual(self.test_task6.status, self.status_hrev)
        self.assertEqual(self.test_task3.status, self.status_drev)
        self.assertEqual(self.test_task9.status, self.status_drev)

    # STOP: OH dependencies -> DREV
    def test_resume_in_STOP_leaf_task_with_OH_dependencies(self):
        """testing if the status will be updated to WIP when the resume action
        is used in a STOP leaf task with OH dependencies
        """
        self.test_task3.status = self.status_rts
        self.test_task9.status = self.status_rts
        self.test_task9.depends = [self.test_task3]

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_rts)
        self.assertEqual(self.test_task9.status, self.status_wfd)

        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()

        # start working on task3
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now,
            end=now + td(hours=1)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_wip)
        self.assertEqual(self.test_task9.status, self.status_wfd)

        # complete task3
        reviews = self.test_task3.request_review()
        for r in reviews:
            r.approve()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_rts)

        # start working on task9
        self.test_task9.create_time_log(
            resource=self.test_task9.resources[0],
            start=now + td(hours=1),
            end=now + td(hours=2)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_wip)

        # stop task9
        self.test_task9.stop()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_cmpl)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # request a revision to task3
        self.test_task3.request_revision(
            reviewer=self.test_user1
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_hrev)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # now continue working on task3
        self.test_task3.create_time_log(
            resource=self.test_task3.resources[0],
            start=now + td(hours=2),
            end=now + td(hours=3)
        )

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_wip)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # hold task3
        self.test_task3.hold()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_oh)
        self.assertEqual(self.test_task9.status, self.status_stop)

        # now resume task9
        self.test_task9.resume()

        # check statuses
        self.assertEqual(self.test_task3.status, self.status_oh)
        self.assertEqual(self.test_task9.status, self.status_drev)

    # STOP: STOP dependencies -> WIP
    def test_resume_in_STOP_leaf_task_with_STOP_dependencies(self):
        """testing if the status will be updated to WIP when the resume action
        is used in a STOP leaf task with STOP dependencies
        """
        self.test_task3.status = self.status_rts
        self.test_task9.status = self.status_rts
        self.test_task9.depends = [self.test_task3]

        self.test_task3.status = self.status_stop
        self.test_task9.status = self.status_stop

        self.test_task9.resume()
        self.assertEqual(self.test_task9.status, self.status_wip)

    # STOP: CMPL dependencies -> WIP
    def test_resume_in_STOP_leaf_task_with_CMPL_dependencies(self):
        """testing if the status will be updated to WIP when the resume action
        is used in a STOP leaf task with CMPL dependencies
        """
        self.test_task3.status = self.status_rts
        self.test_task9.status = self.status_rts
        self.test_task9.depends = [self.test_task3]

        self.test_task3.status = self.status_cmpl
        self.test_task9.status = self.status_stop

        self.test_task9.resume()
        self.assertEqual(self.test_task9.status, self.status_wip)

    # CMPL
    def test_resume_in_CMPL_leaf_task(self):
        """testing if a StatusError will be raised when the resume action is used
        in a CMPL leaf task
        """
        self.test_task3.status = self.status_drev
        self.assertRaises(StatusError, self.test_task3.resume)

    def test_review_set_review_number_is_skipped(self):
        """testing if the latest review set will be returned if the
        review_number argument is skipped in Task.review_set() method
        """
        self.test_task3.status = self.status_wip

        # request a review
        reviews = self.test_task3.request_review()
        self.assertEqual(2, len(reviews))

        # check the review_set() method with no review number
        self.assertEqual(
            reviews,
            self.test_task3.review_set()
        )

        # now finalize the reviews
        reviews[0].approve()
        reviews[1].request_revision()

        # task should have been set to hrev
        self.assertEqual(
            self.status_hrev,
            self.test_task3.status
        )

        # set the status to wip again
        self.test_task3.status = self.status_wip

        # request a new set of reviews
        reviews2 = self.test_task3.request_review()

        # confirm that they it is a different set of review
        self.assertNotEqual(reviews, reviews2)

        # now check if review_set() will return reviews2
        self.assertEqual(
            reviews2,
            self.test_task3.review_set()
        )

    def test_review_set_review_number_is_not_an_integer(self):
        """testing if a TypeError will be raised when the review_number
        argument value is not an integer in Task.review_set() method
        """
        with self.assertRaises(TypeError) as cm:
            self.test_task3.review_set('not an integer')

        self.assertEqual(
            'review_number argument in Task.review_set should be a positive '
            'integer, not str',
            str(cm.exception)
        )

    def test_review_set_review_number_is_a_negative_integer(self):
        """testing if a ValueError will be raised when the review_number is a
        negative number
        """
        with self.assertRaises(TypeError) as cm:
            self.test_task3.review_set(-10)

        self.assertEqual(
            'review_number argument in Task.review_set should be a positive '
            'integer, not -10',
            str(cm.exception)
        )

    def test_review_set_review_number_is_zero(self):
        """testing if a ValueError will be raised when the review_number is
        zero
        """
        with self.assertRaises(TypeError) as cm:
            self.test_task3.review_set(0)

        self.assertEqual(
            'review_number argument in Task.review_set should be a positive '
            'integer, not 0',
            str(cm.exception)
        )

    def test_review_set_method_is_working_properly(self):
        """testing if the review_set() method is working properly
        """
        self.test_task3.status = self.status_wip

        # request a review
        reviews = self.test_task3.request_review()
        self.assertEqual(2, len(reviews))

        # check the review_set() method with no review number
        self.assertEqual(
            reviews,
            self.test_task3.review_set()
        )

        # now finalize the reviews
        reviews[0].approve()
        reviews[1].request_revision()

        # task should have been set to hrev
        self.assertEqual(
            self.status_hrev,
            self.test_task3.status
        )

        # set the status to wip again
        self.test_task3.status = self.status_wip

        # request a new set of reviews
        reviews2 = self.test_task3.request_review()

        # confirm that they it is a different set of review
        self.assertNotEqual(reviews, reviews2)

        # now check if review_set() will return reviews2
        self.assertEqual(
            reviews2,
            self.test_task3.review_set()
        )

        # and use a review_number
        self.assertEqual(
            reviews,
            self.test_task3.review_set(1)
        )

        self.assertEqual(
            reviews2,
            self.test_task3.review_set(2)
        )

    def test_leaf_DREV_task_with_no_dependency_and_no_timelogs_update_status_with_dependent_statuses_fixes_status(self):
        """testing if a Task.update_status_with_dependent_statuses() will fix
        the status of a leaf DREV task with no dependency (something went
        wrong) to RTS if there is no TimeLog and to WIP if there is a TimeLog
        """
        # use task6 and task5
        self.test_task5.depends = []

        # set the statuses
        self.test_task5.status = self.status_drev

        self.assertEqual(
            self.status_drev,
            self.test_task5.status
        )

        # fix status with dependencies
        self.test_task5.update_status_with_dependent_statuses()

        # check the status
        self.assertEqual(
            self.status_rts,
            self.test_task5.status
        )

    def test_leaf_DREV_task_with_no_dependency_but_with_timelogs_update_status_with_dependent_statuses_fixes_status(self):
        """testing if a Task.update_status_with_dependent_statuses() will fix
        the status of a leaf DREV task with no dependency (something went
        wrong) to RTS if there is no TimeLog and to WIP if there is a TimeLog
        """
        # use task6 and task5
        self.test_task5.depends = []

        # create some time logs for
        dt = datetime.datetime
        td = datetime.timedelta
        now = dt.now()
        self.test_task5.create_time_log(
            resource=self.test_task5.resources[0],
            start=now,
            end=now + td(hours=1)
        )

        # set the statuses
        self.test_task5.status = self.status_drev

        self.assertEqual(
            self.status_drev,
            self.test_task5.status
        )

        # fix status with dependencies
        self.test_task5.update_status_with_dependent_statuses()

        # check the status
        self.assertEqual(
            self.status_wip,
            self.test_task5.status
        )

    def test_leaf_WIP_task_with_no_dependency_and_no_timelogs_update_status_with_dependent_statuses_fixes_status(self):
        """testing if a Task.update_status_with_dependent_statuses() will fix
        the status of a leaf WIP task with no dependency (something went
        wrong) to RTS if there is no TimeLog and to WIP if there is a TimeLog
        """
        # use task6 and task5
        self.test_task5.depends = []

        # check if there is no time logs
        self.assertEqual(self.test_task5.time_logs, [])

        # set the statuses
        self.test_task5.status = self.status_wip

        self.assertEqual(
            self.status_wip,
            self.test_task5.status
        )

        # fix status with dependencies
        self.test_task5.update_status_with_dependent_statuses()

        # check the status
        self.assertEqual(
            self.status_rts,
            self.test_task5.status
        )
