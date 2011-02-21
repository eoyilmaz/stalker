#-*- coding: utf-8 -*-


import re
import datetime
import platform
import uuid

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
    
    :param created_by: The :class:`stalker.core.models.User` who has created
      this object
    
    :type created_by: :class:`stalker.core.models.User`
    
    :param updated_by: The :class:`stalker.core.models.User` who has updated
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
      omitted and it will be set to the uppercase version of the nice_name
      attribute. If both the name and code arguments are given the code
      attribute will be set to the given code argument value, but in any update
      to name attribute the code also will be updated to the uppercase form of
      the nice_name attribute. When the code is directly edited the code will
      not be formated other than removing any illegal characters. The default
      value is the upper case form of the nice_name.
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
            self._name = self._validate_name(name_in)
            
            # also set the nice_name
            self._nice_name = self._condition_nice_name(self._name)
            
            # set the code
            self.code = self._nice_name.upper()
        
        doc = """Name of this object"""
        
        return locals()
    
    name = property(**name())
    
    
    
    #----------------------------------------------------------------------
    def nice_name():
        
        def fget(self):
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
            code_in = self.nice_name.upper()
        
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
        
        ## raise ValueError when:
        ## it is None
        #if created_by_in is None:
            #raise ValueError("the created_by attribute can not be set to None")
        
        if created_by_in is not None:
            if not isinstance(created_by_in, User):
                raise ValueError("the created_by attribute should be an "
                                 "instance of stalker.core.models.User")
        
        return created_by_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_updated_by(self, updated_by_in):
        """validates the given updated_by_in attribute
        """
        
        if updated_by_in is None:
            # set it to what created_by attribute has
            updated_by_in = self._created_by
        
        if updated_by_in is not None:
            if not isinstance(updated_by_in, User):
                raise ValueError("the updated_by attribute should be an "
                                 "instance of stalker.core.models.User")
        
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
        
        doc = """The code name of this object.
        
        It accepts string or unicode values and any other kind of objects will
        be converted to string. In any update to the name attribute the code
        also will be updated to the uppercase form of the nice_name attribute.
        If the not initialized or given as None, it will be set to the
        uppercase version of the nice_name attribute. Setting the code
        attribute to None will reset it to the default value. The default value
        is the upper case form of the nice_name. """
        
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
    
    :param list tags: A list of :class:`stalker.core.models.Tag` objects
      related to this entity. tags could be an empty list, or when omitted it
      will be set to an empty list.
    
    :param list notes: A list of :class:`stalker.core.models.Note` instances.
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
            raise ValueError("notes should be an instance of list")
        
        for element in notes_in:
            if not isinstance(element, Note):
                raise ValueError("every element in notes should be an "
                                 "instance of stalker.core.models.Note "
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
        
        doc = """All the notes about this entity.
        
        It is a list of :class:`stalker.core.models.Note` objects or an empty
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
        
        It is a list of :class:`stalker.core.models.Tag` instances which shows
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
class TypeEntity(Entity):
    """The entry point for **Types**.
    
    There are currently four Type classes in Stalker:
     
     * :class:`~stalker.core.models.AssetType`
     * :class:`~stalker.core.models.LinkType`
     * :class:`~stalker.core.models.ProjectType`
     * :class:`~stalker.core.models.TaskType`
    
    All derives from :class:`stalker.core.models.TypeEntity`.
    
    The main purpose of these classes are to introduce reusable *Types* of the
    related class. So an :class:`~stalker.core.models.AssetType` introduces
    reusable types for :class:`~stalker.core.models.Asset`,
    :class:`~stalker.core.models.LinkType` for
    :class:`~stalker.core.models.Link` and
    :class:`~stalker.core.models.ProjectType` for
    :class:`~stalker.core.models.Project`\ and finaly
    :class:`~stalker.core.models.TaskType` for
    :class:`~stalker.core.more.Task`.
    
    By using these *type classes* you are able to let say create *Commercial*
    projects, or create a *Character* assets, *Image* links or *Modeling*
    tasks.
    
    One another use of the :class:`~stalker.core.models.TypeEntity` is, to
    group the instances deriving from the inherited classes, so any other
    classes accepting a ``TypeEntity`` object can have one of the derived
    classes, this is done in that way mainly to ease the of creation of only
    one :class:`stalker.core.models.TypeTemplate` class and let the others (the
    inherited classes) to use this one TypeTemplate class.
    
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






########################################################################
class Link(Entity):
    """Holds data about external links.
    
    Links are all about to give some external information to the current entity
    (external to the database, so it can be something on the
    :class:`stalker.core.models.Repository` or in the Web). The
    link type is defined by the :class:`stalker.core.models.LinkType` object
    and it can be anything like *General*, *File*, *Folder*, *WebPage*,
    *Image*, *ImageSequence*, *Movie*, *Text* etc. (you can also use multiple
    :class:`stalker.core.models.Tag` objects to adding more information,
    and filtering back). Again it is defined by the needs of the studio.
    
    :param path: The Path to the link, it can be a path to a file in the file
      system, or a web page.  Setting path to None or an empty string is not
      accepted and causes a ValueError to be raised.
    
    :param filename: The file name part of the link url, for file sequences use
      "#" in place of the numerator (`Nuke`_ style). Setting filename to None
      or an empty string is not accepted and causes a ValueError to be raised.
    
    :param type\_: The type of the link. It should be an instance of
      :class:`stalker.core.models.LinkType`, the type can not be
      None or anything other than a
      :class:`stalker.core.models.LinkType` object. Specifies the link
      type, can be an LinkType with name Image, Movie/Video, Sound etc.
    
    .. _Nuke: http://www.thefoundry.co.uk
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, path="", filename="", type=None, **kwargs):
        super(Link, self).__init__(**kwargs)
        
        self._path = self._validate_path(path)
        self._filename = self._validate_filename(filename)
        self._type = self._validate_type(type)
    
    
    
    #----------------------------------------------------------------------
    def _validate_path(self, path_in):
        """validates the given path
        """
        
        if path_in is None:
            raise ValueError("path can not be None")
        
        if not isinstance(path_in, (str, unicode)):
            raise ValueError("path should be an instance of string or unicode")
        
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
            raise ValueError("filename can not be None")
        
        if not isinstance(filename_in, (str, unicode)):
            raise ValueError("filename should be an instance of string or "
                             "unicode")
        
        if filename_in=="":
            raise ValueError("filename can not be an empty string")
        
        return filename_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_type(self, type_in):
        """validates the given type
        """
        
        if type_in is None:
            raise ValueError("type can not be None, set it to a "
                             "stalker.core.models.LinkType object")
        
        if not isinstance(type_in, LinkType):
            raise ValueError("type should be an instance of "
                             "stalker.core.models.LinkType object")
        
        return type_in
    
    
    
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
    
    
    
    #----------------------------------------------------------------------
    def type():
        def fget(self):
            return self._type
        
        def fset(self, type_in):
            self._type = self._validate_type(type_in)
        
        doc="""the type of the link, it should be a
        :class:`stalker.core.models.LinkType` object and it can not be
        None"""
        
        return locals()
    
    type = property(**type())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Link, self).__eq__(other) and \
               isinstance(other, Link) and \
               self.path == other.path and \
               self.filename == other.filename and \
               self.type == other.type






########################################################################
class ReferenceMixin(object):
    """Adds reference capabilities to the mixed in class.
    
    References are :class:`stalker.core.models.Link` objects which adds
    outside information to the attached objects. The aim of the References are
    generally to give more info to direct the evolution of the objects,
    generally these objects are :class:`stalker.core.models.Asset`\ s.
    """
    
    
    
    _references = ValidatedList([], Link)
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 references=ValidatedList([], Link),
                 **kwargs):
        
        self._validate_references(references)
    
    
    
    #----------------------------------------------------------------------
    def _validate_references(self, references_in):
        """validates the given references_in
        """
        
        # it should be an object supporting indexing, not necessarily a list
        if not (hasattr(references_in, "__setitem__") and \
                hasattr(references_in, "__getitem__")):
            raise ValueError("the references_in should support indexing")
        
        # all the elements should be instance of stalker.core.models.Link
        if not all([isinstance(element, Link)
                    for element in references_in]):
            raise ValueError("all the elements should be instances of "
                             ":class:`stalker.core.models.Link`")
        
        return ValidatedList(references_in, Link)
    
    
    
    #----------------------------------------------------------------------
    def references():
        
        def fget(self):
            return self._references
        
        def fset(self, references_in):
            self._references = self._validate_references(references_in)
        
        doc="""references are lists containing
        :class:`stalker.core.models.Link` objects
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
    def __init__(self, status=0, status_list=None, **kwargs):
        
        self._status_list = self._validate_status_list(status_list)
        self._status = self._validate_status(status)
    
    
    
    #----------------------------------------------------------------------
    def _validate_status_list(self, status_list_in):
        """validates the given status_list_in value
        """
        
        # raise ValueError when:
        
        # it is not an instance of status_list
        if not isinstance(status_list_in, StatusList):
            raise ValueError("the status list should be an instance of "
                             "stalker.core.models.StatusList")
        
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
        
        if not isinstance(self.status_list, StatusList):
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
        
        doc = """The current status index of the object.
        
        This is an integer value and shows the index of the
        :class:`stalker.core.models.Status` object in the
        :class:`stalker.core.models.StatusList` of this object.
        """
        
        return locals()
    
    status = property(**status())
        
    
    
    
    #----------------------------------------------------------------------
    def status_list():
        
        def fget(self):
            return self._status_list
        
        def fset(self, status_list_in):
            self._status_list = self._validate_status_list(status_list_in)
        
        doc = """The list of statuses that this object can have.
        
        
        """
        
        return locals()
    
    status_list = property(**status_list())






########################################################################
class ScheduleMixin(object):
    """Adds schedule info to the mixed in class.
    
    The schedule is the right mixin for entities which needs schedule
    information like ``start_date``, ``due_date`` and ``duration``
    
    The date attributes can be managed with timezones. Follow the Python idioms
    shown in the `documentation of datetime`_
    
    .. _documentation of datetime: http://docs.python.org/library/datetime.html
    
    :param start_date: the start date of the entity, should be a datetime.date
      instance, when given as None or tried to be set to None, it is to set to
      today, setting the start date also effects due date, if the new
      start_date passes the due_date the due_date is also changed to a date to
      keep the timedelta between dates. The default value is
      datetime.date.today()
    
    :type start_date: :class:`datetime.datetime`
    
    :param due_date: the due_date of the entity, should be a datetime.date or
      datetime.timedelta instance, if given as a datetime.timedelta, then it
      will be converted to date by adding the timedelta to the start_date
      attribute, when the start_date is changed to a date passing the due_date,
      then the due_date is also changed to a later date so the timedelta is
      kept between the dates. The default value is 10 days given as
      datetime.timedelta
    
    :type due_date: :class:`datetime.datetime` or :class:`datetime.timedelta`
    
    """
    
    
    _start_date = datetime.date.today()
    _due_date = _start_date + datetime.timedelta(days=10)
    _duration = _due_date - _start_date
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 start_date=datetime.date.today(),
                 due_date=datetime.timedelta(days=10),
                 **kwargs
                 ):
        
        self._start_date = self._validate_start_date(start_date)
        self._due_date = self._validate_due_date(due_date)
        self._duration = self.due_date - self.start_date
    
    
    
    #----------------------------------------------------------------------
    def _validate_due_date(self, due_date_in):
        """validates the given due_date_in value
        """
        
        if due_date_in is None:
            due_date_in = datetime.timedelta(days=10)
        
        if not isinstance(due_date_in, (datetime.date, datetime.timedelta)):
            raise ValueError("the due_date should be an instance of "
                             "datetime.date or datetime.timedelta")
        
        if isinstance(due_date_in, datetime.date) and \
           self.start_date > due_date_in:
            raise ValueError("the due_date should be set to a date passing "
                             "the start_date, or should be set to a "
                             "datetime.timedelta")
        
        if isinstance(due_date_in, datetime.timedelta):
            due_date_in = self._start_date + due_date_in
        
        return due_date_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_start_date(self, start_date_in):
        """validates the given start_date_in value
        """
        
        if start_date_in is None:
            start_date_in = datetime.date.today()
        
        if not isinstance(start_date_in, datetime.date):
            raise ValueError("start_date shouldbe an instance of "
                             "datetime.date")
        
        return start_date_in
    
    
    
    #----------------------------------------------------------------------
    def due_date():
        def fget(self):
            return self._due_date
        
        def fset(self, due_date_in):
            self._due_date = self._validate_due_date(due_date_in)
            
            # update the _project_duration
            self._duration = self._due_date - self._start_date
        
        doc = """The date that the entity should be delivered.
        
        The due_date can be set to a datetime.timedelta and in this case it
        will be calculated as an offset from the start_date and converted to
        datetime.date again. Setting the start_date to a date passing the
        due_date will also set the due_date so the timedelta between them is
        preserved, default value is 10 days"""
        
        return locals()
    
    due_date = property(**due_date())
    
    
    
    #----------------------------------------------------------------------
    def start_date():
        def fget(self):
            return self._start_date
        
        def fset(self, start_date_in):
            self._start_date = self._validate_start_date(start_date_in)
            
            # check if start_date is passing due_date and offset due_date
            # accordingly
            if self._start_date > self._due_date:
                self._due_date = self._start_date + self._duration
            
            # update the project duration
            self._duration = self._due_date - self._start_date
        
        doc = """The date that this entity should start.
        
        Also effects the due_date in certain conditions, if the start_date is
        set to a time passing the due_date it will also offset the due_date to
        keep the time difference between the start_date and due_date.
        start_date should be an instance of datetime.date and the default value
        is datetime.date.today()"""
        
        return locals()
    
    start_date = property(**start_date())
    
    
    
    #----------------------------------------------------------------------
    def duration():
        def fget(self):
            return self._duration
        
        doc = """Duration of the project.
        
        The duration is calculated by subtracting start_date from the due_date,
        so it is a datetime.timedelta, for now it is read-only
        """
        
        return locals()
    
    duration = property(**duration())






########################################################################
class AssetBase(Entity, ReferenceMixin, StatusMixin):
    """The base class for :class:`~stalker.core.models.Shot` and :class:`~stalker.core.models.Asset` classes.
    
    This the base class for :class:`stalker.core.models.Shot` and
    :class:`stalker.core.models.Asset` classes which gathers the common
    attributes of these two entities.
    
    :param type: The type of the asset or shot. The default value is None.
    
    :type type: :class:`stalker.core.models.AssetType`
    
    :param list tasks: The list of tasks. Should be a list of
      :class:`stalker.core.models.Task` instances. Default value is an
      empty list.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, type=None, tasks=[], **kwargs):
        super(AssetBase, self).__init__(**kwargs)
        self._tasks = self._validate_tasks(tasks)
        self._type = self._validate_type(type)
    
    
    
    #----------------------------------------------------------------------
    def _validate_tasks(self, tasks_in):
        """validates the given tasks_in value
        """
        
        if tasks_in is None:
            tasks_in = []
        
        if not isinstance(tasks_in, list):
            raise ValueError("tasks should be a list")
        
        for item in tasks_in:
            if not isinstance(item, Task):
                raise ValueError("tasks should be a list of "
                "stalker.core.models.Task instances")
        
        return ValidatedList(tasks_in, Task)
    
    
    
    #----------------------------------------------------------------------
    def _validate_type(self, type_in):
        """validates the given type_in value
        """
        
        if type_in is not None:
            if not isinstance(type_in, AssetType):
                raise ValueError("type should be an instance of "
                                 "stalker.core.models.AssetType")
        
        return type_in
    
    
    
    #----------------------------------------------------------------------
    def tasks():
        def fget(self):
            return self._tasks
        def fset(self, task_in):
            self._tasks = self._validate_tasks(task_in)
        
        doc = """The list of :class:`~stalker.core.models.Task` instances.
        """
        
        return locals()
    
    tasks = property(**tasks())
    
    
    
    #----------------------------------------------------------------------
    def type():
        def fget(self):
            return self._type
        def fset(self, type_in):
            self._type = self._validate_type(type_in)
        
        doc = """The type of this object."""
        
        return locals()
    
    type = property(**type())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(AssetBase, self).__eq__(other) and \
               isinstance(other, AssetBase) and self.type == other.type






########################################################################
class Asset(AssetBase):
    """The Asset class is the whole idea behind Stalker.
    """
    
    
    
    pass






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
      Anything other than a string or unicode will raise a ValueError.
    
    :param to: the relation variable, that holds the connection that this
      comment is related to. it should be an Entity object, any other will
      raise a ValueError
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
            raise ValueError("the body attribute should be an instance of "
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
            raise ValueError("the to attribute could not be empty")
        
        if not isinstance(to_in, Entity):
            raise ValueError("the to attibute should be an instance of "
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
        
        for member in members:
            if not isinstance(member, User):
                raise ValueError("every element in the members list should be "
                                 "an instance of stalker.core.models.User"
                                 " class")
        
        return ValidatedList(members, User)
    
    
    
    #----------------------------------------------------------------------
    def _validate_lead(self, lead):
        """validates the given lead attribute
        """
        
        # the lead should not be None
        #if lead is None:
            #raise ValueError("lead could not be set to None")
        
        if lead is not None:
            # the lead should be an instance of User class
            if not isinstance(lead, User):
                raise ValueError("lead should be an instance of "
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
class LoginError(Exception):
    """Raised when the login information is not correct or not correlate with
    the data in the database
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, value):
        self.value = value
    
    
    
    #----------------------------------------------------------------------
    def __str__(self):
        return repr(self.value)






########################################################################
class Group(Entity):
    """the group class
    """
    
    pass






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
            raise ValueError("width should be an instance of int or float")
        
        if width <= 0:
            raise ValueError("width shouldn't be zero or negative")
        
        return int(width)
    
    
    
    #----------------------------------------------------------------------
    def _validate_height(self, height):
        """validates the given height
        """
        if not isinstance(height, (int, float)):
            raise ValueError("height should be an instance of int or float")
        
        if height <= 0:
            raise ValueError("height shouldn't be zero or negative")
        
        return int(height)
    
    
    
    #----------------------------------------------------------------------
    def _validate_pixel_aspect(self, pixel_aspect):
        """validates the given pixel aspect
        """
        if not isinstance(pixel_aspect, (int, float)):
            raise ValueError("pixel_aspect should be an instance of int or "
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
            raise ValueError("print resolution should be an instance of int "
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
        * for improper inputs the object will raise a ValueError
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
        * for improper inputs the object will raise a ValueError
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
        * for improper inputs the object will raise a ValueError
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
        * for improper inputs the object will raise a ValueError
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
class Message(Entity, StatusMixin):
    """The base of the messaging system in Stalker
    
    Messages are one of the ways to collaborate in Stalker. The model of the
    messages is taken from the e-mail system. So it is pretty similiar to an
    e-mail message.
    
    :param from: the :class:`stalker.core.models.User` object sending the
      message
    
    :param to: the list of :class:`stalker.core.models.User`\ s to
      receive this message
    
    :param subject: the subject of the message
    
    :param body: the body of the message
    
    :param in_reply_to: the :class:`stalker.core.models.Message`
      object which this message is a reply to.
    
    :param replies: the list of :class:`stalker.core.models.Message`
      objects which are the direct replies of this message
    
    :param attachments: a list of
      :class:`stalker.core.models.SimpleEntity` objects attached to
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
            raise ValueError("content should be an instance of string or "
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
        than None or string or unicode will raise a ValueError"""
        
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
class TaskType(TypeEntity):
    """Defines the type of the a :class:`~stalker.core.models.Task`.
    
    A TaskType object represents the general steps which are used around the
    studio. A couple of examples are:
    
      * Design
      * Model
      * Rig
      * Fur
      * Shading
      * Previs
      * Match Move
      * Animations
      
      etc.
    
    Doesn't add any new parameter for its parent class.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(TaskType, self).__init__(**kwargs)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(TaskType, self).__eq__(other) and \
               isinstance(other, TaskType)






########################################################################
class Project(Entity, ReferenceMixin, StatusMixin, ScheduleMixin):
    """All the information about a Project in Stalker is hold in this class.
    
    Project is one of the main classes that will direct the others. A project
    in Stalker is a gathering point.
    
    It is mixed with :class:`stalker.core.models.ReferenceMixin`,
    :class:`stalker.core.models.StatusMixin` and
    :class:`stalker.core.models.ScheduleMixin` to give reference, status
    and schedule abilities.
    
    :param lead: The lead of the project. Default value is None.
    
    :type lead: :class:`stalker.core.models.User`
    
    :param list users: The users assigned to this project, should be a list of
      :class:`stalker.core.models.User` instances, if set to None it is
      converted to an empty list. Default value is an empty list.
    
    :param list sequences: The sequences of the project, it should be a list of
      :class:`stalker.core.models.Sequence` instances, if set to None it is
      converted to an empty list. Default value is an empty list.
    
    :param list assets: The assets used in this project, it should be a list of
      :class:`stalker.core.models.Asset` instances, if set to None it is
      converted to an empty list. Default value is an empty list.
    
    :param image_format: The output image format of the project. Default
      value is None.
    
    :type image_format: :class:`stalker.core.models.ImageFormat`
    
    :param float fps: The FPS of the project, it should be a integer or float
      number, or a string literal which can be correctly converted to a float.
      Default value is 25.0.
    
    :param type: The type of the project. Default value is None.
    
    :type type: :class:`stalker.core.models.ProjectType`
    
    :param structure: The structure of the project. Default value is None
    
    :type structure: :class:`stalker.core.models.Structure`
    
    :param repository: The repository that the project files are going to be
      stored in. You can not create the project folder structure if the project
      doesn't have a connection to a
      :class:`stalker.core.models.Repository`. Default value is
      None.
    
    :type repository: :class:`stalker.core.models.Repository`.
    
    :param bool is_stereoscopic: a bool value, showing if the project is going
      to be a stereo 3D project, anything given as the argument will be
      converted to True or False. Default value is False.
    
    :param float display_width: the width of the display that the output of the
      project is going to be displayed (very unnecessary if you are not using
      stereo 3D setup). Should be an int or float value, negative values
      converted to the positive values. Default value is 1.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 start_date=datetime.date.today(),
                 due_date=datetime.timedelta(days=10),
                 lead=None,
                 users=[],
                 repository=None,
                 type=None,
                 structure=None,
                 sequences=[],
                 assets=[],
                 image_format=None,
                 fps=25.0,
                 is_stereoscopic=False,
                 display_width=1.0,
                 references=[],
                 **kwargs):
        
        super(Project, self).__init__(**kwargs)
        # call the mixin __init__ methods
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)
        
        self._start_date = self._validate_start_date(start_date)
        self._due_date = self._validate_due_date(due_date)
        self._lead = self._validate_lead(lead)
        self._users = self._validate_users(users)
        self._repository = self._validate_repository(repository)
        self._type = self._validate_type(type)
        self._structure = self._validate_structure(structure)
        self._sequences = self._validate_sequences(sequences)
        self._assets = self._validate_assets(assets)
        
        # do not persist this attribute
        self._project_duration = self._due_date - self._start_date
        
        self._image_format = self._validate_image_format(image_format)
        self._fps = self._validate_fps(fps)
        self._is_stereoscopic = bool(is_stereoscopic)
        self._display_width = self._validate_display_width(display_width)
        
        ## update the mixin side of the project class (status and references)
        #self.status_list = status_list
        #self.status = status
        #self.references = references
        #self.start_date = start_date
        #self.due_date = due_date
    
    
    
    #----------------------------------------------------------------------
    def _validate_assets(self, assets_in):
        """validates the given assets_in lists
        """
        
        if assets_in is None:
            assets_in = []
        
        if not all([isinstance(element, Asset)
                    for element in assets_in]):
            raise ValueError("the elements in assets lists should be all "
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
            raise ValueError("the image_format should be an instance of "
                             "stalker.core.models.ImageFormat")
        
        return image_format_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_lead(self, lead_in):
        """validates the given lead_in value
        """
        
        if lead_in is not None:
            if not isinstance(lead_in, User):
                raise ValueError("lead must be an instance of "
                                 "stalker.core.models.User")
        
        return lead_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_repository(self, repository_in):
        """validates the given repository_in value
        """
        
        if repository_in is not None and \
           not isinstance(repository_in, Repository):
            raise ValueError("the repsoitory should be an instance of "
                             "stalker.core.models.Repository")
        
        return repository_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_sequences(self, sequences_in):
        """validates the given sequences_in value
        """
        
        if sequences_in is None:
            sequences_in = []
        
        if not all([isinstance(seq, Sequence)
                    for seq in sequences_in]):
            raise ValueError("sequences should be a list of "
                             "stalker.core.models.Sequence instances")
        
        return ValidatedList(sequences_in, Sequence)
    
    
    
    #----------------------------------------------------------------------
    def _validate_structure(self, structure_in):
        """validates the given structure_in vlaue
        """
        
        if structure_in is not None:
            if not isinstance(structure_in, Structure):
                raise ValueError("structure should be an instance of "
                                 "stalker.core.models.Structure")
        
        return structure_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_type(self, type_in):
        """validates the given type_in value
        """
        
        if type_in is not None and not isinstance(type_in, ProjectType):
            raise ValueError("type should be an instance of "
                             "stalker.core.models.ProjectType")
        
        return type_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_users(self, users_in):
        """validates the given users_in value
        """
        
        if users_in is None:
            users_in = []
        
        if not all([isinstance(element, User) \
                    for element in users_in]):
            raise ValueError("users should be a list containing instances of "
                             ":class:`stalker.core.models.User`")
        
        return ValidatedList(users_in)
    
    
    
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
        :class:`stalker.core.models.ImageFormat`, can not be
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
        :class:`stalker.core.models.User`, also can set to None"""
        
        return locals()
    
    lead = property(**lead())
    
    
    
    #----------------------------------------------------------------------
    def repository():
        def fget(self):
            return self._repository
        def fset(self, repository_in):
            self._repository = self._validate_repository(repository_in)
        
        doc = """the repository that this project should reside, should be an
        instance of :class:`stalker.core.models.Repository`, can
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
        containing all of :class:`stalker.core.models.Sequence`
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
        :class:`stalker.core.models.Structure` class"""
        
        return locals()
    
    structure = property(**structure())
    
    
    
    
    #----------------------------------------------------------------------
    def type():
        def fget(self):
            return self._type
        def fset(self, type_in):
            self._type = self._validate_type(type_in)
        
        doc = """defines the type of the project, should be an instance of
        :class:`stalker.core.models.ProjectType`"""
        
        return locals()
    
    type = property(**type())
    
    
    
    #----------------------------------------------------------------------
    def users():
        def fget(self):
            return self._users
        def fset(self, users_in):
            self._users = self._validate_users(users_in)
        
        doc = """the users assigned to this project. Should be a list of
        :class:`stalker.core.models.User` instances. Can be and empty
        list, and when set to None it will be converted to an empty list"""
        
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
            raise ValueError("linux_path should be an instance of string or "
                             "unicode")
        
        return linux_path_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_osx_path(self, osx_path_in):
        """validates the given osx path
        """
        
        if not isinstance(osx_path_in, (str, unicode)):
            raise ValueError("osx_path should be an instance of string or "
                             "unicode")
        
        return osx_path_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_windows_path(self, windows_path_in):
        """validates the given windows path
        """
        
        if not isinstance(windows_path_in, (str, unicode)):
            raise ValueError("windows_path should be an instance of string or "
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
class Sequence(Entity, ReferenceMixin, StatusMixin, ScheduleMixin):
    """Stores data about Sequences.
    
    Sequences are holders of the :class:`stalker.core.models.Shot` objects.
    They orginize the conceptual data with another level of complexity.
    
    :param project: The :class:`stalker.core.models.Project` that this
      Sequence belongs to. The default value is None.
    
    :type project: :class:`stalker.core.models.Project`.
    
    :param list shots: The list of :class:`stalker.core.models.Shot` objects
      that this Sequence has. The default value is an empty list.
    
    :param lead: The lead of this Seuqence. The default value is None.
    
    :type lead: :class:`stalker.core.models.User`
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 project=None,
                 shots=[],
                 lead=None,
                 **kwargs
                 ):
        
        super(Sequence, self).__init__(**kwargs)
        
        # call the mixin __init__ methods
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)
        
        self._project = self._validate_project(project)
        self._lead = self._validate_lead(lead)
        self._shots = self._validate_shots(shots)
    
    
    
    #----------------------------------------------------------------------
    def _validate_project(self, project_in):
        """validates the given project_in value
        """
        
        if project_in is not None:
            if not isinstance(project_in, Project):
                raise ValueError("project should be instance of"
                                 "stalker.core.models.Project")
        
        return project_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_lead(self, lead_in):
        """validates the given lead_in value
        """
        
        if lead_in is not None:
            if not isinstance(lead_in, User):
                raise ValueError("lead should be instance of "
                                 "stalker.core.models.User")
        
        return lead_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_shots(self, shots_in):
        """validates the given shots_in value
        """
        
        if shots_in is None:
            shots_in = []
        
        if not isinstance(shots_in, list):
            raise ValueError("shots should be list containing "
                             "stalker.core.models.Shot instances")
        
        for element in shots_in:
            if not isinstance(element, Shot):
                raise ValueError("every item in the shots list should be an "
                                 "instance of stalker.core.models.Shot")
        
        return ValidatedList(shots_in, Shot)
        
    
    
    
    #----------------------------------------------------------------------
    def project():
        def fget(self):
            return self._project
        def fset(self, project_in):
            self._project = self._validate_project(project_in)
        
        doc ="""The Project of this sequence object."""
        
        return locals()
    
    project = property(**project())
    
    
    
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
class Shot(AssetBase):
    """Manage Shot related data.
    
    WARNING: (obviously) not implemented yet!
    
    Because most of the shots in different projects are going to have the same
    name, which is a kind of code like SH001, SH012A etc., and in Stalker you
    can not have two entities with the same name if their types are also
    matching, to guarantee all the shots are going to have different names the
    :attr:`~stalker.core.models.Shot.name` attribute of the Shot instances are
    automatically set to a generated uuid sequence.
    
    But there is no such rule for the code attribute, which should be used to
    give shot codes to individual shots.
    
    :param sequence: The :class:`~stalker.core.models.Sequence` that this shot
      blengs to.
    
    :type sequence: :class:`stalker.core.models.Sequence`
    
    :param assets: The list of :class:`~stalker.core.models.Asset`\ s used in
      this shot.
    
    :type assets: list of :class:`stalker.core.models.Asset` instances
    
    :param integer cut_in: The in frame number that this shot starts.
    
    :param integer cut_out: The out frame number taht this shot ends.
    
    :param integer cut_duration: The duration of this shot in frames.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        kwargs["name"] = kwargs["code"] # create the test for it
        super(Shot, self).__init__(**kwargs)






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
      type that this StatusList is designed for. It accepts entity_type names.
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
            target_type=Project.entit_type
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
            raise ValueError("statuses should be an instance of list")
        
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
            raise ValueError("target_entity_type can not be None")
        
        if str(target_entity_type_in)=="":
            raise ValueError("target_entity_type can not be empty string")
        
        return str(target_entity_type_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_status(self, status_in):
        """validates the given status_in
        """
        
        if not isinstance(status_in, Status):
            raise ValueError("all elements must be an instance of Status in "
                             "the given statuses list")
        
        return status_in
    
    
    
    #----------------------------------------------------------------------
    def statuses():
        
        def fget(self):
            return self._statuses
        
        def fset(self, statuses):
            self._statuses = self._validate_statuses(statuses)
        
        doc = """list of :class:`stalker.core.models.Status` objects,
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
class Structure(Entity):
    """A structure object is the place to hold data about how the physical
    files are arranged in the
    :class:`stalker.core.models.Repository`.
    
    :param project_template: it is a string holding several lines of text
      showing the folder structure of the project. Whenever a project is
      created, folders are created by looking at this folder template.
      
      The template string can have Jinja2 directives. These variables are given
      to the template engine:
      
        * *project*: holds the current
          :class:`stalker.core.models.Project`
          object using this structure, so you can use {{project.code}} or
          {{project.sequences}} kind of variables in the Jinja2 template
    
    :param asset_templates: holds :class:`stalker.core.models.TypeTemplate`
      objects with an :class:`stalker.core.models.AssetType` connected to its
      `type` attribute, which can help specifying templates based on the
      related :class:`stalker.core.models.AssetType` object.
      
      Testing a second paragraph addition.
    
    :param reference_templates: holds
      :class:`stalker.core.models.TypeTemplate` objects, which can help
      specifying templates based on the given
      :class:`stalker.core.models.LinkType` object
    
    This templates are used in creation of Project folder structure and also
    while interacting with the assets and references in the current
    :class:`stalker.core.models.Project`. You can create one project
    structure for `Commmercials` and another project structure for `Movies` and
    another one for `Print` projects etc. and can reuse them with new projects.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 project_template="",
                 asset_templates=[],
                 reference_templates=[], **kwargs):
        super(Structure, self).__init__(**kwargs)
        
        self._project_template = self._validate_project_template(project_template)
        self._asset_templates = self._validate_asset_templates(asset_templates)
        self._reference_templates = \
            self._validate_reference_templates(reference_templates)
    
    
    
    #----------------------------------------------------------------------
    def _validate_asset_templates(self, asset_templates_in):
        """validates the given asset_templates list
        """
        
        if not isinstance(asset_templates_in, list):
            raise ValueError("asset_templates should be a list object")
        
        for element in asset_templates_in:
            if not isinstance(element, TypeTemplate):
                raise ValueError(
                    "asset_templates should only contain instances of "
                    "stalker.core.models.TypeTemplate objects"
                )
        
        return ValidatedList(asset_templates_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_reference_templates(self, reference_templates_in):
        """validates the given reference_templates list
        """
        
        if not isinstance(reference_templates_in, list):
            raise ValueError("reference_templates should be a list object")
        
        for element in reference_templates_in:
            if not isinstance(element, TypeTemplate):
                raise ValueError(
                    "reference_templates should only contain instances of "
                    "stalker.core.models.TypeTemplate objects"
                )
        
        return ValidatedList(reference_templates_in)
    
    
    
    #----------------------------------------------------------------------
    def _validate_project_template(self, project_template_in):
        """validates the given project_template object
        """
        
        if not isinstance(project_template_in, (str, unicode)):
            raise ValueError(
                "project_template should be an instance of string or unicode"
            )
        
        return project_template_in
    
    
    
    #----------------------------------------------------------------------
    def asset_templates():
        
        def fget(self):
            return self._asset_templates
        
        def fset(self, asset_templates_in):
            self._asset_templates = \
                self._validate_asset_templates(asset_templates_in)
        
        doc = """A list of :class:`stalker.core.models.TypeTemplate` objects
        which gives information about the :class:`stalker.core.models.Asset`
        :class:`stalker.core.models.Version` file placements"""
        
        return locals()
    
    asset_templates = property(**asset_templates())
    
    
    
    #----------------------------------------------------------------------
    def reference_templates():
        
        def fget(self):
            return self._reference_templates
        
        def fset(self, reference_templates_in):
            self._reference_templates = \
                self._validate_reference_templates(reference_templates_in)
        
        doc = """A list of :class:`stalker.core.models.TypeTemplate` objects
        which gives information about the placement of references to
        entities"""
        
        return locals()
    
    reference_templates = property(**reference_templates())
    
    
    
    #----------------------------------------------------------------------
    def project_template():
        
        def fget(self):
            return self._project_template
        
        def fset(self, project_template_in):
            self._project_template = \
                self._validate_project_template(project_template_in)
        
        doc= """A string which shows the folder structure of the current
        project. It can have Jinja2 directives. See the documentation of
        :class:`stalker.core.models.Structure` object for more information"""
        
        return locals()
    
    project_template = property(**project_template())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Structure, self).__eq__(other) and \
               isinstance(other, Structure) and \
               self.project_template == other.project_template and \
               self.reference_templates == other.reference_templates and \
               self.asset_templates == other.asset_templates






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
class Task(Entity, StatusMixin, ScheduleMixin):
    """Manages Task related data.
    
    WARNING: (obviously) not implemented yet!
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)






########################################################################
class AssetType(TypeEntity):
    """Holds the information about the asset types.
    
    One AssetType object gives information about the
    :class:`~stalker.core.models.TaskType`\ s that this type of asset
    can intially have.
    
    So for example one can create a "Character"
    :class:`~stalker.core.models.AssetType` and then link "Design", "Modeling",
    "Rig", "Shading" :class:`stalker.core.model.TaskType`\ s to this
    :class:`~stalker.core.models.AssetType`. And then have an "Environment"
    :class:`~stalker.core.models.AssetType` and then just link "Design",
    "Modeling", "Shading" :class:`stalker.core.model.TaskType`\ s to it.
    
    The idea behind :class:`~stalker.core.models.AssetType` is to have an
    initial list of :class:`~stalker.core.mddels.TaskType`\ s instances which
    are going to be used to define the automatically created
    :class:`~stalker.core.models.Task`\ s for this
    :class:`~stalker.core.models.AssetType`.
    
    It is still possible to add a new type of
    :class:`~stalker.core.models.Task` to the list of tasks of one
    :class:`~stalker.core.models.Asset` object. The
    :class:`~stalker.core.models.AssetType` and the related
    :class:`~stalker.core.models.TaskType`\ s will only be used to create a
    list of :class:`~stalker.core.models.Task`\ s intially with the
    :class:`~stalker.core.models.AssetBase` (thus for the inherited classes
    like :class:`~stalker.core.models.Asset` and
    :class:`~stalker.core.models.Shot`) it self.
    
    :param task_types: A list of :class:`~stalker.core.models.TaskType`
      instances showing the initial :class:`~stalker.core.models.TaskType`\ s
      available for this :class:`~stalker.core.models.AssetType`.
    
    :type task_types: a :class:`stalker.ext.validatedList.ValidatedList` of
      :class:`stalker.core.models.TaskType` instances.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, task_types=[], **kwargs):
        super(AssetType, self).__init__(**kwargs)
        
        self._task_types = self._validate_task_types(task_types)
    
    
    
    #----------------------------------------------------------------------
    def _validate_task_types(self, task_types_in):
        """validates the given task_types list
        """
        
        # raise a Value error if it is not a list
        if not isinstance(task_types_in, list):
            raise ValueError("task_types should be an instance of list")
        
        # raise a Value error if not all of the elements are pipelineStep
        # objects
        if not all([ isinstance(obj, TaskType)
                 for obj in task_types_in]):
            raise ValueError(
                "all of the elements of the given list should be instance of "
                "stalker.core.models.TaskType class"
            )
        
        return ValidatedList(task_types_in)
    
    
    
    #----------------------------------------------------------------------
    def task_types():
        
        def fget(self):
            return self._task_types
        
        def fset(self, task_types_in):
            self._task_types = self._validate_task_types(task_types_in)
        
        doc = """task_types of this AssetType object.
        
        task_types is a list of :class:`stalker.core.models.TaskType` objects,
        showing the list of possible :class:`~stalker.core.models.TaskType`\ s
        that this kind of :class:`~stalker.core.models.Asset`\ s can have. Its
        main use is to create a default :class:`~stalker.core.models.Task`\ s
        list which can be later on edited.
        """
        
        return locals()
    
    task_types = property(**task_types())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(AssetType, self).__eq__(other) and \
               isinstance(other, AssetType) and \
               self.task_types == other.task_types






########################################################################
class LinkType(TypeEntity):
    """Defines the types of :class:`~stalker.core.models.Link` instances.
    
    LinkType objects hold the type of the link and it is generaly used by
    :class:`stalker.core.models.Project` to sort things out. See
    :class:`stalker.core.models.Project` object documentation for details.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(LinkType, self).__init__(**kwargs)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(LinkType, self).__eq__(other) and \
               isinstance(other, LinkType)






########################################################################
class ProjectType(TypeEntity):
    """Defines the types of :class:`~stalker.core.models.Project` instances.
    
    Can be used to create different type projects like Commercial, Movie, Still
    etc.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(ProjectType, self).__init__(**kwargs)
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(ProjectType, self).__eq__(other) and \
               isinstance(other, ProjectType)
        







########################################################################
class TypeTemplate(Entity):
    """The TypeTemplate model holds templates for Types.
    
    TypeTemplate objects help to specify where to place a file related to
    :class:`stalker.core.models.TypeEntity` objects and its derived
    classes.
    
    The first very important usage of TypeTemplates is to place asset
    :class:`stalker.core.models.Version`'s to proper places inside a
    :class:`stalker.core.models.Project`'s
    :class:`stalker.core.models.Structure`.
    
    :param path_code: The Jinja2 template code which specifies the path of the
      given item. It is relative to the project root which is in general
      {{repository.path}}/{{project.code}}/
    
    :param file_code: The Jinja2 template code which specifies the file name of
      the given item
    
    :param type\_: A :class:`stalker.core.models.TypeEntity` object
      or any other class which is derived from TypeEntity.
    
    Examples:
    
    A template for asset versions can have this parameters::
    
      from stalker import db
      from stalker.ext import auth
      from stalker.core.models import AssetTypes, TypeTemplate, PipelineStep
      
      # setup the default database
      db.setup()
      
      # store the query method for ease of use
      session = db.session
      query = db.session.query
      
      # login to the system as admin
      admin = auth.login("admin", "admin")
      
      # create a couple of variables
      path_code = "ASSETS/{{asset_type.name}}/{{task_type.code}}"
      
      file_code = "{{asset.name}}_{{take.name}}_{{asset_type.name}}_\
v{{version.version_number}}"
      
      # create a pipeline step object
      modelingStep = PipelineStep(
          name="Modeling",
          code="MODEL",
          description="The modeling step of the asset",
          created_by=admin
      )
      
      # create a "Character" AssetType with only one step
      typeObj = AssetType(
          name="Character",
          description="this is the character asset type",
          created_by=admin,
          task_types=[modelingStep]
      )
      
      # now create our TypeTemplate
      char_template = TypeTemplate(
          name="Character",
          description="this is the template which explains how to place \
Character assets",
          path_code=path_code,
          file_code=file_code,
          type=typeObj,
      )
      
      # assign this type template to the structure of the project with id=101
      myProject = query(Project).filter_by(id=101).first()
      
      # append the type template to the structures' asset templates
      myProject.structure.asset_templates.append(char_template)
      
      session.commit()
    
    Now with the code above, whenever a new
    :class:`stalker.core.models.Version` created for a **Character**
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
    
    And one of the good side is you can create a version from Linux, Windows or
    OSX all the paths will be correctly handled by Stalker.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 path_code="",
                 file_code="",
                 type=None,
                 **kwargs):
        super(TypeTemplate, self).__init__(**kwargs)
        
        self._path_code = self._validate_path_code(path_code)
        self._file_code = self._validate_file_code(file_code)
        self._type = self._validate_type(type)
    
    
    
    #----------------------------------------------------------------------
    def _validate_path_code(self, path_code_in):
        """validates the given path_code attribute for several conditions
        """
        
        # check if it is None
        if path_code_in is None:
            raise ValueError("path_code could not be None")
        
        # check if it is an instance of string or unicode
        if not isinstance(path_code_in, (str, unicode)):
            raise ValueError("path_code should be an instance of string "
                             "or unicode")
        
        # check if it is an empty string
        if path_code_in == "":
            raise ValueError("path_code could not be an empty string")
        
        return path_code_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_file_code(self, file_code_in):
        """validates the given file_code attribute for several conditions
        """
        
        # check if it is None
        if file_code_in is None:
            raise ValueError("file_code could not be None")
        
        # check if it is an instance of string or unicode
        if not isinstance(file_code_in, (str, unicode)):
            raise ValueError("file_code should be an instance of string "
                             "or unicode")
        
        # check if it is an empty string
        if file_code_in == "":
            raise ValueError("file_code could not be an empty string")
        
        return file_code_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_type(self, type_in):
        """validates the given type attribute for several conditions
        """
        
        # check if it is None
        if type_in is None:
            raise ValueError("type could not be None")
        
        if not isinstance(type_in, TypeEntity):
            raise ValueError("type should be an instance of "
                             "stalker.core.models.TypeEntity")
        
        return type_in
    
    
    
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
    def type():
        
        def fget(self):
            return self._type
        
        def fset(self, type_in):
            self._type = self._validate_type(type_in)
        
        doc = """the target type this template should work on, should be an
        instance of :class:`stalker.core.models.TypeEntity`"""
        
        return locals()
    
    type = property(**type())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """checks the equality of the given object to this one
        """
        #print "running the TypeTemplate.__eq__"
        
        #print super(TypeTemplate, self).__eq__(other)
        #print isinstance(other, TypeTemplate)
        #print self.path_code == other.path_code
        #print self.file_code == other.file_code
        #print self.type == other.type
        
        
        return super(TypeTemplate, self).__eq__(other) and \
               isinstance(other, TypeTemplate) and \
               self.path_code == other.path_code and \
               self.file_code == other.file_code and \
               self.type == other.type





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
       other.
    
     * The :attr:`~stalker.core.models.User.name` is a synonym of the
       :attr:`~stalker.core.models.User.login_name`, so changing one of them
       will change the other.
    
    :param email: holds the e-mail of the user, should be in [part1]@[part2]
      format
    
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
    
    :param first_name: it is the first name of the user, must be a string or
      unicode, middle name also can be added here, so it accepts white-spaces
      in the variable, but it will truncate the white spaces at the beginin and
      at the end of the variable and it can not be empty or None
    
    :param last_name: it is the last name of the user, must be a string or
      unicode, again it can not contain any white spaces at the beggining and
      at the end of the variable and it can be an empty string or None
    
    :param department: it is the department of the current user. It should be
      a Department object. One user can only be listed in one department. A
      user is allowed to have no department to make it easy to create a new
      user and create the department and assign the user it later.
    
    :param password: it is the password of the user, can contain any character.
      Stalker doesn't store the raw passwords of the users. To check a stored
      password with a raw password use
      :meth:`~stalker.core.models.User.check_password` and to set the password
      you can use the :attr:`~stalker.core.models.User.password` property
      directly.
    
    :param permission_groups: it is a list of permission groups that this user
      is belong to
    
    :param tasks: it is a list of Task objects which holds the tasks that this
      user has been assigned to
    
    :param projects: it is a list of Project objects which holds the projects
      that this user is a part of
    
    :param projects_lead: it is a list of Project objects that this user
      is the leader of, it is for back refefrencing purposes
    
    :param sequences_lead: it is a list of Sequence objects that this
      user is the leader of, it is for back referencing purposes
    
    :param last_login: it is a datetime.datetime object holds the last login
      date of the user (not implemented yet)
    
    :param initials: it is the initials of the users name, if nothing given it
      will be calculated from the first and last names of the user
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 department=None,
                 email="",
                 first_name="",
                 last_name="",
                 login_name="",
                 password="",
                 permission_groups=[],
                 projects=[],
                 projects_lead=[],
                 sequences_lead=[],
                 tasks=[],
                 last_login=None,
                 initials="",
                 **kwargs
                 ):
        
        # use the login_name for name if there are no name attribute present
        name = kwargs.get("name")
        
        if login_name is not None and login_name != "":
            name = login_name
        else:
            login_name = name
        
        kwargs["name"] = name
        
        super(User, self).__init__(**kwargs)
        
        self._department = self._validate_department(department)
        self._email = self._validate_email(email)
        self._first_name = self._validate_first_name(first_name)
        self._last_name = self._validate_last_name(last_name)
        self._login_name = self._validate_login_name(login_name)
        self._initials = self._validate_initials(initials)
        
        # to be able to mangle the password do it like this
        self._password = None
        self.password = password
        
        self._permission_groups = \
            self._validate_permission_groups(permission_groups)
        self._projects = self._validate_projects(projects)
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
        
        ## check if department_in is None
        #if department_in is None:
            #raise ValueError("department could not be None")
        
        # check if it is intance of Department object
        if department_in is not None:
            if not isinstance(department_in, Department):
                raise ValueError("department should be instance of "
                                 "stalker.core.models.Department")
        
        return department_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_email(self, email_in):
        """validates the given email value
        """
        
        # check if email_in is an instance of string or unicode
        if not isinstance(email_in, (str, unicode)):
            raise ValueError("email should be an instance of string or "
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
            raise ValueError("first_name cannot be none")
        
        if not isinstance(first_name_in, (str, unicode)):
            raise ValueError("first_name should be instance of string or "
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
            raise ValueError("last_login should be an instance of "
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
                raise ValueError("last_name should be instance of string or "
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
            raise ValueError("login name could not be None")
        
        #if not isinstance(login_name_in, (str, unicode)):
            #raise ValueError("login_name should be instance of string or "
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
            raise ValueError("password cannot be None")
        
        return password_in
    
    
    
    #----------------------------------------------------------------------
    def _validate_permission_groups(self, permission_groups_in):
        """check the given permission_group
        """
        
        if permission_groups_in is None:
            raise ValueError("permission_groups attribute can not be None")
        
        if not isinstance(permission_groups_in, list):
            raise ValueError("permission_groups should be a list of group "
                             "objects")
        
        for permission_group in permission_groups_in:
            if not isinstance(permission_group, Group):
                raise ValueError("any group in permission_groups should be an "
                                 "instance of stalker.core.models.Group")
        
        #if len(permission_groups_in) == 0:
            #raise ValueError("users should be assigned at least to one "
            #                 "permission_group")
        
        return ValidatedList(permission_groups_in, Group)
    
    
    
    #----------------------------------------------------------------------
    def _validate_projects(self, projects_in):
        """validates the given projects attribute
        """
        
        # projects can not be None
        if projects_in is None:
            raise ValueError("projects can not be None")
        
        if not isinstance(projects_in, list):
            raise ValueError("projects should be a list of "
                             "stalker.core.models.Project objects")
        
        for a_project in projects_in:
            if not isinstance(a_project, Project):
                raise ValueError(
                    "any element in projects should be an instance of "
                    "stalker.core.models.Project"
                )
        
        return ValidatedList(projects_in, Project)
        
    
    
    #----------------------------------------------------------------------
    def _validate_projects_lead(self, projects_lead_in):
        """validates the given projects_lead attribute
        """
        
        if projects_lead_in is None:
            raise ValueError("projects_lead attribute could not be None, try "
                             "setting it to an empty list")
        
        if not isinstance(projects_lead_in, list):
            raise ValueError("projects_lead should be a list of "
                             "stalker.core.models.Project objects")
        
        for a_project in projects_lead_in:
            if not isinstance(a_project, Project):
                raise ValueError(
                    "any element in projects_lead should be an instance of "
                    "stalker.core.models.Project class")
        
        return ValidatedList(projects_lead_in, Project)
    
    
    
    #----------------------------------------------------------------------
    def _validate_sequences_lead(self, sequences_lead_in):
        """validates the given sequences_lead attribute
        """
        
        if sequences_lead_in is None:
            raise ValueError("sequences_lead attribute could not be None, try "
                             "setting it to an empty list")
        
        if not isinstance(sequences_lead_in, list):
            raise ValueError("sequences_lead should be a list of "
                             "stalker.core.models.Sequence objects")
        
        for a_sequence in sequences_lead_in:
            if not isinstance(a_sequence, Sequence):
                raise ValueError(
                    "any element in sequences_lead should be an instance of "
                    "stalker.core.models.Sequence class"
                )
        
        return ValidatedList(sequences_lead_in, Sequence)
    
    
    
    #----------------------------------------------------------------------
    def _validate_tasks(self, tasks_in):
        """validates the given taks attribute
        """
        
        if tasks_in is None:
            raise ValueError("tasks attribute could not be None, try setting "
                             "it to an empty list")
        
        if not isinstance(tasks_in, list):
            raise ValueError("tasks should be a list of "
                             "stalker.core.models.Task objects")
        
        for a_task in tasks_in:
            if not isinstance(a_task, Task):
                raise ValueError(
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
        :class:`stalker.core.models.Department` object"""
        
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
            self.code = self._nice_name.upper()
        
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
        :class:`stalker.core.models.Group` object"""
        
        return locals()
    
    permission_groups = property(**permission_groups())
    
    
    
    #----------------------------------------------------------------------
    def projects():
        
        def fget(self):
            return self._projects
        
        def fset(self, projects_in):
            self._projects = self._validate_projects(projects_in)
        
        doc = """projects those the current user assigned to, accepts
        :class:`stalker.core.models.Project` object"""
        
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
        :class:`stalker.core.models.Project` object"""
        
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
        :class:`stalker.core.models.Sequence` objects"""
        
        return locals()
    
    sequences_lead = property(**sequences_lead())
    
    
    
    #----------------------------------------------------------------------
    def tasks():
        
        def fget(self):
            return self._tasks
        
        def fset(self, tasks_in):
            self._tasks = self._validate_tasks(tasks_in)
        
        doc = """tasks assigned to the current user, accepts
        :class:`stalker.core.models.Task` objects"""
        
        return locals()
    
    tasks = property(**tasks())






########################################################################
class Version(Entity, StatusMixin):
    """The Version class is the connection of Assets to versions of that asset.
    So it connects the Assets to file system, and manages the files as
    versions.
    """
    
    
    
    pass
