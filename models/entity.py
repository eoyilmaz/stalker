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
from stalker.models import status




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
        self._name = self._check_name(name)
        self._description = self._check_description(description)
        self._date_created = self._check_date_created(date_created)
        self._date_updated = self._check_date_updated(date_updated)
        self._created_by = self._check_created_by(created_by)
        self._updated_by = self._check_updated_by(updated_by)
        self._tags = self._check_tags(tags)
        self._links = self._check_links(links)
        self._status_list = self._check_status_list(status_list)
        self._status = self._check_status(status)
        self._notes = self._check_notes(notes)
        self._thumbnail = thumbnail
    
    
    
    #----------------------------------------------------------------------
    def _check_created_by(self, created_by_in):
        """checks the given created_by_in attribute
        """
        
        #-------------------------------------------------------------------
        # Python documentation says one of the nice ways to over come circular
        # imports is late imports and it is perfectly ok to use it like that
        # 
        # just try to import the module as late as possible
        # 
        # ref:
        # http://docs.python.org/faq/programming.html#what-are-the-best-
        #                               practices-for-using-import-in-a-module
        #-------------------------------------------------------------------
        from stalker.models import user
        
        # raise ValueError when:
        # it is None
        if created_by_in is None:
            raise ValueError("the created_by attribute can not be set to None")
        
        if not isinstance(created_by_in, user.User):
            raise ValueError("the created_by attribute should be an instance \
            of stalker.models.user.User")
        
        return created_by_in
    
    
    
    #----------------------------------------------------------------------
    def _check_updated_by(self, updated_by_in):
        """checks the given updated_by_in attribute
        """
        
        from stalker.models import user
        
        # raise ValueError when:
        # it is None
        if updated_by_in is None:
            raise ValueError("the created_by attribute can not be set to None")
        
        if not isinstance(updated_by_in, user.User):
            raise ValueError("the updated_by attribute should be an instance \
            of stalker.models.user.User")
        
        return updated_by_in
    
    
    
    #----------------------------------------------------------------------
    def _check_date_created(self, date_created_in):
        """checks the given date_creaetd_in
        """
        
        # raise ValueError when:
        
        # it is None
        if date_created_in is None:
            raise ValueError("the date_created could not be None")
        
        if not isinstance(date_created_in, datetime.datetime):
            raise ValueError("the date_created should be an instance of \
            datetime.datetime")
        
        return date_created_in
    
    
    
    #----------------------------------------------------------------------
    def _check_date_updated(self, date_updated_in):
        """checks the given date_updated_in
        """
        
        # raise ValueError when:
        
        # it is None
        if date_updated_in is None:
            raise ValueError("the date_updated could not be None")
        
        # it is not an instance of datetime.datetime
        if not isinstance(date_updated_in, datetime.datetime):
            raise ValueError("the date_updated should be an instance of \
            datetime.datetime")
        
        # lower than date_created
        if date_updated_in < self.date_created:
            raise ValueError("the date_updated could not be set to a date \
            before date_created, try setting the date_created before")
        
        return date_updated_in
    
    
    
    #----------------------------------------------------------------------
    def _check_description(self, description_in):
        """checks the given description_in value
        """
        
        # raise ValueError when:
        
        # it is not an instance of string or unicode
        if not isinstance(description_in, (str, unicode)):
            raise ValueError("the description should be set to a string or \
            unicode")
        
        return description_in
    
    
    #----------------------------------------------------------------------
    def _check_links(self, links_in):
        """checks the given links_in value
        """
        
        # raise ValueError when:
        
        # it is not an instance of list
        if not isinstance(links_in, list):
            raise ValueError("the lists attribute should be set to a list")
        
        return links_in
    
    
    
    #----------------------------------------------------------------------
    def _check_name(self, name_in):
        """checks the given name_in value
        """
        
        # raise ValueError when:
        
        # it is not an instance of string or unicode
        if not isinstance(name_in, (str, unicode)):
            raise ValueError("the name attribute should be set to a string \
            or unicode")
        
        # it is empty
        if name_in == "":
            raise ValueError("the name couldn't be an empty string")
        
        if name_in is None:
            raise ValueError("the name couldn't be set to None")
        
        return self._condition_name(name_in)
    
    
    
    #----------------------------------------------------------------------
    def _condition_name(self, name_in):
        """conditions the name_in value
        """
        
        import re
        
        print name_in
        # remove unnecesary characters from the beginning
        name_in = re.sub('(^[^A-Za-z]+)', r'', name_in)
        print name_in
        
        # remove white spaces
        name_in = re.sub('([\s])+', r'', name_in)
        print name_in
        
        # capitalize the first letter
        name_in = name_in[0].upper() + name_in[1:]
        print name_in
        
        return name_in
        
        
    
    
    
    #----------------------------------------------------------------------
    def _check_notes(self, notes_in):
        """checks the given notes_in value
        """
        
        # raise ValueError when:
        
        # it is not an instance of list
        if not isinstance(notes_in, list):
            raise ValueError("the notes attribute should be an instance of \
            list")
        
        return notes_in
    
    
    
    #----------------------------------------------------------------------
    def _check_tags(self, tags_in):
        """checks the given tags_in value
        """
        
        # raise ValueError when:
        
        # it is not an instance of list
        if not isinstance(tags_in, list):
            raise ValueError("the tags attribute should be set to a list")
        
        return tags_in
    
    
    
    #----------------------------------------------------------------------
    def _check_status_list(self, status_list_in):
        """checks the given status_list_in value
        """
        
        # raise ValueError when:
        
        # it is not an instance of status_list
        if not isinstance(status_list_in, status.StatusList):
            raise ValueError("the status list should be an instance of \
            stalker.models.status.StatusList")
        
        return status_list_in
    
    
    
    #----------------------------------------------------------------------
    def _check_status(self, status_in):
        """checks the given status_in value
        """
        
        # raise ValueError when:
        # it is set to None
        if status_in is None:
            raise ValueError("the status couldn't be None, set it to a \
            non-negative integer")
        
        # it is not an instance of int
        if not isinstance(status_in, int):
            raise ValueError("the status must be an instance of integer")
        
        # if it is not in the correct range:
        if status_in < 0:
            raise ValueError("the status must be a non-negative integer")
        
        if status_in >= len(self._status_list.statuses):
            raise ValueError("the status can not be bigger than the length of \
            the status_list")
    
    
    
    #----------------------------------------------------------------------
    def created_by():
        
        def fget(self):
            return self._created_by
        
        def fset(self, created_by_in):
            self._created_by = self._check_created_by(created_by_in)
        
        doc = """this is the property that sets and returns the created_by
        attribute"""
        
        return locals()
    
    created_by = property(**created_by())
    
    
    
    #----------------------------------------------------------------------
    def updated_by():
        
        def fget(self):
            return self._updated_by
        
        def fset(self, updated_by_in):
            self._updated_by = self._check_updated_by(updated_by_in)
        
        doc = """this is the property that sets and returns the updated_by
        attribute"""
        
        return locals()
    
    updated_by = property(**updated_by())
    
    
    
    #----------------------------------------------------------------------
    def links():
        
        def fget(self):
            return self._links
        
        def fset(self, links_in):
            self._links = self._check_links(links_in)
        
        doc = """this is the property that sets and returns the links attribute
        """
        
        return locals()
    
    links = property(**links())
    
    
    
    #----------------------------------------------------------------------
    def notes():
        
        def fget(self):
            return self._notes
        
        def fset(self, notes_in):
            self._notes = notes_in
        
        doc = """this is the property that sets and returns the notes attribute
        """
        
        return locals()
    
    notes = property(**notes())
    
    
    
    #----------------------------------------------------------------------
    def tags():
        
        def fget(self):
            return self._tags
        
        def fset(self, tags_in):
            self._tags = tags_in
        
        doc = """this is the property that sets and returns the tags attribute
        """
        
        return locals()
    
    tags = property(**tags())
    
    
    
    #----------------------------------------------------------------------
    def date_created():
        
        def fget(self):
            return self._date_created
        
        def fset(self, date_created_in):
            self._date_created = self._check_date_created(date_created_in)
        
        doc = """this is the property that sets and returns the date_created
        attribute"""
        
        return locals()
    
    date_created = property(**date_created())
    
    
    
    #----------------------------------------------------------------------
    def date_updated():
        
        def fget(self):
            return self._date_updated
        
        def fset(self, date_updated_in):
            self._date_updated = self._check_date_updated(date_updated_in)
        
        doc = """this is the property that sets and returns the date_updated
        attribute"""
        
        return locals()
    
    date_updated = property(**date_updated())
    
    
    
    #----------------------------------------------------------------------
    def description():
        
        def fget(self):
            return self._description
        
        def fset(self, description_in):
            self._description = self._check_description(description_in)
        
        doc = """this is the property that sets and returns the description
        attribute"""
        
        return locals()
    
    description = property(**description())
    
    
    
    #----------------------------------------------------------------------
    def links():
        
        def fget(self):
            return self._links
        
        def fset(self, links_in):
            self._links = self._check_links(links_in)
        
        doc = """this is the property that sets and returns the links \
        attribute"""
        
        return locals()
    
    links = property(**links())
    
    
    
    #----------------------------------------------------------------------
    def status():
        
        def fget(self):
            return self._status
        
        def fset(self, status_in):
            self._status = self._check_status(status_in)
        
        doc = """this is the property that sets and returns the status \
        attribute"""
        
        return locals()
    
    status = property(**status())
        
    
    
    
    #----------------------------------------------------------------------
    def status_list():
        
        def fget(self):
            return self._status_list
        
        def fset(self, status_list_in):
            self._status_list = self._check_status_list(status_list_in)
        
        doc = """this is the property that sets and returns the status_list \
        attribute"""
        
        return locals()
    
    status_list = property(**status_list())
    
    
    
    #----------------------------------------------------------------------
    def name():
        
        def fget(self):
            return self._name
        
        def fset(self, name_in):
            self._name = self._check_name(name_in)
        
        doc = """this is the property that sets and returns the name \
        attribute"""
        
        return locals()
    
    name = property(**name())
    
    
    
    #----------------------------------------------------------------------
    def notes():
        
        def fget(self):
            return self._notes
        
        def fset(self, notes_in):
            self._notes = self._check_notes(notes_in)
        
        doc = """this is the property that sets and returns the notes \
        attribute"""
        
        return locals()
    
    notes = property(**notes())
    
    
    
    