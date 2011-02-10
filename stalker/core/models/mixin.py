#-*- coding: utf-8 -*-
"""This module contains the Mixins (ta taaa).

Mixins are, you know, things that we love. Ok I don't have anything to write,
just use and love them.

By the way, for SQLAlchemy part of the mixins (tables and mappers) refer to the
:mod:`~stalker.db.mixin`. There is a corresponding type for every mixin
implemented in this module. Also the documentation explains how to mixin tables
and mappers.
"""



from stalker.core.models import link, status
from stalker.ext.validatedList import ValidatedList





########################################################################
class ReferenceMixin(object):
    """Adds reference capabilities to the mixed in class.
    
    References are :class:`~stalker.core.models.link.Link` objects which adds
    outside information to the attached objects. The aim of the References are
    generally to give more info to direct the evolution of the objects,
    generally these objects are :class:`~stalker.core.models.asset.Asset`\ s.
    """
    
    
    
    _references = ValidatedList([], link.Link)
    
    
    
    #----------------------------------------------------------------------
    def _validate_references(self, references_in):
        """validates the given references_in
        """
        
        # it should be an object supporting indexing, not necessarily a list
        if not hasattr(references_in, "__setitem__"):
            raise ValueError("the references_in should support indexing")
        
        # all the elements should be instance of stalker.core.models.link.Link
        if not all([isinstance(element, link.Link)
                    for element in references_in]):
            raise ValueError("all the elements should be instances of "
                             ":class:`~stalker.core.models.link.Link`")
        
        return ValidatedList(references_in, link.Link)
    
    
    
    #----------------------------------------------------------------------
    def references():
        
        def fget(self):
            return self._references
        
        def fset(self, references_in):
            self._references = self._validate_references(references_in)
        
        doc="""references are lists containing
        :class:`~stalker.core.models.link.Link` objects
        """
        
        return locals()
    
    references = property(**references())






########################################################################
class StatusMixin(object):
    """Adds statusabilities to the object.
    
    This mixin adds status and statusList variables to the list. Any object
    that needs a status and a corresponding status list can include this mixin.
    
    When mixed with a class which don't have an __init__ method, the mixin
    supplies one, and in this case the parameters below must be defined.
    
    :param status_list: this attribute holds a status list object, which shows
      the possible statuses that this entity could be in. This attribute can
      not be empty or None. Giving a StatusList object, the
      StatusList.target_type should match the current class.
    
    :param status: an integer value which is the index of the status in the
      status_list attribute. So the value of this attribute couldn't be lower
      than 0 and higher than the length-1 of the status_list object and nothing
      other than an integer
    """
    
    
    
    _status_list = None
    _status = 0
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, status=0, status_list=None):
        
        self._status_list = self._validate_status_list(status_list)
        self._status = self._validate_status(status)
    
    
    
    #----------------------------------------------------------------------
    def _validate_status_list(self, status_list_in):
        """validates the given status_list_in value
        """
        
        # raise ValueError when:
        
        # it is not an instance of status_list
        if not isinstance(status_list_in, status.StatusList):
            raise ValueError("the status list should be an instance of "
                             "stalker.core.models.status.StatusList")
        
        # check if the entity_type matches to the StatusList.target_entity_type
        if self.entity_type != status_list_in.target_entity_type:
            raise TypeError("the given StatusLists' target_entity_type is %s, "
                            "whereas the entity_type of this object is %s" % \
                            (status_list_in.target_entity_type,
                             self.entity_type))
        
        return status_list_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_status(self, status_in):
        """validates the given status_in value
        """
        
        # raise ValueError when there is no status_list is not an instance of
        # StatusList
        
        if not isinstance(self.status_list, status.StatusList):
            raise ValueError("please set the status_list attribute first")
        
        # it is set to None
        if status_in is None:
            raise ValueError("the status couldn't be None, set it to a "
                             "non-negative integer")
        
        # it is not an instance of int
        if not isinstance(status_in, int):
            raise ValueError("the status must be an instance of integer")
        
        # if it is not in the correct range:
        if status_in < 0:
            raise ValueError("the status must be a non-negative integer")
        
        if status_in >= len(self._status_list.statuses):
            raise ValueError("the status can not be bigger than the length of "
                             "the status_list")
        
        return status_in
    
    
    
    #----------------------------------------------------------------------
    def status():
        
        def fget(self):
            return self._status
        
        def fset(self, status_in):
            self._status = self._validate_status(status_in)
        
        doc = """this is the property that sets and returns the status
        attribute"""
        
        return locals()
    
    status = property(**status())
        
    
    
    
    #----------------------------------------------------------------------
    def status_list():
        
        def fget(self):
            return self._status_list
        
        def fset(self, status_list_in):
            self._status_list = self._validate_status_list(status_list_in)
        
        doc = """this is the property that sets and returns the status_list
        attribute"""
        
        return locals()
    
    status_list = property(**status_list())