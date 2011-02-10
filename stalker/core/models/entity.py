#-*- coding: utf-8 -*-



import datetime
import re
from stalker.ext.validatedList import ValidatedList



########################################################################
class EntityMeta(type):
    """the metaclass for the very basic entity, just adds the name of the class
    as the entity_type class attribute
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(cls, classname, bases, dict_):
        setattr(cls, "entity_type", unicode(classname))
        return type.__init__(cls, classname, bases, dict_)






########################################################################
class SimpleEntity(object):
    """The base class of all the others
    
    This class has the basic information about an entity which are the name,
    the description, tags and the audit information like created_by,
    updated_by, date_created and date_updated about this entity.
    
    Two SimpleEntities considered equal if they have the same name, the other
    attributes doesn't matter.
    
    :param name: a string or unicode attribute that holds the name of this
      entity. it could not be empty, the first letter should be an alphabetic
      (not alphanumeric) letter and it should not contain any white space
      at the beggining and at the end of the string, giving an object the
      object will be converted to string and then the resulting string will be
      conditioned.
    
    :param description: a string or unicode attribute that holds the
      description of this entity object, it could be an empty string, and it
      could not again have white spaces at the beggining and at the end of the
      string, again any given objects will be converted to strings
    
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
    
    :param code: this is the code name of this simple entity, can be omitted
      and it will be set to the uppercase version of the nice_name attribute.
      it accepts string or unicode values and any other kind of objects will be
      converted to string. If both the name and code arguments are given the
      code property will be set to code, but in any update to name attribute
      the code also will be updated to the uppercase form of the nice_name
      attribute
    """
    
    
    
    __metaclass__ = EntityMeta
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 name=None,
                 description="",
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
            raise ValueError("the name couldn't be set to None")
        
        name_in = self._condition_name(str(name_in))
        
        # it is empty
        if name_in == "":
            raise ValueError("the name couldn't be an empty string")
        
        return name_in
    
    
    
    def _condition_code(self, code_in):
        """formats the given code_in value
        """
        
        # just set it to the uppercase of what nice_name gives
        return self._condition_nice_name(code_in).upper()
    
    
    
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
        
        doc = """the description of the entity"""
        
        return locals()
    
    description = property(**description())
    
    
    
    #----------------------------------------------------------------------
    def name():
        
        def fget(self):
            return self._name
        
        def fset(self, name_in):
            self._name = self._validate_name(name_in)
            
            # also set the nice_name
            self._nice_name = self._condition_nice_name(self._name)
            
            # set the code
            self.code = self._name
        
        doc = """the name of the entity"""
        
        return locals()
    
    name = property(**name())
    
    
    
    #----------------------------------------------------------------------
    def nice_name():
        
        def fget(self):
            return self._nice_name
        
        doc = """this is the ``nice name`` of the SimpleEntity. It has the same
        value with the name (contextually) but with a different format like,
        all the whitespaces replaced by underscores ("\_"), all the CamelCase
        form will be expanded by underscore (\_) characters and it is always
        lowercase.
        
        There is also the ``code`` attribute which is simple the uppercase form
        of ``nice_name`` if it is not defined differently (i.e set to another
        value).
        """
        
        return locals()
    
    nice_name = property(**nice_name())
    
    
    
    #----------------------------------------------------------------------
    def _validate_code(self, code_in):
        """validates the given code value
        """
        
        # check if the code_in is None
        if code_in is None:
            raise ValueError("the code attribute can not be None")
        
        # check if the code_in is empty
        if code_in=="":
            raise ValueError("the code attribute can not be an empty string")
        
        ## check if it is something other than a string
        #if not isinstance(code_in, (str, unicode)):
            #raise ValueError("the code should be an instance of string or "
            #                 "unicode")
        
        return self._condition_code(str(code_in))
    
    
    
    #----------------------------------------------------------------------
    def _validate_created_by(self, created_by_in):
        """validates the given created_by_in attribute
        """
        
        #-------------------------------------------------------------------
        # Python documentation says one of the nice ways to over come circular
        # imports is late imports and it is perfectly ok to use it like that
        # 
        # just try to import the module as late as possible
        # 
        # ref:
        # http://docs.python.org/faq/programming.html#
        #     what-are-the-best-practices-for-using-import-in-a-module
        #-------------------------------------------------------------------
        from stalker.core.models import user
        
        ## raise ValueError when:
        ## it is None
        #if created_by_in is None:
            #raise ValueError("the created_by attribute can not be set to None")
        
        if created_by_in is not None:
            if not isinstance(created_by_in, user.User):
                raise ValueError("the created_by attribute should be an "
                                 "instance of stalker.core.models.user.User")
        
        return created_by_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_updated_by(self, updated_by_in):
        """validates the given updated_by_in attribute
        """
        
        from stalker.core.models import user
        
        if updated_by_in is None:
            # set it to what created_by attribute has
            updated_by_in = self._created_by
        
        if updated_by_in is not None:
            if not isinstance(updated_by_in, user.User):
                raise ValueError("the updated_by attribute should be an "
                                 "instance of stalker.core.models.user.User")
        
        return updated_by_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_date_created(self, date_created_in):
        """validates the given date_creaetd_in
        """
        
        # raise ValueError when:
        
        # it is None
        if date_created_in is None:
            raise ValueError("the date_created could not be None")
        
        if not isinstance(date_created_in, datetime.datetime):
            raise ValueError("the date_created should be an instance of "
                             "datetime.datetime")
        
        return date_created_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_date_updated(self, date_updated_in):
        """validates the given date_updated_in
        """
        
        # raise ValueError when:
        
        # it is None
        if date_updated_in is None:
            raise ValueError("the date_updated could not be None")
        
        # it is not an instance of datetime.datetime
        if not isinstance(date_updated_in, datetime.datetime):
            raise ValueError("the date_updated should be an instance of "
                             "datetime.datetime")
        
        # lower than date_created
        if date_updated_in < self.date_created:
            raise ValueError("the date_updated could not be set to a date "
                             "before date_created, try setting the "
                             "date_created before")
        
        return date_updated_in
    
    
    
    #----------------------------------------------------------------------
    def code():
        def fget(self):
            return self._code
        def fset(self, code_in):
            self._code = self._validate_code(code_in)
        return locals()
    
    code = property(**code())
    
    
    
    #----------------------------------------------------------------------
    def created_by():
        
        def fget(self):
            return self._created_by
        
        def fset(self, created_by_in):
            self._created_by = self._validate_created_by(created_by_in)
        
        doc = """gets and sets the User object who has created this
        AuditEntity"""
        
        return locals()
    
    created_by = property(**created_by())
    
    
    
    #----------------------------------------------------------------------
    def updated_by():
        
        def fget(self):
            return self._updated_by
        
        def fset(self, updated_by_in):
            self._updated_by = self._validate_updated_by(updated_by_in)
        
        doc = """gets and sets the User object who has updated this
        AuditEntity"""
        
        return locals()
    
    updated_by = property(**updated_by())
    
    
    
    #----------------------------------------------------------------------
    def date_created():
        
        def fget(self):
            return self._date_created
        
        def fset(self, date_created_in):
            self._date_created = self._validate_date_created(date_created_in)
        
        doc = """gets and sets the datetime.datetime object which shows when
        this object has been created"""
        
        return locals()
    
    date_created = property(**date_created())
    
    
    
    #----------------------------------------------------------------------
    def date_updated():
        
        def fget(self):
            return self._date_updated
        
        def fset(self, date_updated_in):
            self._date_updated = self._validate_date_updated(date_updated_in)
        
        doc = """gets and sets the datetime.datetime object which shows when
        this object has been updated"""
        
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
    
    :param tags: a list of tag objects related to this entity. tags could be an
      empty list, or when omitted it will be set to an empty list
    
    :param notes: a list of note objects. notes can be an empty list, or when
      omitted it will be set to an empty list
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
            raise ValueError("notes should be an instance of list")
        
        from stalker.core.models import note
        
        for element in notes_in:
            if not isinstance(element, note.Note):
                raise ValueError("every element in notes should be an "
                                 "instance of stalker.core.models.note.Note "
                                 "class")
        
        return ValidatedList(notes_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_tags(self, tags_in):
        """validates the given tags_in value
        """
        
        # it is not an instance of list
        if not isinstance(tags_in, list):
            raise ValueError("the tags attribute should be set to a list")
        
        return ValidatedList(tags_in)
    
    
    
    #----------------------------------------------------------------------
    def notes():
        def fget(self):
            return self._notes
        def fset(self, notes_in):
            self._notes = self._validate_notes(notes_in)
        
        doc = """all the notes about this entity, it should be a list of Notes
        objects or an empty list, None is not accepted
        """
        
        return locals()
    
    notes = property(**notes())
    
    
    
    #----------------------------------------------------------------------
    def tags():
        
        def fget(self):
            return self._tags
        
        def fset(self, tags_in):
            self._tags = self._validate_tags(tags_in)
        
        doc = """a list of Tag objects which shows the related tags to the
        entity"""
        
        return locals()
    
    tags = property(**tags())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Entity, self).__eq__(other) and \
               isinstance(other, Entity)






########################################################################
class TypeEntity(Entity):
    """The entry point for types.
    
    It is created to group the `Type` objects, so any other classes accepting a
    ``TypeEntity`` object can have one of the derived classes, this is done in
    that way mainly to ease the of creation of only one
    :class:`~stalker.core.models.types.TypeTemplate` class and let the
    others to use this one TypeTemplate class.
    
    It doesn't add any new parameters to it's super.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(TypeEntity, self).__init__(**kwargs)
    
    
    
    ##----------------------------------------------------------------------
    #def __repr__(self):
        #"""the representation
        #"""
        
        #return "<TypeEntity (%s, %s)>" % (self.name, self.code)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(TypeEntity, self).__eq__(other) and \
               isinstance(other, TypeEntity)
    
    
    
    #----------------------------------------------------------------------
    def __ne__(self, other):
        """the inequality operator
        """
        
        return not self.__eq__(other)
    
    
    