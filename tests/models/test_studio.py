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
import datetime
import logging

from stalker.db import DBSession
from stalker import (db, defaults, Studio, WorkingHours, Project, StatusList,
                     Status, Repository, Asset, Type, User, Shot, Department,
                     Task, TaskJugglerScheduler, SchedulerBase)


class DummyScheduler(SchedulerBase):
    """this is a dummy scheduler to be used in tests
    """

    def __init__(self, studio=None, callback=None):
        SchedulerBase.__init__(self, studio)
        self.callback = callback

    def schedule(self):
        """call the callback function before finishing
        """
        if self.callback:
            self.callback()


class StudioTester(unittest.TestCase):
    """tests the stalker.models.studio.Studio class
    """

    @classmethod
    def setUpClass(cls):
        """setup once
        """
        logger = logging.getLogger('stalker.models.schedulers')
        logger.setLevel(logging.DEBUG)

    def setUp(self):
        """setup the test
        """
        db.setup()
        db.init()

        self.test_user1 = User(
            name='User 1',
            login='user1',
            email='user1@users.com',
            password='password'
        )
        DBSession.add(self.test_user1)

        self.test_user2 = User(
            name='User 2',
            login='user2',
            email='user2@users.com',
            password='password'
        )
        DBSession.add(self.test_user2)

        self.test_user3 = User(
            name='User 3',
            login='user3',
            email='user3@users.com',
            password='password'
        )
        DBSession.add(self.test_user3)

        self.test_department1 = Department(
            name='Test Department 1'
        )
        DBSession.add(self.test_department1)

        self.test_department2 = Department(
            name='Test Department 2'
        )
        DBSession.add(self.test_department2)

        self.test_status1 = Status(
            name='Status 1',
            code='ST1'
        )
        DBSession.add(self.test_status1)

        self.test_status2 = Status(
            name='Status 2',
            code='ST2'
        )
        DBSession.add(self.test_status2)

        self.test_project_status_list1 = StatusList(
            name='Project Statuses',
            statuses=[self.test_status1, self.test_status2],
            target_entity_type=Project
        )
        DBSession.add(self.test_project_status_list1)

        self.test_repo = Repository(
            name='Test Repository',
            windows_path='T:/',
            linux_path='/mnt/T/',
            osx_path='/Volumes/T/'
        )
        DBSession.add(self.test_repo)

        # create a couple of projects
        self.test_project1 = Project(
            name='Test Project 1',
            code='TP1',
            status_list=self.test_project_status_list1,
            repository=self.test_repo
        )
        DBSession.add(self.test_project1)

        self.test_project2 = Project(
            name='Test Project 2',
            code='TP2',
            status_list=self.test_project_status_list1,
            repository=self.test_repo
        )
        DBSession.add(self.test_project2)

        # an inactive project
        self.test_project3 = Project(
            name='Test Project 3',
            code='TP3',
            status_list=self.test_project_status_list1,
            repository=self.test_repo
        )
        self.test_project3.active = False
        DBSession.add(self.test_project3)

        # create assets and shots
        self.test_asset_type = Type(
            name='Character',
            code='Char',
            target_entity_type=Asset
        )
        DBSession.add(self.test_asset_type)

        self.test_asset_status_list = \
            StatusList.query.filter_by(target_entity_type='Asset').first()

        self.test_asset1 = Asset(
            name='Test Asset 1',
            code='TA1',
            project=self.test_project1,
            type=self.test_asset_type
        )
        DBSession.add(self.test_asset1)

        self.test_asset2 = Asset(
            name='Test Asset 2',
            code='TA2',
            project=self.test_project2,
            type=self.test_asset_type
        )
        DBSession.add(self.test_asset2)

        # shots
        self.test_shot_status_list = \
            StatusList.query.filter_by(target_entity_type='Shot').first()

        # for project 1
        self.test_shot1 = Shot(
            code='shot1',
            project=self.test_project1,
            status_list=self.test_shot_status_list
        )
        DBSession.add(self.test_shot1)

        self.test_shot2 = Shot(
            code='shot2',
            project=self.test_project1,
            status_list=self.test_shot_status_list
        )
        DBSession.add(self.test_shot2)

        # for project 2
        self.test_shot3 = Shot(
            code='shot3',
            project=self.test_project2,
            status_list=self.test_shot_status_list
        )
        DBSession.add(self.test_shot3)

        self.test_shot4 = Shot(
            code='shot4',
            project=self.test_project2,
            status_list=self.test_shot_status_list
        )
        DBSession.add(self.test_shot4)

        # for project 3
        self.test_shot5 = Shot(
            code='shot5',
            project=self.test_project3,
            status_list=self.test_shot_status_list
        )
        DBSession.add(self.test_shot5)

        #########################################################3
        # tasks for projects
        self.test_task_statuses = \
            StatusList.query.filter_by(target_entity_type='Task').first()

        self.test_task1 = Task(
            name='Project Planing',
            project=self.test_project1,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=10,
            schedule_unit='d'
        )
        DBSession.add(self.test_task1)

        self.test_task2 = Task(
            name='Project Planing',
            project=self.test_project2,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=10,
            schedule_unit='d'
        )
        DBSession.add(self.test_task2)

        self.test_task3 = Task(
            name='Project Planing',
            project=self.test_project3,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            status_list=self.test_task_statuses,
            schedule_timing=5,
            schedule_unit='d'
        )
        DBSession.add(self.test_task3)

        # for shots

        # Shot 1
        self.test_task4 = Task(
            name='Match Move',
            parent=self.test_shot1,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=2,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task4)

        self.test_task5 = Task(
            name='FX',
            parent=self.test_shot1,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            depends=[self.test_task4],
            schedule_timing=2,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task5)

        self.test_task6 = Task(
            name='Lighting',
            parent=self.test_shot1,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            depends=[self.test_task4, self.test_task5],
            schedule_timing=3,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task6)

        self.test_task7 = Task(
            name='Comp',
            parent=self.test_shot1,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            depends=[self.test_task6],
            schedule_timing=3,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task7)

        # Shot 2
        self.test_task8 = Task(
            name='Match Move',
            parent=self.test_shot2,
            resources=[self.test_user3],
            alternative_resources=[self.test_user1, self.test_user2],
            schedule_timing=2,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task8)

        self.test_task9 = Task(
            name='FX',
            parent=self.test_shot2,
            resources=[self.test_user3],
            alternative_resources=[self.test_user1, self.test_user2],
            depends=[self.test_task8],
            schedule_timing=2,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task9)

        self.test_task10 = Task(
            name='Lighting',
            parent=self.test_shot2,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            depends=[self.test_task8, self.test_task9],
            schedule_timing=3,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task10)

        self.test_task11 = Task(
            name='Comp',
            parent=self.test_shot2,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            depends=[self.test_task10],
            schedule_timing=4,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task11)

        # Shot 3
        self.test_task12 = Task(
            name='Match Move',
            parent=self.test_shot3,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=2,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task12)

        self.test_task13 = Task(
            name='FX',
            parent=self.test_shot3,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            depends=[self.test_task12],
            schedule_timing=2,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task13)

        self.test_task14 = Task(
            name='Lighting',
            parent=self.test_shot3,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            depends=[self.test_task12, self.test_task13],
            schedule_timing=3,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task14)

        self.test_task15 = Task(
            name='Comp',
            parent=self.test_shot3,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            depends=[self.test_task14],
            schedule_timing=4,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task15)

        # Shot 4
        self.test_task16 = Task(
            name='Match Move',
            parent=self.test_shot4,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            schedule_timing=2,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task16)

        self.test_task17 = Task(
            name='FX',
            parent=self.test_shot4,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            depends=[self.test_task16],
            schedule_timing=2,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task17)

        self.test_task18 = Task(
            name='Lighting',
            parent=self.test_shot4,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            depends=[self.test_task16, self.test_task17],
            schedule_timing=3,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task18)

        self.test_task19 = Task(
            name='Comp',
            parent=self.test_shot4,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            depends=[self.test_task18],
            schedule_timing=4,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task19)

        # Shot 5
        self.test_task20 = Task(
            name='Match Move',
            parent=self.test_shot5,
            resources=[self.test_user3],
            alternative_resources=[self.test_user1, self.test_user2],
            schedule_timing=2,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task20)

        self.test_task21 = Task(
            name='FX',
            parent=self.test_shot5,
            resources=[self.test_user3],
            alternative_resources=[self.test_user1, self.test_user2],
            depends=[self.test_task20],
            schedule_timing=2,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task21)

        self.test_task22 = Task(
            name='Lighting',
            parent=self.test_shot5,
            resources=[self.test_user3],
            alternative_resources=[self.test_user1, self.test_user2],
            depends=[self.test_task20, self.test_task21],
            schedule_timing=3,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task22)

        self.test_task23 = Task(
            name='Comp',
            parent=self.test_shot5,
            resources=[self.test_user3],
            alternative_resources=[self.test_user1, self.test_user2],
            depends=[self.test_task22],
            schedule_timing=4,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task23)

        ####################################################3
        # For Assets

        # Asset 1
        self.test_task24 = Task(
            name='Design',
            parent=self.test_asset1,
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=10,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task24)

        self.test_task25 = Task(
            name='Model',
            parent=self.test_asset1,
            depends=[self.test_task24],
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=15,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task25)

        self.test_task26 = Task(
            name='LookDev',
            parent=self.test_asset1,
            depends=[self.test_task25],
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=10,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task26)

        self.test_task27 = Task(
            name='Rig',
            parent=self.test_asset1,
            depends=[self.test_task25],
            resources=[self.test_user1],
            alternative_resources=[self.test_user2, self.test_user3],
            schedule_timing=10,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task27)

        # Asset 2
        self.test_task28 = Task(
            name='Design',
            parent=self.test_asset2,
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            schedule_timing=10,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task28)

        self.test_task29 = Task(
            name='Model',
            parent=self.test_asset2,
            depends=[self.test_task28],
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            schedule_timing=15,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task29)

        self.test_task30 = Task(
            name='LookDev',
            parent=self.test_asset2,
            depends=[self.test_task29],
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            schedule_timing=10,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task30)

        self.test_task31 = Task(
            name='Rig',
            parent=self.test_asset2,
            depends=[self.test_task29],
            resources=[self.test_user2],
            alternative_resources=[self.test_user1, self.test_user3],
            schedule_timing=10,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task31)

        # TODO: Add Milestones

        self.kwargs = dict(
            name='Studio',
            daily_working_hours=8,
            timing_resolution=datetime.timedelta(hours=1)
        )

        self.test_studio = Studio(**self.kwargs)
        DBSession.add(self.test_studio)
        DBSession.commit()

    def tearDown(self):
        """clean up the test
        """
        DBSession.remove()

    def test_working_hours_argument_is_skipped(self):
        """testing if the default working hours will be used when the
        working_hours argument is skipped
        """
        self.kwargs['name'] = 'New Studio'
        try:
            self.kwargs.pop('working_hours')  # pop if there are any
        except KeyError:
            pass

        new_studio = Studio(**self.kwargs)
        self.assertEqual(new_studio.working_hours, WorkingHours())

    def test_working_hours_argument_is_None(self):
        """testing if the a WorkingHour instance with default settings will be
        used if the working_hours argument is skipped
        """
        self.kwargs['name'] = 'New Studio'
        self.kwargs['working_hours'] = None
        new_studio = Studio(**self.kwargs)
        self.assertEqual(new_studio.working_hours, WorkingHours())

    def test_working_hours_attribute_is_None(self):
        """testing if a WorkingHour instance will be created with the default
        values if the working_hours attribute is set to None
        """
        self.test_studio.working_horus = None
        self.assertEqual(self.test_studio.working_hours, WorkingHours())

    def test_tjp_id_attribute_returns_a_plausible_id(self):
        """testing if the tjp_id is returning something meaningful
        """
        self.test_studio.id = 432
        self.assertEqual(self.test_studio.tjp_id, 'Studio_432')

    def test_projects_attribute_is_read_only(self):
        """testing if the project attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_studio,
                          'projects', [self.test_project1])

    def test_projects_attribute_is_working_properly(self):
        """testing if the projects attribute is working properly
        """
        self.assertEqual(
            sorted(self.test_studio.projects, key=lambda x: x.name),
            sorted(
                [self.test_project1, self.test_project2, self.test_project3],
                key=lambda x: x.name
            )
        )

    def test_active_projects_attribute_is_read_only(self):
        """testing if the active_projects attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_studio,
                          'active_projects', [self.test_project1])

    def test_active_projects_attribute_is_working_properly(self):
        """testing if the active_projects attribute is working properly
        """
        self.assertEqual(
            sorted(self.test_studio.active_projects, key=lambda x: x.name),
            sorted([self.test_project1, self.test_project2],
                   key=lambda x: x.name)
        )

    def test_inactive_projects_attribute_is_read_only(self):
        """testing if the inactive_projects attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_studio,
                          'inactive_projects', [self.test_project1])

    def test_inactive_projects_attribute_is_working_properly(self):
        """testing if the inactive_projects attribute is working properly
        """
        self.assertEqual(
            sorted(self.test_studio.inactive_projects, key=lambda x: x.name),
            sorted([self.test_project3], key=lambda x: x.name)
        )

    def test_departments_attribute_is_read_only(self):
        """testing if the departments attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_studio,
                          'departments', [self.test_project1])

    def test_departments_attribute_is_working_properly(self):
        """testing if the departments attribute is working properly
        """
        # don't forget admins department
        db.init()
        admins_dep = Department.query.filter_by(name='admins').first()
        self.assertEqual(
            sorted(self.test_studio.departments, key=lambda x: x.name),
            sorted([self.test_department1, self.test_department2, admins_dep],
                   key=lambda x: x.name)
        )

    def test_users_attribute_is_read_only(self):
        """testing if the users attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_studio, 'users',
                          [self.test_project1])

    def test_users_attribute_is_working_properly(self):
        """testing if the users attribute is working properly
        """
        # don't forget the admin
        admin = User.query.filter_by(name='admin').first()

        self.assertEqual(
            sorted(self.test_studio.users, key=lambda x: x.name),
            sorted([admin, self.test_user1, self.test_user2, self.test_user3],
                   key=lambda x: x.name)
        )

    def test_to_tjp_attribute_is_read_only(self):
        """testing if the to_tjp attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_studio, 'to_tjp',
                          "some text")

    def test_now_argument_is_skipped(self):
        """testing if the now attribute will use the rounded
        datetime.datetime.now value when the now argument is skipped
        """
        try:
            self.kwargs.pop('now')
        except KeyError:
            pass

        new_studio = Studio(**self.kwargs)
        self.assertEqual(new_studio.now,
                         new_studio.round_time(datetime.datetime.now()))

    def test_now_argument_is_None(self):
        """testing if the now attribute will use the rounded
        datetime.datetime.now value when the now argument is None
        """
        self.kwargs['now'] = None
        new_studio = Studio(**self.kwargs)
        self.assertEqual(new_studio.now,
                         new_studio.round_time(datetime.datetime.now()))

    def test_now_attribute_is_None(self):
        """testing if the now attribute will be equal to the rounded value of
        datetime.datetime.now() if it is set to None
        """
        self.test_studio.now = None
        self.assertEqual(
            self.test_studio.now,
            self.test_studio.round_time(datetime.datetime.now())
        )

    def test_now_argument_is_not_a_datetime_instance(self):
        """testing if a TypeError will be raised when the now argument is not
        a datetime.datetime instance
        """
        self.kwargs['now'] = 'not a datetime instance'
        self.assertRaises(TypeError, Studio, **self.kwargs)

    def test_now_attribute_is_set_to_a_value_other_than_datetime_instance(self):
        """testing if a TypeError will be raised when the now attribute is set
        to a value other than a datetime.datetime instance
        """
        self.assertRaises(TypeError, setattr, self.test_studio, 'now',
                          'not a datetime instance')

    def test_now_argument_is_working_properly(self):
        """testing if the now argument value is passed to the now attribute
        properly
        """
        self.kwargs['now'] = datetime.datetime(2013, 4, 15, 21, 9)
        expected_now = datetime.datetime(2013, 4, 15, 21, 0)
        new_studio = Studio(**self.kwargs)
        self.assertEqual(new_studio.now, expected_now)

    def test_now_attribute_is_working_properly(self):
        """testing if the now attribute is working properly
        """
        self.test_studio.now = datetime.datetime(2013, 4, 15, 21, 11)
        expected_now = datetime.datetime(2013, 4, 15, 21, 0)
        self.assertEqual(self.test_studio.now, expected_now)

    def test_now_attribute_is_working_properly_case2(self):
        """testing if the now attribute is working properly
        """
        self.test_studio._now = None
        expected_now = Studio.round_time(datetime.datetime.now())
        self.assertEqual(
            self.test_studio.now,
            expected_now
        )

    def test_to_tjp_attribute_is_working_properly(self):
        """testing if the to_tjp attribute is working properly
        """
        self.test_studio.start = datetime.datetime(2013, 4, 15, 17, 40)
        self.test_studio.end = datetime.datetime(2013, 6, 30, 17, 40)
        now = self.test_studio.round_time(datetime.datetime.now())
        self.test_studio.working_hours[0] = [[540, 1080]]
        self.test_studio.working_hours[1] = [[540, 1080]]
        self.test_studio.working_hours[2] = [[540, 1080]]
        self.test_studio.working_hours[3] = [[540, 1080]]
        self.test_studio.working_hours[4] = [[540, 1080]]
        self.test_studio.working_hours[5] = [[540, 720]]
        self.test_studio.working_hours[6] = []

        from jinja2 import Template

        expected_tjp_template = Template("""
project Studio_{{studio.id}} "Studio_{{studio.id}}" 2013-04-15 - 2013-06-30 {
    timingresolution 60min
    now {{ studio.now.strftime('%Y-%m-%d-%H:%M') }}
    dailyworkinghours 8
    weekstartsmonday
    workinghours mon 09:00 - 18:00
    workinghours tue 09:00 - 18:00
    workinghours wed 09:00 - 18:00
    workinghours thu 09:00 - 18:00
    workinghours fri 09:00 - 18:00
    workinghours sat 09:00 - 12:00
    workinghours sun off
    timeformat "%Y-%m-%d"
    scenario plan "Plan"
    trackingscenario plan
}
""")

        expected_tjp = expected_tjp_template.render({
            'studio': self.test_studio
        })
        # print('-----------------------------------')
        # print(expected_tjp)
        # print('-----------------------------------')
        # print(self.test_studio.to_tjp)
        # print('-----------------------------------')
        self.assertEqual(self.test_studio.to_tjp, expected_tjp)

    def test_scheduler_attribute_can_be_set_to_None(self):
        """testing if the scheduler attribute can be set to None
        """
        self.test_studio.scheduler = None

    def test_scheduler_attribute_accepts_Scheduler_instances_only(self):
        """testing if a TypeError will be raised when the scheduler attribute
        is set to a value which is not a scheduler instance
        """
        self.assertRaises(TypeError, setattr, self.test_studio, 'scheduler',
                          'not a Scheduler instance')

    def test_scheduler_attribute_is_working_properly(self):
        """testing if the scheduler attribute is working properly
        """
        tj_s = TaskJugglerScheduler()
        self.test_studio.scheduler = tj_s
        self.assertEqual(self.test_studio.scheduler, tj_s)

    def test_schedule_will_not_work_without_a_scheduler(self):
        """testing if a RuntimeError will be raised when the scheduler
        attribute is not set to a Scheduler instance and schedule is called
        """
        self.test_studio.scheduler = None
        self.assertRaises(RuntimeError, self.test_studio.schedule)

    def test_schedule_will_schedule_the_tasks_with_the_given_scheduler(self):
        """testing if the schedule method will schedule the tasks with the
        given scheduler
        """
        tj_scheduler = TaskJugglerScheduler(compute_resources=True)
        self.test_studio.now = datetime.datetime(2013, 4, 15, 22, 56)
        self.test_studio.start = datetime.datetime(2013, 4, 15, 22, 56)
        self.test_studio.end = datetime.datetime(2013, 7, 30, 0, 0)

        # just to be sure that it is not creating any issue on schedule
        self.test_task25.task_depends_to[0].dependency_target = 'onstart'
        self.test_task25.resources = [self.test_user2]

        self.test_studio.scheduler = tj_scheduler
        self.test_studio.schedule()
        db.DBSession.commit()

        # now check the timings of the tasks are all adjusted

        # Projects
        # print "%s:self.test_project" % self.test_project.id
        # print "%s:self.test_project2" % self.test_project2.id
        # print "%s:self.test_project3" % self.test_project3.id
        #
        # print "%s:self.test_asset1" % self.test_asset1.id
        # print "%s:self.test_asset2" % self.test_asset2.id
        #
        # print "%s:self.test_shot1.id" % self.test_shot1.id
        # print "%s:self.test_shot2.id" % self.test_shot2.id
        # print "%s:self.test_shot3.id" % self.test_shot3.id
        # print "%s:self.test_shot4.id" % self.test_shot4.id
        # print "%s:self.test_shot5.id" % self.test_shot5.id
        #
        # print "%s:self.test_task1.id" % self.test_task1.id
        # print "%s:self.test_task2.id" % self.test_task2.id
        # print "%s:self.test_task3.id" % self.test_task3.id
        # print "%s:self.test_task4.id" % self.test_task4.id
        # print "%s:self.test_task5.id" % self.test_task5.id
        # print "%s:self.test_task6.id" % self.test_task6.id
        # print "%s:self.test_task7.id" % self.test_task7.id
        # print "%s:self.test_task8.id" % self.test_task8.id
        # print "%s:self.test_task9.id" % self.test_task9.id
        #
        # print "%s:self.test_task10.id" % self.test_task10.id
        # print "%s:self.test_task11.id" % self.test_task11.id
        # print "%s:self.test_task12.id" % self.test_task12.id
        # print "%s:self.test_task13.id" % self.test_task13.id
        # print "%s:self.test_task14.id" % self.test_task14.id
        # print "%s:self.test_task15.id" % self.test_task15.id
        # print "%s:self.test_task16.id" % self.test_task16.id
        # print "%s:self.test_task17.id" % self.test_task17.id
        # print "%s:self.test_task18.id" % self.test_task18.id
        # print "%s:self.test_task19.id" % self.test_task19.id
        #
        # print "%s:self.test_task20.id" % self.test_task20.id
        # print "%s:self.test_task21.id" % self.test_task21.id
        # print "%s:self.test_task22.id" % self.test_task22.id
        # print "%s:self.test_task23.id" % self.test_task23.id
        # print "%s:self.test_task24.id" % self.test_task24.id
        # print "%s:self.test_task25.id" % self.test_task25.id
        # print "%s:self.test_task26.id" % self.test_task26.id
        # print "%s:self.test_task27.id" % self.test_task27.id
        # print "%s:self.test_task28.id" % self.test_task28.id
        # print "%s:self.test_task29.id" % self.test_task29.id
        # print "%s:self.test_task30.id" % self.test_task30.id
        # print "%s:self.test_task31.id" % self.test_task31.id

        # self.test_project
        self.assertEqual(
            datetime.datetime(2013, 4, 16, 9, 0),
            self.test_project1.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 19, 11, 0),
            self.test_project1.computed_end
        )

        # self.test_asset1
        self.assertEqual(
            datetime.datetime(2013, 4, 16, 9, 0),
            self.test_asset1.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 5, 17, 10, 0),
            self.test_asset1.computed_end
        )

        self.assertEqual(
            self.test_asset1.computed_resources,
            []
        )

        # self.test_task24
        self.assertEqual(
            datetime.datetime(2013, 4, 16, 9, 0),
            self.test_task24.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 4, 26, 17, 0),
            self.test_task24.computed_end
        )

        self.assertEqual(
            self.test_task24.computed_resources,
            [self.test_user1]
        )

        # self.test_task25
        self.assertEqual(
            datetime.datetime(2013, 4, 16, 9, 0),
            self.test_task25.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 5, 3, 12, 0),
            self.test_task25.computed_end
        )

        self.assertEqual(
            self.test_task25.computed_resources,
            [self.test_user3]
        )

        # self.test_task26
        self.assertEqual(
            datetime.datetime(2013, 5, 3, 12, 0),
            self.test_task26.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 5, 16, 11, 0),
            self.test_task26.computed_end
        )

        self.assertEqual(
            self.test_task26.computed_resources,
            [self.test_user3]
        )

        # self.test_task27
        self.assertEqual(
            datetime.datetime(2013, 5, 6, 11, 0),
            self.test_task27.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 5, 17, 10, 0),
            self.test_task27.computed_end
        )

        self.assertEqual(
            self.test_task27.computed_resources,
            [self.test_user2]
        )

        # self.test_shot2
        self.assertEqual(
            datetime.datetime(2013, 4, 26, 17, 0),
            self.test_shot2.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 14, 14, 0),
            self.test_shot2.computed_end
        )

        self.assertEqual(
            self.test_shot2.computed_resources,
            []
        )

        # self.test_task8
        self.assertEqual(
            datetime.datetime(2013, 4, 26, 17, 0),
            self.test_task8.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 4, 30, 15, 0),
            self.test_task8.computed_end
        )

        self.assertEqual(
            self.test_task8.computed_resources,
            [self.test_user2]
        )

        # self.test_task9
        self.assertEqual(
            datetime.datetime(2013, 5, 30, 9, 0),
            self.test_task9.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 5, 31, 16, 0),
            self.test_task9.computed_end
        )

        self.assertEqual(
            self.test_task9.computed_resources,
            [self.test_user2]
        )

        # self.test_task10
        self.assertEqual(
            datetime.datetime(2013, 6, 4, 14, 0),
            self.test_task10.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 7, 11, 0),
            self.test_task10.computed_end
        )

        self.assertEqual(
            self.test_task10.computed_resources,
            [self.test_user2]
        )

        # self.test_task11
        self.assertEqual(
            datetime.datetime(2013, 6, 11, 9, 0),
            self.test_task11.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 14, 14, 0),
            self.test_task11.computed_end
        )

        self.assertEqual(
            self.test_task11.computed_resources,
            [self.test_user3]
        )

        # self.test_shot1
        self.assertEqual(
            datetime.datetime(2013, 5, 16, 11, 0),
            self.test_shot1.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 19, 11, 0),
            self.test_shot1.computed_end
        )

        self.assertEqual(
            self.test_shot1.computed_resources,
            []
        )

        # self.test_task4
        self.assertEqual(
            datetime.datetime(2013, 5, 16, 11, 0),
            self.test_task4.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 5, 17, 18, 0),
            self.test_task4.computed_end
        )

        self.assertEqual(
            self.test_task4.computed_resources,
            [self.test_user1]
        )

        # self.test_task5
        self.assertEqual(
            datetime.datetime(2013, 6, 3, 15, 0),
            self.test_task5.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 5, 13, 0),
            self.test_task5.computed_end
        )

        self.assertEqual(
            self.test_task5.computed_resources,
            [self.test_user1]
        )

        # self.test_task6
        self.assertEqual(
            datetime.datetime(2013, 6, 10, 10, 0),
            self.test_task6.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 12, 16, 0),
            self.test_task6.computed_end
        )

        self.assertEqual(
            self.test_task6.computed_resources,
            [self.test_user1]
        )

        # self.test_task7
        self.assertEqual(
            datetime.datetime(2013, 6, 14, 14, 0),
            self.test_task7.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 19, 11, 0),
            self.test_task7.computed_end
        )

        self.assertEqual(
            self.test_task7.computed_resources,
            [self.test_user3]
        )

        # self.test_task1
        self.assertEqual(
            datetime.datetime(2013, 5, 16, 11, 0),
            self.test_task1.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 5, 29, 10, 0),
            self.test_task1.computed_end
        )

        self.assertEqual(
            self.test_task1.computed_resources,
            [self.test_user3]
        )

        # self.test_project2
        # self.assertEqual(
        #     datetime.datetime(2013, 4, 16, 9, 0),
        #     self.test_project2.computed_start
        # )
        # self.assertEqual(
        #     datetime.datetime(2013, 6, 18, 12, 0),
        #     self.test_project2.computed_end
        # )

        # self.assertEqual(
        #     self.test_project2.computed_resources,
        #     []
        # )

        # self.test_asset2
        self.assertEqual(
            datetime.datetime(2013, 4, 16, 9, 0),
            self.test_asset2.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 5, 30, 17, 0),
            self.test_asset2.computed_end
        )

        self.assertEqual(
            self.test_asset2.computed_resources,
            []
        )

        # self.test_task28
        self.assertEqual(
            datetime.datetime(2013, 4, 16, 9, 0),
            self.test_task28.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 4, 26, 17, 0),
            self.test_task28.computed_end
        )

        self.assertEqual(
            self.test_task28.computed_resources,
            [self.test_user2]
        )

        # self.test_task29
        self.assertEqual(
            datetime.datetime(2013, 4, 26, 17, 0),
            self.test_task29.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 5, 16, 11, 0),
            self.test_task29.computed_end
        )

        self.assertEqual(
            self.test_task29.computed_resources,
            [self.test_user1]
        )

        # self.test_task30
        self.assertEqual(
            datetime.datetime(2013, 5, 17, 10, 0),
            self.test_task30.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 5, 29, 18, 0),
            self.test_task30.computed_end
        )

        self.assertEqual(
            self.test_task30.computed_resources,
            [self.test_user2]
        )

        # self.test_task31
        self.assertEqual(
            datetime.datetime(2013, 5, 20, 9, 0),
            self.test_task31.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 5, 30, 17, 0),
            self.test_task31.computed_end
        )

        self.assertEqual(
            self.test_task31.computed_resources,
            [self.test_user1]
        )

        # self.test_shot3
        self.assertEqual(
            datetime.datetime(2013, 4, 30, 15, 0),
            self.test_shot3.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 17, 13, 0),
            self.test_shot3.computed_end
        )

        self.assertEqual(
            self.test_shot3.computed_resources,
            []
        )

        # self.test_task12
        self.assertEqual(
            datetime.datetime(2013, 4, 30, 15, 0),
            self.test_task12.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 5, 2, 13, 0),
            self.test_task12.computed_end
        )

        self.assertEqual(
            self.test_task12.computed_resources,
            [self.test_user2]
        )

        # self.test_task13
        self.assertEqual(
            datetime.datetime(2013, 5, 30, 17, 0),
            self.test_task13.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 3, 15, 0),
            self.test_task13.computed_end
        )

        self.assertEqual(
            self.test_task13.computed_resources,
            [self.test_user1]
        )

        # self.test_task14
        self.assertEqual(
            datetime.datetime(2013, 6, 5, 13, 0),
            self.test_task14.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 10, 10, 0),
            self.test_task14.computed_end
        )

        self.assertEqual(
            self.test_task14.computed_resources,
            [self.test_user1]
        )

        # self.test_task15
        self.assertEqual(
            datetime.datetime(2013, 6, 11, 17, 0),
            self.test_task15.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 17, 13, 0),
            self.test_task15.computed_end
        )

        self.assertEqual(
            self.test_task15.computed_resources,
            [self.test_user2]
        )

        # self.test_shot4
        self.assertEqual(
            datetime.datetime(2013, 5, 2, 13, 0),
            self.test_shot4.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 18, 12, 0),
            self.test_shot4.computed_end
        )

        self.assertEqual(
            self.test_shot4.computed_resources,
            []
        )

        # self.test_task16
        self.assertEqual(
            datetime.datetime(2013, 5, 2, 13, 0),
            self.test_task16.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 5, 6, 11, 0),
            self.test_task16.computed_end
        )

        self.assertEqual(
            self.test_task16.computed_resources,
            [self.test_user2]
        )

        # self.test_task17
        self.assertEqual(
            datetime.datetime(2013, 5, 31, 16, 0),
            self.test_task17.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 4, 14, 0),
            self.test_task17.computed_end
        )

        self.assertEqual(
            self.test_task17.computed_resources,
            [self.test_user2]
        )

        # self.test_task18
        self.assertEqual(
            datetime.datetime(2013, 6, 7, 11, 0),
            self.test_task18.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 11, 17, 0),
            self.test_task18.computed_end
        )

        self.assertEqual(
            self.test_task18.computed_resources,
            [self.test_user2]
        )

        # self.test_task19
        self.assertEqual(
            datetime.datetime(2013, 6, 12, 16, 0),
            self.test_task19.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 18, 12, 0),
            self.test_task19.computed_end
        )

        self.assertEqual(
            self.test_task19.computed_resources,
            [self.test_user1]
        )

        # self.test_task2
        self.assertEqual(
            datetime.datetime(2013, 5, 29, 10, 0),
            self.test_task2.computed_start
        )
        self.assertEqual(
            datetime.datetime(2013, 6, 10, 18, 0),
            self.test_task2.computed_end
        )

        self.assertEqual(
            self.test_task2.computed_resources,
            [self.test_user3]
        )

    def test_schedule_will_schedule_only_the_tasks_of_the_given_projects_with_the_given_scheduler(self):
        """testing if the schedule method will schedule the tasks of the given
        projects with the given scheduler
        """
        # create a dummy Project to schedule
        dummy_project = Project(
            name='Dummy Project',
            code='DP',
            repository=self.test_repo
        )

        dt1 = Task(
            name='Dummy Task 1',
            project=dummy_project,
            schedule_timing=4,
            schedule_unit='h',
            resources=[self.test_user1]
        )

        dt2 = Task(
            name='Dummy Task 2',
            project=dummy_project,
            schedule_timing=4,
            schedule_unit='h',
            resources=[self.test_user2]
        )
        db.DBSession.add_all([dummy_project, dt1, dt2])
        db.DBSession.commit()

        tj_scheduler = TaskJugglerScheduler(
            compute_resources=True,
            projects=[dummy_project]
        )

        self.test_studio.now = datetime.datetime(2013, 4, 15, 22, 56)
        self.test_studio.start = datetime.datetime(2013, 4, 15, 22, 56)
        self.test_studio.end = datetime.datetime(2013, 7, 30, 0, 0)

        self.test_studio.scheduler = tj_scheduler
        self.test_studio.schedule()
        db.DBSession.commit()

        # now check the timings of the tasks are all adjusted
        self.assertEqual(
            dt1.computed_start,
            datetime.datetime(2013, 4, 16, 9, 0)
        )
        self.assertEqual(
            dt1.computed_end,
            datetime.datetime(2013, 4, 16, 13, 0)
        )

        self.assertEqual(
            dt2.computed_start,
            datetime.datetime(2013, 4, 16, 9, 0)
        )
        self.assertEqual(
            dt2.computed_end,
            datetime.datetime(2013, 4, 16, 13, 0)
        )

        # self.test_project
        self.assertEqual(self.test_project1.computed_start, None)
        self.assertEqual(self.test_project1.computed_end, None)

        # self.test_asset1
        self.assertEqual(self.test_asset1.computed_start, None)
        self.assertEqual(self.test_asset1.computed_end, None)

        self.assertEqual(self.test_asset1.computed_resources,
                         self.test_asset1.resources)

        # self.test_task24
        self.assertEqual(self.test_task24.computed_start, None)
        self.assertEqual(self.test_task24.computed_end, None)

        self.assertEqual(self.test_task24.computed_resources,
                         self.test_task24.resources)

        # self.test_task25
        self.assertEqual(self.test_task25.computed_start, None)
        self.assertEqual(self.test_task25.computed_end, None)

        self.assertEqual(self.test_task25.computed_resources,
                         self.test_task25.resources)

        # self.test_task26
        self.assertEqual(self.test_task26.computed_start, None)
        self.assertEqual(self.test_task26.computed_end, None)

        self.assertEqual(self.test_task26.computed_resources,
                         self.test_task26.resources)

        # self.test_task27
        self.assertEqual(self.test_task27.computed_start, None)
        self.assertEqual(self.test_task27.computed_end, None)

        self.assertEqual(self.test_task27.computed_resources,
                         self.test_task27.resources)

        # self.test_shot2
        self.assertEqual(self.test_shot2.computed_start, None)
        self.assertEqual(self.test_shot2.computed_end, None)

        self.assertEqual(self.test_shot2.computed_resources,
                         self.test_shot2.resources)

        # self.test_task8
        self.assertEqual(self.test_task8.computed_start, None)
        self.assertEqual(self.test_task8.computed_end, None)

        self.assertEqual(self.test_task8.computed_resources,
                         self.test_task8.resources)

        # self.test_task9
        self.assertEqual(self.test_task9.computed_start, None)
        self.assertEqual(self.test_task9.computed_end, None)

        self.assertEqual(self.test_task9.computed_resources,
                         self.test_task9.resources)

        # self.test_task10
        self.assertEqual(self.test_task10.computed_start, None)
        self.assertEqual(self.test_task10.computed_end, None)

        self.assertEqual(self.test_task10.computed_resources,
                         self.test_task10.resources)

        # self.test_task11
        self.assertEqual(self.test_task11.computed_start, None)
        self.assertEqual(self.test_task11.computed_end, None)

        self.assertEqual(self.test_task11.computed_resources,
                         self.test_task11.resources)

        # self.test_shot1
        self.assertEqual(self.test_shot1.computed_start, None)
        self.assertEqual(self.test_shot1.computed_end, None)

        self.assertEqual(self.test_shot1.computed_resources,
                         self.test_shot1.resources)

        # self.test_task4
        self.assertEqual(self.test_task4.computed_start, None)
        self.assertEqual(self.test_task4.computed_end, None)

        self.assertEqual(self.test_task4.computed_resources,
                         self.test_task4.resources)

        # self.test_task5
        self.assertEqual(self.test_task5.computed_start, None)
        self.assertEqual(self.test_task5.computed_end, None)

        self.assertEqual(self.test_task5.computed_resources,
                         self.test_task5.resources)

        # self.test_task6
        self.assertEqual(self.test_task6.computed_start, None)
        self.assertEqual(self.test_task6.computed_end, None)

        self.assertEqual(self.test_task6.computed_resources,
                         self.test_task6.resources)

        # self.test_task7
        self.assertEqual(self.test_task7.computed_start, None)
        self.assertEqual(self.test_task7.computed_end, None)

        self.assertEqual(self.test_task7.computed_resources,
                         self.test_task7.resources)

        # self.test_task1
        self.assertEqual(self.test_task1.computed_start, None)
        self.assertEqual(self.test_task1.computed_end, None)

        self.assertEqual(self.test_task1.computed_resources,
                         self.test_task1.resources)

        # self.test_asset2
        self.assertEqual(self.test_asset2.computed_start, None)
        self.assertEqual(self.test_asset2.computed_end, None)

        self.assertEqual(self.test_asset2.computed_resources,
                         self.test_asset2.resources)

        # self.test_task28
        self.assertEqual(self.test_task28.computed_start, None)
        self.assertEqual(self.test_task28.computed_end, None)

        self.assertEqual(self.test_task28.computed_resources,
                         self.test_task28.resources)

        # self.test_task29
        self.assertEqual(self.test_task29.computed_start, None)
        self.assertEqual(self.test_task29.computed_end, None)

        self.assertEqual(self.test_task29.computed_resources,
                         self.test_task29.resources)

        # self.test_task30
        self.assertEqual(self.test_task30.computed_start, None)
        self.assertEqual(self.test_task30.computed_end, None)

        self.assertEqual(self.test_task30.computed_resources,
                         self.test_task30.resources)

        # self.test_task31
        self.assertEqual(self.test_task31.computed_start, None)
        self.assertEqual(self.test_task31.computed_end, None)

        self.assertEqual(self.test_task31.computed_resources,
                         self.test_task31.resources)

        # self.test_shot3
        self.assertEqual(self.test_shot3.computed_start, None)
        self.assertEqual(self.test_shot3.computed_end, None)

        self.assertEqual(self.test_shot3.computed_resources,
                         self.test_shot3.resources)

        # self.test_task12
        self.assertEqual(self.test_task12.computed_start, None)
        self.assertEqual(self.test_task12.computed_end, None)

        self.assertEqual(self.test_task12.computed_resources,
                         self.test_task12.resources)

        # self.test_task13
        self.assertEqual(self.test_task13.computed_start, None)
        self.assertEqual(self.test_task13.computed_end, None)

        self.assertEqual(self.test_task13.computed_resources,
                         self.test_task13.resources)

        # self.test_task14
        self.assertEqual(self.test_task14.computed_start, None)
        self.assertEqual(self.test_task14.computed_end, None)

        self.assertEqual(self.test_task14.computed_resources,
                         self.test_task14.resources)

        # self.test_task15
        self.assertEqual(self.test_task15.computed_start, None)
        self.assertEqual(self.test_task15.computed_end, None)

        self.assertEqual(self.test_task15.computed_resources,
                         self.test_task15.resources)

        # self.test_shot4
        self.assertEqual(self.test_shot4.computed_start, None)
        self.assertEqual(self.test_shot4.computed_end, None)

        self.assertEqual(self.test_shot4.computed_resources,
                         self.test_shot4.resources)

        # self.test_task16
        self.assertEqual(self.test_task16.computed_start, None)
        self.assertEqual(self.test_task16.computed_end, None)

        self.assertEqual(self.test_task16.computed_resources,
                         self.test_task16.resources)

        # self.test_task17
        self.assertEqual(self.test_task17.computed_start, None)
        self.assertEqual(self.test_task17.computed_end, None)

        self.assertEqual(self.test_task17.computed_resources,
                         self.test_task17.resources)

        # self.test_task18
        self.assertEqual(self.test_task18.computed_start, None)
        self.assertEqual(self.test_task18.computed_end, None)

        self.assertEqual(self.test_task18.computed_resources,
                         self.test_task18.resources)

        # self.test_task19
        self.assertEqual(self.test_task19.computed_start, None)
        self.assertEqual(self.test_task19.computed_end, None)

        self.assertEqual(self.test_task19.computed_resources,
                         self.test_task19.resources)

        # self.test_task2
        self.assertEqual(self.test_task2.computed_start, None)
        self.assertEqual(self.test_task2.computed_end, None)

        self.assertEqual(self.test_task2.computed_resources,
                         self.test_task2.resources)

# def test_schedule_will_raise_a_RuntimeError_if_is_scheduling_is_True(self):
    #     """testing if a RuntimeError will be raised when the schedule method
    #     is called and the is_scheduling attribute is True
    #     """
    #     tj_scheduler = TaskJugglerScheduler()
    #     self.test_studio.now = datetime.datetime(2013, 4, 15, 22, 56)
    #     self.test_studio.start = datetime.datetime(2013, 4, 15, 22, 56)
    #     self.test_studio.end = datetime.datetime(2013, 7, 30, 0, 0)
    #
    #     self.test_studio.scheduler = tj_scheduler
    #     self.test_studio.is_scheduling = True
    #     self.test_studio.is_scheduling_by = self.test_user1
    #     self.assertRaises(RuntimeError, self.test_studio.schedule)

    def test_is_scheduling_will_be_False_after_scheduling_is_done(self):
        """testing if the is_scheduling attribute will be back to False when
        the scheduling is finished
        """
        # use a dummy scheduler
        self.test_studio.now = datetime.datetime(2013, 4, 15, 22, 56)
        self.test_studio.start = datetime.datetime(2013, 4, 15, 22, 56)
        self.test_studio.end = datetime.datetime(2013, 7, 30, 0, 0)

        def callback():
            self.assertTrue(self.test_studio.is_scheduling)

        dummy_scheduler = DummyScheduler(callback=callback)

        self.test_studio.scheduler = dummy_scheduler
        self.assertFalse(self.test_studio.is_scheduling)

        # with v0.2.6.9 it is now the users duty to set is_scheduling to True
        self.test_studio.is_scheduling = True

        self.test_studio.schedule()
        self.assertFalse(self.test_studio.is_scheduling)

    def test_schedule_will_store_schedule_info_in_database(self):
        """testing if the schedule method will store the schedule info in
        database
        """
        tj_scheduler = TaskJugglerScheduler()
        self.test_studio.now = datetime.datetime(2013, 4, 15, 22, 56)
        self.test_studio.start = datetime.datetime(2013, 4, 15, 22, 56)
        self.test_studio.end = datetime.datetime(2013, 7, 30, 0, 0)

        self.test_studio.scheduler = tj_scheduler
        self.test_studio.schedule(scheduled_by=self.test_user1)

        self.assertEqual(self.test_studio.last_scheduled_by, self.test_user1)

        last_schedule_message = self.test_studio.last_schedule_message
        last_scheduled_at = self.test_studio.last_scheduled_at
        last_scheduled_by = self.test_studio.last_scheduled_by

        self.assertTrue(last_schedule_message is not None)
        self.assertTrue(last_scheduled_at is not None)
        self.assertTrue(last_scheduled_by is not None)

        db.DBSession.add(self.test_studio)
        db.DBSession.commit()

        # delete the studio instance and retrieve it back and check if it has
        # the info
        del self.test_studio

        studio = Studio.query.first()

        self.assertFalse(studio.is_scheduling)
        self.assertTrue(
            datetime.datetime.now() - studio.scheduling_started_at <
            datetime.timedelta(minutes=1)
        )
        self.assertEqual(last_schedule_message, studio.last_schedule_message)
        self.assertEqual(last_scheduled_at, studio.last_scheduled_at)
        self.assertEqual(last_scheduled_by, studio.last_scheduled_by)

        self.assertEqual(studio.last_scheduled_by_id, self.test_user1.id)
        self.assertEqual(studio.last_scheduled_by, self.test_user1)

    def test_vacation_attribute_is_read_only(self):
        """testing if the vacation attribute is a read-only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_studio,
                          'vacations', 'some random value')

    def test_vacation_attribute_returns_studio_vacation_instances(self):
        """Testing if the vacation attribute is returning the Vacation
        instances with no user set.
        """
        from stalker.models.studio import Vacation

        vacation1 = Vacation(
            start=datetime.datetime(2013, 8, 2),
            end=datetime.datetime(2013, 8, 10)
        )
        vacation2 = Vacation(
            start=datetime.datetime(2013, 8, 11),
            end=datetime.datetime(2013, 8, 20)
        )
        vacation3 = Vacation(
            user=self.test_user1,
            start=datetime.datetime(2013, 8, 11),
            end=datetime.datetime(2013, 8, 20)
        )
        DBSession.add_all([vacation1, vacation2, vacation3])
        DBSession.commit()

        self.assertEqual(
            sorted(self.test_studio.vacations, key=lambda x: x.name),
            sorted([vacation1, vacation2], key=lambda x: x.name)
        )

    def test_timing_resolution_argument_skipped(self):
        """testing if the timing_resolution attribute will be set to the
        default value from the defaults.timing_resolution if timing_resolution
        argument is skipped
        """
        try:
            self.kwargs.pop('timing_resolution')
        except KeyError:
            pass

        studio = Studio(**self.kwargs)
        self.assertEqual(
            studio.timing_resolution,
            defaults.timing_resolution
        )

    # def test_timing_resolution_argument_skipped_Studio_is_present(self):
    #     """testing if the timing_resolution attribute will be set to the Studio
    #     timing resolution if timing_resolution argument is skipped and there is
    #     a Studio instance
    #     """
    #     try:
    #         self.kwargs.pop('timing_resolution')
    #     except KeyError:
    #         pass
    # 
    #     from stalker import Studio
    #     db.setup({'sqlalchemy.url': 'sqlite:///:memory:'})
    #     studio = Studio(
    #         name='Test Studio',
    #         timing_resolution=datetime.timedelta(minutes=15)
    #     )
    #     DBSession.add(studio)
    #     DBSession.commit()
    # 
    #     new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
    #     self.assertEqual(
    #         new_foo_obj.timing_resolution,
    #         studio.timing_resolution
    #     )

    def test_timing_resolution_argument_is_None(self):
        """testing if the timing_resolution attribute will be set to the
        default value from the default.timing_resolution if timing_resolution
        argument is None
        """
        self.kwargs['timing_resolution'] = None
        studio = Studio(**self.kwargs)
        self.assertEqual(
            studio.timing_resolution,
            defaults.timing_resolution
        )

    # def test_timing_resolution_argument_is_None_Studio_is_present(self):
    #     """testing if the timing_resolution attribute will be set to the
    #     default value from the Studio.timing_resolution if timing_resolution
    #     argument is None and there is a Studio
    #     """
    #     self.kwargs['timing_resolution'] = None
    # 
    #     from stalker import Studio
    #     db.setup({'sqlalchemy.url': 'sqlite:///:memory:'})
    #     studio = Studio(
    #         name='Test Studio',
    #         timing_resolution=datetime.timedelta(minutes=15)
    #     )
    #     DBSession.add(studio)
    #     DBSession.commit()
    # 
    #     new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
    #     self.assertEqual(
    #         new_foo_obj.timing_resolution,
    #         studio.timing_resolution
    #     )

    def test_timing_resolution_attribute_is_set_to_None(self):
        """testing if the timing_resolution attribute will be set to the
        default value from the defaults.timing_resolution if it is set to None
        """
        self.kwargs['timing_resolution'] = datetime.timedelta(minutes=5)
        studio = Studio(**self.kwargs)
        # check start conditions
        self.assertEqual(
            studio.timing_resolution,
            self.kwargs['timing_resolution']
        )
        studio.timing_resolution = None
        self.assertEqual(
            studio.timing_resolution,
            defaults.timing_resolution
        )

    # def test_timing_resolution_attribute_is_set_to_None_Studio_is_present(self):
    #     """testing if the timing_resolution attribute will be set to the
    #     default value from the Studio.timing_resolution if it is set to None
    #     and there is a Studio instance
    #     """
    #     from stalker import Studio
    #     db.setup({'sqlalchemy.url': 'sqlite:///:memory:'})
    #     studio = Studio(
    #         name='Test Studio',
    #         resolution=datetime.timedelta(minutes=15)
    #     )
    #     session.add(studio)
    #     session.commit()
    # 
    #     self.kwargs['timing_resolution'] = datetime.timedelta(minutes=5)
    #     new_foo_obj = DateRangeMixFooMixedInClass(**self.kwargs)
    #     # check start conditions
    #     self.assertEqual(new_foo_obj.timing_resolution,
    #                      self.kwargs['timing_resolution'])
    #     new_foo_obj.timing_resolution = None
    #     self.assertEqual(
    #         studio.timing_resolution,
    #         datetime.timedelta(minutes=15)
    #     )
    #     self.assertEqual(
    #         new_foo_obj.timing_resolution,
    #         studio.timing_resolution
    #     )

    def test_timing_resolution_argument_is_not_a_timedelta_instance(self):
        """testing if a TypeError will be raised when the timing_resolution
        argument is not a datetime.timedelta instance
        """
        self.kwargs['timing_resolution'] = 'not a timedelta instance'
        self.assertRaises(TypeError, Studio, **self.kwargs)

    def test_timing_resolution_attribute_is_not_a_timedelta_instance(self):
        """testing if a TypeError will be raised when the timing_resolution
        attribute is not a datetime.timedelta instance
        """
        new_foo_obj = Studio(**self.kwargs)
        self.assertRaises(TypeError, setattr, new_foo_obj, 'timing_resolution',
                          'not a timedelta instance')

    def test_timing_resolution_argument_is_working_properly(self):
        """testing if the timing_resolution argument value is passed to
        timing_resolution attribute correctly
        """
        self.kwargs['timing_resolution'] = datetime.timedelta(minutes=5)
        studio = Studio(**self.kwargs)
        self.assertEqual(
            studio.timing_resolution,
            self.kwargs['timing_resolution']
        )

    def test_timing_resolution_attribute_is_working_properly(self):
        """testing if the timing_resolution attribute is working properly
        """
        studio = Studio(**self.kwargs)
        res = studio
        new_res = datetime.timedelta(hours=1, minutes=30)
        self.assertNotEqual(res, new_res)
        studio.timing_resolution = new_res
        self.assertEqual(studio.timing_resolution, new_res)


@unittest.skip
def csv_to_test_converter():
    """convert tjp output csv to test case
    """
    #!/usr/bin/python

    import re
    import jinja2

    ids = """28:self.test_user1
    29:self.test_user2
    30:self.test_user3
    38:self.test_project
    39:self.test_project2
    40:self.test_project3
    41:self.test_asset1
    42:self.test_asset2
    43:self.test_shot1
    44:self.test_shot2
    45:self.test_shot3
    46:self.test_shot4
    47:self.test_shot5
    48:self.test_task1
    49:self.test_task2
    50:self.test_task3
    51:self.test_task4
    52:self.test_task5
    53:self.test_task6
    54:self.test_task7
    55:self.test_task8
    56:self.test_task9
    57:self.test_task10
    58:self.test_task11
    59:self.test_task12
    60:self.test_task13
    61:self.test_task14
    62:self.test_task15
    63:self.test_task16
    64:self.test_task17
    65:self.test_task18
    66:self.test_task19
    67:self.test_task20
    68:self.test_task21
    69:self.test_task22
    70:self.test_task23
    71:self.test_task24
    72:self.test_task25
    73:self.test_task26
    74:self.test_task27
    75:self.test_task28
    76:self.test_task29
    77:self.test_task30
    78:self.test_task31"""

    ids_to_name = {}
    for line in ids.split('\n'):
        id_, name = line.split(':')
        ids_to_name[id_] = name

    raw_data = '''"Project_38";"2013-04-16-09:00";"2013-06-19-11:00";""
    "Project_38.Asset_41";"2013-04-16-09:00";"2013-05-17-10:00";""
    "Project_38.Asset_41.Task_71";"2013-04-16-09:00";"2013-04-26-17:00";"User 1 (User_28)"
    "Project_38.Asset_41.Task_72";"2013-04-16-09:00";"2013-05-03-12:00";"User 3 (User_30)"
    "Project_38.Asset_41.Task_73";"2013-05-03-12:00";"2013-05-16-11:00";"User 3 (User_30)"
    "Project_38.Asset_41.Task_74";"2013-05-06-11:00";"2013-05-17-10:00";"User 2 (User_29)"
    "Project_38.Shot_44";"2013-04-26-17:00";"2013-06-14-14:00";""
    "Project_38.Shot_44.Task_55";"2013-04-26-17:00";"2013-04-30-15:00";"User 2 (User_29)"
    "Project_38.Shot_44.Task_56";"2013-05-30-09:00";"2013-05-31-16:00";"User 2 (User_29)"
    "Project_38.Shot_44.Task_57";"2013-06-04-14:00";"2013-06-07-11:00";"User 2 (User_29)"
    "Project_38.Shot_44.Task_58";"2013-06-11-09:00";"2013-06-14-14:00";"User 3 (User_30)"
    "Project_38.Shot_43";"2013-05-16-11:00";"2013-06-19-11:00";""
    "Project_38.Shot_43.Task_51";"2013-05-16-11:00";"2013-05-17-18:00";"User 1 (User_28)"
    "Project_38.Shot_43.Task_52";"2013-06-03-15:00";"2013-06-05-13:00";"User 1 (User_28)"
    "Project_38.Shot_43.Task_53";"2013-06-10-10:00";"2013-06-12-16:00";"User 1 (User_28)"
    "Project_38.Shot_43.Task_54";"2013-06-14-14:00";"2013-06-19-11:00";"User 3 (User_30)"
    "Project_38.Task_48";"2013-05-16-11:00";"2013-05-29-10:00";"User 3 (User_30)"
    "Project_39";"2013-04-16-09:00";"2013-06-18-12:00";""
    "Project_39.Asset_42";"2013-04-16-09:00";"2013-05-30-17:00";""
    "Project_39.Asset_42.Task_75";"2013-04-16-09:00";"2013-04-26-17:00";"User 2 (User_29)"
    "Project_39.Asset_42.Task_76";"2013-04-26-17:00";"2013-05-16-11:00";"User 1 (User_28)"
    "Project_39.Asset_42.Task_77";"2013-05-17-10:00";"2013-05-29-18:00";"User 2 (User_29)"
    "Project_39.Asset_42.Task_78";"2013-05-20-09:00";"2013-05-30-17:00";"User 1 (User_28)"
    "Project_39.Shot_45";"2013-04-30-15:00";"2013-06-17-13:00";""
    "Project_39.Shot_45.Task_59";"2013-04-30-15:00";"2013-05-02-13:00";"User 2 (User_29)"
    "Project_39.Shot_45.Task_60";"2013-05-30-17:00";"2013-06-03-15:00";"User 1 (User_28)"
    "Project_39.Shot_45.Task_61";"2013-06-05-13:00";"2013-06-10-10:00";"User 1 (User_28)"
    "Project_39.Shot_45.Task_62";"2013-06-11-17:00";"2013-06-17-13:00";"User 2 (User_29)"
    "Project_39.Shot_46";"2013-05-02-13:00";"2013-06-18-12:00";""
    "Project_39.Shot_46.Task_63";"2013-05-02-13:00";"2013-05-06-11:00";"User 2 (User_29)"
    "Project_39.Shot_46.Task_64";"2013-05-31-16:00";"2013-06-04-14:00";"User 2 (User_29)"
    "Project_39.Shot_46.Task_65";"2013-06-07-11:00";"2013-06-11-17:00";"User 2 (User_29)"
    "Project_39.Shot_46.Task_66";"2013-06-12-16:00";"2013-06-18-12:00";"User 1 (User_28)"
    "Project_39.Task_49";"2013-05-29-10:00";"2013-06-10-18:00";"User 3 (User_30)"'''

    lines = raw_data.split('\n')

    template_string = """        # {{entity_name}}
            self.assertEqual(
                datetime.datetime({{start_date}}),
                {{entity_name}}.computed_start
            )
            self.assertEqual(
                datetime.datetime({{end_date}}),
                {{entity_name}}.computed_end
            )
            {% if resources %}
            self.assertEqual(
                sorted({{entity_name}}.computed_resources, key=lambda x: x.name),
                soretd([{% for r in resources -%}
                {{r}}{% if loop.index != 1%},{% endif %}
                {%- endfor %}], key=lambda x: x.name)
            )
            {% endif %}
    """

    rendered_data = []
    template = jinja2.Template(template_string)
    for i, line in enumerate(lines):
        line = re.subn('[\s]+', ' ', line)[0]
        line = line.replace('"', '')

        data = line.split(';')

        entity_id = data[0].split('_')[-1]
        entity_name = ids_to_name[entity_id]

        start_date = ', '.join(
            data[1]
            .replace(':', '-')
            .replace('-0', '-')
            .replace('00', '0')
            .split('-')
        )

        end_date = ', '.join(
            data[2]
            .replace(':', '-')
            .replace('-0', '-')
            .replace('00', '0')
            .split('-')
        )

        resource_id = data[3].split('_')[-1][:-1]
        resource_name = ''
        if resource_id:
            resource_name = ids_to_name[resource_id]

        resources = [resource_name]

        #print entity_name, start_date, end_date, resources

        rendered_template = template.render(**{
            'entity_name': entity_name,
            'start_date': start_date,
            'end_date': end_date,
            'resources': resources
        })
        rendered_data.append(rendered_template)

    for r in rendered_data:
        print(r)
