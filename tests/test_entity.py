#-*- coding: utf-8 -*-
########################################################################
# 
# Copyright (C) 2010  Erkan Ozgur Yilmaz
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
# 
########################################################################



import unittest
import mocker
import datetime
from stalker.models import entity, user, link, tag, status






########################################################################
class EntityTest(mocker.MockerTestCase):
    """tests the entity class
    
    the entity class should have this attributes and properties
    
    created_by:
    the created_by attribute should contain a User object who is created this
    object
    
    updated_by:
    the updated_by attribute should contain a User object who is updated the
    user lastly. the created_by and updated_by attributes should point the same
    object if this entity is just created
    
    date_created:
    the date that this object is created. it should be a time before now
    
    date_updated:
    this is the date that this object is updated lastly. for newly created
    entities this is equal to date_created and the date_updated cannot be
    before date_created
    
    name:
    a string or unicode attribute that holds the name of this entity. it could
    not be empty, the first letter should be alphabetic (not alphanumeric).
    
    description:
    a string or unicode attribute that holds the description of this entity
    object, it could be empty
    
    status_list:
    this attribute holds a status list object, which shows the possible
    statuses that this entity could be in. This attribute can not be empty.
    
    status:
    an integer value which is the index of the status in the status_list
    attribute. So the value of this attribute couldn't be lower than 0 and
    higher than the length of the status_list object.
    
    tags:
    a list of tag objects related to this entity. tags could be an empty list.
    
    links: (not sure about the implementation)
    a list of link objects. that shows the various links related to this
    entity object.
    
    thumbnail:
    a file object that shows the thumbnail file of this entity. thumbnail could
    be None.
    
    notes:
    a list of note objects. notes can be an empty list.
    
    all the attributes to objects needs a mock object of that object, that is:
    user
    link
    entity
    file
    note
    status_list
    tag
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        ## create the mocker
        #self._mocker = mocker.Mocker()
        
        # create
        # a mock user
        self.mockUser = self.mocker.mock(user.User)
        
        # a mock link
        self.mockLink = self.mocker.mock(link.Link)
        
        # a mock tag
        self.mockTag1 = self.mocker.mock(tag.Tag)
        self.mockTag2 = self.mocker.mock(tag.Tag)
        
        # a mock status_list
        self.mockStatusList = self.mocker.mock(status.StatusList)
        
        self.mocker.replay()
        
        self.name = 'testEntity'
        self.description = 'Just testing the very first entity'
        self.dateCreated = datetime.datetime(2010, 10, 21, 3, 8, 0)
        self.dateUpdated = self.dateCreated
        
        
        # create a proper entity object
        self._entity = entity.Entity(
            name=self.name,
            description=self.description,
            dateCreated=self.dateCreated,
            dateUpdated=self.dateUpdated,
            createdBy=self.mockUser,
            tags=[self.mockTag1, self.mockTag2],
            links=[self.mockLink]
        )
    
    
    
    #----------------------------------------------------------------------
    def test_created_by(self):
        """testing the created_by attribute
        """
        
        # the created_by attribute should be an instance of User class
        
        # it can not be empty (the first created user going to have some
        # problems if we dont allow empty users, the database should be
        # initialized with an admin user)
        # 
        
        self.fail("tests are not implemented yet!")
        
        # raise a value error in case of setting the created_by attribute
        # anything different than a user object
        #self.assertRaises( ValueError, 
    
    
    
    #----------------------------------------------------------------------
    def test_date_created(self):
        """testing the date_created attribute
        """
        
        # the date_created attribute should be an instance of datetime.datetime
        
        self.fail("tests are not implemented yet!")
    
    
    
    
    
    