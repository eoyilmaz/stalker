# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import datetime
import re
from sqlalchemy import (Table, Column, Integer, String, ForeignKey, DateTime,
                        Enum)
from sqlalchemy.orm import relationship, validates, reconstructor

import stalker
from stalker.db import Base
from stalker.models.mixins import ProjectMixin




class EntityMeta(type):
    """The metaclass for the very basic entity.
    
    Just adds the name of the class as the entity_type class attribute and
    creates an attribute called plural_name to hold the auto generated plural
    form of the class name. These two attributes can be overridden in the
    class itself.
    """
    
    def __new__(mcs, class_name, bases, dict_):
        # create the entity_type
        #dict_["entity_type"] = unicode(class_name)
        
        # try to find a plural name for the class if not given
        if not dict_.has_key("plural_name"):
            plural_name = unicode(class_name + "s")
            
            if class_name[-1] == "y":
                plural_name = unicode(class_name[:-1] + "ies")
            elif class_name[-2] == "ch":
                plural_name = unicode(class_name + "es")
            elif class_name[-1] == "f":
                plural_name = unicode(class_name[:-1] + "ves")
            elif class_name[-1] == "s":
                plural_name = unicode(class_name + "es")

            dict_["plural_name"] = plural_name

        #if not dict_.has_key("__strictly_typed__"):
        #    dict_["__strictly_typed__"] = False
        
        # add the class to the ACLs
        ACLs.insert().values(action='add', class_name=class_name)
        from stalker.db.session import DBSession
        if DBSession.engine:
            pass
        
        return super(EntityMeta, mcs).__new__(mcs, class_name, bases, dict_)

class SimpleEntity(Base):
    """The base class of all the others
    
    The :class:`~stalker.models.entity.SimpleEntity` is the starting point of
    the Stalker Object Model, it starts by adding the basic information about
    an entity which are :attr:`~stalker.models.entity.SimpleEntity.name`,
    :attr:`~stalker.models.entity.SimpleEntity.description`, the audit
    information like :attr:`~stalker.models.entity.SimpleEntity.created_by`,
    :attr:`~stalker.models.entity.SimpleEntity.updated_by`,
    :attr:`~stalker.models.entity.SimpleEntity.date_created`,
    :attr:`~stalker.models.entity.SimpleEntity.date_updated` and a couple of
    naming attributes like :attr:`~stalker.models.entity.SimpleEntity.code` and
    :attr:`~stalker.models.entity.SimpleEntity.nice_name` and last but not
    least the :attr:`~stalker.models.entity.SimpleEntity.type` attribute which
    is very important for entities that needs a type.
    
    For derived classes if the :attr:`~stalker.models.entity.SimpleEntity.type`
    needed to be specifically specified, that is it can not be None or nothing
    else then a :class:`~stalker.models.type.Type` instance, set the
    ``strictly_typed`` class attribute to True::
      
        class NewClass(SimpleEntity):
            __strictly_typed__ = True
    
    This will ensure that the derived class always have a proper
    :attr:`~stalker.models.entity.SimpleEntity.type` attribute and can not
    initialize without one.
    
    Two SimpleEntities considered to be equal if they have the same name, the
    other attributes doesn't matter.
    
    The formatting rules for the code attribute is as follows:
      
        * only alphanumerics and underscore is allowed \[a-zA-Z0-9\_\]
        * no number is allowed at the beginning
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
        | My CODE is Code                   | My_CODE_is_Code                   |
        +-----------------------------------+-----------------------------------+
        | this is another code for an asset | this_is_another_code_for_an_asset |
        +-----------------------------------+-----------------------------------+
      
    :param string name: A string or unicode value that holds the name of this
      entity. It can not be empty, the first letter should be an alphabetic
      ([a-zA-z]) (not alphanumeric [a-zA-Z0-9]) letter and it should not
      contain any white space at the beginning and at the end of the string,
      giving an object the object will be converted to string and then the
      resulting string will be formatted.
    
    :param str description: A string or unicode attribute that holds the
      description of this entity object, it could be an empty string, and it
      could not again have white spaces at the beginning and at the end of the
      string, again any given objects will be converted to strings
    
    :param created_by: The :class:`~stalker.models.auth.User` who has created
      this object
    
    :type created_by: :class:`~stalker.models.auth.User`
    
    :param updated_by: The :class:`~stalker.models.auth.User` who has updated
      this object lastly. The created_by and updated_by attributes point the
      same object if this object is just created.
    
    :param date_created: The date that this object is created.
    
    :type date_created: :class:`datetime.datetime`
    
    :param date_updated: The date that this object is updated lastly. For newly
      created entities this is equal to date_created and the date_updated
      cannot point a date which is before date_created.
    
    :type date_updated: :class:`datetime.datetime`
    
    :param str code: The code name of this object. It accepts string or
      unicode values and any other kind of objects will be converted to
      string. Can be omitted and it will be set to the same value of the
      nice_name attribute. If both the name and code arguments are given the
      code attribute will be set to the given code argument value, but in any
      update to name attribute the code also will be updated to the nice_name
      attribute. When the code is directly edited the code will not be
      formatted other than removing any illegal characters. The default value
      is the same value of the nice_name.
    
    :param type: The type of the current SimpleEntity. Used across several
      places in Stalker. Can be None. The default value is None.
    
    :type type: :class:`~stalker.models.type.Type`
    """
    
    __strictly_typed__ = False
    
    __tablename__ = "SimpleEntities"
    id = Column("id", Integer, primary_key=True)
    
    entity_type = Column(String(128), nullable=False)
    __mapper_args__ = {
        "polymorphic_on": entity_type,
        "polymorphic_identity": "SimpleEntity"
    }
    
    code = Column(
        String(256),
        nullable=False,
        doc="""The code name of this object.
        
        It accepts string or unicode values and any other kind of objects will
        be converted to string. In any update to the name attribute the code
        also will be updated. If the code is not initialized or given as None,
        it will be set to the uppercase version of the nice_name attribute.
        Setting the code attribute to None will reset it to the default value.
        The default value is the upper case form of the nice_name."""
    )
    
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
        doc="""The :class:`~stalker.models.auth.User` who has created this object."""
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
        doc="""The :class:`~stalker.models.auth.User` who has updated this object."""
    )
    
    date_created = Column(
        DateTime,
        default=datetime.datetime.now(),
        doc="""A :class:`datetime.datetime` instance showing the creation date and time of this object."""
    )
    
    date_updated = Column(
        DateTime,
        default=datetime.datetime.now(),
        doc="""A :class:`datetime.datetime` instance showing the update date and time of this object."""
        ,
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
        
        It is an instance of :class:`~stalker.models.type.Type` with a proper
        :attr:`~stalker.models.type.Type.target_entity_type`.
        """
    )
    
    generic_data = relationship(
        'SimpleEntity',
        secondary='SimpleEntity_GenericData',
        primaryjoin='SimpleEntities.c.id==SimpleEntity_GenericData.c.simple_entity_id',
        secondaryjoin='SimpleEntity_GenericData.c.other_simple_entity_id==SimpleEntities.c.id',
        doc='''This attribute can hold any kind of data which exists in SOM.
        '''
    )
    
    __stalker_version__ = Column("stalker_version", String(256))
    
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

    @reconstructor
    def __init_on_load__(self):
        """initialized the instance variables when the instance created with
        SQLAlchemy
        """
        self._nice_name = None

    def __repr__(self):
        """the representation of the SimpleEntity
        """

        return "<%s (%s, %s)>" % (self.entity_type, self.name, self.code)
    
    @validates("description")
    def _validate_description(self, key, description_in):
        """validates the given description_in value
        """

        if description_in is None:
            description_in = ""

        return str(description_in)
    
    @validates("name")
    def _validate_name(self, key, name):
        """validates the given name_in value
        """
        # it is None
        if name is None:
            raise TypeError("%s.name can not be None" %
                            self.__class__.__name__)
        
        if not isinstance(name, (str, unicode)):
            raise TypeError("%s.name should be an instance of string or "
                            "unicode not %s" %
                            (self.__class__.__name__,
                             name.__class__.__name__))
        
        name = self._format_name(str(name))
        
        # it is empty
        if name == "":
            raise ValueError("%s.name can not be an empty string" %
                             self.__class__.__name__)
        
        # also set the nice_name
        self._nice_name = self._format_nice_name(name)
        
        return name
    
    def _format_code(self, code_in):
        """formats the given code_in value
        """

        # just set it to the uppercase of what nice_name gives
        # remove unnecessary characters from the string
        code_in = self._format_name(str(code_in))

        # replace camel case letters
        #code_in = re.sub(r"(.+?[a-z]+)([A-Z])", r"\1_\2", code_in)

        # replace white spaces with under score
        code_in = re.sub("([\s\-])+", r"_", code_in)

        # remove multiple underscores
        code_in = re.sub(r"([_]+)", r"_", code_in)

        return code_in

    def _format_name(self, name_in):
        """formats the name_in value
        """
        # remove unnecessary characters from the string
        name_in = re.sub(r'([^a-zA-Z0-9\s_\-]+)', '', name_in).strip()

        # remove all the characters which are not alphabetic
        name_in = re.sub(r"(^[^a-zA-Z0-9]+)", '', name_in)
        
        # remove multiple spaces
        name_in = re.sub(r'[\s]+', ' ', name_in)

        return name_in

    def _format_nice_name(self, nice_name_in):
        """formats the given nice name
        """

        # remove unnecessary characters from the string
        nice_name_in = self._format_name(str(nice_name_in))

        # replace camel case letters
        nice_name_in = re.sub(r"(.+?[a-z]+)([A-Z])", r"\1_\2", nice_name_in)

        # replace white spaces with under score
        nice_name_in = re.sub("([\s\-])+", r"_", nice_name_in)

        # remove multiple underscores
        nice_name_in = re.sub(r"([_]+)", r"_", nice_name_in)

        # turn it to lower case
        nice_name_in = nice_name_in.lower()

        return nice_name_in

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
            self._nice_name = self._format_nice_name(self.name)

        return self._nice_name

    @validates("code")
    def _validate_code(self, key, code_in):
        """validates the given code value
        """

        # check if the code_in is None or empty string
        if code_in is None or code_in == "":
            # restore the value from nice_name and let it be reformatted
            #code_in = self.nice_name.upper()
            code_in = self.nice_name

        return self._format_code(str(code_in))

    @validates("created_by")
    def _validate_created_by(self, key, created_by_in):
        """validates the given created_by_in attribute
        """
        
        from stalker.models.auth import User

        if created_by_in is not None:
            if not isinstance(created_by_in, User):
                raise TypeError("%s.created_by should be an instance of"
                                "stalker.models.auth.User" %
                                self.__class__.__name__)
        
        return created_by_in

    @validates("updated_by")
    def _validate_updated_by(self, key, updated_by_in):
        """validates the given updated_by_in attribute
        """
        
        from stalker.models.auth import User

        if updated_by_in is None:
            # set it to what created_by attribute has
            updated_by_in = self.created_by

        if updated_by_in is not None:
            if not isinstance(updated_by_in, User):
                raise TypeError("%s.updated_by should be an instance of"
                                "stalker.models.auth.User" %
                                self.__class__.__name__)

        return updated_by_in

    @validates("date_created")
    def _validate_date_created(self, key, date_created_in):
        """validates the given date_created_in
        """

        if date_created_in is None:
            raise TypeError("%s.date_created can not be None" %
                            self.__class__.__name__)

        if not isinstance(date_created_in, datetime.datetime):
            raise TypeError("%s.date_created should be an instance of "
                            "datetime.datetime" % self.__class__.__name__)

        return date_created_in

    @validates("date_updated")
    def _validate_date_updated(self, key, date_updated_in):
        """validates the given date_updated_in
        """

        # it is None
        if date_updated_in is None:
            raise TypeError("%s.date_updated can not be None" %
                            self.__class__.__name__)

        # it is not an instance of datetime.datetime
        if not isinstance(date_updated_in, datetime.datetime):
            raise TypeError("%s.date_updated should be an instance of "
                            "datetime.datetime" % self.__class__.__name__)

        # lower than date_created
        if date_updated_in < self.date_created:
            raise ValueError("%s.date_updated could not be set to a date "
                             "before 'date_created', try setting the "
                             "'date_created' before" %
                             self.__class__.__name__)

        return date_updated_in

    @validates("type")
    def _validate_type(self, key, type_in):
        """validates the given type value
        """
        
        from stalker.models.type import Type

        raise_error = False

        if not self.__strictly_typed__:
            if type_in is not None:
                if not isinstance(type_in, Type):
                    raise_error = True
        else:
            if not isinstance(type_in, Type):
                raise_error = True

        if raise_error:
            raise TypeError("%s.type must be an instance of "
                            "stalker.models.type.Type not %s" %
                            (self.__class__.__name__, type_in))

        return type_in

    def __eq__(self, other):
        """the equality operator
        """

        return isinstance(other, SimpleEntity) and\
               self.name == other.name #and \
        #self.description == other.description

    def __ne__(self, other):
        """the inequality operator
        """

        return not self.__eq__(other)


class Entity(SimpleEntity):
    """Another base data class that adds tags and notes to the attributes list.
    
    This is the entity class which is derived from the SimpleEntity and adds
    only tags to the list of parameters.
    
    Two Entities considered equal if they have the same name. It doesn't matter
    if they have different tags or notes.
    
    :param list tags: A list of :class:`~stalker.models.tag.Tag` objects
      related to this entity. tags could be an empty list, or when omitted it
      will be set to an empty list.
    
    :param list notes: A list of :class:`~stalker.models.note.Note` instances.
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
        
        It is a list of :class:`~stalker.models.tag.Tag` instances which shows
        the tags of this object"""
    )

    notes = relationship(
        "Note",
        primaryjoin="Entities.c.id==Notes.c.entity_id",
        backref="entity",
        doc="""All the :class:`~stalker.models.note.Notes`\ s attached to this entity.
        
        It is a list of :class:`~stalker.models.note.Note` instances or an
        empty list, setting it None will raise a TypeError.
        """
    )

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

    @reconstructor
    def __init_on_load__(self):
        """initialized the instance variables when the instance created with
        SQLAlchemy
        """

        super(Entity, self).__init_on_load__()

    @validates("notes")
    def _validate_notes(self, key, note):
        """validates the given note value
        """
        
        from stalker.models.note import Note

        if not isinstance(note, Note):
            raise TypeError("%s.note should be an instance of "
                            "stalker.models.note.Note not %s" %
                            (self.__class__.__name__,
                             note.__class__.__name__))

        return note

    @validates("tags")
    def _validate_tags(self, key, tag):
        """validates the given tag
        """
        
        from stalker.models.tag import Tag

        if not isinstance(tag, Tag):
            raise TypeError("%s.tag should be an instance of "
                            "stalker.models.tag.Tag not %s" %
                            (self.__class__.__name__,
                             tag.__class__.__name__))

        return tag
    
    def __eq__(self, other):
        """the equality operator
        """

        return super(Entity, self).__eq__(other) and \
               isinstance(other, Entity)


class TaskableEntity(Entity, ProjectMixin):
    """Gives the ability to connect to a list of :class:`~stalker.models.task.Task`\ s to the mixed in object.
    
    TaskMixin is a variant of :class:`~stalker.models.mixins.ProjectMixin` and
    lets the mixed object to have :class:`~stalker.model.task.Task` instances
    to be attached it self. And because :class:`~stalker.models.task.Task`\ s
    are related to :class:`~stalker.models.project.Project`\ s, it also adds
    ability to relate the object to a :class:`~stalker.models.project.Project`
    instance. So every object which is mixed with TaskMixin will have a
    :attr:`~stalker.models.mixins.TaskMixin.tasks` and a
    :attr:`~stalker.models.mixins.TaskMixin.project` attribute. Only the
    ``project`` argument needs to be initialized. See the
    :class:`~stalker.models.mixins.ProjectMixin` for more detail.
    """

    __tablename__ = "TaskableEntities"
    __mapper_args__ = {"polymorphic_identity": "TaskableEntity"}
    taskableEntity_id = Column("id", Integer, ForeignKey("Entities.id"),
                               primary_key=True)
    
    tasks = relationship(
        "Task",
        primaryjoin="TaskableEntities.c.id==Tasks.c.task_of_id",
        #backref="task_of",
        back_populates="task_of",
        post_update=True,
    )

    def __init__(self, tasks=None, **kwargs):
        super(TaskableEntity, self).__init__(**kwargs)
        ProjectMixin.__init__(self, **kwargs)

        if tasks is None:
            tasks = []
        self.tasks = tasks

    @validates("tasks")
    def _validate_tasks(self, key, task):
        """validates the given task value
        """
        
        from stalker.models.task import Task
        
        if not isinstance(task, Task):
            raise TypeError("tasks should be a list of "
                            "stalker.models.task.Task instances")

        return task


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

# SIMPLEENTITY_GENERICDATA
SimpleEntity_GenericData = Table(
   'SimpleEntity_GenericData', Base.metadata,
   Column(
        'simple_entity_id',
       Integer,
       ForeignKey('SimpleEntities.id'),
       primary_key=True
   ),
   Column(
       'other_simple_entity_id',
       Integer,
       ForeignKey('SimpleEntities.id'),
       primary_key=True
   )
)
