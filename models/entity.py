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
    """The base class of all the other main objects
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 name,
                 description='',
                 dateCreated=datetime.datetime.now(),
                 dateUpdated=datetime.datetime.now(),
                 createdBy=None,
                 updatedBy=None,
                 tags=[],
                 links=[],
                 status=-1,
                 statusList=[],
                 notes=[],
                 thumbnail=None,
                 ):
        
        ## the attributes
        #self.name = name
        #self.description = description
        #self.dateCreated = dateCreated
        #self.dateUpdated = dateUpdated
        #self.createdBy = createdBy
        #self.updatedBy = updatedBy
        #self.tags = tags
        #self.links = links
        #self.status = status
        #self.statusList = statusList
        #self.notes = notes
        #self.thumbnail = thumbnail
        pass
    
    
