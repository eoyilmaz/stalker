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
    #Boolean,
    Integer,
    Float,
    String,
    ForeignKey,
    #Date,
    DateTime,
    UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base, synonym_for

import stalker
#from stalker.ext.validatedList import ValidatedList
from stalker.core.errors import CircularDependencyError
from stalker.conf import defaults



Base = declarative_base()






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
    
    code = Column(String(256), nullable=False)
    name = Column(String(256), nullable=False)
    description = Column("description", String)
    
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
    )
    
    date_created = Column(DateTime, default=datetime.datetime.now())
    date_updated = Column(DateTime, default=datetime.datetime.now())
    
    type_id = Column(
        "type_id",
        Integer,
        ForeignKey("Types.id", use_alter=True, name="y")
    )
    
    type = relationship(
        "Type",
        primaryjoin="SimpleEntity.type_id==Type.type_id_local",
    )
    
    UniqueConstraint("name", "db_entity_type")
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
        
        # code attribute
        # just set it to None for now
        #self._code = ""
        
        # name and nice_name
        self._nice_name = ""
        #self._name = ""
        self.name = name
        
        # code
        # if the given code argument is not None
        # use it to set the code
        if code is not None and code is not "":
            #self._code = self._validate_code(code)
            self.code = code
        
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
    def _validate_name(self, key, name_in):
        """validates the given name_in value
        """
        
        # it is None
        if name_in is None:
            raise TypeError("the name couldn't be set to None")
        
        name_in = self._condition_name(str(name_in))
        
        # it is empty
        if name_in == "":
            raise ValueError("the name couldn't be an empty string")
        
        # also set the nice_name
        self._nice_name = self._condition_nice_name(name_in)
        
        # set the code
        self.code = name_in
        
        return name_in
    
    
    
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
        
        #from stalker.core.models import User
        
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
        backref="entities"
    )
    
    notes = relationship(
        "Note",
        primaryjoin="Entity.entity_id==Note.entity_id",
        backref="entity"
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
    def _validate_notes(self, key, note_in):
        """validates the given note value
        """
        
        if not isinstance(note_in, Note):
            raise TypeError("note should be an instance of "
                            "stalker.core.models.Note")
        
        return note_in
    
    
    
    #----------------------------------------------------------------------
    @validates("tags")
    def _validate_tags(self, key, tag_in):
        """validates the given tag
        """
        
        if not isinstance(tag_in, Tag):
            raise TypeError("tag should be an instance of "
                            "stalker.core.models.Tag")
        
        return tag_in
    
    
    
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
    _target_entity_type = Column(String)
    
    
    
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
    
    width = Column(Integer)
    height = Column(Integer)
    pixel_aspect = Column(Float, default="1.0")
    print_resolution = Column(Float, default="300.0")
    
    
    
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
    
    content = Column(String)
    
    
    
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
    
    #department_id = Column(Integer, ForeignKey("Departments.id"))
    email = Column(String(256), unique=True, nullable=False)
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=True)
    password = Column(String(256), nullable=False)
    last_login = Column(DateTime)
    initials = Column(String(16))
    
    #enitites_created = synonym("_entities_created")
    #enitites_updated = synonym("_entities_updated")
    
    
    
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
        
        #self._department = self._validate_department(department)
        self.department = department
        
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.login_name = login_name
        self.initials = initials
        
        # to be able to mangle the password do it like this
        self.password = password
        
        #self.permission_groups = permission_groups
        
        self._projects = []
        self.projects_lead = projects_lead
        self.sequences_lead = sequences_lead
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
    def _validate_name(self, key, name_in):
        """validates the given name value
        """
        
        ## set the login name first
        ## break recursion
        #if self.login_name != name_in:
            #self.login_name = name_in
        
        #name_in = self.login_name
        
        # also set the nice_name
        self._nice_name = self._condition_nice_name(name_in)
        
        # and also the code
        #self.code = self._nice_name.upper()
        self.code = name_in
        
        return name_in
    
    
    
    ##----------------------------------------------------------------------
    #@validates("department")
    #def _validate_department(self, key, department_in):
        #"""validates the given department value
        #"""
        
        ## check if it is intance of Department object
        #if department_in is not None:
            #if not isinstance(department_in, Department):
                #raise TypeError("department should be instance of "
                                 #"stalker.core.models.Department")
        
        #return department_in
    
    
    
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
    
    
    
    ##----------------------------------------------------------------------
    #@validates("login_name")
    #def _validate_login_name(self, key, login_name_in):
        #"""validates the given login_name value
        #"""
        
        #if login_name_in is None:
            #raise TypeError("login name could not be None")
        
        #login_name_in = self._format_login_name(str(login_name_in))
        
        #if login_name_in == "":
            #raise ValueError("login name could not be empty string")
        
        ## set the name
        #if self.name != login_name_in:
            #self.name = login_name
        
        ## set the code
        #print "setting the code to %s" % self.name
        #self.code = self.name
        
        #return login_name_in
    
    
    
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
    
    
    
    ##----------------------------------------------------------------------
    #@property
    #def login_name(self):
        #"""The login name of the user.
        
        #It is a string and also sets the :attr:`~stalker.core.models.User.name`
        #attribute.
        #"""
        
        #return self.name
    
    ##----------------------------------------------------------------------
    #@login_name.setter
    #def login_name(self, login_name_in):
        #self._login_name = self._validate_login_name(login_name_in)
        #self.name = self._login_name
        
        ## also set the code
        #self.code = self._validate_code(self._login_name)
    
    login_name = synonym("name")
    
    
    
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
    
    
    
    ##----------------------------------------------------------------------
    #@validates("permission_groups")
    #def _validate_permission_groups(self, key, permission_groups_in):
        #"""check the given permission_group
        #"""
        
        #if permission_groups_in is None:
            #permission_groups_in = []
        
        #if not isinstance(permission_groups_in, list):
            #raise TypeError("permission_groups should be a list of group "
                             #"objects")
        
        #for permission_group in permission_groups_in:
            #if not isinstance(permission_group, PermissionGroup):
                #raise TypeError(
                    #"any group in permission_groups should be an instance of"
                    #"stalker.core.models.PermissionGroup"
                #)
        
        ##return ValidatedList(permission_groups_in, PermissionGroup)
        #return permission_groups_in
    
    
    
    ##----------------------------------------------------------------------
    #@validates("projects_lead")
    #def _validate_projects_lead(self, key, projects_lead_in):
        #"""validates the given projects_lead attribute
        #"""
        
        #if projects_lead_in is None:
            #projects_lead_in = []
        
        #if not isinstance(projects_lead_in, list):
            #raise TypeError("projects_lead should be a list of "
                             #"stalker.core.models.Project instances")
        
        #for a_project in projects_lead_in:
            #if not isinstance(a_project, Project):
                #raise TypeError(
                    #"any element in projects_lead should be a"
                    #"stalker.core.models.Project instance")
        
        ##return ValidatedList(projects_lead_in, Project)
        #return projects_lead_in
    
    
    
    ##----------------------------------------------------------------------
    #@validates("sequences_lead")
    #def _validate_sequences_lead(self, key, sequences_lead_in):
        #"""validates the given sequences_lead attribute
        #"""
        
        #if sequences_lead_in is None:
            #sequences_lead_in = []
        
        #if not isinstance(sequences_lead_in, list):
            #raise TypeError("sequences_lead should be a list of "
                             #"stalker.core.models.Sequence objects")
        
        #for a_sequence in sequences_lead_in:
            #if not isinstance(a_sequence, Sequence):
                #raise TypeError(
                    #"any element in sequences_lead should be an instance of "
                    #"stalker.core.models.Sequence class"
                #)
        
        ##return ValidatedList(sequences_lead_in, Sequence)
        #return sequences_lead_in
    
    
    
    ##----------------------------------------------------------------------
    #@validates("tasks")
    #def _validate_tasks(self, key, tasks_in):
        #"""validates the given taks attribute
        #"""
        
        #if tasks_in is None:
            #tasks_in = []
        
        #if not isinstance(tasks_in, list):
            #raise TypeError("tasks should be a list of "
                             #"stalker.core.models.Task objects")
        
        #for a_task in tasks_in:
            #if not isinstance(a_task, Task):
                #raise TypeError(
                    #"any element in tasks should be an instance of "
                    #"stalker.core.models.Task class")
        
        ##return ValidatedList(tasks_in, Task)
        #return tasks_in
    
    
    
    ##----------------------------------------------------------------------
    #@property
    #def projects(self):
        #"""The list of :class:`~stlalker.core.models.Project`\ s those the current user assigned to.
        
        #returns a list of :class:`~stalker.core.models.Project` objects.
        #It is a read-only attribute. To assign a
        #:class:`~stalker.core.models.User` to a
        #:class:`~stalker.core.models.Project`, you need to create a new
        #:class:`~stalker.core.models.Task` with the
        #:attr:`~stalker.core.models.Task.resources` is set to this
        #:class:`~stalker.core.models.User` and assign the
        #:class:`~stalker.core.models.Task` to the
        #:class:`~stalker.core.models.Project` by setting the
        #:attr:`~stalker.core.models.Task.project` attribute of the
        #:class:`~stalker.core.models.Task` to the
        #:class:`~stalker.core.models.Project`.
        #"""
        
        ##return self._projects
        #projects = []
        #for task in self.tasks:
            #projects.append(task.task_of.project)
        
        #return list(set(projects))



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