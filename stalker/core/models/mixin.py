#-*- coding: utf-8 -*-
"""This module contains the Mixins (ta taaa).

Mixins are, you know, things that we love. Ok I don't have anything to write,
just use and love them.

By the way, for SQLAlchemy part of the mixins (tables and mappers) refer to the
:mod:`~stalker.db.mixin`. There is a corresponding type for every mixin
implemented in this module. Also the documentation explains how to mixin tables
and mappers.
"""



from stalker.core.models import link






########################################################################
class ReferenceMixin(object):
    """Adds reference capabilities to the mixed in class.
    
    References are :class:`~stalker.core.models.link.Link` objects which adds
    outside information to the attached objects. The aim of the References are
    generally to give more info to direct the evolution of the objects,
    generally these objects are :class:`~stalker.core.models.asset.Asset`\ s.
    
    """
    
    _references = []
    
    
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
            raise ValueError("all the elements should be instances of \
:class:`~stalker.core.models.link.Link`")
        
        return references_in
    
    
    
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
    



