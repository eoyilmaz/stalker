#-*- coding: utf-8 -*-



########################################################################
class ValidatedList(list):
    """A list variant which accepts only one type of element.
    
    A ValidatedList is a regular Python list with overriden methods which helps
    validating the elements in regular list actions. Uses the type of the first
    assigned element if no type\_ is defined.
    
    Reduces the given list\_ to elements with the same type of the first
    element if the type\_ argument is None or uses the type\_ argument if
    given.
    
    :param list\_: the list to initialize this ValidatedList instance, simply
      all the data will be copied to the current ValidatedList instance. Also
      sets the type that this ValidatedList instance works on if no type\_
      argument is given and the given list will be reduced to the same type of
      objects defined with the first elements type or with the given type\_
      argument, default value is an empty list.
    
    :param type\_: if given, the ValidatedList will accept only this type of
      objects. If both the list\_ and the type\_ arguments are given the the
      type\_ will be used as the forced type.
    """
    
    
    #----------------------------------------------------------------------
    def __init__(self, list_=[], type_=None):
        
        self.__type__ = type_
        self.__type_as_str__ = ""
        self.__error_message__ = ""
        
        if list_ and len(list_):
            
            # store the first element type
            if self.__type__ is None:
                self.__set_type__(type(list_[0]))
            else:
                self.__set_type__(self.__type__)
            
            # remove the other type of objects
            reduced_list = [x for x in list_
                            if isinstance(x, self.__type__)]
            
            self.extend(reduced_list)

    
    
    
    #----------------------------------------------------------------------
    def __set_type__(self, type_):
        """sets the type which the list is allowed to work on
        """
        
        self.__type__ = type_
        self.__type_as_str__ = str(self.__type__).split("'")[1]
        self.__error_message__ = "the type of the given value is not " + \
            "correct, please supply an %s instance" % self.__type_as_str__
    
    
    
    #----------------------------------------------------------------------
    def __setitem__(self, key, value):
        """x.__setitem__(i, y) <==> x[i]=y
        
        This is the overriden version of the original method.
        """ + super(ValidatedList, self).__setitem__.__doc__
        
        if not self.__type__:
            self.__set_type__(type(value))
        
        if isinstance(value, self.__type__):
            super(ValidatedList, self).__setitem__(key, value)
        else:
            raise ValueError(self.__error_message__)
        
    
    
    
    #----------------------------------------------------------------------
    def __setslice__(self, i, j, sequence):
        """x.__setslice__(i, j, y) <==> x[i:j]=y
        
        Use  of negative indices is not supported.
        
        This is the overriden version of the original method.
        """
        
        for element in sequence:
            if not isinstance(element, self.__type__):
                raise ValueError(self.__error_message__)
        
        super(ValidatedList, self).__setslice__(i, j, sequence)
    
    
    
    #----------------------------------------------------------------------
    def append(self, object):
        """L.append(object) -- append object to end
        
        This is the overriden version of the original method.
        """
        
        if self.__type__ is None:
            self.__set_type__(type(object))
        else:
            if not isinstance(object, self.__type__):
                raise ValueError(self.__error_message__)
        
        super(ValidatedList, self).append(object)
    
    
    
    #----------------------------------------------------------------------
    def extend(self, iterable):
        """L.extend(iterable) -- extend list by appending elements from the iterable
        
        This is the overriden version of the original method.
        """
        
        if self.__type__ is None:
            try:
                self.__set_type__(type(iterable[0]))
            except IndexError:
                pass
        else:
            for element in iterable:
                if not isinstance(element, self.__type__):
                    raise ValueError(self.__error_message__)
        
        super(ValidatedList, self).extend(iterable)
    
    
    
    #----------------------------------------------------------------------
    def insert(self, index, object):
        """L.insert(index, object) -- insert object before index
        
        This is the overriden version of the original method.
        """
        
        if self.__type__ is None:
            self.__set_type__(type(object))
        else:
            if not isinstance(object, self.__type__):
                raise ValueError(self.__error_message__)
        
        super(ValidatedList, self).insert(index, object)
    
    
    
    #----------------------------------------------------------------------
    def __add__(self, other):
        """x.__add__(y) <==> x+y
        
        This is the overriden version of the original method.
        """
        
        if self.__type__ is None:
            try:
                self.__set_type__(type(other[0]))
            except IndexError:
                pass
        else:
            for element in other:
                if not isinstance(element, self.__type__):
                    raise ValueError(self.__error_message__)
        
        return super(ValidatedList, self).__add__(other)
    
    
    
    #----------------------------------------------------------------------
    def __iadd__(self, other):
        """x.__iadd__(y) <==> x+=y
        
        This is the overriden version of the original method.
        """
        
        if self.__type__ is None:
            try:
                self.__set_type__(type(other[0]))
            except IndexError:
                pass
        else:
            for element in other:
                if not isinstance(element, self.__type__):
                    raise ValueError(self.__error_message__)
        
        return super(ValidatedList, self).__iadd__(other)
