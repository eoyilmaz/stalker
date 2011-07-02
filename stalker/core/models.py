#-*- coding: utf-8 -*-


import re
import datetime
import platform

try:
    from sqlalchemy import orm
except ImportError:
    class orm(object):
        @classmethod
        def reconstructor(self, f):
            return f

from stalker.ext.validatedList import ValidatedList
from stalker.core.errors import CircularDependencyError
from stalker.conf import defaults






########################################################################
class EntityMeta(type):
    """The metaclass for the very basic entity.
    
    Just adds the name of the class as the entity_type class attribute and
    creates an attribute called plural_name to hold the auto generated plural
    form of the class name. These two attributes can be overriden in the
    class itself.
    """
    
    
    #----------------------------------------------------------------------
    def __new__(cls, classname, bases, dict_):
        
        # create the entity_type
        dict_["entity_type"] = unicode(classname)
        
        # try to find a plural name for the class if not given
        if not dict_.has_key("plural_name"):
            
            plural_name = unicode(classname+"s")
            
            if classname[-1] == "y":
                plural_name = unicode(classname[:-1] + "ies")
            elif classname[-2] == "ch":
                plural_name = unicode(classname + "es")
            elif classname[-1] == "f":
                plural_name = unicode(classname[:-1] + "ves")
            elif classname[-1] == "s":
                plural_name = unicode(classname + "es")
            
            dict_["plural_name"] = plural_name
        
        if not dict_.has_key("__strictly_typed__"):
            dict_["__strictly_typed__"] = False
        
        return super(EntityMeta, cls).__new__(cls, classname, bases, dict_)






########################################################################
class SimpleEntity(object):
    """The base class of all the others
    
    The :class:`~stalker.core.models.SimpleEntity` is the starting point of the
    Stalker Object Model, it starts by adding the basic information about an
    entity which are :attr:`~stalker.core.models.SimpleEntity.name`,
    :attr:`~stalker.core.models.SimpleEntity.description`, the audit
    informations like :attr:`~stalker.core.models.SimpleEntity.created_by`,
    :attr:`~stalker.core.models.SimpleEntity.updated_by`,
    :attr:`~stalker.core.models.SimpleEntity.date_created`,
    :attr:`~stalker.core.models.SimpleEntity.date_updated` and a couple of
    naming attributes like :attr:`~stalker.core.models.SimpleEntity.code` and
    :attr:`~stalker.core.models.SimpleEntity.nice_name` and last but not least
    the :attr:`~stalker.core.models.SimpleEntity.type` attribute which is very
    important for entities that needs a type.
    
    For derived classes if the :attr:`~stalker.core.models.SimpleEntity.type`
    needed to be specifically specified, that is it can not be None or nothing
    else then a :class:`~stalker.core.models.Type` instance, set the
    ``strictly_typed`` class attribute to True::
      
      class NewClass(SimpleEntity):
          __strictly_typed__ = True
    
    This will ensure that the derived class always have a proper
    :attr:`~stalker.core.models.SimpleEntity.type` attribute and can not
    initialize without one.
    
    Two SimpleEntities considered to be equal if they have the same name, the
    other attributes doesn't matter.
    
    The formatting rules for the code attribute is as follows:
      
      * only alphanumerics and underscore is allowed \[a-zA-Z0-9_\]
      
      * no number is allowed at the beggining
      
      * no white spaces are allowed
      
      * all the white spaces will be converted to underscore characters
      
      * all the underscores are converted to only one underscore character if
        more than one follows each other
    
    Examples:
    
      +-----------------------------------+-----------------------------------+
      | Input Value                       | Formatted Output                  |
      +===================================+===================================+
      | testCode                          | testCode                          |
      +-----------------------------------+-----------------------------------+
      | 1testCode                         | testCode                          |
      +-----------------------------------+-----------------------------------+
      | _testCode                         | testCode                          |
      +-----------------------------------+-----------------------------------+
      | 2423$+^^+^'%+%%&_testCode         | testCode                          |
      +-----------------------------------+-----------------------------------+
      | 2423$+^^+^'%+%%&_testCode_35      | testCode_35                       |
      +-----------------------------------+-----------------------------------+
      | 2423$ +^^+^ '%+%%&_ testCode\_ 35 | testCode_35                       |
      +-----------------------------------+-----------------------------------+
      | SH001                             | SH001                             |
      +-----------------------------------+-----------------------------------+
      | My CODE is Ozgur                  | My_CODE_is_Ozgur                  |
      +-----------------------------------+-----------------------------------+
      | this is another code for an asset | this_is_another_code_for_an_asset |
      +-----------------------------------+-----------------------------------+
      
    :param string name: A string or unicode value that holds the name of this
      entity. It can not be empty, the first letter should be an alphabetic
      ([a-zA-z]) (not alphanumeric [a-zA-Z0-9]) letter and it should not
      contain any white space at the beggining and at the end of the string,
      giving an object the object will be converted to string and then the
      resulting string will be conditioned.
    
    :param str description: A string or unicode attribute that holds the
      description of this entity object, it could be an empty string, and it
      could not again have white spaces at the beggining and at the end of the
      string, again any given objects will be converted to strings
    
    :param created_by: The :class:`~stalker.core.models.User` who has created
      this object
    
    :type created_by: :class:`~stalker.core.models.User`
    
    :param updated_by: The :class:`~stalker.core.models.User` who has updated
      this object lastly. The created_by and updated_by attributes point the
      same object if this object is just created.
    
    :param date_created: The date that this object is created.
    
    :type date_created: :class:`datetime.datetime`
    
    :param date_updated: The date that this object is updated lastly. For newly
      created entities this is equal to date_created and thedate_updated cannot
      point a date which is before date_created.
    
    :type date_updated: :class:`datetime.datetime`
    
    :param str code: The code name of this object. It accepts string or unicode
      values and any other kind of objects will be converted to string. Can be
      omitted and it will be set to the same value of the nice_name attribute.
      If both the name and code arguments are given the code attribute will be
      set to the given code argument value, but in any update to name attribute
      the code also will be updated to the nice_name attribute. When the code
      is directly edited the code will not be formated other than removing any
      illegal characters. The default value is the same value of the nice_name.
    
    :param type: The type of the current SimpleEntity. Used across several
      places in Stalker. Can be None. The default value is None.
    
    :type type: :class:`~stalker.core.models.Type`
    """
    
    
    
    __metaclass__ = EntityMeta
    _nice_name = None
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 name=None,
                 description="",
                 type=None,
                 created_by=None,
                 updated_by=None,
                 date_created=datetime.datetime.now(),
                 date_updated=datetime.datetime.now(),
                 code=None,
                 **kwargs
                 ):
        
        # code attribute
        # just set it to None for now
        self._code = ""
        
        # name and nice_name
        self._nice_name = ""
        self._name = ""
        self.name = name
        
        # code
        # if the given code argument is not None
        # use it to set the code
        if code is not None and code is not "":
            self._code = self._validate_code(code)
        
        self._description = self._validate_description(description)
        self._created_by = self._validate_created_by(created_by)
        self._updated_by = self._validate_updated_by(updated_by)
        self._date_created = self._validate_date_created(date_created)
        self._date_updated = self._validate_date_updated(date_updated)
        
        self._type = self._validate_type(type)
    
    
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """the representation of the SimpleEntity
        """
        
        return "<%s (%s, %s)>" % (self.entity_type, self.name, self.code)
    
    
    
    #----------------------------------------------------------------------
    def _validate_description(self, description_in):
        """validates the given description_in value
        """
        
        if description_in is None:
            description_in = ""
        
        return str(description_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_name(self, name_in):
        """validates the given name_in value
        """
        
        # it is None
        if name_in is None:
            raise TypeError("the name couldn't be set to None")
        
        name_in = self._condition_name(str(name_in))
        
        # it is empty
        if name_in == "":
            raise ValueError("the name couldn't be an empty string")
        
        return name_in
    
    
    
    #----------------------------------------------------------------------
    def _condition_code(self, code_in):
        """formats the given code_in value
        """
        
        # just set it to the uppercase of what nice_name gives
        # remove unnecesary characters from the string
        code_in = self._validate_name(code_in)
        
        # replace camel case letters
        #code_in = re.sub(r"(.+?[a-z]+)([A-Z])", r"\1_\2", code_in)
        
        # replace white spaces with under score
        code_in = re.sub("([\s\-])+", r"_", code_in)
        
        # remove multiple underscores
        code_in = re.sub(r"([_]+)", r"_", code_in)
        
        return code_in
    
    
    
    #----------------------------------------------------------------------
    def _condition_name(self, name_in):
        """conditions the name_in value
        """
        
        # remove unnecesary characters from the string
        name_in = re.sub("([^a-zA-Z0-9\s_\-]+)", r"", name_in).strip()
        
        # remove all the characters which are not alpabetic
        name_in = re.sub("(^[^a-zA-Z]+)", r"", name_in)
        
        return name_in
    
    
    
    #----------------------------------------------------------------------
    def _condition_nice_name(self, nice_name_in):
        """conditions the given nice name
        """
        
        ## remove unnecesary characters from the beginning
        #nice_name_in = re.sub("(^[^A-Za-z]+)", r"", nice_name_in)
        
        # remove unnecesary characters from the string
        nice_name_in = self._validate_name(nice_name_in)
        
        # replace camel case letters
        nice_name_in = re.sub(r"(.+?[a-z]+)([A-Z])", r"\1_\2", nice_name_in)
        
        # replace white spaces with under score
        nice_name_in = re.sub("([\s\-])+", r"_", nice_name_in)
        
        # remove multiple underscores
        nice_name_in = re.sub(r"([_]+)", r"_", nice_name_in)
        
        # turn it to lower case
        nice_name_in = nice_name_in.lower()
        
        return nice_name_in
        
    
    
    
    #----------------------------------------------------------------------
    def description():
        
        def fget(self):
            return self._description
        
        def fset(self, description_in):
            self._description = self._validate_description(description_in)
        
        doc = """Description of this object."""
        
        return locals()
    
    description = property(**description())
    
    
    
    #----------------------------------------------------------------------
    def name():
        
        def fget(self):
            return self._name
        
        def fset(self, name_in):
            assert(isinstance(self, SimpleEntity))
            self._name = self._validate_name(name_in)
            
            # also set the nice_name
            self._nice_name = self._condition_nice_name(self._name)
            
            # set the code
            #self.code = self._nice_name.upper()
            self.code = self._name
        
        doc = """Name of this object"""
        
        return locals()
    
    name = property(**name())
    
    
    
    #----------------------------------------------------------------------
    def nice_name():
        
        def fget(self):
            # also set the nice_name
            if self._nice_name is None or self._nice_name == "":
                self._nice_name = self._condition_nice_name(self._name)
            
            return self._nice_name
        
        doc = """Nice name of this object.
        
        It has the same value with the name (contextually) but with a different
        format like, all the white spaces replaced by underscores ("\_"), all
        the CamelCase form will be expanded by underscore (\_) characters and
        it is always lower case.
        
        There is also the ``code`` attribute which is simply the upper case
        form of ``nice_name`` if it is not defined differently (i.e set to
        another value)."""
        
        return locals()
    
    nice_name = property(**nice_name())
    
    
    
    #----------------------------------------------------------------------
    def _validate_code(self, code_in):
        """validates the given code value
        """
        
        # check if the code_in is None or empty string
        if code_in is None or code_in=="":
            # restore the value from nice_name and let it be reformatted
            #code_in = self.nice_name.upper()
            code_in = self.nice_name
            
        
        return self._condition_code(str(code_in))
    
    
    
    #----------------------------------------------------------------------
    def _validate_created_by(self, created_by_in):
        """validates the given created_by_in attribute
        """
        
        if created_by_in is not None:
            if not isinstance(created_by_in, User):
                raise TypeError("the created_by attribute should be an "
                                 "instance of stalker.core.models.User")
        
        return created_by_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_updated_by(self, updated_by_in):
        """validates the given updated_by_in attribute
        """
        
        if updated_by_in is None:
            # set it to what created_by attribute has
            updated_by_in = self._created_by
        
        from stalker.core.models import User
        
        if updated_by_in is not None:
            if not isinstance(updated_by_in, User):
                raise TypeError("the updated_by attribute should be an "
                                 "instance of stalker.core.models.User")
        
        return updated_by_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_date_created(self, date_created_in):
        """validates the given date_creaetd_in
        """
        
        if date_created_in is None:
            raise TypeError("the date_created could not be None")
        
        if not isinstance(date_created_in, datetime.datetime):
            raise TypeError("the date_created should be an instance of "
                             "datetime.datetime")
        
        return date_created_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_date_updated(self, date_updated_in):
        """validates the given date_updated_in
        """
        
        # it is None
        if date_updated_in is None:
            raise TypeError("the date_updated could not be None")
        
        # it is not an instance of datetime.datetime
        if not isinstance(date_updated_in, datetime.datetime):
            raise TypeError("the date_updated should be an instance of "
                             "datetime.datetime")
        
        # lower than date_created
        if date_updated_in < self.date_created:
            raise ValueError("the date_updated could not be set to a date "
                             "before date_created, try setting the "
                             "date_created before")
        
        return date_updated_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_type(self, type_in):
        """validates the given type value
        """
        
        raise_error = False
        
        if not self.__strictly_typed__:
            if not type_in is None:
                if not isinstance(type_in, Type):
                    raise_error = True
        else:
            if not isinstance(type_in, Type):
                raise_error = True
        
        if raise_error:
            raise TypeError("%s.type must be an instance of "
                             "stalker.core.models.Type" \
                             % self.entity_type)
        
        return type_in
    
    
    
    #----------------------------------------------------------------------
    def type():
        def fget(self):
            return self._type
        
        def fset(self, type_in):
            self._type = self._validate_type(type_in)
        
        doc = """The type of the object.
        
        It is an instance of :class:`~stalker.core.models.Type` with a proper
        :attr:`~stalker.core.models.Type.target_entity_type`.
        """
        
        return locals()
    
    type = property(**type())
    
    
    
    #----------------------------------------------------------------------
    def code():
        def fget(self):
            return self._code
        
        def fset(self, code_in):
            self._code = self._validate_code(code_in)
        
        doc = """The code name of this object.
        
        It accepts string or unicode values and any other kind of objects will
        be converted to string. In any update to the name attribute the code
        also will be updated. If the code is not initialized or given as None,
        it will be set to the uppercase version of the nice_name attribute.
        Setting the code attribute to None will reset it to the default value.
        The default value is the upper case form of the nice_name."""
        
        return locals()
    
    code = property(**code())
    
    
    
    #----------------------------------------------------------------------
    def created_by():
        
        def fget(self):
            return self._created_by
        
        def fset(self, created_by_in):
            self._created_by = self._validate_created_by(created_by_in)
        
        doc = """The :class:`~stalker.core.models.User` who has created this object."""
        
        return locals()
    
    created_by = property(**created_by())
    
    
    
    #----------------------------------------------------------------------
    def updated_by():
        
        def fget(self):
            return self._updated_by
        
        def fset(self, updated_by_in):
            self._updated_by = self._validate_updated_by(updated_by_in)
        
        doc = """The :class:`~stalker.core.models.User` who has updated this object."""

        
        return locals()
    
    updated_by = property(**updated_by())
    
    
    
    #----------------------------------------------------------------------
    def date_created():
        
        def fget(self):
            return self._date_created
        
        def fset(self, date_created_in):
            self._date_created = self._validate_date_created(date_created_in)
        
        doc = """A :class:`datetime.datetime` instance showing the creation date and time of this object."""
        
        return locals()
    
    date_created = property(**date_created())
    
    
    
    #----------------------------------------------------------------------
    def date_updated():
        
        def fget(self):
            return self._date_updated
        
        def fset(self, date_updated_in):
            self._date_updated = self._validate_date_updated(date_updated_in)
        
        doc = """A :class:`datetime.datetime` instance showing the update date and time of this object."""
        
        return locals()
    
    date_updated = property(**date_updated())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return isinstance(other, SimpleEntity) and \
           self.name == other.name #and \
           #self.description == other.description
    
    
    
    #----------------------------------------------------------------------
    def __ne__(self, other):
        """the inequality operator
        """
        
        return not self.__eq__(other)






########################################################################
class Entity(SimpleEntity):
    """Another base data class that adds tags and notes to the attributes list.
    
    This is the entity class which is derived from the SimpleEntity and adds
    only tags to the list of parameters.
    
    Two Entities considered equal if they have the same name. It doesn't matter
    if they have different tags or notes.
    
    :param list tags: A list of :class:`~stalker.core.models.Tag` objects
      related to this entity. tags could be an empty list, or when omitted it
      will be set to an empty list.
    
    :param list notes: A list of :class:`~stalker.core.models.Note` instances.
      Can be an empty list, or when omitted it will be set to an empty list,
      when set to None it will be converted to an empty list.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 tags=[],
                 notes=[],
                 **kwargs
                 ):
        
        super(Entity, self).__init__(**kwargs)
        
        self._tags = self._validate_tags(tags)
        self._notes = self._validate_notes(notes)
    
    
    
    #----------------------------------------------------------------------
    def _validate_notes(self, notes_in):
        """validates the given notes value
        """
        
        if not isinstance(notes_in, list):
            raise TypeError("notes should be an instance of list")
        
        from stalker.core.models import Note
        
        for element in notes_in:
            if not isinstance(element, Note):
                raise TypeError("every element in notes should be an "
                                 "instance of stalker.core.models.Note "
                                 "class")
        
        return ValidatedList(notes_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_tags(self, tags_in):
        """validates the given tags_in value
        """
        
        # it is not an instance of list
        if not isinstance(tags_in, list):
            raise TypeError("the tags attribute should be set to a list")
        
        return ValidatedList(tags_in)
    
    
    
    #----------------------------------------------------------------------
    def notes():
        def fget(self):
            return self._notes
        def fset(self, notes_in):
            self._notes = self._validate_notes(notes_in)
        
        doc = """All the notes about this entity.
        
        It is a list of :class:`~stalker.core.models.Note` objects or an empty
        list, None will be converted to an empty list.
        """
        
        return locals()
    
    notes = property(**notes())
    
    
    
    #----------------------------------------------------------------------
    def tags():
        
        def fget(self):
            return self._tags
        
        def fset(self, tags_in):
            self._tags = self._validate_tags(tags_in)
        
        doc = """A list of tags attached to this object.
        
        It is a list of :class:`~stalker.core.models.Tag` instances which shows
        the tags of this object"""
        
        return locals()
    
    tags = property(**tags())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Entity, self).__eq__(other) and \
               isinstance(other, Entity)






########################################################################
class Type(Entity):
    """Everything can have a type.
    
    .. versionadded:: 0.1.1
      Types
    
    Type is a generalized version of the previous design that defines types for
    specific classes.
    
    The purpose of the :class:`~stalker.core.models.Type` class is just to
    define a new type for a specific :class:`~stalker.core.models.Entity`. For
    example, you can have a ``Character`` :class:`~stalker.core.models.Asset`
    or you can have a ``Commercial`` :class:`~stalker.core.models.Project` or
    you can define a :class:`~stalker.core.models.Link` as an ``Image`` etc.,
    to create a new :class:`~stalker.core.models.Type` for various classes::
    
      Type(name="Character", target_entity_type="Asset")
      Type(name="Commercial", target_entity_type="Project")
      Type(name="Image", target_entity_type="Link")
    
    or::
      
      Type(name="Character", target_entity_type=Asset.entity_type)
      Type(name="Commercial", target_entity_type=Project.entity_type)
      Type(name="Image", target_entity_type=Link.entity_type)
    
    or even better:
      
      Type(name="Character", target_entity_type=Asset)
      Type(name="Commercial", target_entity_type=Project)
      Type(name="Image", target_entity_type=Link)
    
    By using :class:`~stalker.core.models.Type`\ s, one can able to sort and
    group same type of entities.
    
    :class:`~stalker.core.models.Type`\ s are generally used in
    :class:`~stalker.core.models.Structure`\ s.
    
    :param string target_entity_type: The string defining the target type of
      this :class:`~stalker.core.models.Type`.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, target_entity_type=None, **kwargs):
        super(Type, self).__init__(**kwargs)
        
        self._target_entity_type =\
            self._validate_target_entity_type(target_entity_type)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Type, self).__eq__(other) and isinstance(other, Type) \
               and self.target_entity_type == other.target_entity_type
    
    
    
    #----------------------------------------------------------------------
    def __ne__(self, other):
        """the inequality operator
        """
        
        return not self.__eq__(other)
    
    
    
    #----------------------------------------------------------------------
    def _validate_target_entity_type(self, target_entity_type_in):
        """validates the given target_entity_type value
        """
        
        # check if a class is given
        if isinstance(target_entity_type_in, type):
            target_entity_type_in = target_entity_type_in.__name__
        
        error_string = "target_entity_type must be a string showing the "\
                     "target class name"
        
        if target_entity_type_in is None \
           or not isinstance(target_entity_type_in, str):
            raise TypeError(error_string)
        
        if target_entity_type_in == "":
            raise ValueError(error_string)
        
        return target_entity_type_in
    
    
    
    #----------------------------------------------------------------------
    def target_entity_type():
        def fget(self):
            return self._target_entity_type
        
        doc = """The target type of this Type instance.
        
        It is a string, showing the name of the target type class. It is a
        read-only attribute.
        """
        
        return locals()
    
    target_entity_type = property(**target_entity_type())
    






########################################################################
class Status(Entity):
    """Defins object statutes.
    
    No extra parameters, use the *code* attribute to give a short name for the
    status.
    
    A Status object can be compared with a string or unicode value and it will
    return if the lower case name or lower case code of the status matches the
    lower case form of the given string:
    
    >>> from stalker.core.models import Status
    >>> a_status = Status(name="On Hold", "OH")
    >>> a_status == "on hold"
    True
    >>> a_status != "complete"
    True
    >>> a_status == "oh"
    True
    >>> a_status == "another status"
    False
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        
        super(Status,self).__init__(**kwargs)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        if isinstance(other, (str, unicode)):
            return self.name.lower() == other.lower() or \
                   self.code.lower() == other.lower()
        else:
            return super(Status, self).__eq__(other) and \
                   isinstance(other, Status)






########################################################################
class StatusList(Entity):
    """Type specific list of :class:`~stalker.core.models.Status` instances.
    
    Holds multiple statuses to be used as a choice list for several other
    classes.
    
    A StatusList can only be assigned to only one entity type. So a Project can
    only have a suitable StatusList object which is designed for Project
    entities.
    
    The list of statuses in StatusList can be accessed by using a list like
    indexing and it also supports string indexes only for getting the item,
    you can not set an item with string indices:
    
    >>> from stalker.core.models import Status, StatusList
    >>> status1 = Status(name="Complete", code="CMPLT")
    >>> status2 = Status(name="Work in Progress", code="WIP")
    >>> status3 = Status(name="Pending Review", code="PRev")
    >>> a_status_list = StatusList(name="Asset Status List",
                                   statuses=[status1, status2, status3],
                                   target_entity_type="Asset")
    >>> a_status_list[0]
    <Status (Complete, CMPLT)>
    >>> a_status_list["complete"]
    <Status (Complete, CMPLT)>
    >>> a_status_list["wip"]
    <Status (Work in Progress, WIP)>
    
    :param statuses: this is a list of status objects, so you can prepare
      different StatusList objects for different kind of entities
    
    :param target_entity_type: use this parameter to specify the target entity
      type that this StatusList is designed for. It accepts classes or names
      of classes.
      For example::
        
        from stalker.core.models import Status, StatusList, Project
        
        status_list = [
            Status(name="Waiting To Start", code="WTS"),
            Status(name="On Hold", code="OH"),
            Status(name="In Progress", code="WIP"),
            Status(name="Waiting Review", code="WREV"),
            Status(name="Approved", code="APP"),
            Status(name="Completed", code="CMPLT"),
        ]
        
        project_status_list = StatusList(
            name="Project Status List",
            statuses=status_list,
            target_entity_type="Project"
        )
        
        # or
        project_status_list = StatusList(
            name="Project Status List",
            statuses=status_list,
            target_entity_type=Project
        )
      
      now with the code above you can not assign the ``project_status_list``
      object to any other class than a ``Project`` object.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 statuses=[],
                 target_entity_type="",
                 **kwargs
                 ):
        
        super(StatusList,self).__init__(**kwargs)
        
        self._statuses = self._validate_statuses(statuses)
        
        self._target_entity_type = \
            self._validate_target_entity_type(target_entity_type)
    
    
    
    #----------------------------------------------------------------------
    def _validate_statuses(self, statuses):
        """validates the given status_list
        """
        
        if not isinstance(statuses, list):
            raise TypeError("statuses should be an instance of list")
        
        if len(statuses) < 1:
            raise ValueError("statuses should not be an empty list")
        
        for item in statuses:
            self._validate_status(item)
        
        return ValidatedList(statuses)
    
    
    
    #----------------------------------------------------------------------
    def _validate_target_entity_type(self, target_entity_type_in):
        """validates the given target_entity_type value
        """
        
        # it can not be None
        if target_entity_type_in is None:
            raise TypeError("target_entity_type can not be None")
        
        if str(target_entity_type_in)=="":
            raise ValueError("target_entity_type can not be empty string")
        
        # check if it is a class
        if isinstance(target_entity_type_in, type):
            target_entity_type_in = target_entity_type_in.__name__
        
        return str(target_entity_type_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_status(self, status_in):
        """validates the given status_in
        """
        
        if not isinstance(status_in, Status):
            raise TypeError("all elements must be an instance of Status in "
                            "the given statuses list")
        
        return status_in
    
    
    
    #----------------------------------------------------------------------
    def statuses():
        
        def fget(self):
            return self._statuses
        
        def fset(self, statuses):
            self._statuses = self._validate_statuses(statuses)
        
        doc = """list of :class:`~stalker.core.models.Status` objects,
        showing the possible statuses"""
        
        return locals()
    
    statuses = property(**statuses())
    
    
    
    #----------------------------------------------------------------------
    def target_entity_type():
        
        def fget(self):
            return self._target_entity_type
        
        doc="""the entity type which this StatusList is valid for, usally it
        is set to the TargetClass.entity_type class attribute of the target
        class::
          
          from stalker.core.models import Status, StatusList, Asset
          
          # now create a StatusList valid only for assets
          status1 = Status(name="Waiting To Start", code="WTS")
          status2 = Status(name="Work In Progress", code="WIP")
          status3 = Status(name="Complete", code="CMPLT")
        """
        
        return locals()
    
    target_entity_type = property(**target_entity_type())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(StatusList, self).__eq__(other) and \
               isinstance(other, StatusList) and \
               self.statuses == other.statuses and \
               self.target_entity_type == other.target_entity_type
    
    
    
    #----------------------------------------------------------------------
    def __getitem__(self, key):
        """the indexing attributes for getting item
        """
        if isinstance(key, (str, unicode)):
            for item in self._statuses:
                if item==key:
                    return item
        else:
            return self._statuses[key]
    
    
    #----------------------------------------------------------------------
    def __setitem__(self, key, value):
        """the indexing attributes for setting item
        """
        
        self._statuses[key] = self._validate_status(value)
    
    
    
    #----------------------------------------------------------------------
    def __delitem__(self, key):
        """the indexing attributes for deleting item
        """
        
        del self._statuses[key]
    
    
    
    #----------------------------------------------------------------------
    def __len__(self):
        """the indexing attributes for getting the length
        """
        
        return len(self._statuses)






########################################################################
class ImageFormat(Entity):
    """Common image formats for the projects.
    
    adds up this parameters to the SimpleEntity:
    
    :param width: the width of the format, it cannot be zero or negative, if a
      float number is given it will be converted to integer
    
    :param height: the height of the format, it cannot be zero or negative, if
      a float number is given it will be converted to integer
    
    :param pixel_aspect: the pixel aspect ratio of the current ImageFormat
      object, it can not be zero or negative, and if given as an integer it
      will be converted to a float, the default value is 1.0
    
    :param print_resolution: the print resolution of the ImageFormat given as
      DPI (dot-per-inch). It can not be zero or negative
    
    """
    
    
    
    _device_aspect = None
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 width=None,
                 height=None,
                 pixel_aspect=1.0,
                 print_resolution=300,
                 **kwargs
                 ):
        
        super(ImageFormat,self).__init__(**kwargs)
        
        self._width = self._validate_width(width)
        self._height = self._validate_height(height)
        self._pixel_aspect = self._validate_pixel_aspect(pixel_aspect)
        self._print_resolution = \
            self._validate_print_resolution(print_resolution)
        self._device_aspect = 1.0
        
        self._update_device_aspect()
        
    
    
    #----------------------------------------------------------------------
    def _update_device_aspect(self):
        """updates the device aspect ratio for the given width and height
        """
        self._device_aspect = float(self._width) / float(self._height) \
            * float(self._pixel_aspect)
    
    
    
    #----------------------------------------------------------------------
    def _validate_width(self, width):
        """validates the given width
        """
        if not isinstance(width, (int, float)):
            raise TypeError("width should be an instance of int or float")
        
        if width <= 0:
            raise ValueError("width shouldn't be zero or negative")
        
        return int(width)
    
    
    
    #----------------------------------------------------------------------
    def _validate_height(self, height):
        """validates the given height
        """
        if not isinstance(height, (int, float)):
            raise TypeError("height should be an instance of int or float")
        
        if height <= 0:
            raise ValueError("height shouldn't be zero or negative")
        
        return int(height)
    
    
    
    #----------------------------------------------------------------------
    def _validate_pixel_aspect(self, pixel_aspect):
        """validates the given pixel aspect
        """
        if not isinstance(pixel_aspect, (int, float)):
            raise TypeError("pixel_aspect should be an instance of int or "
                             "float")
        
        if pixel_aspect <= 0:
            raise ValueError("pixel_aspect can not be zero or a negative "
                             "value")
        
        return float(pixel_aspect)
    
    
    
    #----------------------------------------------------------------------
    def _validate_print_resolution(self, print_resolution):
        """validates the print resolution
        """
        if not isinstance(print_resolution, (int, float)):
            raise TypeError("print resolution should be an instance of int "
                             "or float")
        
        if print_resolution <= 0:
            raise ValueError("print resolution should not be zero or "
                             "negative")
        
        return float(print_resolution)
    
    
    
    #----------------------------------------------------------------------
    def width():
        def fget(self):
            """returns the width
            """
            return self._width
        
        def fset(self, width):
            """sets the width
            """
            self._width = self._validate_width(width)
            # also update the device_aspect
            self._update_device_aspect()
        
        doc = """this is a property to set and get the width of the
        image_format
        
        * the width should be set to a positif non-zero integer
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise an exception.
        """
        
        return locals()
    
    width = property(**width())
    
    
    
    #----------------------------------------------------------------------
    def height():
        def fget(self):
            """returns the height
            """
            return self._height
        
        def fset(self, height):
            """sets the height
            """
            self._height = self._validate_height(height)
            
            # also update the device_aspect
            self._update_device_aspect()
        
        doc = """this is a property to set and get the height of the
        image_format
        
        * the height should be set to a positif non-zero integer
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise an exception.
        """
        
        return locals()
    
    height = property(**height())
    
    
    
    #----------------------------------------------------------------------
    def pixel_aspect():
        def fget(self):
            """returns the pixel_aspect ratio
            """
            return self._pixel_aspect
        
        def fset(self, pixel_aspect):
            """sets the pixel_aspect ratio
            """
            self._pixel_aspect = self._validate_pixel_aspect(pixel_aspect)
            
            # also update the device_aspect
            self._update_device_aspect()
        
        doc = """this is a property to set and get the pixel_aspect of the
        ImageFormat
        
        * the pixel_aspect should be set to a positif non-zero float
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise an exception
        """
        
        return locals()
    
    pixel_aspect = property(**pixel_aspect())
    
    
    
    #----------------------------------------------------------------------
    @property
    def device_aspect(self):
        """returns the device aspect
        
        because the device_aspect is calculated from the width/height*pixel
        formula, this property is read-only.
        """
        if self._device_aspect is None:
            self._update_device_aspect()
        return self._device_aspect
    
    
    
    #----------------------------------------------------------------------
    def print_resolution():
        
        def fget(self):
            """returns the print resolution
            """
            return self._print_resolution
        
        def fset(self, print_resolution):
            """sets the print resolution
            """
            self._print_resolution = \
                self._validate_print_resolution(print_resolution)
        
        doc = """this is a property to set and get the print_resolution of the
        ImageFormat
        
        * it should be set to a positif non-zero float or integer
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise an exception.
        """
        
        return locals()
    
    print_resolution = property(**print_resolution())
    
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(ImageFormat, self).__eq__(other) and \
               isinstance(other, ImageFormat) and \
               self.width == other.width and \
               self.height == other.height and \
               self.pixel_aspect == other.pixel_aspect






########################################################################
class Link(Entity):
    """Holds data about external links.
    
    Links are all about to give some external information to the current entity
    (external to the database, so it can be something on the
    :class:`~stalker.core.models.Repository` or in the Web). The
    link type is defined by the :class:`~stalker.core.models.LinkType` object
    and it can be anything like *General*, *File*, *Folder*, *WebPage*,
    *Image*, *ImageSequence*, *Movie*, *Text* etc. (you can also use multiple
    :class:`~stalker.core.models.Tag` objects to adding more information,
    and filtering back). Again it is defined by the needs of the studio.
    
    :param path: The Path to the link, it can be a path to a file in the file
      system, or a web page.  Setting path to None or an empty string is not
      accepted.
    
    :param filename: The file name part of the link url, for file sequences use
      "#" in place of the numerator (`Nuke`_ style). Setting filename to None
      or an empty string is not accepted.
    
    .. _Nuke: http://www.thefoundry.co.uk
    """
    
    
    
    __strictly_typed__ = True
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, path="", filename="", **kwargs):
        super(Link, self).__init__(**kwargs)
        
        self._path = self._validate_path(path)
        self._filename = self._validate_filename(filename)
        #self._type = self._validate_type(type)
    
    
    
    #----------------------------------------------------------------------
    def _validate_path(self, path_in):
        """validates the given path
        """
        
        if path_in is None:
            raise TypeError("path can not be None")
        
        if not isinstance(path_in, (str, unicode)):
            raise TypeError("path should be an instance of string or unicode")
        
        if path_in=="":
            raise ValueError("path can not be an empty string")
        
        return self._format_path(path_in)
    
    
    
    #----------------------------------------------------------------------
    def _format_path(self, path_in):
        """formats the path to internal format, which is Linux forward slashes
        for path seperation
        """
        
        return path_in.replace("\\", "/")
    
    
    
    #----------------------------------------------------------------------
    def _validate_filename(self, filename_in):
        """validates the given filename
        """
        
        if filename_in is None:
            raise TypeError("filename can not be None")
        
        if not isinstance(filename_in, (str, unicode)):
            raise TypeError("filename should be an instance of string or "
                             "unicode")
        
        if filename_in=="":
            raise ValueError("filename can not be an empty string")
        
        return filename_in
    
    
    
    #----------------------------------------------------------------------
    def path():
        def fget(self):
            return self._path
        
        def fset(self, path_in):
            self._path = self._validate_path(path_in)
        
        doc="""the path part of the url to the link, it can not be None or an
        empty string, it should be a string or unicode"""
        
        return locals()
    
    path = property(**path())
    
    
    
    #----------------------------------------------------------------------
    def filename():
        def fget(self):
            return self._filename
        
        def fset(self, filename_in):
            self._filename = self._validate_filename(filename_in)
        
        doc="""the filename part of the url to the link, it can not be None or
        an empty string, it should be a string or unicode"""
        
        return locals()
    
    filename = property(**filename())
    
    
    
    ##----------------------------------------------------------------------
    #def type():
        #def fget(self):
            #return self._type
        
        #def fset(self, type_in):
            #self._type = self._validate_type(type_in)
        
        #doc="""the type of the link, it should be a
        #:class:`~stalker.core.models.LinkType` object and it can not be
        #None"""
        
        #return locals()
    
    #type = property(**type())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Link, self).__eq__(other) and \
               isinstance(other, Link) and \
               self.path == other.path and \
               self.filename == other.filename and \
               self.type == other.type





# mixin class imports should be placed after StatusList and Link definitions
from stalker.core.mixins import (ReferenceMixin, ScheduleMixin, StatusMixin,
                                 TaskMixin, ProjectMixin)






########################################################################
class Booking(Entity):
    """Holds information about the time spend on a specific task by a specific user.
    """
    
    
    
    pass







########################################################################
class Comment(Entity):
    """User reviews and comments about other entities.
    
    :param body: the body of the comment, it is a string or unicode variable,
      it can be empty but it is then meaningles to have an empty comment.
      Anything other than a string or unicode will raise a TypeError.
    
    :param to: the relation variable, that holds the connection that this
      comment is related to. it should be an Entity object, any other will
      raise a TypeError.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, body="", to=None, **kwargs):
        super(Comment, self).__init__(**kwargs)
        
        self._body = self._validate_body(body)
        self._to = self._validate_to(to)
    
    
    
    #----------------------------------------------------------------------
    def _validate_body(self, body_in):
        """validates the given body variable
        """
        
        # the body could be empty
        # but it should be an instance of string or unicode
        
        if not isinstance(body_in, (str, unicode)):
            raise TypeError("the body attribute should be an instance of "
                              "string or unicode")
        
        return body_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_to(self, to_in):
        """validates the given to variable
        """
        
        
        # the to variable should be:
        # - not None
        # - an instance of Entity object
        
        if to_in is None:
            raise TypeError("the to attribute could not be None")
        
        if not isinstance(to_in, Entity):
            raise TypeError("the to attibute should be an instance of "
                             "Entity class")
        
        return to_in
    
    
    
    #----------------------------------------------------------------------
    def body():
        def fget(self):
            return self._body
        
        def fset(self, body_in):
            self._body = self._validate_body(body_in)
        
        doc = """this is the property that sets and returns the body attribute
        """
        
        return locals()
    
    body = property(**body())
    
    
    
    #----------------------------------------------------------------------
    def to():
        def fget(self):
            return self._to
        
        def fset(self, to_in):
            self._to = self._validate_to(to_in)
        
        doc = """this is the property that sets and returns the to attribute
        """
        
        return locals()
    
    to = property(**to())






########################################################################
class Department(Entity):
    """The departments that forms the studio itself.
    
    The informations that a Department object holds is like:
    
      * The members of the department
      * The lead of the department
      * and all the other things those are inherited from the AuditEntity class
    
    Two Department object considered the same if they have the same name, the
    the members list nor the lead info is important, a "Modeling" department
    should of course be the same with another department which has the name
    "Modeling" again.
    
    so creating a department object needs the following parameters:
    
    :param members: it can be an empty list, so one department can be created
      without any member in it. But this parameter should be a list of User
      objects.
    
    :param lead: this is a User object, that holds the lead information, a lead
      could be in this department but it is not forced to be also a member of
      the department. So another departments member can be a lead for another
      department. Lead attribute can not be empty or None.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, members=[], lead=None, **kwargs):
        super(Department, self).__init__(**kwargs)
        
        self._members = self._validate_members(members)
        self._lead = self._validate_lead(lead)
    
    
    
    #----------------------------------------------------------------------
    def _validate_members(self, members):
        """validates the given members attribute
        """
        
        if not isinstance(members, list):
            raise TypeError("members should be a list of "
                             "stalker.core.models.User instances")
        
        if not all([isinstance(member, User) for member in members]):
            raise TypeError("every element in the members list should be "
                             "an instance of stalker.core.models.User"
                             " class")
        
        return ValidatedList(members, User)
    
    
    
    #----------------------------------------------------------------------
    def _validate_lead(self, lead):
        """validates the given lead attribute
        """
        
        if lead is not None:
            # the lead should be an instance of User class
            if not isinstance(lead, User):
                raise TypeError("lead should be an instance of "
                                 "stalker.core.models.User")
        
        return lead
    
    
    
    #----------------------------------------------------------------------
    def members():
        
        def fget(self):
            return self._members
        
        def fset(self, members):
            self._members = self._validate_members(members)
        
        doc = """members are a list of users representing the members of this
        department"""
        
        return locals()
    
    members = property(**members())
    
    
    
    #----------------------------------------------------------------------
    def lead():
        
        def fget(self):
            return self._lead
        
        def fset(self, lead):
            self._lead = self._validate_lead(lead)
        
        doc = """lead is the lead of this department, it is a User object"""
        
        return locals()
    
    lead = property(**lead())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Department, self).__eq__(other) and \
               isinstance(other, Department)





########################################################################
class PermissionGroup(SimpleEntity):    
    """Manages permission in the system.
    
    A PermissionGroup object maps permission for tasks like Create, Read,
    Update, Delete operations in the system to available classes in the system.
    
    It reads the :attr:`~stalker.conf.defaults.CORE_MODEL_CLASSES` list to get
    the list of available classes which can be created. It then stores a binary
    value for each of the class.
    
    A :class:`~stalker.core.models.User` can be in several
    :class:`~stalker.core.models.PermissionGroup`\ s. The combined permission
    for an object is calculated with an ``OR`` (``^``) operation. So if one of
    the :class:`~stalker.core.models.PermissionGroup`\ s of the
    :class:`~stalker.core.models.User` is allowing the action then the user is
    allowed to do the operation.
    
    The permissions are stored in a dictionary. The key is the class name and
    the value is a 4-bit binary integer value like 0b0001.
    
    +-------------------+--------+------+--------+--------+
    |        0b         |   0    |  0   |   0    |   0    |
    +-------------------+--------+------+--------+--------+
    | binary identifier | Create | Read | Update | Delete |
    |                   | Bit    | Bit  | Bit    | Bit    |
    +-------------------+--------+------+--------+--------+
    
    :param dict permissions: A Python dictionary showing the permissions. The
      key is the name of the Class and the value is the permission bit.
    
    
    NOTE TO DEVELOPERS: a Dictionary-Based Collections should be used in
    SQLAlchemy.
    """
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(PermissionGroup, self).__init__(**kwargs)
        
        pass






########################################################################
class Message(Entity, StatusMixin):
    """The base of the messaging system in Stalker
    
    Messages are one of the ways to collaborate in Stalker. The model of the
    messages is taken from the e-mail system. So it is pretty similiar to an
    e-mail message.
    
    :param from: the :class:`~stalker.core.models.User` object sending the
      message
    
    :param to: the list of :class:`~stalker.core.models.User`\ s to
      receive this message
    
    :param subject: the subject of the message
    
    :param body: the body of the message
    
    :param in_reply_to: the :class:`~stalker.core.models.Message`
      object which this message is a reply to.
    
    :param replies: the list of :class:`~stalker.core.models.Message`
      objects which are the direct replies of this message
    
    :param attachments: a list of
      :class:`~stalker.core.models.SimpleEntity` objects attached to
      this message (so anything can be attached to a message)
    
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(Message, self).__init__(**kwargs)






########################################################################
class Note(SimpleEntity):
    """To leave notes about the connected node
    
    To leave notes in Stalker use the Note class
    
    :param content: the content of the note
    
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, content="", **kwargs):
        super(Note, self).__init__(**kwargs)
        
        self._content = self._validate_content(content)
    
    
    
    #----------------------------------------------------------------------
    def _validate_content(self, content_in):
        """validates the given content
        """
        
        
        
        if content_in is not None and \
           not isinstance(content_in, (str, unicode)):
            raise TypeError("content should be an instance of string or "
                             "unicode")
        
        return content_in
    
    
    
    #----------------------------------------------------------------------
    def content():
        def fget(self):
            return self._content
        
        def fset(self, content_in):
            self._content = self._validate_content(content_in)
        
        doc = """content is a string representing the content of this Note,
        can be given as an empty string or can be even None, but anything other
        than None or string or unicode will raise a TypeError"""
        
        return locals()
    
    content = property(**content())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Note, self).__eq__(other) and \
               isinstance(other, Note) and \
               self.content == other.content






########################################################################
class Project(Entity, ReferenceMixin, StatusMixin, ScheduleMixin, TaskMixin):
    """All the information about a Project in Stalker is hold in this class.
    
    Project is one of the main classes that will direct the others. A project
    in Stalker is a gathering point.
    
    It is mixed with :class:`~stalker.core.mixins.ReferenceMixin`,
    :class:`~stalker.core.mixins.StatusMixin`,
    :class:`~stalker.core.mixins.ScheduleMixin` and
    :class:`~stalker.core.mixins.TaskMixin` to give reference, status, schedule
    and task abilities. Please read the individual documentation of each of the
    mixins.
    
    The :attr:`~stalker.core.models.Project.users` attributes content is
    gathered from all the :class:`~stalker.core.models.Task`\ s of the project
    itself and from the :class:`~stalker.core.models.Task`\ s of the
    :class:`~stalker.core.models.Sequence`\ s stored in the
    :attr:`~stalker.core.models.Project.sequences` attribute, the
    :class:`~stalker.core.models.Shot`\ s stored in the
    :attr:`~stalker.core.models.Sequence.shots` attribute, the
    :class:`~stalker.core.models.Asset`\ s stored in the
    :attr:`~stalker.core.models.Project.assets`. It is a read only attribute.
    
    :param lead: The lead of the project. Default value is None.
    
    :type lead: :class:`~stalker.core.models.User`
    
    :param list sequences: The sequences of the project, it should be a list of
      :class:`~stalker.core.models.Sequence` instances, if set to None it is
      converted to an empty list. Default value is an empty list.
    
    :param list assets: The assets used in this project, it should be a list of
      :class:`~stalker.core.models.Asset` instances, if set to None it is
      converted to an empty list. Default value is an empty list.
    
    :param image_format: The output image format of the project. Default
      value is None.
    
    :type image_format: :class:`~stalker.core.models.ImageFormat`
    
    :param float fps: The FPS of the project, it should be a integer or float
      number, or a string literal which can be correctly converted to a float.
      Default value is 25.0.
    
    :param type: The type of the project. Default value is None.
    
    :type type: :class:`~stalker.core.models.ProjectType`
    
    :param structure: The structure of the project. Default value is None
    
    :type structure: :class:`~stalker.core.models.Structure`
    
    :param repository: The repository that the project files are going to be
      stored in. You can not create the project folder structure if the project
      doesn't have a connection to a
      :class:`~stalker.core.models.Repository`. Default value is
      None.
    
    :type repository: :class:`~stalker.core.models.Repository`.
    
    :param bool is_stereoscopic: a bool value, showing if the project is going
      to be a stereo 3D project, anything given as the argument will be
      converted to True or False. Default value is False.
    
    :param float display_width: the width of the display that the output of the
      project is going to be displayed (very unnecessary if you are not using
      stereo 3D setup). Should be an int or float value, negative values
      converted to the positive values. Default value is 1.
    """
    
    
    
    __strictly_typed__ = True
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 lead=None,
                 repository=None,
                 structure=None,
                 sequences=[],
                 assets=[],
                 image_format=None,
                 fps=25.0,
                 is_stereoscopic=False,
                 display_width=1.0,
                 **kwargs):
        
        super(Project, self).__init__(**kwargs)
        # call the mixin __init__ methods
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)
        TaskMixin.__init__(self, **kwargs)
        
        self._lead = self._validate_lead(lead)
        self._users = []
        self._repository = self._validate_repository(repository)
        self._structure = self._validate_structure(structure)
        self._sequences = self._validate_sequences(sequences)
        self._assets = self._validate_assets(assets)
        
        # do not persist this attribute
        self._project_duration = self._due_date - self._start_date
        
        self._image_format = self._validate_image_format(image_format)
        self._fps = self._validate_fps(fps)
        self._is_stereoscopic = bool(is_stereoscopic)
        self._display_width = self._validate_display_width(display_width)
    
    
    
    #----------------------------------------------------------------------
    def _validate_assets(self, assets_in):
        """validates the given assets_in lists
        """
        
        if assets_in is None:
            assets_in = []
        
        if not isinstance(assets_in, list):
            raise TypeError("assets should be a list of "
                            "stalker.core.models.Assets instances")
        
        if not all([isinstance(element, Asset)
                    for element in assets_in]):
            raise TypeError("the elements in assets lists should be all "
                            "stalker.core.models.Asset instances")
        
        return ValidatedList(assets_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_display_width(self, display_width_in):
        """validates the given display_width_in value
        """
        
        return abs(float(display_width_in))
    
    
    
    #----------------------------------------------------------------------
    def _validate_fps(self, fps_in):
        """validates the given fps_in value
        """
        
        fps_in = float(fps_in)
        
        return fps_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_image_format(self, image_format_in):
        """validates the given image format
        """
        
        if image_format_in is not None and \
           not isinstance(image_format_in, ImageFormat):
            raise TypeError("the image_format should be an instance of "
                            "stalker.core.models.ImageFormat")
        
        return image_format_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_lead(self, lead_in):
        """validates the given lead_in value
        """
        
        if lead_in is not None:
            if not isinstance(lead_in, User):
                raise TypeError("lead must be an instance of "
                                "stalker.core.models.User")
        
        return lead_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_repository(self, repository_in):
        """validates the given repository_in value
        """
        
        if repository_in is not None and \
           not isinstance(repository_in, Repository):
            raise TypeError("the repsoitory should be an instance of "
                            "stalker.core.models.Repository")
        
        return repository_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_sequences(self, sequences_in):
        """validates the given sequences_in value
        """
        
        if sequences_in is None:
            sequences_in = []
        
        if not isinstance(sequences_in, list):
            raise TypeError("sequences should be a list of "
                            "stalker.core.models.Sequence instances")
        
        if not all([isinstance(seq, Sequence)
                    for seq in sequences_in]):
            raise TypeError("sequences should be a list of "
                            "stalker.core.models.Sequence instances")
        
        return ValidatedList(sequences_in, Sequence)
    
    
    
    #----------------------------------------------------------------------
    def _validate_structure(self, structure_in):
        """validates the given structure_in vlaue
        """
        
        if structure_in is not None:
            if not isinstance(structure_in, Structure):
                raise TypeError("structure should be an instance of "
                                 "stalker.core.models.Structure")
        
        return structure_in
    
    
    
    ##----------------------------------------------------------------------
    #def _validate_users(self, users_in):
        #"""validates the given users_in value
        #"""
        
        #if users_in is None:
            #users_in = []
        
        #if not isinstance(users_in, list):
            #raise TypeError("users should be a list of "
                             #"stalker.core.models.User instances")
        
        #if not all([isinstance(element, User) \
                    #for element in users_in]):
            #raise TypeError("users should be a list containing instances of "
                             #":class:`~stalker.core.models.User`")
        
        #return ValidatedList(users_in)
    
    
    
    #----------------------------------------------------------------------
    def assets():
        def fget(self):
            return self._assets
        
        def fset(self, assets_in):
            self._assets = self._validate_assets(assets_in)
        
        doc = """the list of assets created in this project"""
        
        return locals()
    
    assets = property(**assets())
    
    
    
    #----------------------------------------------------------------------
    def display_width():
        def fget(self):
            return self._display_width
        
        def fset(self, display_width_in):
            self._display_width = \
                self._validate_display_width(display_width_in)
        
        doc = """the target display width that this project is going to be
        displayed on, meaningfull if this project is a stereoscopic project"""
        
        return locals()
    
    display_width = property(**display_width())
    
    
    
    #----------------------------------------------------------------------
    def fps():
        def fget(self):
            return self._fps
        def fset(self, fps_in):
            self._fps = self._validate_fps(fps_in)
        
        doc = """the fps of the project, it is a float value, any other types
        will be converted to float. The default value is 25.0"""
        
        return locals()
    
    fps = property(**fps())
    
    
    
    #----------------------------------------------------------------------
    def image_format():
        def fget(self):
            return self._image_format
        def fset(self, image_format_in):
            self._image_format = \
                self._validate_image_format(image_format_in)
        
        doc = """the image format of the current project. This value defines
        the output image format of the project, should be an instance of
        :class:`~stalker.core.models.ImageFormat`, can not be
        skipped"""
        
        return locals()
    
    image_format = property(**image_format())
    
    
    
    #----------------------------------------------------------------------
    def is_stereoscopic():
        def fget(self):
            return self._is_stereoscopic
        def fset(self, is_stereoscopic_in):
            self._is_stereoscopic = bool(is_stereoscopic_in)
        
        doc= """True if the project is a stereoscopic project"""
        
        return locals()
    
    is_stereoscopic = property(**is_stereoscopic())
    
    
    
    #----------------------------------------------------------------------
    def lead():
        def fget(self):
            return self._lead
        def fset(self, lead_in):
            self._lead = self._validate_lead(lead_in)
        
        doc = """the lead of the project, should be an instance of
        :class:`~stalker.core.models.User`, also can set to None"""
        
        return locals()
    
    lead = property(**lead())
    
    
    
    #----------------------------------------------------------------------
    def repository():
        def fget(self):
            return self._repository
        def fset(self, repository_in):
            self._repository = self._validate_repository(repository_in)
        
        doc = """the repository that this project should reside, should be an
        instance of :class:`~stalker.core.models.Repository`, can
        not be skipped"""
        
        return locals()
    
    repository = property(**repository())
    
    
    
    #----------------------------------------------------------------------
    def sequences():
        def fget(self):
            return self._sequences
        def fset(self, sequences_in):
            self._sequences = self._validate_sequences(sequences_in)
        
        doc = """the sequences contained in this project, should be a list
        containing all of :class:`~stalker.core.models.Sequence`
        instances, when set to None it is converted to an empty list"""
        
        return locals()
    
    sequences = property(**sequences())
    
    
    
    #----------------------------------------------------------------------
    def structure():
        def fget(self):
            return self._structure
        def fset(self, structure_in):
            self._structure = self._validate_structure(structure_in)
        
        doc = """The structure of the project. Should be an instance of
        :class:`~stalker.core.models.Structure` class"""
        
        return locals()
    
    structure = property(**structure())
    
    
    
    #----------------------------------------------------------------------
    def users():
        def fget(self):
            #return self._users
            
            self._users = []
            # project tasks
            for task in self.tasks:
                self._users.extend(task.resources)
            
            # sequence tasks
            for seq in self.sequences:
                for task in seq.tasks:
                    self._users.extend(task.resources)
                
                # shot tasks
                for shot in seq.shots:
                    for task in shot.tasks:
                        self._users.extend(task.resources)
            
            # asset tasks
            for asset in self.assets:
                for task in asset.tasks:
                    self._users.extend(task.resources)
            
            self._users = list(set(self._users))
            
            return self._users
        
        doc = """The users assigned to this project.
        
        This is a list of :class:`~stalker.core.models.User` instances. All the
        elements are gathered from all the
        :class:`~stalker.core.models.Task`\ s of the project itself and from
        :class:`~stalker.core.models.Sequence`\ s,
        :class:`~stalker.core.models.Shot`\ s,
        :class:`~stalker.core.models.Asset`\ s.
        """
        
        return locals()
    
    users = property(**users())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Project, self).__eq__(other) and \
               isinstance(other, Project)






########################################################################
class Repository(Entity):
    """Repository is a class to hold repository server data. A repository is a
    network share that all users have access to.
    
    A studio can create several repositories, for example, one for movie
    projects and one for commercial projects.
    
    A repository also defines the default paths for linux, windows and mac
    fileshares.
    
    :param linux_path: shows the linux path of the repository root, should be a
      string
    
    :param osx_path: shows the mac osx path of the repository root, should be a
      string
    
    :param windows_path: shows the windows path of the repository root, should
      be a string
    
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, linux_path="", windows_path="", osx_path="", **kwargs):
        super(Repository, self).__init__(**kwargs)
        
        self._linux_path = self._validate_linux_path(linux_path)
        self._windows_path = self._validate_windows_path(windows_path)
        self._osx_path = self._validate_osx_path(osx_path)
    
    
    
    #----------------------------------------------------------------------
    def _validate_linux_path(self, linux_path_in):
        """validates the given linux path
        """
        
        if not isinstance(linux_path_in, (str, unicode)):
            raise TypeError("linux_path should be an instance of string or "
                             "unicode")
        
        return linux_path_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_osx_path(self, osx_path_in):
        """validates the given osx path
        """
        
        if not isinstance(osx_path_in, (str, unicode)):
            raise TypeError("osx_path should be an instance of string or "
                             "unicode")
        
        return osx_path_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_windows_path(self, windows_path_in):
        """validates the given windows path
        """
        
        if not isinstance(windows_path_in, (str, unicode)):
            raise TypeError("windows_path should be an instance of string or "
                             "unicode")
        
        return windows_path_in
    
    
    
    #----------------------------------------------------------------------
    def linux_path():
        
        def fget(self):
            return self._linux_path
        
        def fset(self, linux_path_in):
            self._linux_path = self._validate_linux_path(linux_path_in)
        
        doc = """property that helps to set and get linux_path values"""
        
        return locals()
    
    linux_path = property(**linux_path())
    
    
    
    #----------------------------------------------------------------------
    def osx_path():
        
        def fget(self):
            return self._osx_path
        
        def fset(self, osx_path_in):
            self._osx_path = self._validate_osx_path(osx_path_in)
        
        doc = """property that helps to set and get osx_path values"""
        
        return locals()
    
    osx_path = property(**osx_path())
    
    
    
    #----------------------------------------------------------------------
    def windows_path():
        
        def fget(self):
            return self._windows_path
        
        def fset(self, windows_path_in):
            self._windows_path = self._validate_windows_path(windows_path_in)
        
        doc = """property that helps to set and get windows_path values"""
        
        return locals()
    
    windows_path = property(**windows_path())
    
    
    
    #----------------------------------------------------------------------
    def path():
        
        def fget(self):
            
            # return the proper value according to the current os
            platform_system = platform.system()
            
            if platform_system == "Linux":
                return self.linux_path
            elif platform_system == "Windows":
                return self.windows_path
            elif platform_system == "Darwin":
                return self.osx_path
        
        doc = """property that helps to get path for the current os"""
        
        return locals()
    
    path = property(**path())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Repository, self).__eq__(other) and \
               isinstance(other, Repository) and \
               self.linux_path == other.linux_path and \
               self.osx_path == other.osx_path and \
               self.windows_path == other.windows_path






########################################################################
class Sequence(Entity,
               ReferenceMixin,
               StatusMixin,
               ScheduleMixin,
               TaskMixin,
               ProjectMixin):
    """Stores data about Sequences.
    
    Sequences are holders of the :class:`~stalker.core.models.Shot` objects.
    They orginize the conceptual data with another level of complexity.
    
    :param lead: The lead of this Seuqence. The default value is None.
    
    :type lead: :class:`~stalker.core.models.User`
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 shots=[],
                 lead=None,
                 **kwargs
                 ):
        
        super(Sequence, self).__init__(**kwargs)
        
        # call the mixin __init__ methods
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)
        TaskMixin.__init__(self, **kwargs)
        ProjectMixin.__init__(self, **kwargs)
        
        self._lead = self._validate_lead(lead)
        self._shots = self._validate_shots(None)
    
    
    
    #----------------------------------------------------------------------
    def _validate_lead(self, lead_in):
        """validates the given lead_in value
        """
        
        if lead_in is not None:
            if not isinstance(lead_in, User):
                raise TypeError("lead should be instance of "
                                "stalker.core.models.User")
        
        return lead_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_shots(self, shots_in):
        """validates the given shots_in value
        """
        
        if shots_in is None:
            shots_in = []
        
        if not isinstance(shots_in, list):
            raise TypeError("shots should be list containing "
                            "stalker.core.models.Shot instances")
        
        for element in shots_in:
            if not isinstance(element, Shot):
                raise TypeError("every item in the shots list should be an "
                                "instance of stalker.core.models.Shot")
        
        return ValidatedList(shots_in, Shot)
        
    
    
    
    #----------------------------------------------------------------------
    def lead():
        def fget(self):
            return self._lead
        def fset(self, lead_in):
            self._lead = self._validate_lead(lead_in)
        
        doc = """The lead of this sequence object."""
        
        return locals()
    
    lead = property(**lead())
    
    
    
    #----------------------------------------------------------------------
    def shots():
        def fget(self):
            return self._shots
        def fset(self, shots_in):
            self._shots = self._validate_shots(shots_in)
        
        doc = """The shots of this sequence object."""
        
        return locals()
    
    shots = property(**shots())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Sequence, self).__eq__(other) and \
               isinstance(other, Sequence)






########################################################################
class Shot(Entity, ReferenceMixin, StatusMixin, TaskMixin):
    """Manages Shot related data.
    
    Because most of the shots in different projects are going to have the same
    name, which is a kind of a code like SH001, SH012A etc., and in Stalker you
    can not have two entities with the same name if their types are also
    matching, to guarantee all the shots are going to have different names the
    :attr:`~stalker.core.models.Shot.name` attribute of the Shot instances are
    automatically set to a randomly generated **uuid4** sequence.
    
    But there is no such rule for the
    :attr:`~stalker.core.models.Shot.code` attribute, which should be used to
    give shot codes to individual shots.
    
    Two shots with the same :attr:`~stalker.core.models.Shot.code` can not be
    assigned to the same :class:`~stalker.core.models.Sequence`.
    
    The :attr:`~stalker.core.models.Shot.cut_out` and
    :attr:`~stalker.core.models.Shot.cut_duration` attributes effects each
    other. Setting the :attr:`~stalker.core.models.Shot.cut_out` will change
    the :attr:`~stalker.core.models.Shot.cut_duration` and setting the
    :attr:`~stalker.core.models.Shot.cut_duration` will change the
    :attr:`~stalker.core.models.Shot.cut_out` value. The default value of the
    :attr:`~stalker.core.models.Shot.cut_out` attribute is calculated from the
    :attr:`~stalker.core.models.Shot.cut_in` and
    :attr:`~stalker.core.models.Shot.cut_duration` attributes. If both
    :attr:`~stalker.core.models.Shot.cut_out` and
    :attr:`~stalker.core.models.Shot.cut_duration` arguments are set to None,
    the :attr:`~stalker.core.models.Shot.cut_duration` defaults to 100 and
    :attr:`~stalker.core.models.Shot.cut_out` will be set to
    :attr:`~stalker.core.models.Shot.cut_in` +
    :attr:`~stalker.core.models.Shot.cut_duration`. So the priority of the
    attributes are as follows:
    
      :attr:`~stalker.core.models.Shot.cut_in` >
      :attr:`~stalker.core.models.Shot.cut_duration` >
      :attr:`~stalker.core.models.Shot.cut_out`
    
    For still images (which can be also managed by shots) the
    :attr:`~stalker.core.models.Shot.cut_in` and
    :attr:`~stalker.core.models.Shot.cut_out` can be set to the same value
    so the :attr:`~stalker.core.models.Shot.cut_duration` can be set to zero.
    
    :param sequence: The :class:`~stalker.core.models.Sequence` that this shot
      blengs to. A shot can only be created with a
      :class:`~stalker.core.models.Sequence` instance, so it can not be None.
      The shot itself will be added to the
      :attr:`~stalker.core.models.Sequence.shots` list of the given sequence.
    
    :type sequence: :class:`~stalker.core.models.Sequence`
    
    :param integer cut_in: The in frame number that this shot starts. The
      default value is 1. When the ``cut_in`` is bigger then
      ``cut_out``, the :attr:`~stalker.core.models.Shot.cut_out` attribute is
      set to :attr:`~stalker.core.models.Shot.cut_in` + 1.
    
    :param integer cut_duration: The duration of this shot in frames. It should
      be zero or a positive integer value (natural number?) or . The default
      value is None.
    
    :param integer cut_out: The out frame number that this shot ends. If it is
      given as a value lower then the ``cut_in`` parameter, then the
      :attr:`~stalker.core.models.Shot.cut_out` will be set to the same value
      with :attr:`~stalker.core.models.Shot.cut_in` and the
      :attr:`~stalker.core.models.Shot.cut_duration` attribute will be set to
      1. Can be skipped. The default value is None.
    """
    
    
    
    # fix creation with __new__
    #_cut_out = None
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 code=None,
                 sequence=None,
                 cut_in=1,
                 cut_out=None,
                 cut_duration=None,
                 **kwargs):
        
        kwargs["name"] = code
        
        super(Shot, self).__init__(**kwargs)
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        TaskMixin.__init__(self, **kwargs)
        
        # set the code
        self._code = self._validate_code(code)
        
        # set the name atribute
        import uuid
        self._name = uuid.uuid4().hex
        
        self._sequence = self._validate_sequence(sequence)
        # add the shot to the sequences shot list
        self._sequence.shots.append(self)
        
        
        self._cut_in = cut_in
        self._cut_duration = cut_duration
        self._cut_out = cut_out
        
        self._update_cut_info(cut_in, cut_duration, cut_out)
    
    
    
    #----------------------------------------------------------------------
    @orm.reconstructor
    def init_on_load(self):
        self._cut_out = None
        self._update_cut_info(cut_in, cut_duration, cut_out)
    
    
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """the representation of the Shot
        """
        
        return "<%s (%s, %s)>" % (self.entity_type, self.code, self.code)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """equality operator
        """
        
        # __eq__ always returns false but to be safe the code will be added
        # here
        
        return self.code == other.code and isinstance(other, Shot) and \
               self.sequence == other.sequence
    
    
    
    #----------------------------------------------------------------------
    def _update_cut_info(self, cut_in, cut_duration, cut_out):
        """updates the cut_in, cut_duration and cut_out attributes
        """
        
        # validate all the values
        self._cut_in = self._validate_cut_in(cut_in)
        self._cut_duration = self._validate_cut_duration(cut_duration)
        self._cut_out = self._validate_cut_out(cut_out)
        
        if self._cut_in is None:
            self._cut_in = 1
        
        if self._cut_out is not None:
            if self._cut_in > self._cut_out:
                # just update cut_duration
                self._cut_duration = 1
        #else:
            #self._cut_o
        
        if self._cut_duration is None or self._cut_duration <= 0:
            self._cut_duration = 1
        
        self._cut_out = self._cut_in + self._cut_duration - 1
    
    
    
    
    ##----------------------------------------------------------------------
    #def _validate_assets(self, assets_in):
        #"""validates the given assets_in value
        #"""
        
        #if assets_in is None:
            #assets_in = []
        
        #if not isinstance(assets_in, list):
            #raise TypeError("assets should be an instance of list")
        
        #for item in assets_in:
            #if not isinstance(item, Asset):
                #raise TypeError("all the items in the assets list should be"
                                 #"an instance of stalker.core.models.Asset")
        
        #return ValidatedList(assets_in, Asset)
    
    
    
    #----------------------------------------------------------------------
    def _validate_code(self, code_in):
        """validates the given code value
        """
        
        # check if the code_in is None or empty string
        if code_in is None:
            raise TypeError("the code can not be None")
        
        if code_in=="":
            raise ValueError("the code can not be empty string")
        
        return self._condition_code(str(code_in))
    
    
    
    #----------------------------------------------------------------------
    def _validate_cut_duration(self, cut_duration_in):
        """validates the given cut_duration value
        """
        
        if cut_duration_in is not None and \
           not isinstance(cut_duration_in, int):
            raise TypeError("cut_duration should be an instance of int")
        
        #if cut_duration_in is None or cut_duration_in <= 0:
                #if self._cut_out is None:
                    #raise ValueError("cut_duration can not be None or negative"
                                     #"when the cut_out is also undefined")
                #else:
                    #cut_duration_in = self._cut_out - self._cut_in + 1
        
        return cut_duration_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_cut_in(self, cut_in_in):
        """validates the given cut_in_in value
        """
        
        if cut_in_in is not None:
            if not isinstance(cut_in_in, int):
                raise TypeError("cut_in should be an instance of int")
        
        return cut_in_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_cut_out(self, cut_out_in):
        """validates the given cut_out_in value
        """
        
        if cut_out_in is not None:
            if not isinstance(cut_out_in, int):
                raise TypeError("cut_out should be an instance of int")
        
        return cut_out_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_sequence(self, sequence_in):
        """validates the given sequence_in value
        """
        
        if not isinstance(sequence_in, Sequence):
            raise TypeError("the sequence should be an instance of"
                             "stalker.core.models.Sequence instance")
        
        for shot in sequence_in.shots:
            #assert(isinstance(shot, Shot))
            
            if self.code ==  shot.code:
                raise ValueError("the given sequence already has a shot with "
                                 "a code %s" % self.code)
        
        return sequence_in
    
    
    
    ##----------------------------------------------------------------------
    #def assets():
        
        #def fget(self):
            #return self._assets
        
        #def fset(self, assets_in):
            #self._assets = self._validate_assets(assets_in)
        
        #doc = """The list of :class:`~stalker.core.models.Asset`\ s used in this shot.
        
        #When it is set to None, it defaults to the default value and the
        #default value is an empty list."""
        
        #return locals()
    
    #assets = property(**assets())
    
    
    
    #----------------------------------------------------------------------
    def code():
        def fget(self):
            return self._code
        
        def fset(self, code_in):
            self._code = self._validate_code(code_in)
        
        doc = """The code of this :class:`~stalker.core.models.Shot`.
        
        Contrary to the original attribute from the inherited parent
        (:attr:`~stalker.core.models.SimpleEntity.code`), the code attribute
        can not be set to None or empty string."""
        
        return locals()
    
    code = property(**code())
        
    
    
    
    #----------------------------------------------------------------------
    def cut_duration():
        
        def fget(self):
            return self._cut_duration
        
        def fset(self, cut_duration_in):
            #self._cut_duration = self._validate_cut_duration(cut_duration_in)
            
            # also set the cut_out
            #self._cut_out = self._cut_in + self._cut_duration - 1
            
            self._update_cut_info(self._cut_in, cut_duration_in, self._cut_out)
        
        doc = """The duration of this shot in frames.
        
        It should be a positive integer value. If updated also updates the
        :attr:`~stalker.core.models.Shot.cut_duration` attribute. The default
        value is 100."""
        
        return locals()
    
    cut_duration = property(**cut_duration())
    
    
    
    #----------------------------------------------------------------------
    def cut_in():
        
        def fget(self):
            return self._cut_in
        
        def fset(self, cut_in_in):
            #self._cut_in = self._validate_cut_in(cut_in_in)
            
            #if self._cut_in > self._cut_out:
                ## udpate the cut_out value
                #self._cut_out = self._cut_in + 1
            
            #self._update_cut_duration()
            
            self._update_cut_info(cut_in_in, self._cut_duration, self._cut_out)
        
        doc = """The in frame number taht this shot starts.
        
        The default value is 1. When the cut_in is bigger then
        :attr:`~stalker.core.models.Shot.cut_out`, the
        :attr:`~stalker.core.models.Shot.cut_out` value is update to
        :attr:`~stalker.core.models.Shot.cut_in` + 1."""
        
        return locals()
    
    cut_in = property(**cut_in())
    
    
    
    #----------------------------------------------------------------------
    def cut_out():
        def fget(self):
            if self._cut_out is None:
                self._update_cut_info(self._cut_in, self._cut_duration, None)
            return self._cut_out
        
        def fset(self, cut_out_in):
            #self._cut_out = self._validate_cut_out(cut_out_in)
            
            #if self._cut_out is None:
                #self._cut_out = self._cut_in + self._cut_duration - 1
            
            #self._update_cut_duration()
            self._update_cut_info(self._cut_in, self._cut_duration, cut_out_in)
        
        doc = """The out frame number that this shot ends.
        
        When the :attr:`~stalker.core.models.Shot.cut_out` is set to a value
        lower than :attr:`~stalker.core.models.Shot.cut_in`,
        :attr:`~stalker.core.models.Shot.cut_out` will be updated to
        :attr:`~stalker.core.models.Shot.cut_in` + 1. The default value is
        :attr:`~stalker.core.models.Shot.cut_in` +
        :attr:`~stalker.core.models.Shot.cut_duration`."""
        
        return locals()
    
    cut_out = property(**cut_out())
    
    
    
    #----------------------------------------------------------------------
    def name():
        def fget(self):
            return self._name
        
        def fset(self, name_in):
            pass
        
        doc = """Name of this Shot.
        
        Different than other :class:`~stalker.core.models.SimpleEntity`
        derivatives, the :class:`~stalker.core.models.Shot` classes
        :attr:`~stalker.core.models.Shot.name` attribute is read-only. And the
        stored value is a uuid4 sequence.
        """
        
        return locals()
    
    name = property(**name())
    
    
    
    #----------------------------------------------------------------------
    def sequence():
        def fget(self):
            return self._sequence
        
        doc = """The :class:`~stalker.core.models.Sequence` instance that this :class:`~stalker.core.models.Shot` instance belongs to.
        
        It is a read-only attribute."""
        
        return locals()
    
    sequence = property(**sequence())
        






########################################################################
class Structure(Entity):
    """A structure object is the place to hold data about how the physical files are arranged in the :class:`~stalker.core.models.Repository`.
    
    Structures are generally owned by :class:`~stalker.core.models.Project`
    objects. Whenever a :class:`~stalker.core.models.Project` is physicaly
    created, project folders are created by looking at
    :attr:`~stalker.core.models.Structure.custom_template` of the
    :class:`~stalker.core.models.Structure`, the
    :class:`~stalker.core.models.Project` object is generally given to the
    :class:`~stalker.core.models.Structure`. So it is possible to use a
    variable like "{{project}}" or derived variables like::
      
      {% for seq in project.sequences %}
          {{do something here}}
    
    :param templates: A list of
      :class:`~stalker.core.models.FilenameTemplate`\ s which
      defines a specific template for the given
      :attr:`~stalker.core.models.FilenameTemplate.target_entity_type`\ s.
    
    :type templates: list of :class:`~stalker.core.models.FilenameTemplate`\ s
    
    :param str custom_template: A string containing several lines of folder
      names. The folders are relative to the
      :class:`~stalker.core.models.Project` root. It can also contain a Jinja2
      Template code. Which will be rendered to show the list of folders to be
      created with the project. The Jinja2 Template is going to have the
      {{project}} variable. The important point to be careful about is to list
      all the custom folders of the project in a new line in this string. For
      example a :class:`~stalker.core.models.Structure` for a
      :class:`~stalker.core.models.Project` can have the following
      :attr:`~stalker.core.models.Structure.custom_template`::
        
        ASSETS
        {% for asset in project.assets %}
            {% set asset_root = 'ASSETS/' + asset.code %}
            {{asset_root}}
            
            {% for task in asset.tasks %}
                {% set task_root = asset_root + '/' + task.code %}
                {{task_root}}
        
        SEQUENCES
        {% for seq in project.sequences %}}
            {% set seq_root = 'SEQUENCES/' + {{seq.code}} %}
            {{seq_root}}/Edit
            {{seq_root}}/Edit/AnimaticStoryboard
            {{seq_root}}/Edit/Export
            {{seq_root}}/Storyboard
            
            {% for shot in seq.shots %}
                {% set shot_root = seq_root + '/SHOTS/' + shot.code %}
                {{shot_root}}
                
                {% for task in shot.tasks %}
                    {% set task_root = shot_root + '/' + task.code %}
                    {{task_root}}
      
      The above example has gone far beyond deep than it is needed, where it
      started to define paths for :class:`~stalker.core.models.Asset`\ s. Even
      it is possible to create a :class:`~stalker.core.models.Project`
      structure like that, in general it is unnecessary. Because the above
      folders are going to be created but they are probably going to be empty
      for a while, because the :class:`~stalker.core.models.Asset`\ s are not
      created yet (or in fact no :class:`~stalker.core.models.Version`\ s are
      created for the :class:`~stalker.core.models.Task`\ s). Anyway, it is
      much suitable and desired to create this details by using
      :class:`~stalker.core.models.FilenameTemplate` objects. Which are
      spesific to certain
      :attr:`~stalker.core.FilenameTemplate.target_entity_type`\ s. And by
      using the :attr:`~stalker.core.models.Structure.custom_template`
      attribute, Stalker can not place any source or output file of a
      :class:`~stalker.core.models.Version` in the
      :class:`~stalker.core.models.Repository` where as it can by using
      :class:`~stalker.core.models.FilenameTemplate`\ s.
      
      But for certain types of :class:`~stalker.core.models.Task`\ s it is may
      be good to previously create the folder structure just because in certain
      environments (programs) it is not possible to run a Python code that will
      place the file in to the Repository like in Photoshop.
      
      The ``custom_template`` parameter can be None or an empty string if it is
      not needed. Be carefull not to pass a variable other than a string or
      unicode because it will use the string representation of the given
      variable.
    
    A :class:`~stalker.core.models.Structure` can not be created without a
    ``type`` (__strictly_typed__ = True). By giving a ``type`` to the
    :class:`~stalker.core.models.Strucutre`, you can create one structure for
    **Commmercials** and another project structure for **Movies** and another
    one for **Print** projects etc. and can reuse them with new
    :class:`~stalker.core.models.Project`\ s.
    """
    
    
    
    __strictly_typed__ = True
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, templates=None, custom_template=None, **kwargs):
        super(Structure, self).__init__(**kwargs)
        
        self._templates = self._validate_templates(templates)
        self._custom_template= self._validate_custom_template(custom_template)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Structure, self).__eq__(other) and \
               isinstance(other, Structure) and \
               self.templates == other.templates and \
               self.custom_template == other.custom_template
    
    
    
    #----------------------------------------------------------------------
    def _validate_custom_template(self, custom_template_in):
        """validates the given custom_template value
        """
        
        return custom_template_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_templates(self, templates_in):
        """validates the given templates value
        """
        
        if templates_in is None:
            templates_in = []
        
        if not isinstance(templates_in, list):
            raise TypeError("templates should be a list of "
                            "stalker.core.models.FilenameTemplate instances")
        
        if not all(isinstance(element, FilenameTemplate)
                   for element in templates_in):
            raise TypeError("all the elements in the templates should be a "
                            "list of stalker.core.models.FilenameTemplate "
                            "instances")
        
        return ValidatedList(templates_in)
    
    
    
    #----------------------------------------------------------------------
    def custom_template():
        def fget(self):
            return self._custom_template
        
        def fset(self, custom_template_in):
            self._custom_template =\
                self._validate_custom_template(custom_template_in)
        
        doc = """A string value, which is a list of folder names.
        
        It can also contain Jinja2 direction. See the\
        :class:`~stalker.core.models.Structure` documentaion for more details.
        """
        
        return locals()
    
    custom_template = property(**custom_template())
    
    
    
    #----------------------------------------------------------------------
    def templates():
        def fget(self):
            return self._templates
        
        def fset(self, templates_in):
            self._templates = self._validate_templates(templates_in)
        
        doc = """A list of :class:`~stalker.core.models.FilenameTemplate` instances.
        
        This list shows possible filenaming conventions created along with this
        :class:`~stalker.core.models.Structure` instance. It should be a list
        of :class:`~stalker.core.models.FilenameTemplate` instances.
        """
        
        return locals()
    
    templates = property(**templates())
    






########################################################################
class Tag(SimpleEntity):
    """the tag class
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Tag, self).__eq__(other) and isinstance(other, Tag)
    
    
    
    #----------------------------------------------------------------------
    def __ne__(self, other):
        """the inequality operator
        """
        
        return not self.__eq__(other)






########################################################################
class Asset(Entity, ReferenceMixin, StatusMixin, TaskMixin, ProjectMixin):
    """The Asset class is the whole idea behind Stalker.
    
    *Assets* are containers of :class:`~stalker.core.models.Task`\ s. And
    :class:`~stalker.core.models.Task`\ s are the smallest meaningful part that
    should be accomplished to complete the
    :class:`~stalker.core.models.Project`.
    
    An example could be given as follows; you can create an asset for one of
    the characters in your project. Than you can divide this character asset in
    to :class:`~stalker.core.models.Task`\ s. These
    :class:`~stalker.core.models.Task`\ s can be defined by the type of the
    :class:`~stalker.core.models.Asset`, which is a
    :class:`~stalker.core.models.Type` object created specifically for
    :class:`~stalker.core.models.Asset` (ie. has its
    :attr:`~stalker.core.models.Type.target_entity_type` set to "Asset"),
    """
    
    
    
    __strictly_typed__ = True
    _shots = None
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        
        super(Asset, self).__init__(**kwargs)
        
        # call the mixin init methods
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        TaskMixin.__init__(self, **kwargs)
        ProjectMixin.__init__(self, **kwargs)
        
        self._shots = self._validate_shots(None)
    
    
    
    #----------------------------------------------------------------------
    def _validate_shots(self, shots_in):
        """validates the given shots_in value
        """
        
        if shots_in is None:
            shots_in = []
        
        if not isinstance(shots_in, list):
            raise TypeError("shots should be set to a list of "
                            "stalker.core.models.Shot instances")
        
        if not all([isinstance(shot, Shot)
                    for shot in shots_in]):
            raise TypeError("shots should be set to a list of "
                            "stalker.core.models.Shot objects")
        
        return ValidatedList(shots_in, Shot)
        
    
    
    
    #----------------------------------------------------------------------
    def shots():
        def fget(self):
            return self._shots
        
        def fset(self, shots_in):
            self._shots = self._validate_shots(shots_in)
        
        doc = """The :class:`~stalker.core.models.Shot`\ s that this :class:`~stalker.core.models.Asset` has been used in.
        """
        
        return locals()
    
    shots = property(**shots())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Asset, self).__eq__(other) and \
               isinstance(other, Asset) and self.type == other.type






########################################################################
class Version(Entity, StatusMixin):
    """The connection to the filesystem.
    
    A :class:`~stalker.core.models.Version` holds information about the
    incarnations of the files in the :class:`~stalker.core.models.Repository`.
    So if one creates a new version for a file or a sequences of file for a
    :class:`~stalker.core.models.Task` then the information is hold in the
    :class:`~stalker.core.models.Version` instance.
    
    :param str take: A short string holding the current take name. Can be
      any alphanumeric value (a-zA-Z0-0_)
    
    :param int version: An integer value showing the current version number.
    
    :param source_file: A :class:`~stalker.core.models.Link` instance, showing
      the source file of this version.
    
    :type source_file: :class:`~stalker.core.models.Link`
    
    :param outputs: A list of :class:`~stalker.core.models.Link` instances,
      holding the outputs of the current version.
    
    :type outputs: list of :class:`~stalker.core.models.Link` instances
    
    :param task: A :class:`~stalker.core.models.Task` instance showing the
      owner of this Version.
    
    :type task: :class:`~stalker.core.models.Task`
    """
    #:param review: A list of :class:`~stalker.core.models.Comment` instances,
      #holding all the comments made for this Version.
    
    #:type review: :class:`~stalker.core.models.Stalker`
    #:param bool published: A bool value shows if this version is published or
      #not.
    
    
    
    
    
    pass






########################################################################
class Task(Entity, StatusMixin, ScheduleMixin, ProjectMixin):
    """Manages Task related data.
    
    Tasks are the smallest meaningful part that should be accomplished to
    complete the a :class:`~stalker.core.models.Project`.
    
    In Stalker, currently these items supports Tasks:
    
       * :class:`~stalker.core.models.Project`
    
       * :class:`~stalker.core.models.Sequence`
    
       * :class:`~stalker.core.models.Asset`
    
       * :class:`~stalker.core.models.Shot`
    
    If you want to have your own class to be *taskable* user the
    :class:`~stalker.core.mixins.TaskMixin` to add the ability to connect a
    :class:`~stalker.core.models.Task` to it.
    
    The Task class itself is mixed with
    :class:`~stalker.core.mixins.StatusMixin` and
    :class:`~stalker.core.mixins.ScheduleMixin`. To be able to give the
    :class:`~stalker.core.models.Task` a *Status* and a *start* and *end* time.
    
    :param int priority: It is a number between 0 to 1000 which defines the
      priority of the :class:`~stalker.core.models.Task`. The higher the value
      the higher its priority. The default value is 500.
    
    :param resources: The :class:`~stalker.core.models.User`\ s assigned to
      this :class:`~stalker.core.models.Task`. A
      :class:`~stalker.core.models.Task` without any resource can not be
      scheduled.
    
    :type resources: list of :class:`~stalker.core.models.User`
    
    :param effort: The total effort that needs to be spend to complete this
      Task. Can be used to create an initial bid of how long this task going to
      take. The effort is equaly divided to the assigned resources. So if the
      effort is 10 days and 2 :attr:`~stalker.core.models.Task.resources` is
      assigned then the :attr:`~stalker.core.models.Task.duration` of the task
      is going to be 5 days (if both of the resources are free to work). The
      default value is stalker.conf.defaults.DEFAULT_TASK_DURATION.
      
      The effort argument defines the
      :attr:`~stalker.core.models.Task.duration` of the task. Every resource is
      counted equally effective and the
      :attr:`~stalker.core.models.Task.duration` will be calculated by the
      simple formula:
      
      .. math::
         
         {duration} = \\frac{{effort}}{n_{resources}}
      
      And changing the :attr:`~stalker.core.models.Task.duration` will also
      effect the :attr:`~stalker.core.models.Task.effort` spend. The
      :attr:`~stalker.core.models.Task.effort` will be calculated with the
      formula:
      
      .. math::
         
         {effort} = {duration} \\times {n_{resources}}
    
    :type effort: datetime.timedelta
    
    :param depends: A list of :class:`~stalker.core.models.Task`\ s those this
      :class:`~stalker.core.models.Task` is dependening on.
    
    :type depends: list of :class:`~stalker.core.models.Task`
    
    :param bool milestone: A bool (True or False) value showing if this task is
      a milestone which doesn't need any resource and effort.
    
    :param task_of: A class instance which has an attribute called ``tasks``.
      There is no limit in the type of the class. But it would be correct to
      use something derived from the
      :class:`~stalker.core.models.SimpleEntity` and mixed with
      :class:`~stalker.core.mixins.TaskMixin`. If you are going to use the
      :mod:`stalker.db` module than it have to be something derived from
      the :class:`~stalker.core.models.SimpleEntity`.
      
      Again, only classes that has been mixed with
      :class:`~stalker.core.mixins.TasksMixin` has the attribute called
      ``tasks``. And the instance given, have to be something that is mapped to
      the database if you are going to use the database part of the system.
    
    :type task_of: :class:`~stalker.core.models.SimpleEntity`.
    """
    #.. :param depends: A list of
         #:class:`~stalker.core.models.TaskDependencyRelation` objects. Holds
         #information about the list of other :class:`~stalker.core.models.Task`\ s
         #which the current one is dependent on.
         
      #.. giving information about the dependent tasks. The given list is iterated
         #and the :attr:`~stalker.core.models.Task.start_date` attribute is set to
         #the latest found :attr:`~stalker.core.models.Task.due_date` attribute of
         #the dependent :class:`~stalker.core.models.Task`\ s.
    
    #.. :type depends: list of :class:`~stalker.core.models.TaskDependencyRelation`
    
       
       #:param parent_task: Another :class:`~stalker.core.models.Task` which is the
         #parent of the current :class:`~stalker.core.models.Task`.
         
         #:class:`~stalker.core.models.Task`\ s can be grouped by using parent and
         #child relation.
       
       #:type parent_task: :class:`~stalker.core.models.Task`
       
       #:param sub_tasks: A list of other :class:`~stalker.core.models.Task`\ s
         #which are the child of the current one. A
         #:class:`~stalker.core.models.Task` with other child
         #:class:`~stalker.core.models.Task`\ s:
         
           #* can not have any resources
           #* can not have any effort set
           #* can not have any versions
         
         #The only reason of a :class:`~stalker.core.models.Task` to have other
         #:class:`~stalker.core.models.Task`\ s as child is to group them. So it
         #is meaningles to let a parent :class:`~stalker.core.models.Task` to have
         #any resource or any effort or any verions. The
         #:attr:`~stalker.core.models.Task.start_date`,
         #:attr:`~stalker.core.models.Task.due_date` and
         #:attr:`~stalker.core.models.Task.duration` attributes of a
         #:class:`~stalker.core.models.Task` with child classes will be based on
         #it childrens date attributes.
       
       #:type child_tasks: :class:`~stalker.core.models.Task`.
       
    #:param versions: A list of :class:`~stalker.core.models.Version` objects
      #showing the produced work on the repository. This is the relation between
      #database and the repository.
    
    #:type versions: list of :class:`~stalker.core.models.Version`
    #"""
    
    
    
    _bookings = ValidatedList([], Booking)
    _versions = ValidatedList([], Version)
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 depends=None,
                 effort=None,
                 resources=None,
                 milestone=False,
                 priority=defaults.DEFAULT_TASK_PRIORITY,
                 task_of=None,
                 **kwargs):
        super(Task, self).__init__(**kwargs)
        
        # call the mixin __init__ methods
        StatusMixin.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)
        ProjectMixin.__init__(self, **kwargs)
        
        self._milestone = self._validate_milestone(milestone)
        
        self._depends = self._validate_depends(depends)
        self._resources = []
        self.resources = resources
        
        self._effort = None
        self.effort = effort
        
        self._priority = self._validate_priority(priority)
        
        self._task_of = None
        self.task_of = self._validate_task_of(task_of)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Task, self).__eq__(other) and isinstance(other, Task)
    
    
    
    
    #----------------------------------------------------------------------
    def _validate_bookings(self, bookings_in):
        """validates the given bookings value
        """
        
        if bookings_in is None:
            bookings_in = []
        
        if not all([isinstance(element, Booking) for element in bookings_in]):
            raise TypeError("all the elements in the bookings should be "
                            "an instances of stalker.core.models.Booking")
        
        
        return ValidatedList(bookings_in, Booking)
    
    
    #----------------------------------------------------------------------
    def _validate_complete(self, complete_in):
        """validates the given complete value
        """
        
        return bool(complete_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_depends(self, depends_in):
        """validates the given depends value
        """
        
        if depends_in is None:
            depends_in = []
        
        if not isinstance(depends_in, list):
            raise TypeError("the depends attribute should be an list of"
                            "stalker.core.models.Task instances")
            
        
        if not all([isinstance(element, Task) for element in depends_in]):
            raise TypeError("all the elements in the depends should be an "
                            "instance of stalker.core.models.Task")
        
        # check for the circular dependency
        for task in depends_in:
            _check_circular_dependency(task, self)
        
        return ValidatedList(depends_in, Task)
    
    
    
    #----------------------------------------------------------------------
    def _validate_effort(self, effort_in):
        """validates the given effort
        """
        
        if not isinstance(effort_in, datetime.timedelta):
            effort_in = None
        
        if effort_in is None:
            # take it from the duration and resources
            
            num_of_resources = len(self.resources)
            if num_of_resources == 0:
                num_of_resources = 1
            
            effort_in = self.duration * num_of_resources
        
        return effort_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_milestone(self, milestone_in):
        """validates the given milestone value
        """
        
        return bool(milestone_in)
    
    
    #----------------------------------------------------------------------
    def _validate_task_of(self, task_of_in):
        """validates the given task_of value
        """
        
        # the object given withe the task_of argument should have an attribute
        # called "tasks"
        if task_of_in is None:
            raise TypeError("'task_of' can not be None")
        
        if not hasattr(task_of_in, "tasks"):
            raise AttributeError("the object given with 'task_of' should have "
                                 "an attribute called 'tasks'")
        
        return task_of_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_priority(self, priority_in):
        """validates the given priority value
        """
        
        try:
            priority_in = int(priority_in)
        except (ValueError, TypeError):
            pass
        
        if not isinstance(priority_in, int):
            priority_in = defaults.DEFAULT_TASK_PRIORITY
        
        if priority_in < 0:
            priority_in = 0
        elif priority_in > 1000:
            priority_in = 1000
        
        return priority_in
    
    
    
    
    #----------------------------------------------------------------------
    def _validate_resources(self, resources_in):
        """validates the given resources value
        """
        
        if resources_in is None:
            resources_in = []
        
        if not isinstance(resources_in, list):
            raise TypeError("resources should be a list of "
                            "stalker.core.models.User instances")
        
        if not all([isinstance(element, User) for element in resources_in]):
            raise TypeError("resources should be a list of "
                            "stalker.core.models.User instances")
        
        if self.milestone:
            resources_in = []
        
        return ValidatedList(resources_in, User,
                             self.__resource_item_validator__)
    
    
    
    #----------------------------------------------------------------------
    def _validate_versions(self, versions_in):
        """validates the given version value
        """
        
        if versions_in is None:
            versions_in = []
        
        if not all([isinstance(element, Version) for element in versions_in]):
            raise TypeError("all the elements in the versions list should be "
                            "stalker.core.models.Version instances")
        
        return ValidatedList(versions_in, Version)
    
    
    
    #----------------------------------------------------------------------
    def bookings():
        def fget(self):
            return self._bookings
        
        def fset(self, bookings_in):
            self._bookings = self._validate_bookings(bookings_in)
        
        doc = """A list of :class:`~stalker.core.models.Booking` objects
        showing who and when spent how much effort on this task.
        """
        
        return locals()
    
    bookings = property(**bookings())
    
    
    
    #----------------------------------------------------------------------
    def complete():
        def fget(self):
            return self._complete
        
        def fset(self, complete_in):
            self._complete = self._validate_complete(complete_in)
        
        doc = """A bool value showing if this task is completed or not.
        
        There is a good article_ about why not to use an attribute called
        ``percent_complete`` to measure how much the task is completed.
        
        .. _article: http://www.pmhut.com/how-percent-complete-is-that-task-again
        """
        
        return locals()
    
    complete = property(**complete())
    
    
    
    #----------------------------------------------------------------------
    def depends():
        def fget(self):
            return self._depends
        
        def fset(self, depends_in):
            self._depends = self._validate_depends(depends_in)
        
        doc = """A list of :class:`~stalker.core.models.Task`\ s that this one is depending on.
        
        A CircularDependencyError will be raised when the task dependency
        creates a circlar dependency which means it is not allowed to create
        a dependency for this Task which is depending on another one which in
        some way depends to this one again.
        """
        
        return locals()
    
    depends = property(**depends())
    
    
    
    #----------------------------------------------------------------------
    def duration():
        def fget(self):
            return self._duration
        
        def fset(self, duration_in):
            
            # just call the fset method of the duration property in the super
            ScheduleMixin.duration.fset(self, duration_in)
            
            # then update the effort
            num_of_resources = len(self.resources)
            if num_of_resources == 0:
                num_of_resources = 1
            
            self._effort = self.duration * num_of_resources
        
        doc = """The overriden duration attribute.
        
        It is a datetime.timedelta instance. Showing the difference of the
        :attr:`~stalker.core.mixins.ScheduleMixin.start_date` and the
        :attr:`~stalker.core.mixins.ScheduleMixin.due_date`. If edited it
        changes the :attr:`~stalker.core.mixins.ScheduleMixin.due_date`
        attribute value.
        """
        
        return locals()
    
    duration = property(**duration())
    
    
    
    #----------------------------------------------------------------------
    def effort():
        def fget(self):
            return self._effort
        
        def fset(self, effort_in):
            self._effort = self._validate_effort(effort_in)
            
            # update the duration
            num_of_resources = len(self.resources)
            if num_of_resources == 0:
                num_of_resources = 1
            
            self.duration = self._effort / num_of_resources
        
        doc = """The total effort that needs to be spend to complete this Task.
        
        Can be used to create an initial bid of how long this task going to
        take. The effort is equaly divided to the assigned resources. So if the
        effort is 10 days and 2 resources is assigned then the
        :attr:`~stalker.core.models.Task.duration` of the task is going to be 5
        days (if both of the resources are free to work). The default value is
        stalker.conf.defaults.DEFAULT_TASK_DURATION.
      
        The effort defines the :attr:`~stalker.core.models.Task.duration` of
        the task. Every resource is counted equally effective and the
        :attr:`~stalker.core.models.Task.duration` will be calculated by the
        simple formula:
        
        .. math::
           
           {duration} = \\frac{{effort}}{n_{resources}}
        
        And changing the :attr:`~stalker.core.models.Task.duration` will also
        effect the :attr:`~stalker.core.models.Task.effort` spend. The
        :attr:`~stalker.core.models.Task.effort` will be calculated with the
        formula:
           
        .. math::
           
           {effort} = {duration} \\times {n_{resources}}
        """
        
        return locals()
    
    effort = property(**effort())
    
    
    
    #----------------------------------------------------------------------
    def milestone():
        def fget(self):
            return self._milestone
        
        def fset(self, milestone_in):
            self._milestone = self._validate_milestone(milestone_in)
            
            if self._milestone:
                self._resources = []
        
        doc = """Specifies if this Task is a milestone.
        
        Milestones doesn't need any duration, any effort and any resources. It
        is used to create meaningfull dependencies between the critical stages
        of the project.
        """
        
        return locals()
    
    milestone = property(**milestone())
    
    
    
    #----------------------------------------------------------------------
    def __resource_item_validator__(self, resources_added, resources_removed):
        """a callable for more granular control over resources list
        """
        
        # add the task to the resources
        for resource in resources_added:
            resource._tasks.append(self)
        
        for resource in resources_removed:
            resource._tasks.remove(self)
    
    
    
    #----------------------------------------------------------------------
    def resources():
        def fget(self):
            return self._resources
        
        def fset(self, resources_in):
            
            # validate the incoming resources
            resources_in = self._validate_resources(resources_in)
            
            # remove the current task from the previous resources tasks list
            for resource in self._resources:
                try:
                    resource.tasks.remove(self)
                except ValueError:
                    pass
            
            self._resources = resources_in
            
            # now append the task to every one of the users in the resources_in
            for resource in self._resources:
                if self not in resource.tasks:
                    resource._tasks.append(self)
        
        doc = """The list of :class:`stalker.core.models.User`\ s instances
        assigned to this Task.
        """
        
        return locals()
    
    resources = property(**resources())
    
    
    
    #----------------------------------------------------------------------
    def task_of():
        def fget(self):
            return self._task_of
        
        def fset(self, task_of_in):
            task_of_in = self._validate_task_of(task_of_in)
            
            # remove it from the current task_of attribute
            if not self._task_of is None:
                self._task_of.tasks.remove(self)
            
            # update the back reference attribute tasks
            self._task_of = task_of_in
            self._task_of.tasks.append(self)
        
        doc = """An object that this Task is a part of.
        
        The assigned object should have an attribute called ``tasks``. Any
        object which doesn't have a ``tasks`` attribute will raise an
        AttributeError.
        """
        
        return locals()
    
    task_of = property(**task_of())
    
    
    
    #----------------------------------------------------------------------
    def priority():
        def fget(self):
            return self._priority
        
        def fset(self, priority_in):
            self._priority = self._validate_priority(priority_in)
        
        doc = """The priority of the current Task.
        
        It is a number between 0 and 1000 shows how important this task is
        among the others.
        """
        
        return locals()
    
    priority = property(**priority())
    
    
    
    #----------------------------------------------------------------------
    def versions():
        def fget(self):
            return self._versions
        
        def fset(self, versions_in):
            self._versions = self._validate_versions(versions_in)
        
        doc = """A list of :class:`~stalker.core.models.Version` instances
        showing the files created for this task.
        """
        
        return locals()
    
    versions = property(**versions())
    






#----------------------------------------------------------------------
def _check_circular_dependency(task, check_for_task):
    """checks the circular dependency in task if it has check_for_task in its
    depends list
    
    !!!!WARNING NO TEST FOR THIS FUNCTION!!!!
    """
    
    for dependent_task in task.depends:
        if dependent_task is check_for_task:
            raise CircularDependencyError(
                "task %s and %s creates a circular dependency" % \
                (task, check_for_task)
            )
        else:
            _check_circular_dependency(dependent_task, check_for_task)






#########################################################################
#class TaskDependencyRelation(object):
    #"""Holds information about :class:`~stalker.core.models.Task` dependencies.
    
    #(DEVELOPERS: It could be an association proxy for the Task class)
    
    #A TaskDependencyRelation object basically defines which
    #:class:`~stalker.core.models.Task` is dependedt
    #to which other :class:`~stalker.core.models.Task` and what is the lag
    #between the end of the dependent to the start of the dependee.
    
    #A :class:`~stalker.core.models.Task` can not be set dependent to it self.
    #So the the :attr:`~stalker.core.models.TaskDependencyRelation.depends` list
    #can not contain the same value with
    #:attr:`~stalker.core.models.TaskDependencyRelation.task`.
    
    #:param task: The :class:`~stalker.core.models.Task` that is dependent to
      #others.
    
    #:type task: :class:`~stalker.core.models.Task`
    
    #:param depends: A :class:`~stalker.core.models.Task`\ s that the
      #:class:`~stalker.core.models.Task` which is held by the
      #:attr:`~stakler.core.models.TaskDependencyRelation.task` attribute is
      #dependening on. The :attr:`~stalker.core.models.Task.start_date` and the
      #:attr:`~stalker.core.models.Task.due_date` attributes of the
      #:class:`~stalker.core.models.Task` is updated if it is before the
      #``due_date`` of the dependent :class:`~stalker.core.models.Task`.
    
    #:type depends: :class:`~stalker.core.models.Task`
    
    #:param lag: The lag between the end of the dependent task to the start of
      #the dependee. It is an instance of timedelta and could be a negative
      #value. The default is 0. So the end of the task is start of the other.
    #"""
    
    ##----------------------------------------------------------------------
    #def __init__(self):
        #pass






########################################################################
class FilenameTemplate(Entity):
    """Holds templates for filename conventions.
    
    FilenameTemplate objects help to specify where to place a file related to
    its :attr:`~stalker.core.models.FilenameTemplate.target_entity_type`.
    
    The first very important usage of FilenameTemplates is to place asset file
    :class:`~stalker.core.models.Version`'s to proper places inside a
    :class:`~stalker.core.models.Project`'s
    :class:`~stalker.core.models.Structure`.
    
    Secondly, it can be used in the process of injecting files in to the
    repository. By creating templates for :class:`~stalker.core.models.Links`.
    
    :param str target_entity_type: The class name that this FilenameTemplate
      is designed for. You can also pass the class itself. So both of the
      examples below can work::
        
        new_filename_template1 = FilenameTemplate(target_entity_type="Asset")
        new_filename_template2 = FilenameTemplate(target_entity_type=Asset)
    
      A TypeError will be raised when it is skipped or it is None and a
      ValueErorr will be raised when it is given as and empty string.
    
    :param str path_code: A Jinja2 template code which specifies the path of
      the given item. It is relative to the project root. A typical example
      could be::
        
        asset_path_code = "ASSETS/{{asset.code}}/{{task.code}}/"
    
    :param str file_code: A Jinja2 template code which specifies the file name
      of the given item. It is relative to the
      :attr:`~stalker.core.models.FilenameTemplate.path_code`. A typical
      example could be::
        
        asset_file_code = "{{asset.code}}_{{version.take}}_{{task.code}}_"\\
                          "{{version.version}}_{{user.initials}}"
      
      Could be set to an empty string or None, the default value is None.
    
    :param str output_path_code: A Jinja2 template code specifying where to
      place the outputs of the applied
      :attr:`~stalker.core.models.FilenameTemplate.target_entity_type`. If it
      is empty and the
      :attr:`~stalker.core.models.FilenameTemplate.output_is_relative` is True,
      then the outputs will naturally be in the same place with the
      :attr:`~stalker.core.models.FilenameTemplate.path_code`. If the
      :attr:`~stalker.core.models.FilenameTemplate.output_is_relative` is False
      then :attr:`~stalker.core.models.FilenameTemplate.output_path_code` will
      be the same code with
      :attr:`~stalker.core.models.FilenameTemplate.path_code`.
      
      It can be None, or an empty string, or it can be skipped.
    
    :param str output_file_code: A Jinja2 template code specifying what will be
      the file name of the output. If it is skipped or given as None or as an
      empty string, it will be the same with the
      :attr:`~stalker.core.models.FilenameTemplate.file_code`.
      
      It can be skipped, or can be set to None or an empty string. The default
      value is None, and this will set the
      :attr:`~stalker.core.models.FilenameTemplate.output_file_code` to the
      same value with :attr:`~stalker.core.models.FilenameTemplate.file_code`.
    
    :param bool output_is_relative: A bool value specifying if the
      :attr:`~stalker.core.models.FilenameTemplate.output_path_code` is
      relative to the :attr:`~stalker.core.models.FilenameTemplate.path_code`.
      The default value is True. Can be skipped, any other than a bool value
      will be evaluated to a bool value.
    
    Examples:
    
    A template for asset versions can be used like this::
      
      from stalker.core.models import Type, FilenameTemplate, TaskTemplate
      
      # create a couple of variables
      path_code = "ASSETS/{{asset_type.name}}/{{task_type.code}}"
      
      file_code =
      "{{asset.name}}_{{take.name}}_{{asset_type.name}}_v{{version.version_number}}"
      
      output_path_code = "OUTPUT"
      output_file_code = file_code
      
      # create a type for modeling task
      modeling = Type(
          name="Modeling",
          code="MODEL",
          description="The modeling step of the asset",
          target_entity_type=Task
      )
      
      # create a "Character" Type for Asset classes
      character = Type(
          name="Character",
          description="this is the character asset type",
          target_entity_type=Asset
      )
      
      # now create our FilenameTemplate
      char_template = FilenameTemplate(
          name="Character",
          description="this is the template which explains how to place \
Character assets",
          target_entity_type="Asset",
          path_code=path_code,
          file_code=file_code,
          output_path_code=output_path_code,
          output_file_code=output_file_code,
          output_is_relative=True,
      )
      
      # assign this type template to the structure of the project with id=101
      myProject = query(Project).filter_by(id=101).first()
      
      # append the type template to the structures' templates
      myProject.structure.templates.append(char_template)
      
      # commit everything to the database
      session.commit()
    
    Now with the code above, whenever a new
    :class:`~stalker.core.models.Version` created for a **Character**
    asset, Stalker will automatically place the related file to a certain
    folder and with a certain file name defined by the template. For example
    the above template should render something like below for Windows::
    
      |- M:\\\PROJECTS  --> {{repository.path}}
       |- PRENSESIN_UYKUSU  --> {{project.code}}
        |- ASSETS  --> "ASSETS"
         |- Character  --> {{asset_type.name}}
          |- Olum  --> {{asset.name}}
           |- MODEL  --> {{task_type.code}}
            |- Olum_MAIN_MODEL_v001.ma --> {{asset.name}}_\
{{take.name}}_{{asset_type.name}}_v{{version.version_number}}
    
    And one of the best side is you can create a version from Linux, Windows or
    OSX all the paths will be correctly handled by Stalker.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 target_entity_type=None,
                 path_code=None,
                 file_code=None,
                 output_path_code=None,
                 output_file_code=None,
                 output_is_relative=True,
                 **kwargs):
        super(FilenameTemplate, self).__init__(**kwargs)
        
        self._target_entity_type =\
            self._validate_target_entity_type(target_entity_type)
        self._path_code = self._validate_path_code(path_code)
        self._file_code = self._validate_file_code(file_code)
        self._output_is_relative =\
            self._validate_output_is_relative(output_is_relative)
        self._output_path_code =\
            self._validate_output_path_code(output_path_code)
        self._output_file_code =\
            self._validate_output_file_code(output_file_code)
    
    
    
    #----------------------------------------------------------------------
    def _validate_path_code(self, path_code_in):
        """validates the given path_code attribute for several conditions
        """
        
        # check if it is None
        if path_code_in is None:
            path_code_in = u""
        
        path_code_in = unicode(path_code_in)
        
        return path_code_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_file_code(self, file_code_in):
        """validates the given file_code attribute for several conditions
        """
        
        # check if it is None
        if file_code_in is None:
            file_code_in = u""
        
        # convert it to unicode
        file_code_in = unicode(file_code_in)
        
        return file_code_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_target_entity_type(self, target_entity_type_in):
        """validates the given target_entity_type attribute for several
        conditions
        """
        
        # check if it is None
        if target_entity_type_in is None:
            raise TypeError("target_entity_type can not be None")
        
        if isinstance(target_entity_type_in, type):
            target_entity_type_in = target_entity_type_in.__name__
        
        return target_entity_type_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_output_path_code(self, output_path_code_in):
        """validates the given output_path_code value
        """
        
        if output_path_code_in == None or output_path_code_in == "":
            if self.output_is_relative:
                output_path_code_in = ""
            else:
                output_path_code_in = self.path_code
        
        return output_path_code_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_output_file_code(self, output_file_code_in):
        """validates the given output_file_code value
        """
        
        if output_file_code_in == None or output_file_code_in == "":
            if self.output_is_relative:
                output_file_code_in = ""
            else:
                output_file_code_in = self.file_code
        
        return output_file_code_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_output_is_relative(self, output_is_relative_in):
        """validates the given output_is_relative value
        """
        
        return bool(output_is_relative_in)
    
    
    
    #----------------------------------------------------------------------
    def path_code():
        
        def fget(self):
            return self._path_code
        
        def fset(self, path_code_in):
            self._path_code = self._validate_path_code(path_code_in)
        
        doc = """this is the property that helps you assign values to
        path_code attribute"""
        
        return locals()
    
    path_code = property(**path_code())
    
    
    
    #----------------------------------------------------------------------
    def file_code():
        
        def fget(self):
            return self._file_code
        
        def fset(self, file_code_in):
            self._file_code = self._validate_file_code(file_code_in)
        
        doc = """this is the property that helps you assign values to
        file_code attribute"""
        
        return locals()
    
    file_code = property(**file_code())
    
    
    
    #----------------------------------------------------------------------
    def target_entity_type():
        
        def fget(self):
            return self._target_entity_type
        
        doc = """the target entity type this FilenameTemplate object should
        work on, should be a string value or the class itself"""
        
        return locals()
    
    target_entity_type = property(**target_entity_type())
    
    
    
    #----------------------------------------------------------------------
    def output_path_code():
        def fget(self):
            return self._output_path_code
        
        def fset(self, output_path_code_in):
            self._output_path_code =\
                self._validate_output_path_code(output_path_code_in)
        
        doc = """The output_path_code of this FilenameTemplate object.
        
        Should be a unicode string. None and empty string is also accepted, but
        in this case the value is copied from the
        :attr:`~stalker.core.models.FilenameTemplate.path_code` if also the
        :attr:`~stalker.core.models.FilenameTemplate.output_is_relative` is
        False. If
        :attr:`~stalker.core.models.FilenameTemplate.output_is_relative` is
        True then it will left as an empty string.
        """
        
        return locals()
    
    output_path_code = property(**output_path_code())
    
    
    
    #----------------------------------------------------------------------
    def output_file_code():
        def fget(self):
            return self._output_file_code
        
        def fset(self, output_file_code_in):
            self._output_file_code =\
                self._validate_output_file_code(output_file_code_in)
        
        doc = """The output_file_code of this FilenameTemplate object.
        
        Should be a unicode string. None and empty string is also accepted, but
        in this case the value is copied from the
        :attr:`~stalker.core.models.FilenameTemplate.file_code` if also the
        :attr:`~stalker.core.models.FilenameTemplate.output_is_relative` is
        False. If
        :attr:`~stalker.core.models.FilenameTemplate.output_is_relative` is
        True then it will left as an empty string.
        """
        
        return locals()
    
    output_file_code = property(**output_file_code())
    
    
    
    #----------------------------------------------------------------------
    def output_is_relative():
        def fget(self):
            return self._output_is_relative
        
        def fset(self, output_is_relative_in):
            self._output_is_relative =\
                self._validate_output_is_relative(output_is_relative_in)
        
        doc = """
        """
        
        return locals()
    
    output_is_relative = property(**output_is_relative())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """checks the equality of the given object to this one
        """
        
        return super(FilenameTemplate, self).__eq__(other) and \
               isinstance(other, FilenameTemplate) and \
               self.target_entity_type == other.target_entity_type and \
               self.path_code == other.path_code and \
               self.file_code == other.file_code and \
               self.output_path_code == other.output_path_code and \
               self.output_file_code == other.output_file_code





########################################################################
class User(Entity):
    """The user class is designed to hold data about a User in the system.
    
    There are a couple of points to take your attention to:
     
     * The :attr:`~stalker.core.models.User.code` attribute is derived from
       the :attr:`~stalker.core.models.User.nice_name` as it is in a
       :class:`~stalker.core.models.SimpleEntity`, but the
       :attr:`~stalker.core.models.User.nice_name` is derived from the
       :attr:`~stalker.core.models.User.login_name` instead of the
       :attr:`~stalker.core.models.User.name` attribute, so the
       :attr:`~stalker.core.models.User.code` of a
       :class:`~stalker.core.models.User` and a
       :class:`~stalker.core.models.SimpleEntity` will be different then each
       other. The formatting of the :attr:`~stalker.core.models.User.code`
       attribute is as follows:
         
         * no underscore character is allowed, so while in the
           :class:`~stalker.core.models.SimpleEntity` class the code could have
           underscores, in :class:`~stalker.core.models.User` class it is not
           allowed.
        
         * all the letters in the code will be converted to lower case.
       
       Other than this two new rules all the previous formatting rules from the
       :class:`~stalker.core.models.SimpleEntity` are still in charge.
    
     * The :attr:`~stalker.core.models.User.name` is a synonym of the
       :attr:`~stalker.core.models.User.login_name`, so changing one of them
       will change the other.
    
    :param email: holds the e-mail of the user, should be in [part1]@[part2]
      format
    
    :type email: unicode
    
    :param login_name: it is the login name of the user, it should be all lower
      case. Giving a string or unicode that has uppercase letters, it will be
      converted to lower case. It can not be an empty string or None and it can
      not contain any white space inside. login_name parameter will be copied
      over name if both of them is given, if one of them given they will have
      the same value which is the formatted login_name value. Setting the name
      value also sets the login_name and setting the login_name property also
      sets the name, while creating a User object you don't need to specify
      both of them, one is enough and if the two is given `login_name` will be
      used.
    
    :type login_name: unicode
    
    :param first_name: it is the first name of the user, must be a string or
      unicode, middle name also can be added here, so it accepts white-spaces
      in the variable, but it will truncate the white spaces at the beginin and
      at the end of the variable and it can not be empty or None
    
    :type first_name: unicode
    
    :param last_name: it is the last name of the user, must be a string or
      unicode, again it can not contain any white spaces at the beggining and
      at the end of the variable and it can be an empty string or None
    
    :type last_name: unicode
    
    :param department: it is the department of the current user. It should be
      a Department object. One user can only be listed in one department. A
      user is allowed to have no department to make it easy to create a new
      user and create the department and assign the user it later.
    
    :type department: :class:`~stalker.core.models.Department`
    
    :param password: it is the password of the user, can contain any character.
      Stalker doesn't store the raw passwords of the users. To check a stored
      password with a raw password use
      :meth:`~stalker.core.models.User.check_password` and to set the password
      you can use the :attr:`~stalker.core.models.User.password` property
      directly.
    
    :type password: unicode
    
    :param permission_groups: it is a list of permission groups that this user
      is belong to
    
    :type permission_groups: :class:`~stalker.core.models.PermissionGroup`
    
    :param tasks: it is a list of Task objects which holds the tasks that this
      user has been assigned to
    
    :type tasks: list of :class:`~stalker.core.models.Task`\ s
    
    :param projects_lead: it is a list of Project objects that this user
      is the leader of, it is for back refefrencing purposes.
    
    :type projects_lead: list of :class:`~stalker.core.models.Project`\ s
    
    :param sequences_lead: it is a list of Sequence objects that this
      user is the leader of, it is for back referencing purposes
    
    :type sequences_lead: list of :class:`~stalker.core.models.Sequence`
    
    :param last_login: it is a datetime.datetime object holds the last login
      date of the user (not implemented yet)
    
    :type last_login: datetime.datetime
    
    :param initials: it is the initials of the users name, if nothing given it
      will be calculated from the first and last names of the user
    
    :type initials: unicode
    """
    
    #:param projects: it is a list of Project objects which holds the projects
      #that this user is a part of. Calculated from all the
      #:class:`~stalker.core.models.Task`\ s of the current User.
    
    
    
    # fix __new__ errors
    _projects = []
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 department=None,
                 email="",
                 first_name="",
                 last_name="",
                 login_name="",
                 password="",
                 permission_groups=[],
                 #projects=[],
                 projects_lead=[],
                 sequences_lead=[],
                 tasks=[],
                 last_login=None,
                 initials="",
                 **kwargs
                 ):
        
        # use the login_name for name if there are no name attribute present
        name = kwargs.get("name")
        
        if name is None:
            name = login_name
        
        if login_name == "":
            login_name = name
        
        name = login_name
        kwargs["name"] = name
        
        super(User, self).__init__(**kwargs)
        
        self._department = self._validate_department(department)
        self._email = self._validate_email(email)
        self._first_name = self._validate_first_name(first_name)
        self._last_name = self._validate_last_name(last_name)
        
        #self._login_name = ""
        #self.login_name = login_name
        self._login_name = self._validate_login_name(login_name)
        
        self._initials = self._validate_initials(initials)
        
        # to be able to mangle the password do it like this
        self._password = None
        self.password = password
        
        self._permission_groups = \
            self._validate_permission_groups(permission_groups)
        #self._projects = self._validate_projects(projects)
        self._projects_lead = self._validate_projects_lead(projects_lead)
        self._sequences_lead = self._validate_sequences_lead(sequences_lead)
        self._tasks = self._validate_tasks(tasks)
        
        self._last_login = self._validate_last_login(last_login)
    
    
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """return the representation of the current User
        """
        
        return "<User (%s %s ('%s'))>" % \
               (self.first_name, self.last_name, self.login_name)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(User, self).__eq__(other) and \
               isinstance(other, User) and \
               self.email == other.email and \
               self.login_name == other.login_name and \
               self.first_name == other.first_name and \
               self.last_name == other.last_name and \
               self.name == other.name
    
    
    
    #----------------------------------------------------------------------
    def __ne__(self, other):
        """the inequality operator
        """
        
        return not self.__eq__(other)
    
    
    
    #----------------------------------------------------------------------
    def _validate_department(self, department_in):
        """validates the given department value
        """
        
        # check if it is intance of Department object
        if department_in is not None:
            if not isinstance(department_in, Department):
                raise TypeError("department should be instance of "
                                 "stalker.core.models.Department")
        
        return department_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_email(self, email_in):
        """validates the given email value
        """
        
        # check if email_in is an instance of string or unicode
        if not isinstance(email_in, (str, unicode)):
            raise TypeError("email should be an instance of string or "
                             "unicode")
        
        return self._validate_email_format(email_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_email_format(self, email_in):
        """formats the email
        """
        
        # split the mail from @ sign
        splits = email_in.split("@")
        len_splits = len(splits)
        
        # there should be one and only one @ sign
        if len_splits > 2:
            raise ValueError("check the email formatting, there are more than "
                             "one @ sign")
        
        if len_splits < 2:
            raise ValueError("check the email formatting, there are no @ sign")
        
        if splits[0] == "":
            raise ValueError("check the email formatting, the name part is "
                             "missing")
        
        if splits[1] == "":
            raise ValueError("check the email formatting, the domain part is "
                             "missing")
        
        return email_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_first_name(self, first_name_in):
        """validates the given first_name attribute
        """
        
        if first_name_in is None:
            raise TypeError("first_name cannot be None")
        
        if not isinstance(first_name_in, (str, unicode)):
            raise TypeError("first_name should be instance of string or "
                             "unicode")
        
        if first_name_in == "":
            raise ValueError("first_name can not be an empty string")
        
        return self._format_first_name(first_name_in)
    
    
    
    #----------------------------------------------------------------------
    def _format_first_name(self, first_name_in):
        """formats the given first_name
        """
        
        return first_name_in.strip().title()
    
    
    
    #----------------------------------------------------------------------
    def _validate_initials(self, initials_in):
        """validates the given initials
        """
        
        initials_in = str(initials_in)
        
        if initials_in == "":
            # derive the initials from the first and last name
            
            initials_in = re.sub("[^A-Z]+", "",
                                 self.first_name.title() + " " + \
                                 self.last_name.title()).lower()
        
        return initials_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_last_login(self, last_login_in):
        """validates the given last_login argument
        """
        
        if not isinstance(last_login_in, datetime.datetime) and \
           last_login_in is not None:
            raise TypeError("last_login should be an instance of "
                            "datetime.datetime or None")
        
        return last_login_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_last_name(self, last_name_in):
        """validates the given last_name attribute
        """
        
        #if last_name_in is None:
            #raise ValueError("last_name cannot be none")
        if last_name_in is not None:
            if not isinstance(last_name_in, (str, unicode)):
                raise TypeError("last_name should be instance of string or "
                                "unicode")
        else:
            last_name_in = ""
        
        #if last_name_in == "":
            #raise ValueError("last_name can not be an empty string")
        
        return self._format_last_name(last_name_in)
    
    
    
    #----------------------------------------------------------------------
    def _format_last_name(self, last_name_in):
        """formats the given last_name
        """
        
        return last_name_in.strip().title()
    
    
    
    #----------------------------------------------------------------------
    def _validate_login_name(self, login_name_in):
        """validates the given login_name value
        """
        
        if login_name_in is None:
            raise TypeError("login name could not be None")
        
        #if not isinstance(login_name_in, (str, unicode)):
            #raise TypeError("login_name should be instance of string or "
                            #"unicode")
        login_name_in = self._format_login_name(str(login_name_in))
        
        if login_name_in == "":
            raise ValueError("login name could not be empty string")
        
        return login_name_in
    
    
    
    #----------------------------------------------------------------------
    def _format_login_name(self, login_name_in):
        """formats the given login_name
        """
        
        # be sure it is a string
        login_name_in = str(login_name_in)
        
        # strip white spaces from start and end
        login_name_in = login_name_in.strip()
        
        # remove all the spaces
        login_name_in = login_name_in.replace(" ","")
        
        # make it lowercase
        login_name_in = login_name_in.lower()
        
        # remove any illegal characters
        login_name_in = re.sub( "[^\\(a-zA-Z0-9)]+", "", login_name_in)
        
        # remove any number at the begining
        login_name_in = re.sub( "^[0-9]+", "", login_name_in)
        
        return login_name_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_password(self, password_in):
        """validates the given password
        """
        
        if password_in is None:
            raise TypeError("password cannot be None")
        
        return password_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_permission_groups(self, permission_groups_in):
        """check the given permission_group
        """
        
        if permission_groups_in is None:
            permission_groups_in = []
        
        if not isinstance(permission_groups_in, list):
            raise TypeError("permission_groups should be a list of group "
                             "objects")
        
        for permission_group in permission_groups_in:
            if not isinstance(permission_group, PermissionGroup):
                raise TypeError(
                    "any group in permission_groups should be an instance of"
                    "stalker.core.models.PermissionGroup"
                )
        
        return ValidatedList(permission_groups_in, PermissionGroup)
    
    
    
    ##----------------------------------------------------------------------
    #def _validate_projects(self, projects_in):
        #"""validates the given projects attribute
        #"""
        
        #if projects_in is None:
            #projects_in = []
        
        #if not isinstance(projects_in, list):
            #raise TypeError("projects should be a list of "
                             #"stalker.core.models.Project objects")
        
        #for a_project in projects_in:
            #if not isinstance(a_project, Project):
                #raise TypeError(
                    #"any element in projects should be an instance of "
                    #"stalker.core.models.Project"
                #)
        
        #return ValidatedList(projects_in, Project)
        
    
    
    #----------------------------------------------------------------------
    def _validate_projects_lead(self, projects_lead_in):
        """validates the given projects_lead attribute
        """
        
        if projects_lead_in is None:
            projects_lead_in = []
        
        if not isinstance(projects_lead_in, list):
            raise TypeError("projects_lead should be a list of "
                             "stalker.core.models.Project instances")
        
        for a_project in projects_lead_in:
            if not isinstance(a_project, Project):
                raise TypeError(
                    "any element in projects_lead should be a"
                    "stalker.core.models.Project instance")
        
        return ValidatedList(projects_lead_in, Project)
    
    
    
    #----------------------------------------------------------------------
    def _validate_sequences_lead(self, sequences_lead_in):
        """validates the given sequences_lead attribute
        """
        
        if sequences_lead_in is None:
            sequences_lead_in = []
        
        if not isinstance(sequences_lead_in, list):
            raise TypeError("sequences_lead should be a list of "
                             "stalker.core.models.Sequence objects")
        
        for a_sequence in sequences_lead_in:
            if not isinstance(a_sequence, Sequence):
                raise TypeError(
                    "any element in sequences_lead should be an instance of "
                    "stalker.core.models.Sequence class"
                )
        
        return ValidatedList(sequences_lead_in, Sequence)
    
    
    
    #----------------------------------------------------------------------
    def _validate_tasks(self, tasks_in):
        """validates the given taks attribute
        """
        
        if tasks_in is None:
            tasks_in = []
        
        if not isinstance(tasks_in, list):
            raise TypeError("tasks should be a list of "
                             "stalker.core.models.Task objects")
        
        for a_task in tasks_in:
            if not isinstance(a_task, Task):
                raise TypeError(
                    "any element in tasks should be an instance of "
                    "stalker.core.models.Task class")
        
        return ValidatedList(tasks_in, Task)
    
    
    
    #----------------------------------------------------------------------
    def check_password(self, raw_password):
        """Checks the given raw_password.
        
        Checks the given raw_password with the current Users objects encrypted
        password.
        """
        
        from stalker.ext import auth
        return auth.check_password(raw_password, self._password)
    
    
    
    #----------------------------------------------------------------------
    def department():
        
        def fget(self):
            return self._department
        
        def fset(self, department_in):
            self._department = self._validate_department(department_in)
        
        doc = """department of the user, it is a
        :class:`~stalker.core.models.Department` object"""
        
        return locals()
    
    department = property(**department())
    
    
    
    #----------------------------------------------------------------------
    def email():
        
        def fget(self):
            return self._email
        
        def fset(self, email_in):
            self._email = self._validate_email(email_in)
        
        doc = """email of the user, accepts strings or unicodes
        """
        
        return locals()
    
    email = property(**email())
    
    
    
    #----------------------------------------------------------------------
    def first_name():
        
        def fget(self):
            return self._first_name
        
        def fset(self, first_name_in):
            self._first_name = self._validate_first_name(first_name_in)
        
        doc = """first name of the user, accepts string or unicode"""
        
        return locals()
    
    first_name = property(**first_name())
    
    
    
    #----------------------------------------------------------------------
    def initials():
        
        def fget(self):
            return self._initials
        
        def fset(self, initials_in):
            self._intials = self._validate_initials(initials_in)
        
        doc = """The initials of the user.
        
        If not spesified, it is the upper case form of first letters of the
        :attr:`~stalker.core.models.User.first_name` and
        :attr:`~stalker.core.models.User.last_name`"""
        
        return locals()
    
    initials = property(**initials())
    
    
    
    #----------------------------------------------------------------------
    def last_login():
        
        def fget(self):
            return self._last_login
        
        def fset(self, last_login_in):
            self._last_login = self._validate_last_login(last_login_in)
        
        doc = """The last login time of this user.
        
        It is an instance of datetime.datetime class."""
        
        return locals()
    
    last_login = property(**last_login())
    
    
    
    #----------------------------------------------------------------------
    def last_name():
        
        def fget(self):
            return self._last_name
        
        def fset(self, last_name_in):
            self._last_name = self._validate_last_name(last_name_in)
        
        doc = """The last name of the user.
        
        It is a string and can be None or empty string"""
        
        return locals()
    
    last_name = property(**last_name())
    
    
    
    #----------------------------------------------------------------------
    def login_name():
        
        def fget(self):
            return self._name
        
        def fset(self, login_name_in):
            self._name = self._validate_login_name(login_name_in)
            # set the name attribute
            #self._login_name = self._validate_name(login_name_in)
            self._login_name = self._name
            
            # also set the code
            self._code = self._validate_code(self._name)
        
        doc = """The login name of the user.
        
        It is a string and also sets the :attr:`~stalker.core.models.User.name`
        attribute"""
        
        return locals()
    
    login_name = property(**login_name())
    
    
    
    #----------------------------------------------------------------------
    def name():
        
        def fget(self):
            return self._name
        
        def fset(self, name_in):
            
            # set the login name first
            self._login_name = self._validate_login_name(name_in)
            self._name = self._login_name
            
            # also set the nice_name
            self._nice_name = self._condition_nice_name(self._name)
            
            # and also the code
            #self.code = self._nice_name.upper()
            self.code = self._name
        
        doc = """The name of this user.
        
        It is the synonym for the
        :attr:`~stalker.core.models.User.login_name`\."""
        
        return locals()
    
    name = property(**name())
    
    
    
    #----------------------------------------------------------------------
    def password():
        
        def fget(self):
            return self._password
        
        def fset(self, password_in):
            from stalker.ext import auth
            self._password = auth.set_password(password_in)
        
        doc = """The password of the user.
        
        It is scrambled before it is stored."""
        
        return locals()
    
    password = property(**password())
    
    
    
    #----------------------------------------------------------------------
    def permission_groups():
        
        def fget(self):
            return self._permission_groups
        
        def fset(self, permission_groups_in):
            self._permission_groups = \
                self._validate_permission_groups(permission_groups_in)
        
        doc = """permission groups that this users is a member of, accepts
        :class:`~stalker.core.models.PermissionGroup` object"""
        
        return locals()
    
    permission_groups = property(**permission_groups())
    
    
    
    #----------------------------------------------------------------------
    def projects():
        
        def fget(self):
            #return self._projects
            projects = []
            for task in self.tasks:
                projects.append(task.project)
            
            return list(set(projects))
        
        doc = """The list of :class:`~stlalker.core.models.Project`\ s those the current user assigned to.
        
        returns a list of :class:`~stalker.core.models.Project` objects.
        It is a read-only attribute. To assign a
        :class:`~stalker.core.models.User` to a
        :class:`~stalker.core.models.Project`, you need to create a new
        :class:`~stalker.core.models.Task` with the
        :attr:`~stalker.core.models.Task.resources` is set to this
        :class:`~stalker.core.models.User` and assign the
        :class:`~stalker.core.models.Task` to the
        :class:`~stalker.core.models.Project` by setting the
        :attr:`~stalker.core.models.Task.project` attribute of the
        :class:`~stalker.core.models.Task` to the
        :class:`~stalker.core.models.Project`.
        """
        
        return locals()
    
    projects = property(**projects())
    
    
    
    #----------------------------------------------------------------------
    def projects_lead():
        
        def fget(self):
            return self._projects_lead
        
        def fset(self, projects_lead_in):
            self._projects_lead = \
                self._validate_projects_lead(projects_lead_in)
        
        doc = """projects lead by this current user, accepts
        :class:`~stalker.core.models.Project` object"""
        
        return locals()
    
    projects_lead = property(**projects_lead())
    
    
    
    #----------------------------------------------------------------------
    def sequences_lead():
        
        def fget(self):
            return self._sequences_lead
        
        def fset(self, sequences_lead_in):
            self._sequences_lead = \
                self._validate_sequences_lead(sequences_lead_in)
        
        doc = """sequences lead by this user, accpets
        :class:`~stalker.core.models.Sequence` objects"""
        
        return locals()
    
    sequences_lead = property(**sequences_lead())
    
    
    
    #----------------------------------------------------------------------
    def tasks():
        
        def fget(self):
            return self._tasks
        
        def fset(self, tasks_in):
            self._tasks = self._validate_tasks(tasks_in)
        
        doc = """tasks assigned to the current user, accepts
        :class:`~stalker.core.models.Task` objects"""
        
        return locals()
    
    tasks = property(**tasks())



