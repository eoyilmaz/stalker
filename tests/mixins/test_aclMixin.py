# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause


import unittest
from stalker import db
from stalker.db.session import DBSession, ZopeTransactionExtension

from stalker.models.mixins import ACLMixin
from stalker.db.declarative import Base
from stalker.models.auth import Permission


# create a new class and mix it with ACLMixin
class TestClass(Base, ACLMixin):
    pass


class ACLMixinTester(unittest.TestCase):
    """tests the stalker.models.mixins.ACLMixin class
    """
    @classmethod
    def setUpClass(cls):
        """setup the test in class level
        """
        DBSession.remove()
        DBSession.configure(extension=None)
    
    @classmethod
    def tearDownClass(cls):
        """cleanup the test in class level
        """
        DBSession.remove()
        DBSession.configure(extension=ZopeTransactionExtension)
    
    def setUp(self):
        """setup the test
        """
        
        db.setup()
        
        # get the Actions from DB
        
        # create permissions
        self.test_perm1 = Permission(access='Allow', action='')
        
        self.test_instance = TestClass()
        
    
    def tearDown(self):
        """clean the test
        """
        DBSession.remove()
    
    def test_permission_attribute_accept_Permission_instances_only(self):
        """testing if the permissions attribute accepts only Permission
        instances
        """
        self.fail('test is not implemented yet')
    
    def test_acl_property_returns_a_list(self):
        """testing if the __acl__ property returns a list
        """
        self.fail('test is not implemented yet')
    
    def test_acl_property_returns_a_proper_ACL_list(self):
        """testing if the __acl__ property returns a proper ACL list according
        to the given permissions
        """
        self.fail('test is not implemented yet')
