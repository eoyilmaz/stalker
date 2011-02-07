#-*- coding: utf-8 -*-



########################################################################
class ValidatedList(list):
    """A list variant which accepts only one type of element and validates the
    elements in regular list actions. Uses the type of the first assigned
    element.
    """
    
    
    #----------------------------------------------------------------------
    def __init__(self, original_list=[]):
        """
        """
        
        self.__type__ = None
        self.__type_as_str__ = ""
        self.__error_message__ = ""
        self.extend(original_list)
        
        if original_list and len(original_list):
            # store the first element type
            self.__set_type__(original_list[0])
    
    
    
    #----------------------------------------------------------------------
    def __set_type__(self, value):
            self.__type__ = type(value)
            self.__type_as_str__ = str(self.__type__).split("'")[1]
            self.__error_message__ = "the type of the given value is not \
correct, please supply an %s instance" % self.__type_as_str__
    
    
    
    #----------------------------------------------------------------------
    def __setitem__(self, key, value):
        """overriden __setitem__ method
        
        checks if the given value is in correct type
        """
        if not self.__type__:
            self.__set_type__(value)
        
        if isinstance(value, self.__type__):
            super(ValidatedList, self).__setitem__(key, value)
        else:
            raise ValueError(self.__error_message__)
        
    
    
    
    #----------------------------------------------------------------------
    def __setslice__(self, i, j, sequence):
        """overriden __setslice__ method
        """
        
        for element in sequence:
            if not isinstance(element, self.__type__):
                raise ValueError(self.__error_message__)
        
        super(ValidatedList, self).__setslice__(i, j, sequence)
    
    
    
    #----------------------------------------------------------------------
    def append(self, object):
        """the overriden append method
        """
        
        if self.__type__ is None:
            self.__set_type__(object)
        else:
            if not isinstance(object, self.__type__):
                raise ValueError(self.__error_message__)
        
        super(ValidatedList, self).append(object)
    
    
    
    #----------------------------------------------------------------------
    def extend(self, iterable):
        """the overriden extend method
        """
        
        if self.__type__ is None:
            try:
                self.__set_type__(iterable[0])
            except IndexError:
                pass
        else:
            for element in iterable:
                if not isinstance(element, self.__type__):
                    raise ValueError(self.__error_message__)
        
        super(ValidatedList, self).extend(iterable)
    
    
    
    #----------------------------------------------------------------------
    def insert(self, index, object):
        """the overriden insert method
        """
        
        if self.__type__ is None:
            self.__set_type__(object)
        else:
            if not isinstance(object, self.__type__):
                raise ValueError(self.__error_message__)
        
        super(ValidatedList, self).insert(index, object)
    
    
    
    #----------------------------------------------------------------------
    def __add__(self, other):
        """the overriden __add__ method
        """
        
        if self.__type__ is None:
            try:
                self.__set_type__(other[0])
            except IndexError:
                pass
        else:
            for element in other:
                if not isinstance(element, self.__type__):
                    raise ValueError(self.__error_message__)
        
        return super(ValidatedList, self).__add__(other)
    
    
    
    #----------------------------------------------------------------------
    def __iadd__(self, other):
        """the overriden __iadd__ method
        """
        
        if self.__type__ is None:
            try:
                self.__set_type__(other[0])
            except IndexError:
                pass
        else:
            for element in other:
                if not isinstance(element, self.__type__):
                    raise ValueError(self.__error_message__)
        
        return super(ValidatedList, self).__iadd__(other)
