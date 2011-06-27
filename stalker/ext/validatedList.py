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
    
    :param list\_: The list to initialize this ValidatedList instance, simply
      all the data will be copied to the current ValidatedList instance. Also
      sets the type that this ValidatedList instance works on if no type\_
      argument is given and the given list will be reduced to the same type of
      objects defined with the first elements type or with the given type\_
      argument, default value is an empty list.
    
    :param type\_: If given, the ValidatedList will accept only this type of
      objects. If both the list\_ and the type\_ arguments are given the the
      type\_ will be used as the forced type. Can be a string showing the
      absolute path of the type object.
    
    :param validator: A callable which will be called with the newly passed
      elements. The ValidatedList instance will call the callable when the
      __setitem__, __setslice__, append, extend, insert, __add__, __iadd__,
      pop or remove methods are called. The regular validations will still be
      done by the ValidatedList instance, but for extra actions (like back
      reference updates for example) the callable will be called with the list
      of elements. Callables should be in the following form::
        
        def func1(list_of_elements_added, list_of_elements_removed):
            pass
      
    """
    
    
    #----------------------------------------------------------------------
    def __init__(self, list_=[], element_type=None, validator=None):
        
        self.__type__ = None
        self.__lazy_load_type__ = False
        self._validator = validator
        
        if element_type is not None:
            self.__set_type__(element_type)
        
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
    def __set_type__(self, element_type):
        """sets the type which the list is allowed to work on
        """
        
        if isinstance(element_type, (str, unicode)):
            self.__lazy_load_type__ = True
            self.__type__ = element_type
        else:
            if isinstance(element_type, type):
                self.__type__ = element_type
            else:
                self.__type__ = type(element_type)
            
            self.__type_as_str__ = str(self.__type__).split("'")[1]
            self.__error_message__ = "the type of the given value is not " + \
                "correct, please supply an %s instance" % self.__type_as_str__
    
    
    
    #----------------------------------------------------------------------
    def __do_import__(self, element_type):
        """imports the module
        """
        
        #if isinstance(type_, (str, unicode)):
        if self.__lazy_load_type__:
            # get the class from the string
            from stalker.utils import path_to_exec
            exec_, module, object_ = path_to_exec(element_type)
            
            if module != "":
                # import the object
                imported_module = __import__(module, globals(),
                                             locals(), [object_], -1)
                element_type = eval("imported_module." + object_)
            else:
                element_type = eval(object_)
            
            self.__lazy_load_type__ = False
        
        self.__set_type__(element_type)
    
    
    
    #----------------------------------------------------------------------
    def __setitem__(self, key, value):
        """x.__setitem__(i, y) <==> x[i]=y
        
        This is the overriden version of the original method.
        """
        
        if self.__lazy_load_type__:
            self.__do_import__(self.__type__)
        
        if isinstance(value, self.__type__):
            # call the callable with the value
            if not self._validator is None:
                self._validator([value], [self[key]])

            super(ValidatedList, self).__setitem__(key, value)
        else:
            raise TypeError(self.__error_message__)
    
    
    
    
    #----------------------------------------------------------------------
    def __setslice__(self, i, j, sequence):
        """x.__setslice__(i, j, y) <==> x[i:j]=y
        
        Use  of negative indices is not supported.
        
        This is the overriden version of the original method.
        """
        
        if self.__lazy_load_type__:
            self.__do_import__(self.__type__)
        
        for element in sequence:
            if not isinstance(element, self.__type__):
                raise TypeError(self.__error_message__)
        
        # call the callable with the sequence
        if not self._validator is None:
            self._validator(sequence, self[i:j])
        
        super(ValidatedList, self).__setslice__(i, j, sequence)
    
    
    
    #----------------------------------------------------------------------
    def append(self, object):
        """L.append(object) -- append object to end
        
        This is the overriden version of the original method.
        """
        
        if self.__type__ is None:
            self.__set_type__(type(object))
        else:
            
            if self.__lazy_load_type__:
                self.__do_import__(self.__type__)
            
            if not isinstance(object, self.__type__):
                raise TypeError(self.__error_message__)
        
        # call the validator
        if not self._validator is None:
            self._validator([object], [])
        
        super(ValidatedList, self).append(object)
    
    
    
    #----------------------------------------------------------------------
    def extend(self, iterable):
        """L.extend(iterable) -- extend list by appending elements from the iterable
        
        This is the overriden version of the original method.
        """
        
        if self.__lazy_load_type__:
            self.__do_import__(self.__type__)
        
        if self.__type__ is None:
            try:
                self.__set_type__(type(iterable[0]))
            except IndexError:
                pass
        else:
            for element in iterable:
                if not isinstance(element, self.__type__):
                    raise TypeError(self.__error_message__)
        
        # call the callable with the value
        if not self._validator is None:
            self._validator(iterable, [])
        
        super(ValidatedList, self).extend(iterable)
    
    
    
    #----------------------------------------------------------------------
    def insert(self, index, object):
        """L.insert(index, object) -- insert object before index
        
        This is the overriden version of the original method.
        """
        
        if self.__lazy_load_type__:
            self.__do_import__(self.__type__)
        
        if self.__type__ is None:
            self.__set_type__(type(object))
        else:
            if not isinstance(object, self.__type__):
                raise TypeError(self.__error_message__)
        
        # call the callable with the value
        if not self._validator is None:
            self._validator([object], [])
        
        super(ValidatedList, self).insert(index, object)
    
    
    
    #----------------------------------------------------------------------
    def __add__(self, other):
        """x.__add__(y) <==> x+y
        
        This is the overriden version of the original method.
        """
        
        if self.__lazy_load_type__:
            self.__do_import__(self.__type__)
        
        if self.__type__ is None:
            try:
                self.__set_type__(type(other[0]))
            except IndexError:
                pass
        else:
            for element in other:
                if not isinstance(element, self.__type__):
                    raise TypeError(self.__error_message__)
        
        # call the callable with the value
        if not self._validator is None:
            self._validator(other, [])
        
        return super(ValidatedList, self).__add__(other)
    
    
    
    #----------------------------------------------------------------------
    def __iadd__(self, other):
        """x.__iadd__(y) <==> x+=y
        
        This is the overriden version of the original method.
        """
        
        if self.__lazy_load_type__:
            self.__do_import__(self.__type__)
        
        if self.__type__ is None:
            try:
                self.__set_type__(type(other[0]))
            except IndexError:
                pass
        else:
            for element in other:
                if not isinstance(element, self.__type__):
                    raise TypeError(self.__error_message__)
        
        # call the callable with the value
        if not self._validator is None:
            self._validator(other, [])
        
        return super(ValidatedList, self).__iadd__(other)
    
    
    
    #----------------------------------------------------------------------
    def pop(self, index=-1):
        """ L.pop([index]) -> item -- remove and return item at index (default last).
        Raises IndexError if list is empty or index is out of range.
        
        This is the overriden version of the original method.
        """
        
        # call the original method
        popped_item = super(ValidatedList, self).pop(index)
        
        if not self._validator is None:
            self._validator([], [popped_item])
        
        # call the original method
        return popped_item
    
    
    
    #----------------------------------------------------------------------
    def remove(self, value):
        """ L.remove(value) -- remove first occurrence of value.
        Raises ValueError if the value is not present.
        """
        
        if not self._validator is None:
            try:
                index = self.index(value)
                self._validator([], [self[index]])
            except ValueError:
                pass
        
        # call the original method
        super(ValidatedList, self).remove(value)
    
    
    
    