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



import datetime





########################################################################
class Entity(object):
    """The base class of all the other classes
    
    :param created_by: the created_by attribute should contain a User object
      who is created this object
    
    :param updated_by: the updated_by attribute should contain a User object
      who is updated the user lastly. the created_by and updated_by attributes
      should point the same object if this entity is just created
    
    :param date_created: the date that this object is created. it should be a
      time before now
    
    :param date_updated: this is the date that this object is updated lastly.
      for newly created entities this is equal to date_created and the
      date_updated cannot be before date_created
    
    :param name: a string or unicode attribute that holds the name of this
      entity. it could not be empty, the first letter should be an upper case
      alphabetic (not alphanumeric).
    
    :param description: a string or unicode attribute that holds the
      description of this entity object, it could be empty
    
    :param status_list: this attribute holds a status list object, which shows
      the possible statuses that this entity could be in. This attribute can
      not be empty.
    
    :param status: an integer value which is the index of the status in the
      status_list attribute. So the value of this attribute couldn't be lower
      than 0 and higher than the length of the status_list object and nothing
      other than an integer
    
    :param tags: a list of tag objects related to this entity. tags could be an
      empty list, or when omitted it will be set to an empty list
    
    :param links: (not sure about the implementation) a list of link objects.
      that shows the various links related to this entity object. it is
      initialized with an empty list when omitted
    
    :param thumbnail: (not tested yet) a file object that shows the thumbnail
      file of this entity. thumbnail could be None.
    
    :param notes: a list of note objects. notes can be an empty list.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 name,
                 created_by=None,
                 updated_by=None,
                 status_list=[],
                 status=0,
                 date_created=datetime.datetime.now(),
                 date_updated=datetime.datetime.now(),
                 description='',
                 tags=[],
                 links=[],
                 notes=[],
                 thumbnail=None,
                 ):
        
        # the attributes
        self.name = name
        self.description = description
        self.date_created = date_created
        self.date_updated = date_updated
        self.created_by = created_by
        self.updated_by = updated_by
        self.tags = tags
        self.links = links
        self.status = status
        self.status_list = status_list
        self.notes = notes
        self.thumbnail = thumbnail
        
        