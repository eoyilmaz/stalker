# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import unittest
from stalker import (db, Daily, Project, Repository, Status, StatusList, Task,
                     Version, Link, DailyLink)


class DailyTestBase(unittest.TestCase):
    """Tests the stalker.models.review.Daily class
    """

    @classmethod
    def setUpClass(cls):
        """setup once
        """
        db.setup()
        db.init()

        cls.status_new = Status.query.filter_by(code='NEW').first()
        cls.status_wip = Status.query.filter_by(code='WIP').first()
        cls.status_cmpl = Status.query.filter_by(code='CMPL').first()

        cls.test_project_status_list = StatusList(
            name='Project Statuses',
            target_entity_type='Project',
            statuses=[cls.status_new, cls.status_wip, cls.status_cmpl]
        )

        cls.test_repo = Repository(name='Test Repository')

        cls.test_project = Project(
            name='Test Project',
            code='TP',
            repository=cls.test_repo,
            status_list=cls.test_project_status_list
        )

        cls.test_task1 = Task(
            name='Test Task 1',
            project=cls.test_project
        )
        cls.test_task2 = Task(
            name='Test Task 2',
            project=cls.test_project
        )
        cls.test_task3 = Task(
            name='Test Task 3',
            project=cls.test_project
        )

        cls.test_version1 = Version(task=cls.test_task1)
        db.DBSession.add(cls.test_version1)
        db.DBSession.commit()

        cls.test_version2 = Version(task=cls.test_task1)
        db.DBSession.add(cls.test_version2)
        db.DBSession.commit()

        cls.test_version3 = Version(task=cls.test_task1)
        db.DBSession.add(cls.test_version3)
        db.DBSession.commit()

        cls.test_version4 = Version(task=cls.test_task2)
        db.DBSession.add(cls.test_version4)
        db.DBSession.commit()

        cls.test_link1 = Link(original_filename='test_render1.jpg')
        cls.test_link2 = Link(original_filename='test_render2.jpg')
        cls.test_link3 = Link(original_filename='test_render3.jpg')
        cls.test_link4 = Link(original_filename='test_render4.jpg')

        cls.test_version1.outputs = [
            cls.test_link1,
            cls.test_link2,
            cls.test_link3
        ]
        cls.test_version4.outputs = [
            cls.test_link4
        ]

        db.DBSession.add_all([
            cls.test_task1, cls.test_task2, cls.test_task3,
            cls.test_version1, cls.test_version2, cls.test_version3,
            cls.test_version4,
            cls.test_link1, cls.test_link2, cls.test_link3, cls.test_link4
        ])
        db.DBSession.commit()


class DailyTestCase(DailyTestBase):
    """Tests the stalker.models.review.Daily class
    """

    def test_daily_instance_creation(self):
        """testing if it is possible to create a Daily without a problem
        """
        daily = Daily(name='Test Daily', project=self.test_project)
        self.assertTrue(isinstance(daily, Daily))

    def test_links_argument_is_skipped(self):
        """testing if the links attribute will be an empty list if the links
        argument is skipped
        """
        daily = Daily(name='Test Daily', project=self.test_project)
        self.assertEqual(daily.links, [])

    def test_links_argument_is_none(self):
        """testing if the links attribute will be an empty list when the links
        argument is None
        """
        daily = Daily(name='Test Daily', links=None, project=self.test_project)
        self.assertEqual(daily.links, [])

    def test_links_attribute_is_set_to_none(self):
        """testing if a TypeError will be raised when the links attribute is
        set to None
        """
        daily = Daily(name='Test Daily', project=self.test_project)
        with self.assertRaises(TypeError):
            daily.links = None

    def test_links_argument_is_not_a_list_instance(self):
        """testing if a TypeError will be raised when the links argument is not
        a list
        """
        with self.assertRaises(TypeError) as cm:
            Daily(
                name='Test Daily',
                links='not a list of Daily instances',
                project=self.test_project
            )

        self.assertEqual(
            str(cm.exception),
            'DailyLink.link should be an instance of stalker.models.link.Link '
            'instance, not str'
        )

    def test_links_argument_is_not_a_list_of_link_instances(self):
        """testing if a TypeError will be raised when the links argument is not
        a list of Link instances
        """
        with self.assertRaises(TypeError) as cm:
            Daily(
                name='Test Daily',
                links=['not', 1, 'list', 'of', Daily, 'instances'],
                project=self.test_project
            )

        self.assertEqual(
            str(cm.exception),
            'DailyLink.link should be an instance of stalker.models.link.Link '
            'instance, not str'
        )

    def test_links_argument_is_working_properly(self):
        """testing if the links argument value is correctly passed to the links
        attribute
        """
        test_value = [self.test_link1, self.test_link2]
        daily = Daily(
            name='Test Daily',
            links=test_value,
            project=self.test_project
        )
        self.assertEqual(daily.links, test_value)

    def test_links_attribute_is_working_properly(self):
        """testing if the links attribute is working properly
        """
        daily = Daily(name='Test Daily', project=self.test_project)
        daily.links.append(self.test_link1)

        self.assertEqual(daily.links, [self.test_link1])

    def test_versions_attribute_is_read_only(self):
        """testing if versions attribute is a read only attribute
        """
        daily = Daily(name='Test Daily', project=self.test_project)
        with self.assertRaises(AttributeError):
            setattr(daily, 'versions', 10)

    def test_versions_attribute_will_return_a_list_of_versions(self):
        """testing if the versions attribute is a list of Version instances
        related to the given links
        """
        daily = Daily(name='Test Daily', project=self.test_project)
        daily.links = [self.test_link1, self.test_link2]
        db.DBSession.add(daily)
        db.DBSession.commit()
        self.assertEqual(daily.versions, [self.test_version1])

    def test_tasks_attribute_will_return_a_list_of_tasks(self):
        """testing if the tasks attribute is a list of Task instances related
        to the given links
        """
        daily = Daily(name='Test Daily', project=self.test_project)
        daily.links = [self.test_link1, self.test_link2]
        db.DBSession.add(daily)
        db.DBSession.commit()
        self.assertEqual(daily.tasks, [self.test_task1])


class DailyLinkTestCase(DailyTestBase):
    """tests the DailyLink class
    """

    def test_rank_argument_is_skipped(self):
        """testing if rank attribute will use the default value is when skipped
        """
        dl = DailyLink()
        self.assertEqual(dl.rank, 0)
