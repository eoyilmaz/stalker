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
import transaction

from pyramid import testing

from stalker import db, StatusList, Project, Status, Repository
from stalker.db.session import DBSession
from stalker.views import asset



import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TestMyView(unittest.TestCase):
    """tests asset view
    """

    def setUp(self):
        self.config = testing.setUp()
        db.setup({'sqlalchemy.url': 'sqlite:///:memory:'})
        
        self.test_status1 = Status(name='Test Status 1', code='TS1')
        self.test_status2 = Status(name='Test Status 2', code='TS2')
        self.test_status3 = Status(name='Test Status 3', code='TS3')
        
        self.test_project_status_list = StatusList(
            target_entity_type='Project',
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3
            ]
        )
        
        self.test_repo = Repository(
            name='Test Repository',
            windows_path='T:/',
            linux_path='/mnt/T',
            osx_path='/Volumes/T'
        )
        
        self.test_project = Project(
            name='Test Project 1',
            code='TP1',
            status_list=self.test_project_status_list,
            repository=self.test_repo
        )
        
        DBSession.add(self.test_project)
        transaction.commit()
        
        DBSession.add(self.test_project)
        
        self.params = {
            'mode': 'CREATE'
        }
        
        self.matchdict = {
            'project_id': self.test_project.id
        }
        self.request = testing.DummyRequest(params=self.params)
        self.request.matchdict = self.matchdict
        
    
    def tearDown(self):
        DBSession.remove()
        testing.tearDown()
    
    def test_create_asset_dialog_project_id_is_skipped(self):
        """testing if a KeyError will be raised when the project_id parameter
        is skipped
        """
        self.assertRaises(KeyError, asset.create_asset_dialog, request)
    
    def test_create_asset_dialog_name_parameter_is_skipped(self):
        """testing if a KeyError will be raised when the name parameter is
        skipped
        """
        request
    
    def test_asset_dialog_create_asset_is_working_properly(self):
        """testing if the dialog_create_asset view is working properly
        """
        request = testing.DummyRequest()
        info = asset.create_asset_dialog(request)
        
        # it should return all the projects
        self.assertEqual(info['mode'], 'CREATE')
