#-*- coding: utf-8 -*-



from stalker.models import entity



########################################################################
class Status(entity.Entity):
    """The Status class
    
    :param short_name: the short_name of the status name, keep it as simple
      as possible, the string will be formated to have all upper-case and no
      white spaces at the beggining and at the end of the attribute
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 #name=None,
                 short_name=None,
                 thumbnail=None,
                 **kwargs
                 ):
        
        super(Status,self).__init__(**kwargs)
        
        self._short_name = self._check_short_name(short_name)
    
    
    
    #----------------------------------------------------------------------
    def _check_short_name(self, short_name):
        """checks the short_name attribute
        """
        
        if short_name == '' \
           or not isinstance(short_name, (str, unicode)):
            raise(ValueError("the short_name shouldn't be empty and it \
            should be a str or unicode"))
        
        return short_name
    
    
    
    #----------------------------------------------------------------------
    def short_name():
        def fget(self):
            """returns the short_name property
            """
            return self._short_name
        
        def fset(self, short_name):
            """sets the short_name
            """
            self._short_name = self._check_short_name(short_name)
        
        return locals()
    
    short_name = property(**short_name())






########################################################################
class StatusList(entity.Entity):
    """the list version of the Status
    
    Holds multiple statuses to be used as a choice list for several other
    classes
    
    :param statuses: this is a list of status objects, so you can prepare
      different StatusList objects for different kind of entities
    """
    
    #----------------------------------------------------------------------
    def __init__(self,
                 #name=None,
                 statuses=[],
                 **kwargs
                 ):
        
        super(StatusList,self).__init__(**kwargs)
        
        #self._name = self._check_name(name)
        self._statuses = self._check_statuses(statuses)
    
    
    
    #----------------------------------------------------------------------
    def _check_statuses(self, statuses):
        """checks the given status_list
        """
        
        if not isinstance(statuses, list):
            raise(ValueError('statuses should be an instance of list'))
        
        if len(statuses) < 1:
            raise(ValueError('statuses should not be an empty list'))
        
        for status in statuses:
            if not isinstance(status, Status):
                raise(ValueError('all elements must be an object of Status in \
                the given statuses list'))
        
        return statuses
    
    
    
    ##----------------------------------------------------------------------
    #def name():
        
        #def fget(self):
            #"""returns the name attribute
            #"""
            #return self._name
        
        #def fset(self, name):
            #"""sets the name attribute
            #"""
            #self._name = self._check_name(name)
        
        #return locals()
    
    #name = property(**name())
    
    
    
    #----------------------------------------------------------------------
    def statuses():
        
        def fget(self):
            return self._statuses
        
        def fset(self, statuses):
            self._statuses = self._check_statuses(statuses)
        
        doc = """this is the property that sets and returns the statuses, or
        namely the status list of this StatusList object"""
        
        return locals()
    
    statuses = property(**statuses())
    
    
    