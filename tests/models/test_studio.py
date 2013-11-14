# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
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

import unittest2
import datetime
from stalker import (defaults, Studio, WorkingHours, Project, StatusList,
                     Status, Repository, Asset, Type, User, Shot, Department,
                     Task, TaskJugglerScheduler)
from stalker import db
from stalker.db import DBSession

# for IDEs to help them in code compilation
if False:
    from sqlalchemy.orm import Session

    assert isinstance(DBSession, Session)


class StudioTester(unittest2.TestCase):
    """tests the stalker.models.studio.Studio class
    """

    @classmethod
    def setUpClass(cls):
        """setup the test
        """
        DBSession.configure(extension=None)

    @classmethod
    def tearDownClass(cls):
        """cleanup the test
        """
        DBSession.configure(extension=None)

    def setUp(self):
        """setup the test
        """
        db.setup({
            "sqlalchemy.url": "sqlite:///:memory:",
            "sqlalchemy.echo": False,
        })
        # db.init()

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
            name='ProjectStatuses',
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

        self.test_asset_status_list = StatusList(
            name='AssetStatuses',
            statuses=[self.test_status1, self.test_status2],
            target_entity_type=Asset,
        )
        DBSession.add(self.test_asset_status_list)

        self.test_asset1 = Asset(
            name='Test Asset 1',
            code='TA1',
            project=self.test_project1,
            status_list=self.test_asset_status_list,
            type=self.test_asset_type
        )
        DBSession.add(self.test_asset1)

        self.test_asset2 = Asset(
            name='Test Asset 2',
            code='TA2',
            project=self.test_project2,
            status_list=self.test_asset_status_list,
            type=self.test_asset_type
        )
        DBSession.add(self.test_asset2)

        # shots
        self.test_shot_status_list = StatusList(
            name='ShotStatuses',
            statuses=[self.test_status1, self.test_status2],
            target_entity_type=Shot
        )
        DBSession.add(self.test_shot_status_list)

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
        self.test_task_statuses = StatusList(
            name='Task Statuses',
            statuses=[self.test_status1, self.test_status2],
            target_entity_type=Task,
        )
        DBSession.add(self.test_task_statuses)

        self.test_task1 = Task(
            name='Project Planing',
            project=self.test_project1,
            resources=[self.test_user1],
            status_list=self.test_task_statuses,
            schedule_timing=10,
            schedule_unit='d'
        )
        DBSession.add(self.test_task1)

        self.test_task2 = Task(
            name='Project Planing',
            project=self.test_project2,
            resources=[self.test_user1],
            status_list=self.test_task_statuses,
            schedule_timing=10,
            schedule_unit='d'
        )
        DBSession.add(self.test_task2)

        self.test_task3 = Task(
            name='Project Planing',
            project=self.test_project3,
            resources=[self.test_user1],
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
            schedule_timing=2,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task4)

        self.test_task5 = Task(
            name='FX',
            parent=self.test_shot1,
            resources=[self.test_user2],
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
            schedule_timing=2,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task8)

        self.test_task9 = Task(
            name='FX',
            parent=self.test_shot2,
            resources=[self.test_user3],
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
            schedule_timing=2,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task12)

        self.test_task13 = Task(
            name='FX',
            parent=self.test_shot3,
            resources=[self.test_user1],
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
            schedule_timing=2,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task16)

        self.test_task17 = Task(
            name='FX',
            parent=self.test_shot4,
            resources=[self.test_user2],
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
            schedule_timing=2,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task20)

        self.test_task21 = Task(
            name='FX',
            parent=self.test_shot5,
            resources=[self.test_user3],
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
            schedule_timing=10,
            schedule_unit='d',
            status_list=self.test_task_statuses
        )
        DBSession.add(self.test_task31)

        # TODO: Add Milestones

        self.kwargs = dict(
            name='Studio',
            daily_working_hours=8,
        )

        self.test_studio = Studio(**self.kwargs)
        DBSession.add(self.test_studio)
        DBSession.commit()

    def test_daily_working_hours_argument_is_skipped(self):
        """testing if the daily_working_hours attribute will be equal to the
        default settings when the daily_working_hours argument is skipped
        """
        try:
            self.kwargs.pop('daily_working_hours')
        except KeyError:
            pass
        new_studio = Studio(**self.kwargs)
        self.assertEqual(new_studio.daily_working_hours,
                         defaults.daily_working_hours)

    def test_daily_working_hours_argument_is_None(self):
        """testing if the daily_working_hours attribute will be equal to the
        default settings value when the daily_working_hours argument is None
        """
        self.kwargs['daily_working_hours'] = None
        new_studio = Studio(**self.kwargs)
        self.assertEqual(new_studio.daily_working_hours,
                         defaults.daily_working_hours)

    def test_daily_working_hours_attribute_is_None(self):
        """testing if the daily_working_hours attribute will be equal to the
        default settings value when it is set to None
        """
        self.test_studio.daily_working_hours = None
        self.assertEqual(self.test_studio.daily_working_hours,
                         defaults.daily_working_hours)

    def test_daily_working_hours_argument_is_not_integer(self):
        """testing if a TypeError will be raised when the daily_working_hours
        argument is not an integer
        """
        self.kwargs['daily_working_hours'] = 'not an integer'
        self.assertRaises(TypeError, Studio, **self.kwargs)

    def test_daily_working_hours_attribute_is_not_an_integer(self):
        """testing if a TypeError will be raised when the daily_working hours
        attribute is set to a value other than an integer
        """
        self.assertRaises(TypeError, setattr, self.test_studio,
                          'daily_working_hours', 'not an intger')

    def test_daily_working_hours_argument_is_working_fine(self):
        """testing if the daily working hours argument value is correctly
        passed to daily_working_hours attribute
        """
        self.kwargs['daily_working_hours'] = 12
        new_project = Studio(**self.kwargs)
        self.assertEqual(new_project.daily_working_hours, 12)

    def test_daily_working_hours_attribute_is_working_properly(self):
        """testing if the daily_working_hours attribute is working properly
        """
        self.test_studio.daily_working_hours = 23
        self.assertEqual(self.test_studio.daily_working_hours, 23)

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
        self.assertItemsEqual(
            self.test_studio.projects,
            [self.test_project1, self.test_project2, self.test_project3]
        )

    def test_active_projects_attribute_is_read_only(self):
        """testing if the active_projects attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_studio,
                          'active_projects', [self.test_project1])

    def test_active_projects_attribute_is_working_properly(self):
        """testing if the active_projects attribute is working properly
        """
        self.assertItemsEqual(
            self.test_studio.active_projects,
            [self.test_project1, self.test_project2]
        )

    def test_inactive_projects_attribute_is_read_only(self):
        """testing if the inactive_projects attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_studio,
                          'inactive_projects', [self.test_project1])

    def test_inactive_projects_attribute_is_working_properly(self):
        """testing if the inactive_projects attribute is working properly
        """
        self.assertItemsEqual(
            self.test_studio.inactive_projects,
            [self.test_project3]
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
        self.assertItemsEqual(self.test_studio.departments,
                              [self.test_department1, self.test_department2,
                               admins_dep])

    def test_users_attribute_is_read_only(self):
        """testing if the users attribute is a read only attribute
        """
        self.assertRaises(AttributeError, setattr, self.test_studio, 'users',
                          [self.test_project1])

    def test_users_attribute_is_working_properly(self):
        """testing if the users attribute is working properly
        """
        # don't forget the admin
        # admin = User.query.filter_by(name='admin').first()

        self.assertItemsEqual(
            self.test_studio.users,
            [self.test_user1, self.test_user2, self.test_user3]
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

        expected_tjp_template = Template("""project Studio_{{ studio.id }} "Studio" 2013-04-15 - 2013-06-30 {
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
        #print '-----------------------------------'
        #print expected_tjp
        #print '-----------------------------------'
        #print self.test_studio.to_tjp
        #print '-----------------------------------'
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
        tj_scheduler = TaskJugglerScheduler()
        self.test_studio.now = datetime.datetime(2013, 4, 15, 22, 56)
        self.test_studio.start = datetime.datetime(2013, 4, 15, 22, 56)
        self.test_studio.end = datetime.datetime(2013, 7, 30, 0, 0)

        self.test_studio.scheduler = tj_scheduler
        self.test_studio.schedule()

        # now check the timings of the tasks are all adjusted

        # Projects

        # Project 1
        self.assertEqual(
            self.test_project1.computed_start,
            datetime.datetime(2013, 4, 16, 9, 0)
        )

        self.assertEqual(
            self.test_project1.computed_end,
            datetime.datetime(2013, 7, 19, 13, 0)
        )

        # Project 2
        self.assertEqual(
            self.test_project2.computed_start,
            datetime.datetime(2013, 4, 16, 9, 0)
        )

        self.assertEqual(
            self.test_project1.computed_end,
            datetime.datetime(2013, 7, 19, 13, 0)
        )

        # Project 3
        self.assertIsNone(self.test_project3.computed_start)
        self.assertIsNone(self.test_project3.computed_end)

        # self.test_asset1
        self.assertEqual(
            self.test_asset1.computed_start,
            datetime.datetime(2013, 04, 16, 9, 0)
        )
        self.assertEqual(
            self.test_asset1.computed_end,
            datetime.datetime(2013, 06, 12, 16, 00)
        )

        # self.test_asset2
        self.assertEqual(
            self.test_asset2.computed_start,
            datetime.datetime(2013, 04, 16, 9, 0)
        )
        self.assertEqual(
            self.test_asset2.computed_end,
            datetime.datetime(2013, 06, 12, 16, 00)
        )

        # self.test_shot1
        self.assertEqual(
            self.test_shot1.computed_start,
            datetime.datetime(2013, 07, 8, 14, 0)
        )
        self.assertEqual(
            self.test_shot1.computed_end,
            datetime.datetime(2013, 07, 19, 13, 00)
        )

        # self.test_shot2
        self.assertEqual(
            self.test_shot2.computed_start,
            datetime.datetime(2013, 04, 16, 9, 0)
        )
        self.assertEqual(
            self.test_shot2.computed_end,
            datetime.datetime(2013, 06, 27, 13, 00)
        )

        # self.test_shot3
        self.assertEqual(
            self.test_shot3.computed_start,
            datetime.datetime(2013, 05, 16, 11, 00)
        )
        self.assertEqual(
            self.test_shot3.computed_end,
            datetime.datetime(2013, 07, 22, 12, 00)
        )

        # self.test_shot4
        self.assertEqual(
            self.test_shot4.computed_start,
            datetime.datetime(2013, 05, 16, 11, 00)
        )
        self.assertEqual(
            self.test_shot4.computed_end,
            datetime.datetime(2013, 07, 02, 18, 00)
        )

        # self.test_shot5
        self.assertIsNone(self.test_shot5.computed_start)
        self.assertIsNone(self.test_shot5.computed_end)

        # self.test_task1
        self.assertEqual(
            self.test_task1.computed_start,
            datetime.datetime(2013, 06, 12, 16, 00)
        )
        self.assertEqual(
            self.test_task1.computed_end,
            datetime.datetime(2013, 06, 25, 15, 00)
        )

        # self.test_task2
        self.assertEqual(
            self.test_task2.computed_start,
            datetime.datetime(2013, 06, 25, 15, 00)
        )
        self.assertEqual(
            self.test_task2.computed_end,
            datetime.datetime(2013, 07, 8, 14, 0)
        )

        # self.test_task3
        self.assertIsNone(self.test_task3.computed_start)
        self.assertIsNone(self.test_task3.computed_end)

        # self.test_task4
        self.assertEqual(
            self.test_task4.computed_start,
            datetime.datetime(2013, 07, 8, 14, 0)
        )
        self.assertEqual(
            self.test_task4.computed_end,
            datetime.datetime(2013, 07, 10, 12, 00)
        )

        # self.test_task5
        self.assertEqual(
            self.test_task5.computed_start,
            datetime.datetime(2013, 07, 10, 12, 00)
        )
        self.assertEqual(
            self.test_task5.computed_end,
            datetime.datetime(2013, 07, 12, 10, 00)
        )

        # self.test_task6
        self.assertEqual(
            self.test_task6.computed_start,
            datetime.datetime(2013, 07, 12, 10, 00)
        )
        self.assertEqual(
            self.test_task6.computed_end,
            datetime.datetime(2013, 07, 16, 16, 00)
        )

        # self.test_task7
        self.assertEqual(
            self.test_task7.computed_start,
            datetime.datetime(2013, 07, 16, 16, 00)
        )
        self.assertEqual(
            self.test_task7.computed_end,
            datetime.datetime(2013, 07, 19, 13, 00)
        )

        # self.test_task8
        self.assertEqual(
            self.test_task8.computed_start,
            datetime.datetime(2013, 04, 16, 9, 0)
        )
        self.assertEqual(
            self.test_task8.computed_end,
            datetime.datetime(2013, 04, 17, 16, 00)
        )

        # self.test_task9
        self.assertEqual(
            self.test_task9.computed_start,
            datetime.datetime(2013, 04, 17, 16, 00)
        )
        self.assertEqual(
            self.test_task9.computed_end,
            datetime.datetime(2013, 04, 19, 14, 00)
        )

        # self.test_task10
        self.assertEqual(
            self.test_task10.computed_start,
            datetime.datetime(2013, 06, 14, 14, 00)
        )
        self.assertEqual(
            self.test_task10.computed_end,
            datetime.datetime(2013, 06, 19, 11, 00)
        )

        # self.test_task11
        self.assertEqual(
            self.test_task11.computed_start,
            datetime.datetime(2013, 06, 21, 17, 00)
        )
        self.assertEqual(
            self.test_task11.computed_end,
            datetime.datetime(2013, 06, 27, 13, 00)
        )

        # self.test_task12
        self.assertEqual(
            self.test_task12.computed_start,
            datetime.datetime(2013, 05, 16, 11, 00)
        )
        self.assertEqual(
            self.test_task12.computed_end,
            datetime.datetime(2013, 05, 17, 18, 00)
        )

        # self.test_task13
        self.assertEqual(
            self.test_task13.computed_start,
            datetime.datetime(2013, 07, 10, 12, 00)
        )
        self.assertEqual(
            self.test_task13.computed_end,
            datetime.datetime(2013, 07, 12, 10, 00)
        )

        # self.test_task14
        self.assertEqual(
            self.test_task14.computed_start,
            datetime.datetime(2013, 07, 12, 10, 00)
        )
        self.assertEqual(
            self.test_task14.computed_end,
            datetime.datetime(2013, 07, 16, 16, 00)
        )

        # self.test_task15
        self.assertEqual(
            self.test_task15.computed_start,
            datetime.datetime(2013, 07, 16, 16, 00)
        )
        self.assertEqual(
            self.test_task15.computed_end,
            datetime.datetime(2013, 07, 22, 12, 00)
        )

        # self.test_task16
        self.assertEqual(
            self.test_task16.computed_start,
            datetime.datetime(2013, 05, 16, 11, 00)
        )
        self.assertEqual(
            self.test_task16.computed_end,
            datetime.datetime(2013, 05, 17, 18, 00)
        )

        # self.test_task17
        self.assertEqual(
            self.test_task17.computed_start,
            datetime.datetime(2013, 06, 12, 16, 00)
        )
        self.assertEqual(
            self.test_task17.computed_end,
            datetime.datetime(2013, 06, 14, 14, 00)
        )

        # self.test_task18
        self.assertEqual(
            self.test_task18.computed_start,
            datetime.datetime(2013, 06, 19, 11, 00)
        )
        self.assertEqual(
            self.test_task18.computed_end,
            datetime.datetime(2013, 06, 21, 17, 00)
        )

        # self.test_task19
        self.assertEqual(
            self.test_task19.computed_start,
            datetime.datetime(2013, 06, 27, 13, 00)
        )
        self.assertEqual(
            self.test_task19.computed_end,
            datetime.datetime(2013, 07, 02, 18, 00)
        )

        # self.test_task20
        self.assertIsNone(self.test_task20.computed_start)
        self.assertIsNone(self.test_task20.computed_end)

        # self.test_task21
        self.assertIsNone(self.test_task21.computed_start)
        self.assertIsNone(self.test_task21.computed_end)

        # self.test_task22
        self.assertIsNone(self.test_task22.computed_start)
        self.assertIsNone(self.test_task22.computed_end)

        # self.test_task23
        self.assertIsNone(self.test_task23.computed_start)
        self.assertIsNone(self.test_task23.computed_end)

        # self.test_task24
        self.assertEqual(
            self.test_task24.computed_start,
            datetime.datetime(2013, 04, 16, 9, 0)
        )
        self.assertEqual(
            self.test_task24.computed_end,
            datetime.datetime(2013, 04, 26, 17, 00)
        )

        # self.test_task25
        self.assertEqual(
            self.test_task25.computed_start,
            datetime.datetime(2013, 04, 26, 17, 00)
        )
        self.assertEqual(
            self.test_task25.computed_end,
            datetime.datetime(2013, 05, 16, 11, 00)
        )

        # self.test_task26
        self.assertEqual(
            self.test_task26.computed_start,
            datetime.datetime(2013, 05, 20, 9, 0)
        )
        self.assertEqual(
            self.test_task26.computed_end,
            datetime.datetime(2013, 05, 30, 17, 00)
        )

        # self.test_task27
        self.assertEqual(
            self.test_task27.computed_start,
            datetime.datetime(2013, 05, 30, 17, 00)
        )
        self.assertEqual(
            self.test_task27.computed_end,
            datetime.datetime(2013, 06, 12, 16, 00)
        )

        # self.test_task28
        self.assertEqual(
            self.test_task28.computed_start,
            datetime.datetime(2013, 04, 16, 9, 0)
        )
        self.assertEqual(
            self.test_task28.computed_end,
            datetime.datetime(2013, 04, 26, 17, 00)
        )

        # self.test_task29
        self.assertEqual(
            self.test_task29.computed_start,
            datetime.datetime(2013, 04, 26, 17, 00)
        )
        self.assertEqual(
            self.test_task29.computed_end,
            datetime.datetime(2013, 05, 16, 11, 00)
        )

        # self.test_task30
        self.assertEqual(
            self.test_task30.computed_start,
            datetime.datetime(2013, 05, 20, 9, 0)
        )
        self.assertEqual(
            self.test_task30.computed_end,
            datetime.datetime(2013, 05, 30, 17, 00)
        )

        # self.test_task31
        self.assertEqual(
            self.test_task31.computed_start,
            datetime.datetime(2013, 05, 30, 17, 00)
        )
        self.assertEqual(
            self.test_task31.computed_end,
            datetime.datetime(2013, 06, 12, 16, 00)
        )

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

        self.assertItemsEqual(
            self.test_studio.vacations,
            [vacation1, vacation2]
        )
