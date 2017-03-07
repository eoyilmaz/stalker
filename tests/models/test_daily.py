# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2016 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# Stalker is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# Stalker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with Stalker.  If not, see <http://www.gnu.org/licenses/>

from stalker.testing import UnitTestBase


class DailyTestBase(UnitTestBase):
    """Tests the stalker.models.review.Daily class
    """

    def setUp(self):
        super(DailyTestBase, self).setUp()

        from stalker import db, Status, StatusList
        self.status_new = Status.query.filter_by(code='NEW').first()
        self.status_wip = Status.query.filter_by(code='WIP').first()
        self.status_cmpl = Status.query.filter_by(code='CMPL').first()

        self.test_project_status_list = StatusList(
            name='Project Statuses',
            target_entity_type='Project',
            statuses=[self.status_new, self.status_wip, self.status_cmpl]
        )
        db.DBSession.add(self.test_project_status_list)

        from stalker import Repository, Project
        self.test_repo = Repository(name='Test Repository')
        db.DBSession.add(self.test_repo)

        self.test_project = Project(
            name='Test Project',
            code='TP',
            repository=self.test_repo,
            status_list=self.test_project_status_list
        )
        db.DBSession.add(self.test_project)

        from stalker import Task
        self.test_task1 = Task(
            name='Test Task 1',
            project=self.test_project
        )
        db.DBSession.add(self.test_task1)
        self.test_task2 = Task(
            name='Test Task 2',
            project=self.test_project
        )
        db.DBSession.add(self.test_task2)
        self.test_task3 = Task(
            name='Test Task 3',
            project=self.test_project
        )
        db.DBSession.add(self.test_task3)

        from stalker import Version
        self.test_version1 = Version(task=self.test_task1)
        db.DBSession.add(self.test_version1)
        db.DBSession.commit()

        self.test_version2 = Version(task=self.test_task1)
        db.DBSession.add(self.test_version2)
        db.DBSession.commit()

        self.test_version3 = Version(task=self.test_task1)
        db.DBSession.add(self.test_version3)
        db.DBSession.commit()

        self.test_version4 = Version(task=self.test_task2)
        db.DBSession.add(self.test_version4)
        db.DBSession.commit()

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

        db.DBSession.add_all([
            self.test_task1, self.test_task2, self.test_task3,
            self.test_version1, self.test_version2, self.test_version3,
            self.test_version4,
            self.test_link1, self.test_link2, self.test_link3, self.test_link4
        ])
        db.DBSession.commit()


class DailyTestCase(DailyTestBase):
    """Tests the stalker.models.review.Daily class
    """

    def test_daily_instance_creation(self):
        """testing if it is possible to create a Daily without a problem
        """
        from stalker import Daily
        daily = Daily(name='Test Daily', project=self.test_project)
        self.assertTrue(isinstance(daily, Daily))

    def test_links_argument_is_skipped(self):
        """testing if the links attribute will be an empty list if the links
        argument is skipped
        """
        from stalker import Daily
        daily = Daily(name='Test Daily', project=self.test_project)
        self.assertEqual(daily.links, [])

    def test_links_argument_is_none(self):
        """testing if the links attribute will be an empty list when the links
        argument is None
        """
        from stalker import Daily
        daily = Daily(name='Test Daily', links=None, project=self.test_project)
        self.assertEqual(daily.links, [])

    def test_links_attribute_is_set_to_none(self):
        """testing if a TypeError will be raised when the links attribute is
        set to None
        """
        from stalker import Daily
        daily = Daily(name='Test Daily', project=self.test_project)
        with self.assertRaises(TypeError):
            daily.links = None

    def test_links_argument_is_not_a_list_instance(self):
        """testing if a TypeError will be raised when the links argument is not
        a list
        """
        from stalker import Daily
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
        from stalker import Daily
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
        from stalker import Daily
        daily = Daily(
            name='Test Daily',
            links=test_value,
            project=self.test_project
        )
        self.assertEqual(daily.links, test_value)

    def test_links_attribute_is_working_properly(self):
        """testing if the links attribute is working properly
        """
        from stalker import Daily
        daily = Daily(name='Test Daily', project=self.test_project)
        daily.links.append(self.test_link1)

        self.assertEqual(daily.links, [self.test_link1])

    def test_versions_attribute_is_read_only(self):
        """testing if versions attribute is a read only attribute
        """
        from stalker import Daily
        daily = Daily(name='Test Daily', project=self.test_project)
        with self.assertRaises(AttributeError):
            setattr(daily, 'versions', 10)

    def test_versions_attribute_will_return_a_list_of_versions(self):
        """testing if the versions attribute is a list of Version instances
        related to the given links
        """
        from stalker import db, Daily
        daily = Daily(name='Test Daily', project=self.test_project)
        daily.links = [self.test_link1, self.test_link2]
        db.DBSession.add(daily)
        db.DBSession.commit()
        self.assertEqual(daily.versions, [self.test_version1])

    def test_tasks_attribute_will_return_a_list_of_tasks(self):
        """testing if the tasks attribute is a list of Task instances related
        to the given links
        """
        from stalker import db, Daily
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
        from stalker import DailyLink
        dl = DailyLink()
        self.assertEqual(dl.rank, 0)
