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

import datetime
import unittest2
import os

from stalker import (db, Department, User, Repository, Status, StatusList,
                     Project, Task, TaskJugglerScheduler, Studio)

import stalker
from stalker.db import DBSession


class TaskJugglerSchedulerTester(unittest2.TestCase):
    """tests the stalker.models.scheduler.TaskJugglerScheduler class
    """

    @classmethod
    def setUpClass(cls):
        if DBSession:
            DBSession.remove()
        DBSession.configure(extension=None)
    
    @classmethod
    def tearDownClass(cls):
        """clean up the test
        """
        DBSession.configure(extension=None)

    def setUp(self):
        """set up the test
        """
        # we need a database
        db.setup({
            'sqlalchemy.url': 'sqlite:///:memory:',
            'sqlalchemy.echo': False
        })
        db.init()

        # replace datetime now function

        # create departments
        self.test_dep1 = Department(name='Dep1')
        self.test_dep2 = Department(name='Dep2')

        # create resources
        self.test_user1 = User(
            login='user1',
            name='User1',
            email='user1@users.com',
            password='1234',
            departments=[self.test_dep1]
        )
        DBSession.add(self.test_user1)

        self.test_user2 = User(
            login='user2',
            name='User2',
            email='user2@users.com',
            password='1234',
            departments=[self.test_dep1]
        )
        DBSession.add(self.test_user2)

        self.test_user3 = User(
            login='user3',
            name='User3',
            email='user3@users.com',
            password='1234',
            departments=[self.test_dep2]
        )
        DBSession.add(self.test_user3)

        self.test_user4 = User(
            login='user4',
            name='User4',
            email='user4@users.com',
            password='1234',
            departments=[self.test_dep2]
        )
        DBSession.add(self.test_user4)

        # user with two departments
        self.test_user5 = User(
            login='user5',
            name='User5',
            email='user5@users.com',
            password='1234',
            departments=[self.test_dep1, self.test_dep2]
        )
        DBSession.add(self.test_user5)

        # user with no departments
        self.test_user6 = User(
            login='user6',
            name='User6',
            email='user6@users.com',
            password='1234'
        )
        DBSession.add(self.test_user6)

        # repository
        self.test_repo = Repository(
            name='Test Repository',
            linux_path='/mnt/T/',
            windows_path='T:/',
            osx_path='/Volumes/T/'
        )
        DBSession.add(self.test_repo)

        # statuses
        self.test_status1 = Status(name='Status 1', code='STS1')
        self.test_status2 = Status(name='Status 2', code='STS2')
        self.test_status3 = Status(name='Status 3', code='STS3')
        self.test_status4 = Status(name='Status 4', code='STS4')
        self.test_status5 = Status(name='Status 5', code='STS5')
        DBSession.add_all([self.test_status1,
                           self.test_status2,
                           self.test_status3,
                           self.test_status4,
                           self.test_status5])

        # status lists
        self.test_proj_status_list = StatusList(
            name='Project Status List',
            statuses=[self.test_status1, self.test_status2, self.test_status3],
            target_entity_type='Project'
        )
        DBSession.add(self.test_proj_status_list) 

        # create one project
        self.test_proj1 = Project(
            name='Test Project 1',
            code='TP1',
            repository=self.test_repo,
            status_list=self.test_proj_status_list,
            start=datetime.datetime(2013, 4, 4),
            end = datetime.datetime(2013, 5, 4)
        )
        DBSession.add(self.test_proj1)
        self.test_proj1.now = datetime.datetime(2013, 4, 4)

        # create task status list
        self.test_task_status_list = StatusList(
            name='Task Statuses',
            statuses=[self.test_status4, self.test_status5],
            target_entity_type='Task'
        )
        DBSession.add(self.test_task_status_list)

        # create two tasks with the same resources
        self.test_task1 = Task(
            name='Task1',
            project=self.test_proj1,
            resources=[self.test_user1, self.test_user2],
            schedule_model=0,
            schedule_timing=50,
            schedule_unit='h',
            status_list=self.test_task_status_list
        )
        DBSession.add(self.test_task1)

        self.test_task2 = Task(
            name='Task2',
            project=self.test_proj1,
            resources=[self.test_user1, self.test_user2],
            schedule_model=0,
            schedule_timing=60,
            schedule_unit='h',
            status_list=self.test_task_status_list
        )
        DBSession.add(self.test_task2)
        DBSession.commit()

    def test_tjp_file_is_created(self):
        """testing if the tjp file is correctly created
        """
        # create the scheduler
        tjp_sched = TaskJugglerScheduler()
        tjp_sched.projects = [self.test_proj1]

        tjp_sched._create_tjp_file()
        tjp_sched._create_tjp_file_content()
        tjp_sched._fill_tjp_file()

        # check
        self.assertTrue(os.path.exists(tjp_sched.tjp_file_full_path))

        # clean up the test
        tjp_sched._clean_up()

    def test_tjp_file_content_is_correct(self):
        """testing if the tjp file content is correct
        """
        tjp_sched = TaskJugglerScheduler()
        test_studio = Studio(name='Test Studio')
        test_studio.daily_working_hours = 9

        test_studio.id = 564
        test_studio.start = datetime.datetime(2013, 4, 16, 0, 7)
        test_studio.end = datetime.datetime(2013, 6, 30, 0, 0)
        test_studio.now = datetime.datetime(2013, 4, 16, 0, 0)
        tjp_sched.studio = test_studio

        tjp_sched._create_tjp_file()
        tjp_sched._create_tjp_file_content()

        import jinja2
        expected_tjp_template = jinja2.Template(
        """# Generated By Stalker v{{stalker.__version__}}
        project Studio_564 "Test Studio" 2013-04-16 - 2013-06-30 {
            timingresolution 60min
            now {{studio.now.strftime('%Y-%m-%d-%H:%M')}}
            dailyworkinghours 9
            weekstartsmonday
            workinghours mon 09:00 - 18:00
            workinghours tue 09:00 - 18:00
            workinghours wed 09:00 - 18:00
            workinghours thu 09:00 - 18:00
            workinghours fri 09:00 - 18:00
            workinghours sat off
            workinghours sun off
            timeformat "%Y-%m-%d"
            scenario plan "Plan"
            trackingscenario plan
        }
        

        # resources
        resource resources "Resources" {
            resource User_3 "admin"
            resource User_12 "User1"
            resource User_14 "User2"
            resource User_15 "User3"
            resource User_17 "User4"
            resource User_18 "User5"
            resource User_19 "User6"
        }

        # tasks
        
            task Project_28 "Test Project 1" {
            
                task Task_29 "Task1" {
        
            
            effort 50.0h
            allocate User_12, User_14
        }
        
            
                task Task_30 "Task2" {
        
            
            effort 60.0h
            allocate User_12, User_14
        }
        
            
        }
        
        

        # reports
        taskreport breakdown "{{csv_path}}"{
            formats csv
            timeformat "%Y-%m-%d-%H:%M"
            columns id, start, end
        }
        """)
        expected_tjp_content = expected_tjp_template.render(
            {
                'stalker': stalker,
                'studio': test_studio,
                'csv_path': tjp_sched.temp_file_full_path
            }
        )

        self.maxDiff = None
        tjp_sched._clean_up()
        self.assertEqual(tjp_sched.tjp_content, expected_tjp_content)

    def test_schedule_will_not_work_when_the_studio_attribute_is_None(self):
        """testing if a TypeError will be raised when the studio attribute is
        None
        """
        tjp_sched = TaskJugglerScheduler()
        tjp_sched.studio = None
        self.assertRaises(TypeError, tjp_sched.schedule)

    def test_tasks_are_correctly_scheduled(self):
        """testing if the tasks are correctly scheduled
        """
        tjp_sched = TaskJugglerScheduler()
        test_studio = Studio(name='Test Studio',
                             now=datetime.datetime(2013, 4, 16, 0, 0))
        test_studio.daily_working_hours = 9
        DBSession.add(test_studio)

        tjp_sched.studio = test_studio
        tjp_sched.schedule()

        # check if the task and project timings are all adjusted
        self.assertEqual(
            self.test_proj1.computed_start,
            datetime.datetime(2013, 4, 16, 9, 0)
        )

        self.assertEqual(
            self.test_proj1.computed_end,
            datetime.datetime(2013, 4, 24, 10, 0)
        )

        self.assertEqual(
            self.test_task1.computed_start,
            datetime.datetime(2013, 4, 19, 12, 0)
        )
        self.assertEqual(
            self.test_task1.computed_end,
            datetime.datetime(2013, 4, 24, 10, 0)
        )

        self.assertEqual(
            self.test_task2.computed_start,
            datetime.datetime(2013, 4, 16, 9, 0)
        )

        self.assertEqual(
            self.test_task2.computed_end,
            datetime.datetime(2013, 4, 19, 12, 0)
        )
