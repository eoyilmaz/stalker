# -*- coding: utf-8 -*-

import datetime
import re
import uuid

import pytz
import functools

from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, validates

from stalker.db.declarative import Base
from stalker.db.types import GenericDateTime
from stalker.log import logging_level

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class SimpleEntity(Base):
    """The base class of all the others

    The ``SimpleEntity`` is the starting point of the Stalker Object Model, it
    starts by adding the basic information about an entity which are
    :attr:`.name`, :attr:`.description`, the audit information like
    :attr:`.created_by`, :attr:`.updated_by`, :attr:`.date_created`,
    :attr:`.date_updated` and a couple of naming attributes like
    :attr:`.nice_name` and last but not least the :attr:`.type` attribute which
    is very important for entities that needs a type.

    .. versionadded: 0.2.2.3
        :attr:`.html_style` and :attr:`.html_class` attributes:

        SimpleEntity instances now have two new attributes called
        :attr:`.html_style` and :attr:`.html_class` which can be used to store
        html styles and html classes per entity. (Hint: Can be used to colorize
        different type of Tasks in different colors or different statused tasks
        in different classes etc.)

    .. note::

       For derived classes if the
       :attr:`.SimpleEntity.type` needed to be specifically specified, that is
       it can not be None or nothing else then a :class:`.Type` instance, set
       the ``strictly_typed`` class attribute to True::

           class NewClass(SimpleEntity):
               __strictly_typed__ = True

       This will ensure that the derived class always have a proper
       :attr:`.SimpleEntity.type` attribute and can not be initialized without
       one.

    Two SimpleEntities considered to be equal if they have the same
    :attr:`.name`, the other attributes doesn't matter.

    .. versionadded:: 0.2.0
       Name attribute can be skipped. Starting from version 0.2.0 the ``name``
       attribute can be skipped. For derived classes use the ``__auto_name__``
       class attribute to control auto naming behaviour.

    :param string name: A string value that holds the name of this entity.
      It should not contain any white space at the beginning and at the end of
      the string. Valid characters are [a-zA-Z0-9\_/S].

      Advanced::

        For classes derived from the SimpleEntity, if an automatic name is
        desired, the ``__auto_name__`` class attribute can be set to True. Then
        Stalker will automatically generate a uuid4 sequence for the name
        attribute.

    :param str description: A string attribute that holds the description of
      this entity object, it could be an empty string, and it could not again
      have white spaces at the beginning and at the end of the string,
      again any given objects will be converted to strings

    :param str generic_text: A string attribute that holds any text based
      information that should be affiliated with this entity, it could be an
      empty string, and it could not again have white spaces at the beginning
      and at the end of the string, again any given objects will be converted
      to strings.

    :param created_by: The :class:`.User` who has created
      this object

    :type created_by: :class:`.User`

    :param updated_by: The :class:`.User` who has updated this object lastly.
      The created_by and updated_by attributes point the same object if this
      object is just created.

    :param date_created: The date that this object is created.

    :type date_created: :class:`datetime.datetime`

    :param date_updated: The date that this object is updated lastly. For newly
      created entities this is equal to date_created and the date_updated
      cannot point a date which is before date_created.

    :type date_updated: :class:`datetime.datetime`

    :param type: The type of the current SimpleEntity. Used across several
      places in Stalker. Can be None. The default value is None.

    :type type: :class:`.Type`
    """
    # auto generate name values
    __auto_name__ = True
    __strictly_typed__ = False

    # TODO: Allow the user to specify the formatting of the name attribute with
    #       a formatter function
    __name_formatter__ = None

    __tablename__ = "SimpleEntities"
    id = Column("id", Integer, primary_key=True)

    entity_type = Column(String(128), nullable=False)
    __mapper_args__ = {
        "polymorphic_on": entity_type,
        "polymorphic_identity": "SimpleEntity"
    }

    name = Column(
        String(256),
        nullable=False,
        doc="""Name of this object"""
    )

    description = Column(
        "description",
        Text,
        doc="""Description of this object."""
    )

    created_by_id = Column(
        "created_by_id",
        Integer,
        ForeignKey("Users.id", use_alter=True, name="xc"),
        doc="""The id of the :class:`.User` who has created this entity."""
    )

    created_by = relationship(
        "User",
        backref="entities_created",
        primaryjoin="SimpleEntity.created_by_id==User.user_id",
        post_update=True,
        doc="""The :class:`.User` who has created this object."""
    )

    updated_by_id = Column(
        "updated_by_id",
        Integer,
        ForeignKey("Users.id", use_alter=True, name="xu"),
        doc="""The id of the :class:`.User` who has updated this entity."""
    )

    updated_by = relationship(
        "User",
        backref="entities_updated",
        primaryjoin="SimpleEntity.updated_by_id==User.user_id",
        post_update=True,
        doc="""The :class:`.User` who has updated this object."""
    )

    date_created = Column(
        GenericDateTime,
        default=functools.partial(datetime.datetime.now, pytz.utc),
        doc="""A :class:`datetime.datetime` instance showing the creation date
        and time of this object."""
    )

    date_updated = Column(
        GenericDateTime,
        default=functools.partial(datetime.datetime.now, pytz.utc),
        doc="""A :class:`datetime.datetime` instance showing the update date
        and time of this object."""
        ,
    )

    type_id = Column(
        "type_id",
        Integer,
        ForeignKey("Types.id", use_alter=True, name="y"),
        doc="""The id of the :class:`.Type` of this entity. Mainly used by
        SQLAlchemy to create a Many-to-One relates between SimpleEntities and
        Types.
        """
    )

    type = relationship(
        "Type",
        primaryjoin="SimpleEntities.c.type_id==Types.c.id",
        post_update=True,
        doc="""The type of the object.

        It is a :class:`.Type` instance with a proper
        :attr:`.Type.target_entity_type`.
        """
    )

    generic_data = relationship(
        'SimpleEntity',
        secondary='SimpleEntity_GenericData',
        primaryjoin='SimpleEntities.c.id=='
                    'SimpleEntity_GenericData.c.simple_entity_id',
        secondaryjoin='SimpleEntity_GenericData.c.other_simple_entity_id=='
                      'SimpleEntities.c.id',
        post_update=True,
        doc='''This attribute can hold any kind of data which exists in SOM.
        '''
    )

    generic_text = Column(
        "generic_text",
        Text,
        doc="""This attribute can hold any text."""
    )

    thumbnail_id = Column(
        'thumbnail_id',
        Integer,
        ForeignKey('Links.id', use_alter=True, name='z')
    )

    thumbnail = relationship(
        'Link',
        primaryjoin='SimpleEntities.c.thumbnail_id==Links.c.id',
        post_update=True
    )

    html_style = Column(String(64), nullable=True, default='')
    html_class = Column(String(64), nullable=True, default='')

    __stalker_version__ = Column("stalker_version", String(256))

    def __init__(
            self,
            name=None,
            description="",
            generic_text="",
            type=None,
            created_by=None,
            updated_by=None,
            date_created=None,
            date_updated=None,
            thumbnail=None,
            html_style='',
            html_class='',
            **kwargs
    ):  # pylint: disable=W0613

        # name and nice_name
        self._nice_name = ""

        self.name = name

        self.description = description
        self.created_by = created_by
        self.updated_by = updated_by
        if date_created is None:
            date_created = datetime.datetime.now(pytz.utc)
        if date_updated is None:
            date_updated = date_created

        self.date_created = date_created
        self.date_updated = date_updated
        self.type = type
        self.thumbnail = thumbnail
        self.generic_text = generic_text
        self.html_style = html_style
        self.html_class = html_class

        import stalker
        self.__stalker_version__ = stalker.__version__

    def __repr__(self):
        """the representation of the SimpleEntity
        """
        return "<%s (%s)>" % (self.name, self.entity_type)

    def __eq__(self, other):
        """the equality operator
        """
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            return isinstance(other, SimpleEntity) and self.name == other.name

    def __ne__(self, other):
        """the inequality operator
        """
        return not self.__eq__(other)

    def __hash__(self):
        """the overridden __hash__ method
        """
        return hash(self.id) + 2 * hash(self.name) + 3 * hash(self.entity_type)

    @validates("description")
    def _validate_description(self, key, description):
        """validates the given description value
        """
        if description is None:
            description = ""

        from stalker import __string_types__
        if not isinstance(description, __string_types__):
            raise TypeError(
                '%s.description should be a string, not %s' %
                (self.__class__.__name__, description.__class__.__name__)
            )
        return description

    @validates("generic_text")
    def _validate_generic_text(self, key, generic_text):
        """validates the given generic_text value
        """
        if generic_text is None:
            generic_text = ""

        from stalker import __string_types__
        if not isinstance(generic_text, __string_types__):
            raise TypeError(
                '%s.generic_text should be a string, not %s' %
                (self.__class__.__name__, generic_text.__class__.__name__)
            )
        return generic_text

    @validates("name")
    def _validate_name(self, key, name):
        """validates the given name_in value
        """
        if self.__auto_name__:
            if name is None or name == '':
                # generate a uuid4
                name = '%s_%s' % (self.__class__.__name__,
                                  uuid.uuid4().urn.split(':')[2])

        # it is None
        if name is None:
            raise TypeError(
                "%s.name can not be None" % self.__class__.__name__
            )

        from stalker import __string_types__
        if not isinstance(name, __string_types__):
            raise TypeError(
                "%s.name should be a string not %s" %
                (self.__class__.__name__, name.__class__.__name__)
            )

        name = self._format_name(name)

        # it is empty
        if name == "":
            raise ValueError(
                "%s.name can not be an empty string" % self.__class__.__name__
            )

        # also set the nice_name
        self._nice_name = self._format_nice_name(name)

        return name

    @classmethod
    def _format_name(cls, name_in):
        """formats the name_in value
        """
        # remove unnecessary characters from the string
        name_in = name_in.strip()

        # remove multiple spaces
        name_in = re.sub(r'[\s]+', ' ', name_in)

        return name_in

    @classmethod
    def _format_nice_name(cls, nice_name_in):
        """formats the given nice name
        """
        # remove unnecessary characters from the string
        nice_name_in = nice_name_in.strip()
        nice_name_in = re.sub(r'([^a-zA-Z0-9\s_\-@]+)', '',
                              nice_name_in).strip()

        # remove all the characters which are not alphabetic from the start of
        # the string
        nice_name_in = re.sub(r"(^[^a-zA-Z0-9]+)", '', nice_name_in)

        # remove multiple spaces
        nice_name_in = re.sub(r'[\s]+', ' ', nice_name_in)

        # # replace camel case letters
        # nice_name_in = re.sub(r"(.+?[a-z]+)([A-Z])", r"\1_\2", nice_name_in)

        # replace white spaces and dashes with under score
        nice_name_in = re.sub("([ -])+", r"_", nice_name_in)

        # remove multiple underscores
        nice_name_in = re.sub(r"([_]+)", r"_", nice_name_in)

        return nice_name_in

    @property
    def nice_name(self):
        """Nice name of this object.

        It has the same value with the name (contextually) but with a different
        format like, all the white spaces replaced by underscores ("\_"), all
        the CamelCase form will be expanded by underscore (\_) characters and
        it is always lower case.
        """
        # also set the nice_name
        # if self._nice_name is None or self._nice_name == "":
        self._nice_name = self._format_nice_name(self.name)
        return self._nice_name

    @validates("created_by")
    def _validate_created_by(self, key, created_by_in):
        """validates the given created_by_in attribute
        """
        from stalker.models.auth import User

        if created_by_in is not None:
            if not isinstance(created_by_in, User):
                raise TypeError(
                    "%s.created_by should be a stalker.models.auth.User "
                    "instance, not %s" % (self.__class__.__name__,
                                          created_by_in.__class__.__name__)
                )
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
                raise TypeError(
                    "%s.updated_by should be a stalker.models.auth.User "
                    "instance, not %s" % (self.__class__.__name__,
                                          updated_by_in.__class__.__name__)
                )
        return updated_by_in

    @validates("date_created")
    def _validate_date_created(self, key, date_created_in):
        """validates the given date_created_in
        """
        if date_created_in is None:
            raise TypeError(
                "%s.date_created can not be None" % self.__class__.__name__
            )

        if not isinstance(date_created_in, datetime.datetime):
            raise TypeError(
                "%s.date_created should be a datetime.datetime instance" %
                self.__class__.__name__
            )

        return date_created_in

    @validates("date_updated")
    def _validate_date_updated(self, key, date_updated_in):
        """validates the given date_updated_in
        """
        # it is None
        if date_updated_in is None:
            raise TypeError(
                "%s.date_updated can not be None" % self.__class__.__name__
            )

        # it is not a datetime.datetime instance
        if not isinstance(date_updated_in, datetime.datetime):
            raise TypeError(
                "%s.date_updated should be a datetime.datetime instance" %
                self.__class__.__name__
            )

        # lower than date_created
        if date_updated_in < self.date_created:
            raise ValueError(
                "%(class)s.date_updated could not be set to a date before "
                "%(class)s.date_created, try setting the ``date_created`` "
                "first."
                % {'class': self.__class__.__name__}
            )
        return date_updated_in

    @validates("type")
    def _validate_type(self, key, type_in):
        """validates the given type value
        """
        check_for_type_class = True
        if not self.__strictly_typed__ and type_in is None:
            check_for_type_class = False

        if check_for_type_class:
            from stalker.models.type import Type
            if not isinstance(type_in, Type):
                raise TypeError(
                    "%s.type must be a stalker.models.type.Type instance, not "
                    "%s" % (self.__class__.__name__, type_in))
        return type_in

    @validates('thumbnail')
    def _validate_thumbnail(self, key, thumb):
        """validates the given thumb value
        """
        if thumb is not None:
            from stalker import Link

            if not isinstance(thumb, Link):
                raise TypeError(
                    '%s.thumbnail should be a stalker.models.link.Link '
                    'instance, not %s' %
                    (self.__class__.__name__, thumb.__class__.__name__)
                )
        return thumb

    @property
    def tjp_id(self):
        """returns TaskJuggler compatible id
        """
        return "%s_%s" % (self.__class__.__name__, self.id)

    @property
    def to_tjp(self):
        """renders a TaskJuggler compliant string used for TaskJuggler
        integration. Needs to be overridden in inherited classes.
        """
        raise NotImplementedError(
            'This property is not implemented in %s' % self.__class__.__name__
        )

    @validates('html_style')
    def _validate_html_style(self, key, html_style):
        """validates the given html_style value
        """
        if html_style is None:
            html_style = ''

        from stalker import __string_types__
        if not isinstance(html_style, __string_types__):
            raise TypeError(
                '%s.html_style should be a basestring instance, not %s' %
                (self.__class__.__name__, html_style.__class__.__name__)
            )
        return html_style

    @validates('html_class')
    def _validate_html_class(self, key, html_class):
        """validates the given html_class value
        """
        if html_class is None:
            html_class = ''

        from stalker import __string_types__
        if not isinstance(html_class, __string_types__):
            raise TypeError(
                '%s.html_class should be a basestring instance, not %s' %
                (self.__class__.__name__, html_class.__class__.__name__)
            )
        return html_class


class Entity(SimpleEntity):
    """Another base data class that adds tags and notes to the attributes list.

    This is the entity class which is derived from the SimpleEntity and adds
    only tags to the list of parameters.

    Two Entities considered equal if they have the same name. It doesn't matter
    if they have different tags or notes.

    :param list tags: A list of :class:`.Tag` objects related to this entity.
      tags could be an empty list, or when omitted it will be set to an empty
      list.

    :param list notes: A list of :class:`.Note` instances. Can be an empty
      list, or when omitted it will be set to an empty list, when set to None
      it will be converted to an empty list.
    """
    __auto_name__ = True
    __tablename__ = "Entities"
    __mapper_args__ = {"polymorphic_identity": "Entity"}
    entity_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                       primary_key=True)

    tags = relationship(
        "Tag",
        secondary="Entity_Tags",
        backref="entities",
        doc="""A list of tags attached to this object.

        It is a list of :class:`.Tag` instances which shows
        the tags of this object"""
    )

    notes = relationship(
        "Note",
        secondary="Entity_Notes",
        backref="entities",
        doc="""All the :class:`.Notes` s attached to this entity.

        It is a list of :class:`.Note` instances or an
        empty list, setting it to None will raise a TypeError.
        """
    )

    def __init__(self,
                 tags=None,
                 notes=None,
                 **kwargs):
        super(Entity, self).__init__(**kwargs)

        if tags is None:
            tags = []

        if notes is None:
            notes = []

        self.tags = tags
        self.notes = notes

    @validates("notes")
    def _validate_notes(self, key, note):
        """validates the given note value
        """
        from stalker.models.note import Note
        if not isinstance(note, Note):
            raise TypeError(
                "%s.note should be a stalker.models.note.Note instance, not "
                "%s" % (self.__class__.__name__, note.__class__.__name__)
            )
        return note

    @validates("tags")
    def _validate_tags(self, key, tag):
        """validates the given tag
        """
        from stalker.models.tag import Tag
        if not isinstance(tag, Tag):
            raise TypeError(
                "%s.tag should be a stalker.models.tag.Tag instance, not %s" %
                (self.__class__.__name__, tag.__class__.__name__)
            )
        return tag

    def __eq__(self, other):
        """the equality operator
        """
        return super(Entity, self).__eq__(other) \
            and isinstance(other, Entity)

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(Entity, self).__hash__()


class EntityGroup(Entity):
    """Groups a wide variety of objects together to let one easily reach them.

    :class:`.EntityGroup` helps grouping different types of entities together
    to let one easily reach to them.
    """

    __auto_name__ = True
    __tablename__ = "EntityGroups"
    __mapper_args__ = {"polymorphic_identity": "EntityGroup"}
    entity_group_id = Column("id", Integer, ForeignKey("Entities.id"),
                             primary_key=True)

    entities = relationship(
        "SimpleEntity",
        secondary="EntityGroup_Entities",
        # primaryjoin='EntityGroups.c.id=='
        #             'EntityGroup_Entities.c.entity_group_id',
        # secondaryjoin='EntityGroup_Entities.c.other_entity_id=='
        #               'SimpleEntities.c.id',
        post_update=True,
        backref="entity_groups",
        doc="""All the :class:`.SimpleEntity`s grouped in this EntityGroup.
        """
    )

    def __init__(self, entities=None, **kwargs):
        super(Entity, self).__init__(**kwargs)

        if entities is None:
            entities = []

        self.entities = entities

    @validates('entities')
    def _validate_entities(self, key, entity):
        """validates the given entity value
        """
        if not isinstance(entity, SimpleEntity):
            raise TypeError(
                '%s.entities should be a list of SimpleEntities, not %s' % (
                    self.__class__.__name__,
                    entity.__class__.__name__
                )
            )

        return entity

    def __eq__(self, other):
        """the equality operator
        """
        return super(SimpleEntity, self).__eq__(other) \
            and isinstance(other, EntityGroup)

    def __hash__(self):
        """the overridden __hash__ method
        """
        return super(SimpleEntity, self).__hash__()


# Entity Tags
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

# Entity Notes
Entity_Notes = Table(
    "Entity_Notes", Base.metadata,
    Column(
        "entity_id",
        Integer,
        ForeignKey("Entities.id"),
        primary_key=True,
    ),

    Column(
        "note_id",
        Integer,
        ForeignKey("Notes.id"),
        primary_key=True,
    )
)

# SimpleEntity Generic Data
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

# EntityGroup Entities
EntityGroup_Entities = Table(
    'EntityGroup_Entities', Base.metadata,
    Column(
        'entity_group_id',
        Integer,
        ForeignKey('EntityGroups.id'),
        primary_key=True
    ),
    Column(
        'other_entity_id',
        Integer,
        ForeignKey('SimpleEntities.id'),
        primary_key=True
    )
)
