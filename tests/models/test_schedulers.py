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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

import unittest
from zope.sqlalchemy import ZopeTransactionExtension
from stalker import db, Department, User, Project, Repository, Status, StatusList, Task
from stalker.db import DBSession


class TaskJugglerSchedulerTester(unittest.TestCase):
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
        DBSession.configure(extension=ZopeTransactionExtension())
    
    def setUp(self):
        """set up the test
        """
        # we need a database
        db.setup({
            'sqlalchemy.url': 'sqlite:///:memory:',
            'sqlalchemy.echo': False
        })
        
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
        
        self.test_user2 = User(
            login='user2',
            name='User2',
            email='user2@users.com',
            password='1234',
            departments=[self.test_dep1]
        )
        
        self.test_user3 = User(
            login='user3',
            name='User3',
            email='user3@users.com',
            password='1234',
            departments=[self.test_dep2]
        )
        
        self.test_user4 = User(
            login='user4',
            name='User4',
            email='user4@users.com',
            password='1234',
            departments=[self.test_dep2]
        )
        
        self.test_user5 = User(
            login='user5',
            name='User5',
            email='user5@users.com',
            password='1234',
            departments=[self.test_dep1, self.test_dep2]
        )
        
        # repository
        self.test_repo = Repository(
            name='Test Repository',
            linux_path='/mnt/T/',
            windows_path='T:/',
            osx_path='/Volumes/T/'
        )
        
        # statuses
        self.test_status1 = Status(name='Status 1', code='STS1')
        self.test_status2 = Status(name='Status 2', code='STS2')
        self.test_status3 = Status(name='Status 3', code='STS3')
        self.test_status4 = Status(name='Status 4', code='STS4')
        self.test_status5 = Status(name='Status 5', code='STS5')
        
        # status lists
        self.test_proj_status_list = StatusList(
            name='Project Status List',
            statuses=[self.test_status1, self.test_status2, self.test_status3],
            target_entity_type='Project'
        )
        
        # create one project
        self.test_proj1 = Project(
            name='Test Project 1',
            code='TP1',
            repository=self.test_repo,
            status_list=self.test_proj_status_list
        )
        
        self.test_task_status_list = StatusList(
            name='Task Statuses',
            statuses=[self.test_status4, self.test_status5],
            target_entity_type='Task'
        )
        
        # create tasks
        self.test_task1 = Task(
            name='Task1',
            project=self.test_proj1,
            resources=[self.test_user1, self.test_user2],
            effort=50
        )
        
    def test_setup(self):
        """is setup working
        """
        pass
        
        
