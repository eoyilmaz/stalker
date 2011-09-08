#-*- coding: utf-8 -*-

import re
import datetime
import platform
import uuid

from sqlalchemy import orm
from sqlalchemy.orm import relationship, synonym, validates
from sqlalchemy import (
    Table,
    Column,
    Boolean,
    Integer,
    Float,
    String,
    ForeignKey,
    Date,
    DateTime,
    Interval,
    UniqueConstraint
)
from sqlalchemy.ext.declarative import (declarative_base, synonym_for,
                                        declared_attr)

import stalker
from stalker.core.errors import CircularDependencyError
from stalker.conf import defaults



Base = declarative_base()








########################################################################
class EntityMeta(type):
    """The metaclass for the very basic entity.
    
    Just adds the name of the class as the entity_type class attribute and
    creates an attribute called plural_name to hold the auto generated plural
    form of the class name. These two attributes can be overriden in the
    class itself.
    """
    
    
    #----------------------------------------------------------------------
    def __new__(mcs, classname, bases, dict_):
        
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
        
        return super(EntityMeta, mcs).__new__(mcs, classname, bases, dict_)











########################################################################
class SimpleEntity(Base):
    """The base class of all the others
    
    The :class:`~stalker.core.models.SimpleEntity` is the starting point of the
    Stalker Object Model, it starts by adding the basic information about an
    entity which are :attr:`~stalker.core.models.SimpleEntity.name`,
    :attr:`~stalker.core.models.SimpleEntity.description`, the audit
    information like :attr:`~stalker.core.models.SimpleEntity.created_by`,
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
      
      * only alphanumerics and underscore is allowed \[a-zA-Z0-9\_\]
      
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
      contain any white space at the beginning and at the end of the string,
      giving an object the object will be converted to string and then the
      resulting string will be conditioned.
    
    :param str description: A string or unicode attribute that holds the
      description of this entity object, it could be an empty string, and it
      could not again have white spaces at the beginning and at the end of the
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
      created entities this is equal to date_created and the date_updated
      cannot point a date which is before date_created.
    
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
    
    
    
    __strictly_typed__ = False
    
    __tablename__ = "SimpleEntities"
    id = Column("id", Integer, primary_key=True)
    
    entity_type = Column("db_entity_type", String(128), nullable=False)
    __mapper_args__ = {
        "polymorphic_on": entity_type,
        "polymorphic_identity": "SimpleEntity",
    }
    
    code = Column(String(256), nullable=False,
                  doc="""The code name of this object.
        
        It accepts string or unicode values and any other kind of objects will
        be converted to string. In any update to the name attribute the code
        also will be updated. If the code is not initialized or given as None,
        it will be set to the uppercase version of the nice_name attribute.
        Setting the code attribute to None will reset it to the default value.
        The default value is the upper case form of the nice_name.""")
    
    name = Column(
        String(256),
        nullable=False,
        doc="""Name of this object"""
    )
    
    description = Column(
        "description",
        String,
        doc="""Description of this object."""
    )
    
    created_by_id = Column(
        "created_by_id",
        Integer,
        ForeignKey("Users.id", use_alter=True, name="x")
    )
    
    created_by = relationship(
        "User",
        backref="entities_created",
        primaryjoin="SimpleEntity.created_by_id==User.user_id",
        post_update=True,
        doc="""The :class:`~stalker.core.models.User` who has created this object.""",
    )
    
    updated_by_id = Column(
        "updated_by_id",
        Integer,
        ForeignKey("Users.id", use_alter=True, name="x")
    )
    
    updated_by = relationship(
        "User",
        backref="entities_updated",
        primaryjoin="SimpleEntity.updated_by_id==User.user_id",
        post_update=True,
        doc="""The :class:`~stalker.core.models.User` who has updated this object.""",
    )
    
    date_created = Column(
        DateTime,
        default=datetime.datetime.now(),
        doc="""A :class:`datetime.datetime` instance showing the creation date and time of this object.""",
    )
    
    date_updated = Column(
        DateTime,
        default=datetime.datetime.now(),
        doc="""A :class:`datetime.datetime` instance showing the update date and time of this object.""",
    )
    
    type_id = Column(
        "type_id",
        Integer,
        ForeignKey("Types.id", use_alter=True, name="y")
    )
    
    type = relationship(
        "Type",
        primaryjoin="SimpleEntity.type_id==Type.type_id_local",
        doc="""The type of the object.
        
        It is an instance of :class:`~stalker.core.models.Type` with a proper
        :attr:`~stalker.core.models.Type.target_entity_type`.
        """
    )
    
    #UniqueConstraint("name", "db_entity_type")
    __stalker_version__ = Column("stalker_version", String(256))
    
    
    
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
                 ): # pylint: disable=W0613
        
        # name and nice_name
        self._nice_name = ""
        
        # check the name
        if name is None or name == "":
            if code is None:
                code = ""
            name = code
        
        self.name = name
        
        # code
        # if the given code argument is not None
        # use it to set the code
        if code is not None and code is not "":
            #self._code = self._validate_code(code)
            self.code = code
        else:
            self.code = name
        
        self.description = description
        self.created_by = created_by
        self.updated_by = updated_by
        date_created = date_created
        date_updated = date_updated
        self.date_created = date_created
        self.date_updated = date_updated
        self.type = type
        self.__stalker_version__ = stalker.__version__

    
    
    
    #----------------------------------------------------------------------
    @orm.reconstructor
    def __init_on_load__(self):
        """initialized the instance variables when the instance created with
        SQLAlchemy
        """
        self._nice_name = None
    
    
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """the representation of the SimpleEntity
        """
        
        return "<%s (%s, %s)>" % (self.entity_type, self.name, self.code)
    
    
    
    #----------------------------------------------------------------------
    @validates("description")
    def _validate_description(self, key, description_in):
        """validates the given description_in value
        """
        
        if description_in is None:
            description_in = ""
        
        return str(description_in)
    
    
    
    #----------------------------------------------------------------------
    @validates("name")
    def _validate_name(self, key, name):
        """validates the given name_in value
        """
        
        # it is None
        if name is None:
            raise TypeError("the name couldn't be set to None")
        
        name = self._condition_name(str(name))
        
        # it is empty
        if name == "":
            raise ValueError("the name couldn't be an empty string")
        
        # also set the nice_name
        self._nice_name = self._condition_nice_name(name)
        
        ## set the code
        #self.code = name_in
        
        return name
    
    
    
    #----------------------------------------------------------------------
    def _condition_code(self, code_in):
        """formats the given code_in value
        """
        
        # just set it to the uppercase of what nice_name gives
        # remove unnecesary characters from the string
        code_in = self._condition_name(str(code_in))
        
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
        
        # remove unnecesary characters from the string
        nice_name_in = self._condition_name(str(nice_name_in))
        
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
    @property
    def nice_name(self):
        """Nice name of this object.
        
        It has the same value with the name (contextually) but with a different
        format like, all the white spaces replaced by underscores ("\_"), all
        the CamelCase form will be expanded by underscore (\_) characters and
        it is always lower case.
        
        There is also the ``code`` attribute which is simply the upper case
        form of ``nice_name`` if it is not defined differently (i.e set to
        another value)."""
        
        # also set the nice_name
        if self._nice_name is None or self._nice_name == "":
            self._nice_name = self._condition_nice_name(self.name)
        
        return self._nice_name
    
    
    
    #----------------------------------------------------------------------
    @validates("code")
    def _validate_code(self, key, code_in):
        """validates the given code value
        """
        
        # check if the code_in is None or empty string
        if code_in is None or code_in == "":
            # restore the value from nice_name and let it be reformatted
            #code_in = self.nice_name.upper()
            code_in = self.nice_name
        
        return self._condition_code(str(code_in))
    
    
    
    #----------------------------------------------------------------------
    @validates("created_by")
    def _validate_created_by(self, key, created_by_in):
        """validates the given created_by_in attribute
        """
        
        if created_by_in is not None:
            if not isinstance(created_by_in, User):
                raise TypeError("the created_by attribute should be an "
                                 "instance of stalker.core.models.User")
        
        return created_by_in
    
    
    
    #----------------------------------------------------------------------
    @validates("updated_by")
    def _validate_updated_by(self, key, updated_by_in):
        """validates the given updated_by_in attribute
        """
        
        if updated_by_in is None:
            # set it to what created_by attribute has
            updated_by_in = self.created_by
        
        if updated_by_in is not None:
            if not isinstance(updated_by_in, User):
                raise TypeError("the updated_by attribute should be an "
                                 "instance of stalker.core.models.User")
        
        return updated_by_in
    
    
    
    #----------------------------------------------------------------------
    @validates("date_created")
    def _validate_date_created(self, key, date_created_in):
        """validates the given date_creaetd_in
        """
        
        if date_created_in is None:
            raise TypeError("the date_created could not be None")
        
        if not isinstance(date_created_in, datetime.datetime):
            raise TypeError("the date_created should be an instance of "
                             "datetime.datetime")
        
        return date_created_in
    
    
    
    #----------------------------------------------------------------------
    @validates("date_updated")
    def _validate_date_updated(self, key, date_updated_in):
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
    @validates("type")
    def _validate_type(self, key, type_in):
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
    
    
    
    __tablename__ = "Entities"
    __mapper_args__ = {"polymorphic_identity": "Entity"}
    entity_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                       primary_key=True)
    
    tags = relationship(
        "Tag",
        secondary="Entity_Tags",
        backref="entities",
        doc="""A list of tags attached to this object.
        
        It is a list of :class:`~stalker.core.models.Tag` instances which shows
        the tags of this object"""
    )
    
    notes = relationship(
        "Note",
        primaryjoin="Entities.c.id==Notes.c.entity_id",
        backref="entity",
        doc="""All the :class:`~stalker.core.models.Notes`\ s attached to this entity.
        
        It is a list of :class:`~stalker.core.models.Note` instances or an
        empty list, setting it None will raise a TypeError.
        """
    )
    
    reviews = relationship(
        "Review",
        primaryjoin="Entities.c.id==Reviews.c.to_id",
        back_populates="to",
        doc="""All the :class:`~stalker.core.models.Review`\ s about this Entity.
        
        It is a list of :class:`~stalker.core.models.Review` instances or an
        empty list, setting it None will raise a TypeError.
        """
    )
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 tags=None,
                 notes=None,
                 **kwargs
                 ):
        
        super(Entity, self).__init__(**kwargs)
        
        if tags is None:
            tags = []
        
        if notes is None:
            notes = []
        
        self.tags = tags
        self.notes = notes
    
    
    
    #----------------------------------------------------------------------
    @orm.reconstructor
    def __init_on_load__(self):
        """initialized the instance variables when the instance created with
        SQLAlchemy
        """
        
        super(Entity, self).__init_on_load__()
    
    
    
    #----------------------------------------------------------------------
    @validates("notes")
    def _validate_notes(self, key, note):
        """validates the given note value
        """
        
        if not isinstance(note, Note):
            raise TypeError("note should be an instance of "
                            "stalker.core.models.Note")
        
        return note
    
    
    
    #----------------------------------------------------------------------
    @validates("tags")
    def _validate_tags(self, key, tag):
        """validates the given tag
        """
        
        if not isinstance(tag, Tag):
            raise TypeError("tag should be an instance of "
                            "stalker.core.models.Tag")
        
        return tag
    
    
    
    #----------------------------------------------------------------------
    @validates("reviews")
    def _validate_reviews(self, key, review):
        """validates the given review value
        """
        if not isinstance(review, Review):
            raise TypeError("The reviews should be a list of "
                            "stalker.core.models.Review instances")
        
        return review
    
    
    
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
    
    __tablename__ = "Types"
    __mapper_args__ = {"polymorphic_identity": "Type"}
    type_id_local = Column("id", Integer, ForeignKey("Entities.id"),
                           primary_key=True)
    _target_entity_type = Column(
        "target_entity_type",
        String
    )
    
    
    
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
    @synonym_for("_target_entity_type")
    @property
    def target_entity_type(self):
        """The target type of this Type instance.
        
        It is a string, showing the name of the target type class. It is a
        read-only attribute.
        """
        
        return self._target_entity_type






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
    
    
    
    __tablename__ = "Statuses"
    __mapper_args__ = {"polymorphic_identity": "Status"}
    status_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    )
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(Status, self).__init__(**kwargs)
    
    
    
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
    
    Holds multiple :class:`~stalker.core.models.Status`es to be used as a
    choice list for several other classes.
    
    A StatusList can only be assigned to only one entity type. So a
    :class:`~stalker.core.models.Project` can only have a suitable StatusList
    object which is designed for :class:`~stalker.core.models.Project`
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
      
      The StatusList instance can be empty, means it may not have anything in
      its :attr:`~stalker.core.models.StatusList.statuses`. But it is useless.
      The validation for empty statuses list is left to the SOM user.
    """
    
    
    
    __tablename__ = "StatusLists"
    __mapper_args__ = {"polymorphic_identity": "StatusList"}
    
    statusList_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True
    )
    
    statuses = relationship(
        "Status",
        secondary="StatusList_Statuses",
        doc="""list of :class:`~stalker.core.models.Status` objects, showing the possible statuses"""
    )
    
    _target_entity_type = Column("target_entity_type", String(128),
                                 nullable=False, unique=True)
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 statuses=None,
                 target_entity_type="",
                 **kwargs
                 ):
        
        super(StatusList, self).__init__(**kwargs)
        
        self.statuses = statuses
        self._target_entity_type = \
            self._validate_target_entity_type(target_entity_type)
    
    
    
    #----------------------------------------------------------------------
    @validates("statuses")
    def _validate_statuses(self, key, status):
        """validates the given status
        """
        
        if not isinstance(status, Status):
            raise TypeError("all elements must be an instance of "
                            "stalker.core.models.Status in the given statuses"
                            "list")
        
        return status
    
    
    
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
    @synonym_for("_target_entity_type") # we need it to make the property read
    @property                           # only
    def target_entity_type(self):
        """The entity type which this StatusList is valid for.
        
        Usally it is set to the TargetClass directly::
          
          from stalker.core.models import Status, StatusList, Asset
          
          # create a StatusList valid only for Asset class
          asset_status_list = StatusList(
              name="Asset Statuses",
              statuses = [
                  Status(name="Waiting To Start", code="WTS"),
                  Status(name="Work In Progress", code="WIP"),
                  Status(name="Complete", code="CMPLT")
              ],
              target_entity_type=Asset # or "Asset" is also valid
          )
        """
        return self._target_entity_type
    
    
    
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
            for item in self.statuses:
                if item == key:
                    return item
        else:
            return self.statuses[key]
    
    
    #----------------------------------------------------------------------
    def __setitem__(self, key, value):
        """the indexing attributes for setting item
        """
        
        self.statuses[key] = self._validate_status(value)
    
    
    
    #----------------------------------------------------------------------
    def __delitem__(self, key):
        """the indexing attributes for deleting item
        """
        
        del self.statuses[key]
    
    
    
    #----------------------------------------------------------------------
    def __len__(self):
        """the indexing attributes for getting the length
        """
        
        return len(self.statuses)






########################################################################
class ImageFormat(Entity):
    """Common image formats for the :class:`~stalker.core.models.Project`\ s.
    
    :param width: The width of the format, it cannot be zero or negative, if a
      float number is given it will be converted to integer
    
    :param height: The height of the format, it cannot be zero or negative, if
      a float number is given it will be converted to integer
    
    :param pixel_aspect: The pixel aspect ratio of the current ImageFormat
      object, it can not be zero or negative, and if given as an integer it
      will be converted to a float, the default value is 1.0
    
    :param print_resolution: The print resolution of the ImageFormat given as
      DPI (dot-per-inch). It can not be zero or negative
    """
    
    
    
    __tablename__ = "ImageFormats"
    __mapper_args__ = {"polymorphic_identity": "ImageFormat"}
    
    imageFormat_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    )
    
    width = Column(
        Integer,
        doc="""The width of this format.
        
        * the width should be set to a positif non-zero integer
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise an exception.
        """
    )
    
    height = Column(
        Integer,
        doc="""The height of this format
        
        * the height should be set to a positif non-zero integer
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise an exception.
        """
    )
    
    pixel_aspect = Column(
        Float,
        default="1.0",
        doc="""The pixel aspect ratio of this format.
        
        * the pixel_aspect should be set to a positif non-zero float
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise an exception
        """
    )
    
    print_resolution = Column(
        Float,
        default="300.0",
        doc="""The print resolution of this format
        
        * it should be set to a positif non-zero float or integer
        * integers are also accepted but will be converted to float
        * for improper inputs the object will raise an exception.
        """
    )
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 width=None,
                 height=None,
                 pixel_aspect=1.0,
                 print_resolution=300,
                 **kwargs
                 ):
        
        super(ImageFormat, self).__init__(**kwargs)
        
        self.width = width
        self.height = height
        self.pixel_aspect = pixel_aspect
        self.print_resolution = print_resolution
        self._device_aspect = 1.0
    
    
    
    #----------------------------------------------------------------------
    @orm.reconstructor
    def __init_on_load__(self):
        """initialized the instance variables when the instance created with
        SQLAlchemy
        """
        
        self._device_aspect = None
        self._update_device_aspect()
        
        # call supers __init_on_load__
        super(ImageFormat, self).__init_on_load__()
    
    
    
    #----------------------------------------------------------------------
    @validates("width")
    def _validate_width(self, key, width):
        """validates the given width
        """
        
        if not isinstance(width, (int, float)):
            raise TypeError("width should be an instance of int or float")
        
        if width <= 0:
            raise ValueError("width shouldn't be zero or negative")
        
        return int(width)
    
    
    
    #----------------------------------------------------------------------
    @validates("height")
    def _validate_height(self, key, height):
        """validates the given height
        """
        
        if not isinstance(height, (int, float)):
            raise TypeError("height should be an instance of int or float")
        
        if height <= 0:
            raise ValueError("height shouldn't be zero or negative")
        
        return int(height)
    
    
    
    #----------------------------------------------------------------------
    @validates("pixel_aspect")
    def _validate_pixel_aspect(self, key, pixel_aspect):
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
    @validates("print_resolution")
    def _validate_print_resolution(self, key, print_resolution):
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
    @property
    def device_aspect(self):
        """returns the device aspect
        
        because the device_aspect is calculated from the width/height*pixel
        formula, this property is read-only.
        """
        
        return float(self.width) / float(self.height) * self.pixel_aspect
    
    
    
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
    
    Links are all about giving some external information to the current entity
    (external to the database, so it can be something on the
    :class:`~stalker.core.models.Repository` or in the Web). The type of the
    link (general, file, folder, webpage, image, image sequence, video, movie,
    sound, text etc.) can be defined by a :class:`~stalker.core.models.Type`
    instance (you can also use multiple :class:`~stalker.core.models.Tag`
    instances to add more information, and to filter them back). Again it is
    defined by the needs of the studio.
    
    For sequences of files the file name may contain "#" or muptiple of them
    like "###" to define pading.
    
    :param path: The Path to the link, it can be a path to a folder or a file
      in the file system, or a web page. For file sequences use "#" in place of
      the numerator (`Nuke`_ style). Setting the path to None or an empty
      string is not accepted.
    
    .. _Nuke: http://www.thefoundry.co.uk
    """
    
    
    
    __tablename__ = "Links"
    __mapper_args__ = {"polymorphic_identity": "Link"}
    link_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    )
    path = Column(
        String,
        doc="""The path of the url to the link.
        
        It can not be None or an empty string, it should be a string or
        unicode.
        """
    )
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, path="", **kwargs):
        super(Link, self).__init__(**kwargs)
        self.path = path
    
    
    
    #----------------------------------------------------------------------
    @validates("path")
    def _validate_path(self, key, path):
        """validates the given path
        """
        
        if path is None:
            raise TypeError("path can not be None")
        
        if not isinstance(path, (str, unicode)):
            raise TypeError("path should be an instance of string or unicode")
        
        if path == "":
            raise ValueError("path can not be an empty string")
        
        return self._format_path(path)
    
    
    
    #----------------------------------------------------------------------
    def _format_path(self, path):
        """formats the path to internal format, which is Linux forward slashes
        for path seperation
        """
        
        return path.replace("\\", "/")
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Link, self).__eq__(other) and \
               isinstance(other, Link) and \
               self.path == other.path and \
               self.type == other.type






########################################################################
class Booking(Entity):
    """Holds information about the time spend on a specific task by a specific user.
    """
    
    __tablename__ = "Bookings"
    __mapper_args__ = {"polymorphic_identity": "Booking"}
    booking_id = Column("id", Integer, ForeignKey("Entities.id"),
                        primary_key=True)
    task_id = Column(Integer, ForeignKey("Tasks.id"), nullable=False)
    task = relationship(
        "Task",
        primaryjoin="Bookings.c.task_id==Tasks.c.id",
        uselist=False,
        back_populates="bookings",
        doc="The :class:`~stalker.core.models.Task` instance that this booking is created for"
    )
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, task=None, **kwargs):
        super(Booking, self).__init__(**kwargs)
        
        self.task = task
    
    
    
    #----------------------------------------------------------------------
    @validates("task")
    def _validate_task(self, key, task):
        """validates the given task value
        """
        
        if not isinstance(task, Task):
            raise TypeError("Booking.task should be an instance of "
                            "stalker.core.models.Task")
        
        return task






########################################################################
class Review(Entity):
    """User reviews and comments about other entities.
    
    :param body: the body of the review, it is a string or unicode variable,
      it can be empty but it is then meaningless to have an empty review.
      Anything other than a string or unicode will raise a TypeError.
    
    :param to: The relation variable, that holds the connection that this
      review is related to. Any object which has a list-like attribute called
      "reviews" is accepted. Anything other will raise AttributeError.
    """
    
    
    
    __tablename__ = "Reviews"
    __mapper_args__ = {"polymorphic_identity": "Review"}
    review_id = Column("id", ForeignKey("SimpleEntities.id"),
                       primary_key=True)
    body = Column(
        String,
        doc="""The body (content) of this Review.
        """
    )
    
    to_id = Column(ForeignKey("Entities.id"))
    to = relationship(
        "Entity",
        primaryjoin="Reviews.c.to_id==Entities.c.id",
        back_populates="reviews",
        uselist=False,
        doc="""The owner object of this Review.
        """
    )
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, body="", to=None, **kwargs):
        super(Review, self).__init__(**kwargs)
        
        self.body = body
        self.to = to
    
    
    
    #----------------------------------------------------------------------
    @validates("body")
    def _validate_body(self, key, body):
        """validates the given body variable
        """
        
        # the body could be empty
        # but it should be an instance of string or unicode
        
        if not isinstance(body, (str, unicode)):
            raise TypeError("the body attribute should be an instance of "
                              "string or unicode")
        
        return body
    
    
    
    #----------------------------------------------------------------------
    @validates("to")
    def _validate_to(self, key, to):
        """validates the given to variable
        """
        
        if to is None:
            if not self.to is None:
                raise RuntimeError(
                    "The review can not be removed from the owner Entity "
                    "objects `reviews` attribute. If you want to remove the "
                    "Review instance, either delete it or assign it to a new "
                    "stalker.core.models.Entity instance"
                )
            else:
                raise TypeError(
                    "the object which is given with the `to` should be "
                    "inherited from stalker.core.models.Entity class"
                )
        
        if not isinstance(to, Entity):
            raise TypeError(
                "the object which is given with the `to` should be inherited "
                "from stalker.core.models.Entity class"
            )
        
        return to






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
    
    +-------------------+--------+--------+--------+------+
    |        0b         |   0    |   0    |   0    |  0   |
    +-------------------+--------+--------+--------+------+
    | binary identifier | Delete | Update | Create | Read |
    |                   | Bit    | Bit    | Bit    | Bit  |
    +-------------------+--------+--------+--------+------+
    
    :param dict permissions: A Python dictionary showing the permissions. The
      key is the name of the Class and the value is the permission bit.
    
    
    NOTE TO DEVELOPERS: a Dictionary-Based Collections should be used in
    SQLAlchemy.
    """
    
    __tablename__ = "PermissionGroups"
    __mapper_args__ = {"polymorphic_identity": "PermissionGroup"}
    
    permissionGroup_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                                primary_key=True)
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(PermissionGroup, self).__init__(**kwargs)






########################################################################
class Note(SimpleEntity):
    """Notes for any of the SOM objects.
    
    To leave notes in Stalker use the Note class.
    
    :param content: the content of the note
    
    :param attached_to: The object that this note is attached to.
    """
    
    
    __tablename__ = "Notes"
    __mapper_args__ = {"polymorphic_identity": "Note"}
    
    note_id = Column(
        "id",
        Integer,
        ForeignKey("SimpleEntities.id"),
        primary_key=True
    )
    
    entity_id = Column(
        "entity_id",
        Integer,
        ForeignKey("Entities.id")
    )
    
    content = Column(
        String,
        doc="""The content of this :class:`~stalker.core.models.Note` instance.
        
        Content is a string representing the content of this Note, can be given
        as an empty string or can be even None, but anything other than None or
        string or unicode will raise a TypeError.
        """
    )
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, content="", **kwargs):
        super(Note, self).__init__(**kwargs)
        self.content = content
    
    
    
    #----------------------------------------------------------------------
    @validates("content")
    def _validate_content(self, key, content_in):
        """validates the given content
        """
        
        if content_in is not None and \
           not isinstance(content_in, (str, unicode)):
            raise TypeError("content should be an instance of string or "
                             "unicode")
        
        return content_in
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Note, self).__eq__(other) and \
               isinstance(other, Note) and \
               self.content == other.content






########################################################################
class Tag(SimpleEntity):
    """Use it to create tags for any object available in SOM.
    
    Doesn't have any other attribute than what is inherited from
    :class:`~stalker.core.models.SimpleEntity`
    """
    
    
    
    __tablename__ = "Tags"
    __mapper_args__ = {"polymorphic_identity": "Tag"}
    tag_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                    primary_key=True)
    
    
    
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
class Repository(Entity):
    """Manages fileserver/repository related data.
    
    A repository is a network share that all users have access to.
    
    A studio can create several repositories, for example, one for movie
    projects and one for commercial projects.
    
    A repository also defines the default paths for linux, windows and mac
    fileshares.
    
    The path seperator in the repository is always forward slashes ("/").
    Setting a path that contains backward slashes ("\\"), will be converted to
    a path with forward slashes.
    
    :param linux_path: shows the linux path of the repository root, should be a
      string
    
    :param osx_path: shows the mac osx path of the repository root, should be a
      string
    
    :param windows_path: shows the windows path of the repository root, should
      be a string
    """
    
    __tablename__ = "Repositories"
    __mapper_args__ = {"polymorphic_identity": "Repository"}
    repository_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    )
    linux_path = Column(String(256))
    windows_path = Column(String(256))
    osx_path = Column(String(256))
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 linux_path="",
                 windows_path="",
                 osx_path="",
                 **kwargs):
        super(Repository, self).__init__(**kwargs)
        
        self.linux_path = linux_path
        self.windows_path = windows_path
        self.osx_path = osx_path
    
    
    
    #----------------------------------------------------------------------
    @validates("linux_path")
    def _validate_linux_path(self, key, linux_path_in):
        """validates the given linux path
        """
        
        if not isinstance(linux_path_in, (str, unicode)):
            raise TypeError("linux_path should be an instance of string or "
                             "unicode")
        
        return linux_path_in.replace("\\", "/")
    
    
    
    #----------------------------------------------------------------------
    @validates("osx_path")
    def _validate_osx_path(self, key, osx_path_in):
        """validates the given osx path
        """
        
        if not isinstance(osx_path_in, (str, unicode)):
            raise TypeError("osx_path should be an instance of string or "
                             "unicode")
        
        return osx_path_in.replace("\\", "/")
    
    
    
    #----------------------------------------------------------------------
    @validates("windows_path")
    def _validate_windows_path(self, key, windows_path_in):
        """validates the given windows path
        """
        
        if not isinstance(windows_path_in, (str, unicode)):
            raise TypeError("windows_path should be an instance of string or "
                             "unicode")
        
        return windows_path_in.replace("\\", "/")
    
    
    
    #----------------------------------------------------------------------
    @property
    def path(self):
        """The path for the current os"""
        
        # return the proper value according to the current os
        platform_system = platform.system()
        
        if platform_system == "Linux":
            return self.linux_path
        elif platform_system == "Windows":
            return self.windows_path
        elif platform_system == "Darwin":
            return self.osx_path
    
    
    
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
      ValueError will be raised when it is given as and empty string.
    
    :param str path_code: A `Jinja2`_ template code which specifies the path of
      the given item. It is relative to the project root. A typical example
      could be::
        
        asset_path_code = "ASSETS/{{asset.code}}/{{task.code}}/"
    
    :param str file_code: A `Jinja2`_ template code which specifies the file
      name of the given item. It is relative to the
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
    
    .. _Jinja2: http://jinja.pocoo.org/docs/
    """
    
    
    
    __tablename__ =  "FilenameTemplates"
    filenameTemplate_id = Column( "id", Integer,ForeignKey("Entities.id"),
                                  primary_key=True)
    _target_entity_type = Column("target_entity_type", String)
    path_code = Column(
        String,
        doc="""The templating code for the path of this FilenameTemplate."""
    )
    
    file_code = Column(
        String,
        doc="""The templating code for the file part of the FilenameTemplate."""
    )
    
    output_path_code = Column(
        String,
        doc="""The output_path_code of this FilenameTemplate object.
        
        Should be a unicode string. None and empty string is also accepted, but
        in this case the value is copied from the
        :attr:`~stalker.core.models.FilenameTemplate.path_code` if also the
        :attr:`~stalker.core.models.FilenameTemplate.output_is_relative` is
        False. If
        :attr:`~stalker.core.models.FilenameTemplate.output_is_relative` is
        True then it will left as an empty string.
        """
    )
    
    output_file_code = Column(
        String,
        doc="""The output_file_code of this FilenameTemplate object.
        
        Should be a unicode string. None and empty string is also accepted, but
        in this case the value is copied from the
        :attr:`~stalker.core.models.FilenameTemplate.file_code` if also the
        :attr:`~stalker.core.models.FilenameTemplate.output_is_relative` is
        False. If
        :attr:`~stalker.core.models.FilenameTemplate.output_is_relative` is
        True then it will left as an empty string.
        """
    )
    
    output_is_relative = Column(
        Boolean,
        doc="""Specifies if the output should be calculated relative to the path attribute.
        """
    )
    
    
    
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
        
        self._target_entity_type = \
            self._validate_target_entity_type(target_entity_type)
        self.path_code = path_code
        self.file_code = file_code
        self.output_is_relative = output_is_relative
        self.output_path_code = output_path_code
        self.output_file_code = output_file_code
    
    
    
    #----------------------------------------------------------------------
    @validates("path_code")
    def _validate_path_code(self, key, path_code_in):
        """validates the given path_code attribute for several conditions
        """
        
        # check if it is None
        if path_code_in is None:
            path_code_in = u""
        
        path_code_in = unicode(path_code_in)
        
        return path_code_in
    
    
    
    #----------------------------------------------------------------------
    @validates("file_code")
    def _validate_file_code(self, key, file_code_in):
        """validates the given file_code attribute for several conditions
        """
        
        # check if it is None
        if file_code_in is None:
            file_code_in = u""
        
        # convert it to unicode
        file_code_in = unicode(file_code_in)
        
        return file_code_in
    
    
    
    #----------------------------------------------------------------------
    @validates("output_path_code")
    def _validate_output_path_code(self, key, output_path_code_in):
        """validates the given output_path_code value
        """
        
        if output_path_code_in == None or output_path_code_in == "":
            if self.output_is_relative:
                output_path_code_in = ""
            else:
                output_path_code_in = self.path_code
        
        return output_path_code_in
    
    
    
    #----------------------------------------------------------------------
    @validates("output_file_code")
    def _validate_output_file_code(self, key, output_file_code_in):
        """validates the given output_file_code value
        """
        
        if output_file_code_in == None or output_file_code_in == "":
            if self.output_is_relative:
                output_file_code_in = ""
            else:
                output_file_code_in = self.file_code
        
        return output_file_code_in
    
    
    
    #----------------------------------------------------------------------
    @validates("output_is_relative")
    def _validate_output_is_relative(self, key, output_is_relative_in):
        """validates the given output_is_relative value
        """
        
        return bool(output_is_relative_in)
    
    
    
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
    @synonym_for("_target_entity_type")
    @property
    def target_entity_type(self):
        """The target entity type this FilenameTemplate object should work on.
        
        Should be a string value or the class itself
        """
        
        return self._target_entity_type
    
    
    
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
class Structure(Entity):
    """Holds data about how the physical files are arranged in the :class:`~stalker.core.models.Repository`.
    
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
    
    __tablename__ = "Structures"
    __mapper_args__ = {"polymorphic_identity": "Structure"}
    
    structure_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    )
    
    templates = relationship(
        "FilenameTemplate",
        secondary="Structure_FilenameTemplates"
    )
    
    custom_template = Column("custom_template", String)
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, templates=None, custom_template=None, **kwargs):
        super(Structure, self).__init__(**kwargs)
        
        if templates is None:
            templates = []
        
        self.templates = templates
        self.custom_template = custom_template
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Structure, self).__eq__(other) and \
               isinstance(other, Structure) and \
               self.templates == other.templates and \
               self.custom_template == other.custom_template
    
    
    
    #----------------------------------------------------------------------
    @validates("custom_template")
    def _validate_custom_template(self, key, custom_template_in):
        """validates the given custom_template value
        """
        
        return custom_template_in
    
    
    
    #----------------------------------------------------------------------
    @validates("templates")
    def _validate_templates(self, key, template_in):
        """validates the given template value
        """
        
        if not isinstance(template_in, FilenameTemplate):
            raise TypeError("all the elements in the templates should be a "
                            "list of stalker.core.models.FilenameTemplate "
                            "instances")
        
        return template_in






########################################################################
class Department(Entity):
    """The departments that forms the studio itself.
    
    The information that a Department object holds is like:
    
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
    
    
    
    __tablename__ = "Departments"
    __mapper_args__ = {"polymorphic_identity": "Department"}
    department_id = Column(
        "id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True
    )
    
    lead_id = Column(
        "lead_id",
        Integer,
        ForeignKey("Users.id", use_alter=True, name="x")
    )
    
    lead = relationship(
        "User",
        uselist=False,
        primaryjoin="Department.lead_id==User.user_id",
        post_update=True,
        doc="""The lead of this department, it is a User object""",
    )
    
    members = relationship(
        "User",
        #backref="department",
        primaryjoin= "Departments.c.id==Users.c.department_id",
        back_populates="department",
        doc="""List of users representing the members of this department.""",
    )
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, members=None, lead=None, **kwargs):
        super(Department, self).__init__(**kwargs)
        
        if members is None:
            members = []
        
        self.members = members
        self.lead = lead
    
    
    
    #----------------------------------------------------------------------
    @validates("members")
    def _validate_members(self, key, member):
        """validates the given member attribute
        """
        
        if not isinstance(member, User):
            raise TypeError("every element in the members list should be "
                            "an instance of stalker.core.models.User class")
        
        return member
    
    
    
    #----------------------------------------------------------------------
    @validates("lead")
    def _validate_lead(self, key, lead):
        """validates the given lead attribute
        """
        
        if lead is not None:
            # the lead should be an instance of User class
            if not isinstance(lead, User):
                raise TypeError("lead should be an instance of "
                                 "stalker.core.models.User")
        
        return lead
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Department, self).__eq__(other) and \
               isinstance(other, Department)






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
    
    
    __tablename__ = "Users"
    __mapper_args__ = {"polymorphic_identity": "User"}
    
    user_id = Column("id", Integer, ForeignKey("Entities.id"),
                     primary_key=True)
    
    department_id = Column(
        Integer,
        ForeignKey("Departments.id", use_alter=True, name="department_x"),
    )
    
    department = relationship(
        "Department",
        primaryjoin="Users.c.department_id==Departments.c.id",
        #primaryjoin="User.department_id==Department.department_id",
        #primaryjoin=department_id==Department.department_id,
        back_populates="members",
        uselist=False,
        doc=""":class:`~stalker.core.models.Department` of the user""",
    )
    
    email = Column(
        String(256),
        unique=True,
        nullable=False,
        doc="""email of the user, accepts strings or unicodes"""
    )
    
    first_name = Column(
        String(256),
        nullable=False,
        doc="""first name of the user, accepts string or unicode"""
    )
    
    last_name = Column(
        String(256),
        nullable=True,
        doc="""The last name of the user.
        
        It is a string and can be None or empty string"""
    )
    
    password = Column(
        String(256),
        nullable=False,
        doc="""The password of the user.
        
        It is scrambled before it is stored.
        """
    )
    
    last_login = Column(
        DateTime,
        doc="""The last login time of this user.
        
        It is an instance of datetime.datetime class."""
    )
    
    login_name = synonym(
        "name",
        doc="""The login name of the user.
        
        It is a synonym for the :attr:`~stalker.core.models.User.name`
        attribute.
        """
    )
    
    initials = Column(
        String(16),
        doc="""The initials of the user.
        
        If not spesified, it is the upper case form of first letters of the
        :attr:`~stalker.core.models.User.first_name` and
        :attr:`~stalker.core.models.User.last_name`"""
    )
    
    
    permission_groups = relationship(
        "PermissionGroup",
        secondary="User_PermissionGroups",
        doc="""Permission groups that this users is a member of.
        
        Accepts :class:`~stalker.core.models.PermissionGroup` object.
        """
    )
    
    projects_lead = relationship(
        "Project",
        primaryjoin="Projects.c.lead_id==Users.c.id",
        #uselist=True,
        back_populates="lead",
        doc=""":class:`~stalker.coer.models.Project`\ s lead by this user.
        
        It is a list of :class:`~stalker.core.models.Project` instances.
        """
    )
    
    sequences_lead = relationship(
        "Sequence",
        primaryjoin="Sequences.c.lead_id==Users.c.id",
        uselist=True,
        back_populates="lead",
        doc=""":class:`~stalker.core.models.Sequence`\ s lead by this user.
        
        It is a list of :class:`~stalker.core.models.Sequence` instances.
        """
    )
    
    tasks = relationship(
        "Task",
        secondary="Task_Resources",
        back_populates="resources",
        doc=""":class:`~stalker.core..models.Task`\ s assigned to this user.
        
        It is a list of :class:`~stalker.core.models.Task` instances.
        """
    )
    
    
    #----------------------------------------------------------------------
    def __init__(
        self,
        department=None,
        email="",
        first_name="",
        last_name="",
        login_name="",
        password="",
        permission_groups=None,
        projects_lead=None,
        sequences_lead=None,
        tasks=None,
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
        
        self.department = department
        
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.name = name
        self.login_name = login_name
        self.initials = initials
        
        # to be able to mangle the password do it like this
        self.password = password
        
        if permission_groups is None:
            permission_groups = []
        self.permission_groups = permission_groups
        
        self._projects = []
        
        if projects_lead is None:
            projects_lead = []
        self.projects_lead = projects_lead
        
        if sequences_lead is None:
            sequences_lead = []
        self.sequences_lead = sequences_lead
        
        if tasks is None:
            tasks = []
        
        self.tasks = tasks
        
        self.last_login = last_login
    
    
    
    #----------------------------------------------------------------------
    @orm.reconstructor
    def __init_on_load__(self):
        """initialized the instance variables when the instance created with
        SQLAlchemy
        """
        
        self._projects = []
        # call the Entity __init_on_load__
        super(User, self).__init_on_load__()
    
    
    
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
    @validates("name")
    def _validate_name(self, key, name):
        """validates the given name value
        """
        
        print "name in: ", name
        
        name = self._format_login_name(name)
        
        # also set the nice_name
        self._nice_name = self._condition_nice_name(name)
        
        # and also the code
        self.code = name
        
        print "name out: ", name
        
        return name
    
    
    
    #----------------------------------------------------------------------
    @validates("department")
    def _validate_department(self, key, department):
        """validates the given department value
        """
        
        # check if it is intance of Department object
        if department is not None:
            if not isinstance(department, Department):
                raise TypeError("department should be instance of "
                                 "stalker.core.models.Department")
        
        return department
    
    
    
    #----------------------------------------------------------------------
    @validates("email")
    def _validate_email(self, key, email_in):
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
    @validates("first_name")
    def _validate_first_name(self, key, first_name_in):
        """validates the given first_name attribute
        """
        
        if first_name_in is None:
            raise TypeError("first_name cannot be None")
        
        if not isinstance(first_name_in, (str, unicode)):
            raise TypeError("first_name should be instance of string or "
                             "unicode")
        
        if first_name_in == "":
            raise ValueError("first_name can not be an empty string")
        
        return first_name_in.strip().title()
    
    
    
    #----------------------------------------------------------------------
    @validates("initials")
    def _validate_initials(self, key, initials_in):
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
    @validates("last_login")
    def _validate_last_login(self, key, last_login_in):
        """validates the given last_login argument
        """
        
        if not isinstance(last_login_in, datetime.datetime) and \
           last_login_in is not None:
            raise TypeError("last_login should be an instance of "
                            "datetime.datetime or None")
        
        return last_login_in
    
    
    
    #----------------------------------------------------------------------
    @validates("last_name")
    def _validate_last_name(self, key, last_name_in):
        """validates the given last_name attribute
        """
        
        if last_name_in is not None:
            if not isinstance(last_name_in, (str, unicode)):
                raise TypeError("last_name should be instance of string or "
                                "unicode")
        else:
            last_name_in = ""
        
        return last_name_in.strip().title()
    
    
    
    
    #----------------------------------------------------------------------
    #def _validate_login_name(self, key, login_name):
    #@validates("name")
    #def _validate_name(self, key, name):
        #"""validates the given login_name value
        #"""
        
        #print "login_name_in: ", name
        
        #if name is None:
            #raise TypeError("login name could not be None")
        
        #name = self._format_login_name(str(name))
        
        #if name == "":
            #raise ValueError("login name could not be empty string")
        
        #print "login_name_out: ", name
        
        #return name
    
    
    #----------------------------------------------------------------------
    def _condition_name(self, name):
        """formats the given name
        """
        
        # be sure it is a string
        name = str(name)
        
        # strip white spaces from start and end
        name = name.strip()
        
        # remove all the spaces
        name = name.replace(" ","")
        
        # make it lowercase
        name = name.lower()
        
        # remove any illegal characters
        name = re.sub( "[^\\(a-zA-Z0-9)]+", "", name)
        
        # remove any number at the begining
        name = re.sub( "^[0-9]+", "", name)
        
        return name
    
    
    
    #----------------------------------------------------------------------
    @validates("password")
    def _validate_password(self, key, password_in):
        """validates the given password
        """
        
        if password_in is None:
            raise TypeError("password cannot be None")
        
        # mangle the password
        from stalker.ext import auth  # pylint: disable=W0404
        password_in = auth.set_password(password_in)
        
        return password_in
    
    
    
    #----------------------------------------------------------------------
    def check_password(self, raw_password):
        """Checks the given raw_password.
        
        Checks the given raw_password with the current Users objects encrypted
        password.
        """
        
        from stalker.ext import auth # pylint: disable=W0404
        return auth.check_password(raw_password, self.password)
    
    
    
    #----------------------------------------------------------------------
    @validates("permission_groups")
    def _validate_permission_groups(self, key, permission_group):
        """check the given permission_group
        """
        
        if not isinstance(permission_group, PermissionGroup):
            raise TypeError(
                "any group in permission_groups should be an instance of"
                "stalker.core.models.PermissionGroup"
            )
        
        return permission_group
    
    
    
    #----------------------------------------------------------------------
    @validates("projects_lead")
    def _validate_projects_lead(self, key, project):
        """validates the given projects_lead attribute
        """
        
        if not isinstance(project, Project):
            raise TypeError(
                "any element in projects_lead should be a"
                "stalker.core.models.Project instance")
        
        return project
    
    
    
    #----------------------------------------------------------------------
    @validates("sequences_lead")
    def _validate_sequences_lead(self, key, sequence):
        """validates the given sequences_lead attribute
        """
        
        if not isinstance(sequence, Sequence):
            raise TypeError(
                "any element in sequences_lead should be an instance of "
                "stalker.core.models.Sequence class"
            )
        
        return sequence
    
    
    
    #----------------------------------------------------------------------
    @validates("tasks")
    def _validate_tasks(self, key, task):
        """validates the given taks attribute
        """
        
        if not isinstance(task, Task):
            raise TypeError(
                "any element in tasks should be an instance of "
                "stalker.core.models.Task class")
        
        return task
    
    
    
    #----------------------------------------------------------------------
    @property
    def projects(self):
        """The list of :class:`~stlalker.core.models.Project`\ s those the current user assigned to.
        
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
        
        #return self._projects
        projects = []
        for task in self.tasks:
            projects.append(task.task_of.project)
        
        return list(set(projects))
    
    
    
    ##----------------------------------------------------------------------
    #def _login_name_getter(self):
        #"""The login name of the user.
        
        #It is a string and also sets the :attr:`~stalker.core.models.User.name`
        #attribute.
        #"""
        
        #return self._name
    
    ##----------------------------------------------------------------------
    #def _login_name_setter(self, login_name_in):
        #self.name = self._validate_login_name(login_name_in)
        
        ## set the name attribute
        #self.login_name = self.name
        
        ## also set the code
        #self.code = self._validate_code(self.name)






########################################################################
class ReferenceMixin(object):
    """Adds reference capabilities to the mixed in class.
    
    References are :class:`stalker.core.models.Entity` instances or anything
    derived from it, which adds information to the attached objects. The aim of
    the References are generally to give more info to direct the evolution of
    the object.
    
    :param references: A list of :class:`~stalker.core.models.Entity` objects.
    
    :type references: list of :class:`~stalker.core.models.Entity` objects.
    """
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 references=None,
                 **kwargs):
        if references is None:
            references = []
        
        self.references = references
    
    
    
    #----------------------------------------------------------------------
    @classmethod
    def create_secondary_tables_for_references(cls):
        """creates any secondary table
        """
        
        class_name = cls.__name__
        
        # use the given class_name and the class_table
        secondary_table_name = class_name + "_References"
        secondary_table = None
        
        # check if the table is already defined
        if secondary_table_name not in Base.metadata:
            secondary_table = Table(
                secondary_table_name, Base.metadata,
                Column(
                    class_name.lower() + "_id",
                    Integer,
                    ForeignKey(cls.__tablename__ + ".id"),
                    primary_key=True,
                ),
                
                Column(
                    "reference_id",
                    Integer,
                    ForeignKey("Links.id"),
                    primary_key=True,
                )
            )
        else:
            secondary_table = Base.metadata.tables[secondary_table_name]
        
        return secondary_table
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def references(cls):
        
        class_name = cls.__name__
        
        # get secondary table
        secondary_table = cls.create_secondary_tables_for_references()
        
        # return the relationship
        return relationship("Link", secondary=secondary_table)
    
    
    
    #----------------------------------------------------------------------
    @validates("references")
    def _validate_references(self, key, reference):
        """validates the given reference
        """
        
        #from stalker.core.models import SimpleEntity
        
        # all the elements should be instance of stalker.core.models.Entity
        if not isinstance(reference, SimpleEntity):
            raise TypeError("all the elements should be instances of "
                             ":class:`stalker.core.models.Entity`")
        
        return reference






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
      StatusList.target_entity_type should match the current class.
    
    :param status: an integer value which is the index of the status in the
      status_list attribute. So the value of this attribute couldn't be lower
      than 0 and higher than the length-1 of the status_list object and nothing
      other than an integer
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, status=0, status_list=None, **kwargs):
        self.status_list = status_list
        self.status = status
        pass
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def status(cls):
        return Column("status", Integer, default=0)
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def status_list_id(cls):
        return Column(
            "status_list_id",
            Integer,
            ForeignKey("StatusLists.id"),
            nullable=False
        )
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def status_list(cls):
        return relationship(
            "StatusList",
            primaryjoin=\
                "%s.status_list_id==StatusList.statusList_id" % cls.__name__
        )
    
    
    
    #----------------------------------------------------------------------
    @validates("status_list")
    def _validate_status_list(self, key, status_list):
        """validates the given status_list_in value
        """
        
        # raise TypeError when:
        #from stalker.core.models import StatusList
        
        if status_list is None:
            raise TypeError("'%s' objects can not be initialized without a "
                            "stalker.core.models.StatusList instance, please "
                            "pass a suitable StatusList "
                            "(StatusList.target_entity_type=%s) "
                            "with the 'status_list' argument" 
                            % (self.__class__.__name__,
                               self.__class__.__name__))
        
        # it is not an instance of status_list
        if not isinstance(status_list, StatusList):
            raise TypeError("the status list should be an instance of "
                             "stalker.core.models.StatusList")
        
        # check if the entity_type matches to the StatusList.target_entity_type
        if self.__class__.__name__ != status_list.target_entity_type:
            raise TypeError("the given StatusLists' target_entity_type is %s, "
                            "whereas the entity_type of this object is %s" % \
                            (status_list.target_entity_type,
                             self.__class__.__name__))
        
        return status_list
    
    
    
    #----------------------------------------------------------------------
    @validates("status")
    def _validate_status(self, key, status):
        """validates the given status value
        """
        
        #from stalker.core.models import StatusList
        
        if not isinstance(self.status_list, StatusList):
            raise TypeError("please set the status_list attribute first")
        
        # it is set to None
        if status is None:
            raise TypeError("the status couldn't be None, set it to a "
                             "non-negative integer")
        
        # it is not an instance of int
        if not isinstance(status, int):
            raise TypeError("the status must be an instance of integer")
        
        # if it is not in the correct range:
        if status < 0:
            raise ValueError("the status must be a non-negative integer")
        
        if status >= len(self.status_list.statuses):
            raise ValueError("the status can not be bigger than the length of "
                             "the status_list")
        
        return status






########################################################################
class ScheduleMixin(object):
    """Adds schedule info to the mixed in class.
    
    Adds schedule information like ``start_date``, ``due_date`` and
    ``duration``. There are theree parameters to initialize a class with
    ScheduleMixin, which are, ``start_date``, ``due_date`` and ``duration``.
    Only two of them are enough to initialize the class. The preceeding order
    for the parameters is as follows::
      
      start_date > due_date > duration
    
    So if all of the parameters are given only the ``start_date`` and the
    ``due_date`` will be used and the ``duration`` will be calculated
    accordingly. In any other conditions the missing parameter will be
    calculated from the following table:
    
    +------------+----------+----------+----------------------------------------+
    | start_date | due_date | duration | DEFAULTS                               |
    +============+==========+==========+========================================+
    |            |          |          | start_date = datetime.date.today()     |
    |            |          |          |                                        |
    |            |          |          | duration = datetime.timedelta(days=10) |
    |            |          |          |                                        |
    |            |          |          | due_date = start_date + duration       |
    +------------+----------+----------+----------------------------------------+
    |     X      |          |          | duration = datetime.timedelta(days=10) |
    |            |          |          |                                        |
    |            |          |          | due_date = start_date + duration       |
    +------------+----------+----------+----------------------------------------+
    |     X      |    X     |          | duration = due_date - start_date       |
    +------------+----------+----------+----------------------------------------+
    |     X      |          |    X     | due_date = start_date + duration       |
    +------------+----------+----------+----------------------------------------+
    |     X      |    X     |    X     | duration = due_date - start_date       |
    +------------+----------+----------+----------------------------------------+
    |            |    X     |    X     | start_date = due_date - duration       |
    +------------+----------+----------+----------------------------------------+
    |            |    X     |          | duration = datetime.timedelta(days=10) |
    |            |          |          |                                        |
    |            |          |          | start_date = due_date - duration       |
    +------------+----------+----------+----------------------------------------+
    |            |          |    X     | start_date = datetime.date.today()     |
    |            |          |          |                                        |
    |            |          |          | due_date = start_date + duration       |
    +------------+----------+----------+----------------------------------------+
      
    The date attributes can be managed with timezones. Follow the Python idioms
    shown in the `documentation of datetime`_
    
    .. _documentation of datetime: http://docs.python.org/library/datetime.html
    
    :param start_date: the start date of the entity, should be a datetime.date
      instance, the start_date is the pin point for the date calculation. In
      any condition if the start_date is available then the value will be
      preserved. If start_date passes the due_date the due_date is also changed
      to a date to keep the timedelta between dates. The default value is
      datetime.date.today()
    
    :type start_date: :class:`datetime.datetime`
    
    :param due_date: the due_date of the entity, should be a datetime.date
      instance, when the start_date is changed to a date passing the due_date,
      then the due_date is also changed to a later date so the timedelta
      between the dates is kept.
    
    :type due_date: :class:`datetime.datetime` or :class:`datetime.timedelta`
    
    :param duration: The duration of the entity. It is a
      :class:`datetime.timedelta` instance. The default value is read from
      the :mod:`~stalker.conf.defaults` module. See the table above for the
      initialization rules.
    
    :type duration: :class:`datetime.timedelta`
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 start_date=None,
                 due_date=None,
                 duration=None,
                 **kwargs
                 ):
        
        self._validate_dates(start_date, due_date, duration)
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def _due_date(cls):
        return Column("due_date", Date)
    
    
    
    #----------------------------------------------------------------------
    def _due_date_getter(self):
        """The date that the entity should be delivered.
        
        The due_date can be set to a datetime.timedelta and in this case it
        will be calculated as an offset from the start_date and converted to
        datetime.date again. Setting the start_date to a date passing the
        due_date will also set the due_date so the timedelta between them is
        preserved, default value is 10 days
        """
        
        return self._due_date
    
    #----------------------------------------------------------------------
    def _due_date_setter(self, due_date_in):
        self._validate_dates(self.start_date, due_date_in, self.duration)
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def due_date(cls):
        return synonym(
            "_due_date",
            descriptor=property(
                cls._due_date_getter,
                cls._due_date_setter
            )
        )
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def _start_date(cls):
        return Column("start_date", Date)
    
    
    
    #----------------------------------------------------------------------
    def _start_date_getter(self):
        """The date that this entity should start.
        
        Also effects the
        :attr:`~stalker.core.models.ScheduleMixin.due_date` attribute value in
        certain conditions, if the
        :attr:`~stalker.core.models.ScheduleMixin.start_date` is set to a time
        passing the :attr:`~stalker.core.models.ScheduleMixin.due_date` it will
        also offset the :attr:`~stalker.core.models.ScheduleMixin.due_date` to
        keep the :attr:`~stalker.core.models.ScheduleMixin.duration` value
        fixed. :attr:`~stalker.core.models.ScheduleMixin.start_date` should be
        an instance of class:`datetime.date` and the default value is
        :func:`datetime.date.today()`
        """
        
        return self._start_date
    
    #----------------------------------------------------------------------
    def _start_date_setter(self, start_date_in):
        self._validate_dates(start_date_in, self.due_date, self.duration)
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def start_date(cls):
        return synonym(
            "_start_date",
            descriptor=property(
                cls._start_date_getter,
                cls._start_date_setter,
            )
        )
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def _duration(cls):
        return Column("duration", Interval)
    
    
    
    #----------------------------------------------------------------------
    def _duration_getter(self):
        """Duration of the entity.
        
        It is a datetime.timedelta instance. Showing the difference of the
        :attr:`~stalker.core.models.ScheduleMixin.start_date` and the
        :attr:`~stalker.core.models.ScheduleMixin.due_date`. If edited it
        changes the :attr:`~stalker.core.models.ScheduleMixin.due_date`
        attribute value.
        """
        return self._duration
    
    #----------------------------------------------------------------------
    def _duration_setter(self, duration_in):
        
        if not duration_in is None:
            if isinstance(duration_in, datetime.timedelta):
                # set the due_date to None
                # to make it recalculated
                self._validate_dates(self.start_date, None, duration_in)
            else:
                self._validate_dates(self.start_date, self.due_date, duration_in)
        else:
            self._validate_dates(self.start_date, self.due_date, duration_in)
    
    #----------------------------------------------------------------------
    @declared_attr
    def duration(cls):
        return synonym(
            "_duration",
            descriptor=property(
                cls._duration_getter,
                cls._duration_setter
            )
        )
    
    
    
    #----------------------------------------------------------------------
    def _validate_dates(self, start_date, due_date, duration):
        """updates the date values
        """
        
        
        if not isinstance(start_date, datetime.date):
            start_date = None
        
        if not isinstance(due_date, datetime.date):
            due_date = None
        
        if not isinstance(duration, datetime.timedelta):
            duration = None
        
        
        # check start_date
        if start_date is None:
            # try to calculate the start_date from due_date and duration
            if due_date is None:
                
                # set the defaults
                start_date = datetime.date.today()
                
                if duration is None:
                    # set the defaults
                    duration = defaults.DEFAULT_TASK_DURATION
                
                due_date = start_date + duration
            else:
                
                if duration is None:
                    duration = defaults.DEFAULT_TASK_DURATION
                
                start_date = due_date - duration
        
        # check due_date
        if due_date is None:
            
            if duration is None:
                duration = defaults.DEFAULT_TASK_DURATION
            
            due_date = start_date + duration
        
        
        if due_date < start_date:
            
            # check duration
            if duration < datetime.timedelta(1):
                duration = datetime.timedelta(1)
            
            due_date = start_date + duration
        
        self._start_date = start_date
        self._due_date = due_date
        self._duration = self._due_date - self._start_date






########################################################################
class ProjectMixin(object):
    """Gives the ability to connect to a :class:`~stalker.core.models.Project` to the mixed in object.
    
    :param project: A :class:`~stalker.core.models.Project` instance holding
      the project which this object is related to. It can not be None, or
      anything other than a :class:`~stalker.core.models.Project` instance.
    
    :type project: :class:`~stalker.core.models.Project`
    """
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def project_id(cls):
        return Column(
            "project_id",
            Integer,
            ForeignKey("Projects.id", use_alter=True, name="project_x_id"),
            # cannot use nullable cause a Project object needs
            # insert itself as the project and it needs post_update
            # thus nullable should be True
            #nullable=False,
        )
    
    
    
    #----------------------------------------------------------------------
    @declared_attr
    def project(cls):
        return relationship(
            "Project",
            primaryjoin=\
                cls.__name__ + ".project_id==Project.project_id_local",
            post_update=True, # for project itself
            uselist=False
        )
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 project=None,
                 **kwargs):
        
        self.project = project
    
    
    
    #----------------------------------------------------------------------
    @validates("project")
    def _validate_project(self, key, project):
        """validates the given project value
        """
        
        if project is None:
            raise TypeError("project can not be None it must be an instance "
                            "of stalker.core.models.Project instance")
        
        #from stalker.core.models import Project
        
        if not isinstance(project, Project):
            raise TypeError("project must be an instance of "
                            "stalker.core.models.Project instance")
        
        return project
    
    
    
    ##----------------------------------------------------------------------
    #@synonym_for("_project")
    #@property
    #def project(self):
        #"""A :class:`~stalker.core.models.Project` instance showing the
        #relation of this object to a Stalker
        #:class:`~stalker.core.models.Project`. It is a read only attribute, so
        #you can not change the Project of an already created object.
        #"""
        
        #return self._project






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
    
    
    __tablename__ = "Messages"
    __mapper_args__ = {"polymorphic_identity": "Message"}
    message_id = Column("id", ForeignKey("Entities.id"), primary_key=True)
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(Message, self).__init__(**kwargs)






########################################################################
class Task(Entity, StatusMixin, ScheduleMixin):
    """Manages Task related data.
    
    Tasks are the smallest meaningful part that should be accomplished to
    complete the a :class:`~stalker.core.models.Project`.
    
    In Stalker, currently these items supports Tasks:
    
       * :class:`~stalker.core.models.Project`
    
       * :class:`~stalker.core.models.Sequence`
    
       * :class:`~stalker.core.models.Asset`
    
       * :class:`~stalker.core.models.Shot`
    
    If you want to have your own class to be *taskable* use the
    :class:`~stalker.core.models.TaskMixin` to add the ability to connect a
    :class:`~stalker.core.models.Task` to it.
    
    The Task class itself is mixed with
    :class:`~stalker.core.models.StatusMixin` and
    :class:`~stalker.core.models.ScheduleMixin`. To be able to give the
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
      :class:`~stalker.core.models.TaskMixin`. If you are going to use the
      :mod:`stalker.db` module than it have to be something derived from
      the :class:`~stalker.core.models.SimpleEntity`.
      
      Again, only classes that has been mixed with
      :class:`~stalker.core.models.TasksMixin` has the attribute called
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
    
    
    __tablename__ = "Tasks"
    __mapper_args__ = {"polymorphic_identity": "Task"}
    task_id = Column("id", Integer, ForeignKey("Entities.id"),
                     primary_key=True)
    
    is_milestone = Column(
        Boolean,
        doc="""Specifies if this Task is a milestone.
        
        Milestones doesn't need any duration, any effort and any resources. It
        is used to create meaningfull dependencies between the critical stages
        of the project.
        """
    )
    
    # UPDATE THIS: is_complete should look to Task.status, but it is may be
    # faster to query in this way, judge later
    is_complete = Column(
        Boolean,
        doc="""A bool value showing if this task is completed or not.
        
        There is a good article_ about why not to use an attribute called
        ``percent_complete`` to measure how much the task is completed.
        
        .. _article: http://www.pmhut.com/how-percent-complete-is-that-task-again
        """
    )
    
    depends = relationship(
        "Task",
        secondary="Task_Tasks",
        primaryjoin="Tasks.c.id==Task_Tasks.c.task_id",
        secondaryjoin="Task_Tasks.c.depends_to_task_id==Tasks.c.id",
        backref="dependent_of",
        doc="""A list of :class:`~stalker.core.models.Task`\ s that this one is depending on.
        
        A CircularDependencyError will be raised when the task dependency
        creates a circlar dependency which means it is not allowed to create
        a dependency for this Task which is depending on another one which in
        some way depends to this one again.
        """
    )
    
    resources = relationship(
        "User",
        secondary="Task_Resources",
        primaryjoin="Tasks.c.id==Task_Resources.c.task_id",
        secondaryjoin="Task_Resources.c.resource_id==Users.c.id",
        #backref="tasks",
        back_populates="tasks",
        doc="""The list of :class:`stalker.core.models.User`\ s instances assigned to this Task.
        """
    )
    
    effort = Column(Interval)
    priority = Column(Integer)
    
    task_of_id = Column(Integer, ForeignKey("TaskableEntities.id"))
    
    task_of = relationship(
        "TaskableEntity",
        primaryjoin="Tasks.c.task_of_id==TaskableEntities.c.id",
        back_populates="tasks",
        doc="""An object that this Task is a part of.
        
        The assigned object should have an attribute called ``tasks``. Any
        object which is not inherited from
        :class:`~stalker.core.models.TaskableEntity` thus doesn't have a
        ``tasks`` attribute which is mapped to the Tasks.task_of attribute
        will raise an AttributeError.
        """
    )
    
    bookings = relationship(
        "Booking",
        primaryjoin="Bookings.c.task_id==Tasks.c.id",
        back_populates="task",
        doc="""A list of :class:`~stalker.core.models.Booking` instances showing who and when spent how much effort on this task.
        """
    )
    
    versions = relationship(
        "Version",
        primaryjoin="Versions.c.version_of_id==Tasks.c.id",
        back_populates="version_of",
        doc="""A list of :class:`~stalker.core.models.Version` instances showing the files created for this task.
        """
    )
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 depends=None,
                 effort=None,
                 resources=None,
                 is_milestone=False,
                 priority=defaults.DEFAULT_TASK_PRIORITY,
                 task_of=None,
                 **kwargs):
        super(Task, self).__init__(**kwargs)
        
        # call the mixin __init__ methods
        StatusMixin.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)
        
        self.bookings = []
        self.versions = []
        
        self.is_milestone = is_milestone
        self.is_complete = False
        
        if depends is None:
            depends = []
        
        self.depends = depends
        
        if self.is_milestone:
            resources = None
        
        if resources is None:
            resources = []
        
        self.resources = resources
        self.effort = effort
        
        self.priority = priority
        
        self.task_of = task_of
    
    
    
    #----------------------------------------------------------------------
    @orm.reconstructor
    def __init_on_load__(self):
        """initialized the instance variables when the instance created with
        SQLAlchemy
        """
        # UPDATE THIS
        self.bookings = []
        self.versions = []
        
        # call supers __init_on_load__
        super(Task, self).__init_on_load__()

    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Task, self).__eq__(other) and isinstance(other, Task)
    
    
    
    
    #----------------------------------------------------------------------
    @validates("bookings")
    def _validate_bookings(self, key, booking):
        """validates the given bookings value
        """
        
        if isinstance(booking, Booking):
            raise TypeError("all the elements in the bookings should be "
                            "an instances of stalker.core.models.Booking")
        
        
        return booking
    
    
    #----------------------------------------------------------------------
    @validates("is_complete")
    def _validate_is_complete(self, key, complete_in):
        """validates the given complete value
        """
        return bool(complete_in)
    
    
    
    #----------------------------------------------------------------------
    @validates("depends")
    def _validate_depends(self, key, depends):
        """validates the given depends value
        """
        
        #if depends_in is None:
            #depends_in = []
        
        #if not isinstance(depends_in, list):
            #raise TypeError("the depends attribute should be an list of"
                            #"stalker.core.models.Task instances")
            
        
        if not isinstance(depends, Task):
            raise TypeError("all the elements in the depends should be an "
                            "instance of stalker.core.models.Task")
        
        # check for the circular dependency
        _check_circular_dependency(depends, self)
        
        return depends
    
    
    
    #----------------------------------------------------------------------
    def _validate_effort(self, effort):
        """validates the given effort
        """
        
        if not isinstance(effort, datetime.timedelta):
            effort = None
        
        if effort is None:
            # take it from the duration and resources
            
            num_of_resources = len(self.resources)
            if num_of_resources == 0:
                num_of_resources = 1
            
            effort = self.duration * num_of_resources
        
        return effort
    
    
    
    #----------------------------------------------------------------------
    def _effort_getter(self):
        """the getter for the effort property
        """
        return self._effort
    
    
    
    #----------------------------------------------------------------------
    def _effort_setter(self, effort_in):
        """the setter for the effort property
        """
        self._effort = self._validate_effort(effort_in)
        
        # update the duration
        num_of_resources = len(self.resources)
        if num_of_resources == 0:
            num_of_resources = 1
        
        self.duration = self._effort / num_of_resources
    
    
    
    effort = synonym(
        "_effort",
        descriptor=property(
            fget=_effort_getter,
            fset=_effort_setter
        ),
        doc="""The total effort that needs to be spend to complete this Task.
        
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
    )
    
    
    
    #----------------------------------------------------------------------
    @validates("is_milestone")
    def _validate_is_milestone(self, key, is_milestone):
        """validates the given milestone value
        """
        
        if is_milestone:
            self.resources = []
        
        return bool(is_milestone)
    
    
    #----------------------------------------------------------------------
    @validates("task_of")
    def _validate_task_of(self, key, task_of):
        """validates the given task_of value
        """
        
        # the object given withe the task_of argument should have an attribute
        # called "tasks"
        if task_of is None:
            raise TypeError("'task_of' can not be None, this will produce "
                            "Tasks without a parent, to remove a task from "
                            "a TaskableEntity, assign the task to another "
                            "TaskableEntity or delete it.")
        
        if not hasattr(task_of, "tasks"):
            raise AttributeError("the object given with 'task_of' should have "
                                 "an attribute called 'tasks'")
        
        return task_of
    
    
    
    #----------------------------------------------------------------------
    @validates("priority")
    def _validate_priority(self, key, priority):
        """validates the given priority value
        """
        
        try:
            priority = int(priority)
        except (ValueError, TypeError):
            pass
        
        if not isinstance(priority, int):
            priority = defaults.DEFAULT_TASK_PRIORITY
        
        if priority < 0:
            priority = 0
        elif priority > 1000:
            priority = 1000
        
        return priority
    
    
    
    
    #----------------------------------------------------------------------
    @validates("resources")
    def _validate_resources(self, key, resource):
        """validates the given resources value
        """
        
        if not isinstance(resource, User):
            raise TypeError("resources should be a list of "
                            "stalker.core.models.User instances")
        
        ## milestones do not need resources
        #if self.is_milestone:
            #resource = None
        
        return resource
    
    
    # UPDATE THIS
    #----------------------------------------------------------------------
    @validates("versions")
    def _validate_versions(self, key, version):
        """validates the given version value
        """
        
        if not isinstance(version, Version):
            raise TypeError("all the elements in the versions list should be "
                            "stalker.core.models.Version instances")
        
        return version
    
    
    
    #----------------------------------------------------------------------
    def _duration_getter(self):
        return self._duration
    
    
    
    #----------------------------------------------------------------------
    def _duration_setter(self, duration):
        # just call the fset method of the duration property in the super
        
        #------------------------------------------------------------
        # code copied and pasted from ScheduleMixin - Fix it later
        if not duration is None:
            if isinstance(duration, datetime.timedelta):
                # set the due_date to None
                # to make it recalculated
                self._validate_dates(self.start_date, None, duration)
            else:
                self._validate_dates(self.start_date, self.due_date, duration)
        else:
            self._validate_dates(self.start_date, self.due_date, duration)
        #------------------------------------------------------------
        
        
        # then update the effort
        num_of_resources = len(self.resources)
        if num_of_resources == 0:
            num_of_resources = 1
        
        new_effort_value = self.duration * num_of_resources
        
        # break recursion
        if self.effort != new_effort_value:
            self.effort = new_effort_value
        
        #return duration
    
    duration = synonym(
        "_duration",
        descriptor=property(
            _duration_getter,
            _duration_setter
        ),
        doc="""The overriden duration attribute.
        
        It is a datetime.timedelta instance. Showing the difference of the
        :attr:`~stalker.core.models.ScheduleMixin.start_date` and the
        :attr:`~stalker.core.models.ScheduleMixin.due_date`. If edited it
        changes the :attr:`~stalker.core.models.ScheduleMixin.due_date`
        attribute value.
        """
    )
    
    
    






#----------------------------------------------------------------------
def _check_circular_dependency(task, check_for_task):
    """checks the circular dependency in task if it has check_for_task in its
    depends list
    
    !!!!WARNING THERE IS NO TEST FOR THIS FUNCTION!!!!
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
class TaskableEntity(Entity, ProjectMixin):
    """Gives the abilitiy to connect to a list of :class:`~stalker.core.models.Task`\ s to the mixed in object.
    
    TaskMixin is a variant of :class:`~stalker.core.models.ProjectMixin` and
    lets the mixed object to have :class:`~stalker.core.model.Task` instances
    to be attached it self. And because :class:`~stalker.core.models.Task`\ s
    are related to :class:`~stalker.core.models.Project`\ s, it also adds
    ability to relate the object to a :class:`~stalker.core.models.Project`
    instance. So every object which is mixed with TaskMixin will have a
    :attr:`~stalker.core.models.TaskMixin.tasks` and a
    :attr:`~stalker.core.models.TaskMixin.project` attribute. Only the
    ``project`` argument needs to be initialized. See the
    :class:`~stalker.core.models.ProjectMixin` for more detail.
    """
    
    
    __tablename__ = "TaskableEntities"
    __mapper_args__ = {"polymorphic_identity": "TaskableEntity"}
    taskableEntity_id = Column("id", Integer, ForeignKey("Entities.id"),
                               primary_key=True)
    
    tasks = relationship(
        "Task",
        primaryjoin=taskableEntity_id==Task.task_of_id,
        #backref="task_of",
        back_populates="task_of",
        post_update=True,
    )
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, tasks=None, **kwargs):
        super(TaskableEntity, self).__init__(**kwargs)
        ProjectMixin.__init__(self, **kwargs)
        
        if tasks is None:
            tasks = []
        self.tasks = tasks
    
    
    
    #----------------------------------------------------------------------
    @validates("tasks")
    def _validate_tasks(self, key, task):
        """validates the given task value
        """
        if not isinstance(task, Task):
            raise TypeError("tasks should be a list of "
            "stalker.core.models.Task instances")
        
        return task







########################################################################
class Project(TaskableEntity, ReferenceMixin, StatusMixin, ScheduleMixin):
    """All the information about a Project in Stalker is hold in this class.
    
    Project is one of the main classes that will direct the others. A project
    in Stalker is a gathering point.
    
    It is mixed with :class:`~stalker.core.models.ReferenceMixin`,
    :class:`~stalker.core.models.StatusMixin`,
    :class:`~stalker.core.models.ScheduleMixin` and
    :class:`~stalker.core.models.TaskMixin` to give reference, status, schedule
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
      stored in. You can not create a project without specifying the
      repository argument and passing a
      :class:`~stalker.core.models.Repository` to it. Default value is None
      which raises a TypeError.
    
    :type repository: :class:`~stalker.core.models.Repository`.
    
    :param bool is_stereoscopic: a bool value, showing if the project is going
      to be a stereo 3D project, anything given as the argument will be
      converted to True or False. Default value is False.
    
    :param float display_width: the width of the display that the output of the
      project is going to be displayed (very unnecessary if you are not using
      stereo 3D setup). Should be an int or float value, negative values
      converted to the positive values. Default value is 1.
    """
    
    # ------------------------------------------------------------------------
    # NOTES:
    #
    # Because a Project instance is inherited from TaskableEntity and which is
    # mixed with the ProjectMixin it has a project attribute. In SOM, the
    # project instantly assigns itself to the project attribute (in __init__).
    # But this creates a weird position in database table and mapper
    # configuration where for the Project class the mapper should configure the
    # `project` attribute with the post_update flag is set to True, and this
    # implies the project_id coloumn to be Null for a while, at least
    # SQLAlchemy does an UPDATE to assign the Project itself to the project
    # attribute, thus the project_id column shouldn't be nullable for Project
    # class, but it is not neccessary for the others.
    # 
    # And because SOM is also checking if the project attribute is None or Null
    # for the created instance, I consider doing this safe.
    # ------------------------------------------------------------------------

    
    
    
    __strictly_typed__ = True
    __tablename__ = "Projects"
    project_id_local = Column("id", Integer, ForeignKey("TaskableEntities.id"),
                              primary_key=True)
    
    __mapper_args__ = {"polymorphic_identity": "Project",
                   "inherit_condition":
                       project_id_local==TaskableEntity.taskableEntity_id}
    
    assets = relationship(
        "Asset",
        primaryjoin="TaskableEntities.c.project_id==Projects.c.id",
        back_populates="project",
        uselist=True,
        doc="""The list of :class:`~stalker.core.models.Asset`\ s created in this project.
        
        It is a read-only list. To add an :class:`~stalker.core.models.Asset`
        to this project, the :class:`~stalker.core.models.Asset` need to be
        created with this project is given in the ``project`` argument in the
        :class:`~stalker.core.models.Asset`.
        """
    )
    
    sequences = relationship(
        "Sequence",
        primaryjoin="TaskableEntities.c.project_id==Projects.c.id",
        back_populates="project",
        uselist=True,
        doc="""The :class:`~stalker.core.models.Sequence`\ s that attached to this project.
        
        This attribute holds all the :class:`~stalker.core.models.Sequence`\ s
        that this :class:`~stalker.core.models.Project` has. It is a list of
        :class:`~stalker.core.models.Sequence` instances. The attribute is
        read-only. The only way to attach a
        :class:`~stalker.core.models.Sequence` to this
        :class:`~stalker.core.models.Project` is to create the
        :class:`~stalker.core.models.Sequence` with this
        :class:`~stalker.core.models.Project` by passing this
        :class:`~stalker.core.models.Project` in the ``project`` argument of
        the :class:`~stalker.core.models.Sequence`.
        """
    )
    
    lead_id = Column(Integer, ForeignKey("Users.id"))
    lead = relationship(
        "User",
        primaryjoin="Projects.c.lead_id==Users.c.id",
        back_populates="projects_lead",
        doc="""The lead of the project.
        
        Should be an instance of :class:`~stalker.core.models.User`,
        also can set to None.
        """
    )
    
    repository_id = Column(Integer, ForeignKey("Repositories.id"))
    repository = relationship(
        "Repository",
        primaryjoin="Project.repository_id==Repository.repository_id",
        doc="""The :class:`~stalker.core.models.Repository` that this project should reside.
        
        Should be an instance of :class:`~stalker.core.models.Repository`. It
        is a read-only attribute. So it is not possible to change the
        repository of one project.
        """
    )
    
    structure_id = Column(Integer, ForeignKey("Structures.id"))
    structure = relationship(
        "Structure",
        primaryjoin="Project.structure_id==Structure.structure_id",
        doc="""The structure of the project. Should be an instance of
        :class:`~stalker.core.models.Structure` class"""
    )
    
    image_format_id = Column(Integer, ForeignKey("ImageFormats.id"))
    image_format = relationship(
        "ImageFormat",
        primaryjoin="Projects.c.image_format_id==ImageFormats.c.id",
        doc="""The :class:`~stalker.core.models.ImageFormat` of this project.
        
        This value defines the output image format of the project, should be an
        instance of :class:`~stalker.core.models.ImageFormat`.
        """
    )
    
    
    fps = Column(
        Float(precision=3),
        doc="""The fps of the project.
        
        It is a float value, any other types will be converted to float. The
        default value is 25.0.
        """
    )
    is_stereoscopic = Column(
        Boolean,
        doc="""True if the project is a stereoscopic project"""
    )
    #display_width = Column(
        #Float(precision=3),
        #doc="""The target display width that this project is going to be displayed on.
        
        #Meaningfull if this project is a stereoscopic project.
        #"""
    #)
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 lead=None,
                 repository=None,
                 structure=None,
                 image_format=None,
                 fps=25.0,
                 is_stereoscopic=False,
                 #display_width=1.0,
                 **kwargs):
        
        # a projects project should be self
        # initialize the project argument to self
        kwargs["project"] = self
        
        super(Project, self).__init__(**kwargs)
        # call the mixin __init__ methods
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)
        #TaskMixin.__init__(self, **kwargs)
        
        self.lead = lead
        self._users = []
        self.repository = repository
        self.structure = structure
        self._sequences = []
        self._assets = []
        
        self.image_format = image_format
        self.fps = fps
        self.is_stereoscopic = bool(is_stereoscopic)
        #self.display_width = display_width
    
    
    
    ##----------------------------------------------------------------------
    #@validates("display_width")
    #def _validate_display_width(self, key, display_width_in):
        #"""validates the given display_width_in value
        #"""
        #return abs(float(display_width_in))
    
    
    
    #----------------------------------------------------------------------
    @validates("fps")
    def _validate_fps(self, key, fps):
        """validates the given fps_in value
        """
        return float(fps)
    
    
    
    #----------------------------------------------------------------------
    @validates("image_format")
    def _validate_image_format(self, key, image_format):
        """validates the given image format
        """
        
        if image_format is not None and \
           not isinstance(image_format, ImageFormat):
            raise TypeError("the image_format should be an instance of "
                            "stalker.core.models.ImageFormat")
        
        return image_format
    
    
    
    #----------------------------------------------------------------------
    @validates("lead")
    def _validate_lead(self, key, lead):
        """validates the given lead_in value
        """
        
        if lead is not None:
            if not isinstance(lead, User):
                raise TypeError("lead must be an instance of "
                                "stalker.core.models.User")
        
        return lead
    
    
    
    #----------------------------------------------------------------------
    @validates("repository")
    def _validate_repository(self, key, repository):
        """validates the given repository_in value
        """
        
        if not isinstance(repository, Repository):
            raise TypeError("The stalker.core.models.Project instance should "
                            "be created with a stalker.core.models.Repository "
                            "instance passed through the 'repository' "
                            "argument, the current value is "
                            "'%s'" % repository)
        
        return repository
    
    
    
    #----------------------------------------------------------------------
    @validates("structure")
    def _validate_structure(self, key, structure_in):
        """validates the given structure_in vlaue
        """
        
        if structure_in is not None:
            if not isinstance(structure_in, Structure):
                raise TypeError("structure should be an instance of "
                                 "stalker.core.models.Structure")
        
        return structure_in
    
    
    
    #----------------------------------------------------------------------
    @validates("is_stereoscopic")
    def _validate_is_stereoscopic(self, key, is_stereoscopic_in):
        return bool(is_stereoscopic_in)
    
    
    
    ##----------------------------------------------------------------------
    #@property
    #def sequences(self):
        #"""The :class:`~stalker.core.models.Sequence`\ s that attached to this project.
        
        #This attribute holds all the :class:`~stalker.core.models.Sequence`\ s
        #that this :class:`~stalker.core.models.Project` has. It is a list of
        #:class:`~stalker.core.models.Sequence` instances. The attribute is
        #read-only. The only way to attach a
        #:class:`~stalker.core.models.Sequence` to this
        #:class:`~stalker.core.models.Project` is to create the
        #:class:`~stalker.core.models.Sequence` with this
        #:class:`~stalker.core.models.Project` by passing this
        #:class:`~stalker.core.models.Project` in the ``project`` argument of
        #the :class:`~stalker.core.models.Sequence`.
        #"""
        
        #return self._sequences
    
    
    
    #----------------------------------------------------------------------
    @property
    def users(self):
        """The users assigned to this project.
        
        This is a list of :class:`~stalker.core.models.User` instances. All the
        elements are gathered from all the
        :class:`~stalker.core.models.Task`\ s of the project itself and from
        :class:`~stalker.core.models.Sequence`\ s,
        :class:`~stalker.core.models.Shot`\ s,
        :class:`~stalker.core.models.Asset`\ s.
        """
        
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
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Project, self).__eq__(other) and \
               isinstance(other, Project)






########################################################################
class Sequence(TaskableEntity, ReferenceMixin, StatusMixin, ScheduleMixin):
    """Stores data about Sequences.
    
    Sequences are holders of the :class:`~stalker.core.models.Shot` objects.
    They orginize the conceptual data with another level of complexity.
    
    The Sequence class updates the
    :attr:`~stalker.core.models.Project.sequence` attribute in the
    :class:`~stalker.core.models.Project` class when the Sequence is
    initialized.
    
    :param lead: The lead of this Seuqence. The default value is None.
    
    :type lead: :class:`~stalker.core.models.User`
    """
    
    
    
    __tablename__ = "Sequences"
    __mapper_args__ = {"polymorphic_identity": "Sequence"}
    sequence_id = Column("id", Integer, ForeignKey("TaskableEntities.id"),
                         primary_key=True)
    
    project_id = Column(Integer, ForeignKey("Projects.id"), nullable=False)
    project = relationship(
        "Project",
        primaryjoin="Sequences.c.project_id==Projects.c.id",
        back_populates="sequences",
        uselist=False,
        doc="""The :class:`~stalker.core.models.Project` instance that this Sequence belongs to.
        
        A :class:`~stalker.core.models.Sequence` can not be created without a
        :class:`~stalker.core.models.Project` instance.
        """
    )
    
    lead_id = Column(Integer, ForeignKey("Users.id"))
    lead = relationship(
        "User",
        primaryjoin="Sequences.c.lead_id==Users.c.id",
        back_populates="sequences_lead",
        uselist=False,
        doc="""The lead of this sequence.
        
        A :class:`~stalker.core.models.User` instance which is assigned as the
        lead of this :class:`~stalker.core.models.Sequence`.
        """
    )
    
    shots = relationship(
        "Shot",
        primaryjoin="Shots.c.sequence_id==Sequences.c.id",
        back_populates="_sequence",
        doc="""The :class:`~stalker.core.models.Shot`\ s assigned to this Sequence.
        
        It is a list of :class:`~stalker.core.models.Shot` instances.
        """
    )
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 lead=None,
                 **kwargs
                 ):
        
        super(Sequence, self).__init__(**kwargs)
        
        # call the mixin __init__ methods
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)
        #TaskMixin.__init__(self, **kwargs)
        
        #self._lead = self._validate_lead(lead)
        self.lead = lead
        self.shots = []
        
        ## update the Project._sequences attribute
        #if not self in self.project.sequences:
            #self._project._sequences.append(self)
    
    
    
    #----------------------------------------------------------------------
    @validates("lead")
    def _validate_lead(self, key, lead):
        """validates the given lead_in value
        """
        
        if lead is not None:
            if not isinstance(lead, User):
                raise TypeError("lead should be instance of "
                                "stalker.core.models.User")
        
        return lead
    
    
    
    #----------------------------------------------------------------------
    @validates("shots")
    def _validate_shots(self, key, shot):
        """validates the given shot value
        """
        
        if not isinstance(shot, Shot):
            raise TypeError("every item in the shots list should be an "
                            "instance of stalker.core.models.Shot")
        
        return shot
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Sequence, self).__eq__(other) and \
               isinstance(other, Sequence)






########################################################################
class Shot(TaskableEntity, ReferenceMixin, StatusMixin):
    """Manages Shot related data.
    
    .. deprecated:: 0.1.2
       
       Because most of the shots in different projects are going to have the
       same name, which is a kind of a code like SH001, SH012A etc., and in
       Stalker you can not have two entities with the same name if their types
       are also matching, to guarantee all the shots are going to have
       different names the :attr:`~stalker.core.models.Shot.name` attribute of
       the Shot instances are automatically set to a randomly generated
       **uuid4** sequence.
    
    .. versionadded:: 0.1.2
       
       The name of the shot can be freely set without worrying about clashing
       names.
    
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
    
    Because Shot is getting its relation to a
    :class:`~stalker.core.models.Project` from the
    passed :class:`~stalker.core.models.Sequence`, you can skip the
    ``project`` argument, and if you not the value of the ``project`` argument
    is not going to be used.
    
    :param sequence: The :class:`~stalker.core.models.Sequence` that this shot
      blengs to. A shot can only be created with a
      :class:`~stalker.core.models.Sequence` instance, so it can not be None.
      The shot itself will be added to the
      :attr:`~stalker.core.models.Sequence.shots` list of the given sequence.
      Also the ``project`` of the :class:`~stalker.core.models.Sequence` will
      be used to set the ``project`` of the current Shot.
    
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
    
    
    __tablename__ = "Shots"
    __mapper_args__ = {"polymorphic_identity": "Shot"}
    
    shot_id = Column("id", Integer, ForeignKey("TaskableEntities.id"),
                     primary_key=True)
    sequence_id = Column(Integer, ForeignKey("Sequences.id"))
    _sequence = relationship(
        "Sequence",
        primaryjoin="Shots.c.sequence_id==Sequences.c.id",
        back_populates="shots"
    )
    
    # the cut_duration attribute is not going to be stored in the database,
    # only the cut_in and cut_out will be enough to calculate the cut_duration
    _cut_in = Column(Integer)
    _cut_out = Column(Integer)
    
    assets = relationship(
        "Asset",
        secondary="Shot_Assets",
        #primaryjoin="Shots.c.id==Shot_Assets.c.shot_id",
        #secondaryjoin="Shot_Assets.c.asset_id==Assets.c.id",
        back_populates="shots",
        doc="""The :class:`~stalker.core.models.Asset` instances used in this Shot.
        
        Holds the relation of a :class:`~stalker.core.models.Shot` with a list
        of :class:`~stalker.core.models.Asset`\ s, which are used in this
        :class:`~stalker.core.models.Shot`.
        """
    )
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 #code=None,
                 sequence=None,
                 cut_in=1,
                 cut_out=None,
                 cut_duration=None,
                 assets=None,
                 **kwargs):
        
        sequence = self._validate_sequence(sequence)
        
        # initialize TaskableMixin
        kwargs["project"] = sequence.project
        
        super(Shot, self).__init__(**kwargs)
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        
        self.sequence = self._validate_sequence(sequence)
        
        self._cut_in = cut_in
        self._cut_duration = cut_duration
        self._cut_out = cut_out
        
        self._update_cut_info(cut_in, cut_duration, cut_out)
        
        #self._assets = self._validate_assets(assets)
        if assets is None:
            assets = []
        self.assets = assets
        
    
    
    
    #----------------------------------------------------------------------
    @orm.reconstructor
    def __init_on_load__(self):
        """initialized the instance variables when the instance created with
        SQLAlchemy
        """
        self._cut_duration = None
        self._update_cut_info(self._cut_in, self._cut_duration, self._cut_out)
        
        # call supers __init_on_load__
        super(Shot, self).__init_on_load__()
    
    
    
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
    
    
    
    
    #----------------------------------------------------------------------
    @validates("assets")
    def _validate_assets(self, key, asset):
        """validates the given asset value
        """
        
        if not isinstance(asset, Asset):
            raise TypeError("all the items in the assets list should be"
                             "an instance of stalker.core.models.Asset")
        
        return asset
    
    
    
    ##----------------------------------------------------------------------
    #def _validate_code(self, code_in):
        #"""validates the given code value
        #"""
        
        ## check if the code_in is None or empty string
        #if code_in is None:
            #raise TypeError("the code can not be None")
        
        #if code_in == "":
            #raise ValueError("the code can not be empty string")
        
        #return self._condition_code(str(code_in))
    
    
    
    #----------------------------------------------------------------------
    def _validate_cut_duration(self, cut_duration_in):
        """validates the given cut_duration value
        """
        
        if cut_duration_in is not None and \
           not isinstance(cut_duration_in, int):
            raise TypeError("cut_duration should be an instance of int")
        
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
    def _validate_sequence(self, sequence):
        """validates the given sequence_in value
        """
        
        if not isinstance(sequence, Sequence):
            raise TypeError("the sequence should be an instance of "
                             "stalker.core.models.Sequence instance")
        
        for shot in sequence.shots:
            if self.code ==  shot.code:
                raise ValueError("the given sequence already has a shot with "
                                 "a code %s" % self.code)
        
        return sequence
    
    
    
    #----------------------------------------------------------------------
    def _sequence_getter(self):
        """The getter for the sequence attribute.
        """
        
        return self._sequence
    
    
    
    #----------------------------------------------------------------------
    def _sequence_setter(self, sequence):
        """the setter for the sequence attribute.
        """
        
        self._sequence = self._validate_sequence(sequence)
    
    sequence = synonym(
        "_sequence",
        descriptor=property(_sequence_getter, _sequence_setter),
        doc="""The :class:`~stalker.core.models.Sequence` instance that this :class:`~stalker.core.models.Shot` instance belongs to."""
    )
    
    
    
    ##----------------------------------------------------------------------
    #@property
    #def code(self): # pylint: disable=E0202
        #"""The code of this :class:`~stalker.core.models.Shot`.
        
        #Contrary to the original attribute from the inherited parent
        #(:attr:`~stalker.core.models.SimpleEntity.code`), the code attribute
        #can not be set to None or empty string."""
        
        #return self._code
    
    ##----------------------------------------------------------------------
    #@code.setter # pylint: disable=E1101
    #def code(self, code_in):
        ## pylint: disable=E0102, E0202, W0221
        #self._code = self._validate_code(code_in)
    
    
    
    #----------------------------------------------------------------------
    def _cut_duration_getter(self):
        return self._cut_duration
    
    #----------------------------------------------------------------------
    def _cut_duration_setter(self, cut_duration_in):
        self._update_cut_info(self._cut_in, cut_duration_in, self._cut_out)
    
    cut_duration = synonym(
        "_cut_duration",
        descriptor=property(_cut_duration_getter, _cut_duration_setter),
        doc= """The duration of this shot in frames.
        
        It should be a positive integer value. If updated also updates the
        :attr:`~stalker.core.models.Shot.cut_duration` attribute. The default
        value is 100."""
    )
    
    
    
    #----------------------------------------------------------------------
    def _cut_in_getter(self):
        return self._cut_in
    
    #----------------------------------------------------------------------
    def _cut_in_setter(self, cut_in_in):
        self._update_cut_info(cut_in_in, self._cut_duration, self._cut_out)
    
    cut_in = synonym(
        "_cut_in",
        descriptor=property(_cut_in_getter, _cut_in_setter),
        doc="""The in frame number taht this shot starts.
        
        The default value is 1. When the cut_in is bigger then
        :attr:`~stalker.core.models.Shot.cut_out`, the
        :attr:`~stalker.core.models.Shot.cut_out` value is update to
        :attr:`~stalker.core.models.Shot.cut_in` + 1."""
    )
    
    
    
    #----------------------------------------------------------------------
    def _cut_out_getter(self):
        if self._cut_out is None:
            self._update_cut_info(self._cut_in, self._cut_duration, None)
        return self._cut_out
    
    #----------------------------------------------------------------------
    def _cut_out_setter(self, cut_out_in):
        self._update_cut_info(self._cut_in, self._cut_duration, cut_out_in)
    
    cut_out = synonym(
        "_cut_out",
        descriptor=property(_cut_out_getter, _cut_out_setter),
        doc="""The out frame number that this shot ends.
        
        When the :attr:`~stalker.core.models.Shot.cut_out` is set to a value
        lower than :attr:`~stalker.core.models.Shot.cut_in`,
        :attr:`~stalker.core.models.Shot.cut_out` will be updated to
        :attr:`~stalker.core.models.Shot.cut_in` + 1. The default value is
        :attr:`~stalker.core.models.Shot.cut_in` +
        :attr:`~stalker.core.models.Shot.cut_duration`."""
    )
    
    
    
    ##----------------------------------------------------------------------
    #@property
    #def name(self): # pylint: disable=E0202
        #"""Name of this Shot.
        
        #Different than other :class:`~stalker.core.models.SimpleEntity`
        #derivatives, the :class:`~stalker.core.models.Shot` classes
        #:attr:`~stalker.core.models.Shot.name` attribute is read-only. And the
        #stored value is a uuid4 sequence.
        #"""
        
        #return self._name
    
    ##----------------------------------------------------------------------
    #@name.setter # pylint: disable=E1101
    #def name(self, name_in):
        ## pylint: disable=E0102, E0202, W0221
        #pass






########################################################################
class Asset(TaskableEntity, ReferenceMixin, StatusMixin):
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
    
    An :class:`~stalker.core.models.Asset` instance should be initialized with
    a :class:`~stalker.core.models.Project` instance (as the other classes
    which are mixed with the :class:`~stalekr.core.mixins.TaskMixin`). And when
    a :class:`~stalker.core.models.Project` instance is given then the asset
    will append itself to the :attr:`~stalker.core.models.Project.assets` list.
    """
    
    
    
    __strictly_typed__ = True
    __tablename__ = "Assets"
    __mapper_args__ = {"polymorphic_identity": "Asset"}
    
    asset_id = Column("id", Integer, ForeignKey("TaskableEntities.id"),
                      primary_key=True)
    
    shots = relationship(
        "Shot",
        secondary="Shot_Assets",
        back_populates="assets"
    )
    
    project_id = Column(Integer, ForeignKey("Projects.id"), nullable=False)
    project = relationship(
        "Project",
        primaryjoin="Assets.c.project_id==Projects.c.id",
        back_populates="assets",
        uselist=False,
        doc="""The :class:`~stalker.core.models.Project` instance that this Asset belongs to.
        
        A :class:`~stalker.core.models.Asset` can not be created without a
        :class:`~stalker.core.models.Project` instance.
        """
    )
    

    
    #----------------------------------------------------------------------
    def __init__(self, shots=None, **kwargs):
        
        super(Asset, self).__init__(**kwargs)
        
        # call the mixin init methods
        ReferenceMixin.__init__(self, **kwargs)
        StatusMixin.__init__(self, **kwargs)
        #TaskMixin.__init__(self, **kwargs)
        
        #self._shots = []
        if shots is None:
            shots = []
        self.shots = shots
        
        ## append it self to the given projects assets attribute
        #if not self in self.project._assets:
            #self.project._assets.append(self)
    
    
    
    #----------------------------------------------------------------------
    @orm.reconstructor
    def __init_on_load__(self):
        """initialized the instance variables when the instance created with
        SQLAlchemy
        """
        #self._shots = None
        
        # call supers __init_on_load__
        super(Asset, self).__init_on_load__()
    
    
    
    #----------------------------------------------------------------------
    @validates("shots")
    def _validate_shots(self, key, shot):
        """validates the given shots_in value
        """
        
        if not isinstance(shot, Shot):
            raise TypeError("shots should be set to a list of "
                            "stalker.core.models.Shot objects")
        
        return shot
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Asset, self).__eq__(other) and \
               isinstance(other, Asset) and self.type == other.type






########################################################################
class Version(Entity, StatusMixin):
    """The connection to the filesystem.
    
    A :class:`~stalker.core.models.Version` holds information about the every
    incarnation of the files in the :class:`~stalker.core.models.Repository`.
    So if one creates a new version for a file or a sequences of file for a
    :class:`~stalker.core.models.Task` then the information is hold in the
    :class:`~stalker.core.models.Version` instance.
    
    The :attr:`~stalker.core.models.Version.version` attribute is read-only.
    Trying to change it will produce an AttributeError.
    
    :param str take: A short string holding the current take name. Can be
      any alphanumeric value (a-zA-Z0-9\_). The default is the string "Main".
      When skipped or given as None or an empty string then it will use the
      default value.
    
    :param int version: An integer value showing the current version number.
      The default is "1". If skipped or given as zero or as a negative value a
      ValueError will be raised.
    
    :param source_file: A :class:`~stalker.core.models.Link` instance, showing
      the source file of this version. It can be a Maya scene file
      (*.ma, *.mb), a Nuke file (*.nk) or anything that is opened with the
      application you have created this version.
    
    :type source_file: :class:`~stalker.core.models.Link`
    
    :param outputs: A list of :class:`~stalker.core.models.Link` instances,
      holding the outputs of the current version. It could be the rendered
      image sequences out of Maya or Nuke, or it can be a Targa file which is
      the output of a Photoshop file (*.psd), or anything that you can think as
      the output which is created using the
      :attr:`~stalker.core.models.Version.source_file`\ .
    
    :type outputs: list of :class:`~stalker.core.models.Link` instances
    
    :param task: A :class:`~stalker.core.models.Task` instance showing the
      owner of this Version.
    
    :type task: :class:`~stalker.core.models.Task`
    
    .. todo::
      Think about using Tickets instead of review notes for reporting desired
      changes.
    
    """
    #:param review: A list of :class:`~stalker.core.models.Review` instances,
      #holding all the reviews made for this Version.
    
    #:type review: :class:`~stalker.core.models.Stalker`
    #:param bool published: A bool value shows if this version is published or
      #not.
    
    
    __tablename__ = "Versions"
    __mapper_args__ = {"polymorphic_identity": "Version"}
    
    version_id = Column("id", ForeignKey("Entities.id"), primary_key=True)
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 take="MAIN",
                 version=1,
                 source_file=None,
                 outputs=None,
                 task=None,
                 **kwargs):
        
        # call supers __init__
        super(Version, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)
    
    
    
    






######################################
# SECONDARY TABLES
######################################



# ENTITY_TAGS
Entity_Tags = Table(
    "Entity_Tags", Base.metadata,
    Column(
        "entity_id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    ),
    
    Column(
        "tag_id",
        Integer,
        ForeignKey("Tags.id"),
        primary_key=True,
    )
)



# STATUSLIST_STATUSES
StatusList_Statuses = Table(
    "StatusList_Statuses", Base.metadata,
    Column(
        "statusList_id",
        Integer,
        ForeignKey("StatusLists.id"),
        primary_key=True
    ),
    Column(
        "status_id",
        Integer,
        ForeignKey("Statuses.id"),
        primary_key=True
    )
)



# STRUCTURE_FILENAMETEMPLATES
Structure_FilenameTemplates = Table(
    "Structure_FilenameTemplates", Base.metadata,
    Column("structure_id", Integer, ForeignKey("Structures.id"),
           primary_key=True),
    Column("filenametemplate_id", Integer, ForeignKey("FilenameTemplates.id"),
           primary_key=True)
)



# USER_PERMISSIONGROUPS
User_PermissionGroups = Table(
    "User_PermissionGroups", Base.metadata,
    Column("user_id", Integer, ForeignKey("Users.id"), primary_key=True),
    Column("permissionGroup_id", Integer, ForeignKey("PermissionGroups.id"),
           primary_key=True
    )
)


# TASK_RESOURCES
Task_Resources = Table(
    "Task_Resources", Base.metadata,
    Column("task_id", Integer, ForeignKey("Tasks.id"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("Users.id"), primary_key=True),
)

# TASK_TASKS
Task_Tasks = Table(
    "Task_Tasks", Base.metadata,
    Column("task_id", Integer, ForeignKey("Tasks.id"), primary_key=True),
    Column("depends_to_task_id", Integer, ForeignKey("Tasks.id"),
           primary_key=True),
)

# SHOT ASSETS
Shot_Assets = Table(
    "Shot_Assets", Base.metadata,
    Column("shot_id", Integer, ForeignKey("Shots.id"), primary_key=True),
    Column("asset_id", Integer, ForeignKey("Assets.id"), primary_key=True),
)
