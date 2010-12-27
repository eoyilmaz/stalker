#-*- coding: utf-8 -*-



from stalker.models import entity



########################################################################
class Status(entity.Entity):
    """The Status class
    
    :param shortName: the shortName of the status name, keep it as simple
      as possible, the string will be formated to have all upper-case and no
      white spaces at the beggining and at the end of the attribute
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 #name=None,
                 shortName=None,
                 thumbnail=None,
                 **kwargs
                 ):
        
        super(Status,self).__init__(**kwargs)
        
        self._shortName = self._check_shortName(shortName)
    
    
    
    #----------------------------------------------------------------------
    def _check_shortName(self, shortName):
        """checks the shortName attribute
        """
        
        if shortName == '' \
           or not isinstance(shortName, (str, unicode)):
            raise(ValueError("the shortName shouldn't be empty and it \
            should be a str or unicode"))
        
        return shortName
    
    
    
    #----------------------------------------------------------------------
    def shortName():
        def fget(self):
            """returns the shortName property
            """
            return self._shortName
        
        def fset(self, shortName):
            """sets the shortName
            """
            self._shortName = self._check_shortName(shortName)
        
        return locals()
    
    shortName = property(**shortName())






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
    
    
    