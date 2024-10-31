# -*- coding: utf-8 -*-
"""SimpleEntity, Entity, EntityGroup and other related functions are situated here."""

import datetime
import functools
import re
import uuid

import pytz

from six import string_types

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship, validates

from stalker.db.declarative import Base
from stalker.db.types import GenericDateTime
from stalker.log import get_logger

logger = get_logger(__name__)


class SimpleEntity(Base):
    """The base class of all the others.

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
      the string. Valid characters are [a-zA-Z0-9_/S].

      Advanced::

        For classes derived from the SimpleEntity, if an automatic name is
        desired, the ``__auto_name__`` class attribute can be set to True. Then
        Stalker will automatically generate an uuid4 sequence for the name
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
        "polymorphic_identity": "SimpleEntity",
    }

    name = Column(String(256), nullable=False, doc="""Name of this object""")

    description = Column("description", Text, doc="""Description of this object.""")

    created_by_id = Column(
        "created_by_id",
        Integer,
        ForeignKey("Users.id", use_alter=True, name="xc"),
        doc="""The id of the :class:`.User` who has created this entity.""",
    )

    created_by = relationship(
        "User",
        backref="entities_created",
        primaryjoin="SimpleEntity.created_by_id==User.user_id",
        post_update=True,
        doc="""The :class:`.User` who has created this object.""",
    )

    updated_by_id = Column(
        "updated_by_id",
        Integer,
        ForeignKey("Users.id", use_alter=True, name="xu"),
        doc="""The id of the :class:`.User` who has updated this entity.""",
    )

    updated_by = relationship(
        "User",
        backref="entities_updated",
        primaryjoin="SimpleEntity.updated_by_id==User.user_id",
        post_update=True,
        doc="""The :class:`.User` who has updated this object.""",
    )

    date_created = Column(
        GenericDateTime,
        default=functools.partial(datetime.datetime.now, pytz.utc),
        doc="""A :class:`datetime.datetime` instance showing the creation date
        and time of this object.""",
    )

    date_updated = Column(
        GenericDateTime,
        default=functools.partial(datetime.datetime.now, pytz.utc),
        doc="""A :class:`datetime.datetime` instance showing the update date
        and time of this object.""",
    )

    type_id = Column(
        "type_id",
        Integer,
        ForeignKey("Types.id", use_alter=True, name="y"),
        doc="""The id of the :class:`.Type` of this entity. Mainly used by
        SQLAlchemy to create a Many-to-One relates between SimpleEntities and
        Types.
        """,
    )

    type = relationship(
        "Type",
        primaryjoin="SimpleEntities.c.type_id==Types.c.id",
        post_update=True,
        doc="""The type of the object.

        It is a :class:`.Type` instance with a proper
        :attr:`.Type.target_entity_type`.
        """,
    )

    generic_data = relationship(
        "SimpleEntity",
        secondary="SimpleEntity_GenericData",
        primaryjoin="SimpleEntities.c.id=="
        "SimpleEntity_GenericData.c.simple_entity_id",
        secondaryjoin="SimpleEntity_GenericData.c.other_simple_entity_id=="
        "SimpleEntities.c.id",
        post_update=True,
        doc="""This attribute can hold any kind of data which exists in SOM.
        """,
    )

    generic_text = Column(
        "generic_text", Text, doc="""This attribute can hold any text."""
    )

    thumbnail_id = Column(
        "thumbnail_id", Integer, ForeignKey("Links.id", use_alter=True, name="z")
    )

    thumbnail = relationship(
        "Link",
        primaryjoin="SimpleEntities.c.thumbnail_id==Links.c.id",
        post_update=True,
    )

    html_style = Column(String(64), nullable=True, default="")
    html_class = Column(String(64), nullable=True, default="")

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
        html_style="",
        html_class="",
        **kwargs,
    ):  # noqa: W0613

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
        """Return the str representation of this SimpleEntity.

        Returns:
            str: The str representation of this SimpleEntity.
        """
        return f"<{self.name} ({self.entity_type})>"

    def __eq__(self, other):
        """Check equality.

        Args:
            other (object): An object to check the equality of.

        Returns:
            bool: If the other is a SimpleEntity and its name equals to this one.
        """
        from stalker.db.session import DBSession

        with DBSession.no_autoflush:
            return isinstance(other, SimpleEntity) and self.name == other.name

    def __ne__(self, other):
        """Check inequality.

        This uses the __eq__ operator to get the inequality.

        Args:
            other (object): An object to check the inequality of.

        Returns:
            bool: True if other is not equal to this instance.
        """
        return not self.__eq__(other)

    def __hash__(self):
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return hash(self.id) + 2 * hash(self.name) + 3 * hash(self.entity_type)

    @validates("description")
    def _validate_description(self, key, description):
        """Validate the given description value.

        Args:
            key (str): The name of the validated column.
            description (str): The description value to be validated.

        Raises:
            TypeError: If the description is not None and not a str.

        Returns:
            str: The validated description value.
        """
        if description is None:
            description = ""

        if not isinstance(description, string_types):
            raise TypeError(
                "{}.description should be a string, not {}: '{}'".format(
                    self.__class__.__name__, description.__class__.__name__, description
                )
            )
        return description

    @validates("generic_text")
    def _validate_generic_text(self, key, generic_text):
        """Validate the given generic_text value.

        Args:
            key (str): The name of the validated column.
            generic_text (str): The generic_text value to be validated.

        Raises:
            TypeError: If the generic_text is not None and not a str.

        Returns:
            str: The validated generic_text value.
        """
        if generic_text is None:
            generic_text = ""

        if not isinstance(generic_text, string_types):
            raise TypeError(
                "{}.generic_text should be a string, not {}: '{}'".format(
                    self.__class__.__name__,
                    generic_text.__class__.__name__,
                    generic_text,
                )
            )
        return generic_text

    @validates("name")
    def _validate_name(self, key, name):
        """Validate the name value.

        Args:
            key (str): The name of the validated column.
            name (str): The name value to be validated.

        Raises:
            TypeError: If the name is not a str.
            ValueError: If the name becomes an empty str after formatting.

        Returns:
            str: The validated name value.
        """
        if self.__auto_name__:
            if name is None or name == "":
                # generate a uuid4
                name = "{}_{}".format(
                    self.__class__.__name__,
                    uuid.uuid4().urn.split(":")[2],
                )

        # it is None
        if name is None:
            raise TypeError(f"{self.__class__.__name__}.name can not be None")

        if not isinstance(name, string_types):
            raise TypeError(
                f"{self.__class__.__name__}.name should be a string, "
                f"not {name.__class__.__name__}: '{name}'"
            )

        name = self._format_name(name)

        # it is empty
        if name == "":
            raise ValueError(
                f"{self.__class__.__name__}.name can not be an empty string"
            )

        # also set the nice_name
        self._nice_name = self._format_nice_name(name)

        return name

    @classmethod
    def _format_name(cls, name):
        """Format the name value.

        Args:
            name (str): The name value.

        Returns:
            str: The formatted name value.
        """
        # remove unnecessary characters from the string
        name = name.strip()

        # remove multiple spaces
        name = re.sub(r"\s+", " ", name)

        return name

    @classmethod
    def _format_nice_name(cls, nice_name):
        """Format the given nice name value.

        Args:
            nice_name (str): The nice_name value to be formatted.

        Returns:
            str: The formatted nice name.
        """
        # remove unnecessary characters from the string
        nice_name = nice_name.strip()
        nice_name = re.sub(r"([^a-zA-Z0-9\s_\-@]+)", "", nice_name).strip()

        # remove all the characters which are not alphabetic from the start of
        # the string
        nice_name = re.sub(r"(^[^a-zA-Z0-9]+)", "", nice_name)

        # remove multiple spaces
        nice_name = re.sub(r"\s+", " ", nice_name)

        # # replace camel case letters
        # nice_name = re.sub(r"(.+?[a-z]+)([A-Z])", r"\1_\2", nice_name)

        # replace white spaces and dashes with underscore
        nice_name = re.sub("([ -])+", r"_", nice_name)

        # remove multiple underscores
        nice_name = re.sub(r"(_+)", r"_", nice_name)

        return nice_name

    @property
    def nice_name(self):
        """Nice name of this object.

        It has the same value with the name (contextually) but with a different
        format like, all the white spaces replaced by underscores ("_"), all the
        CamelCase form will be expanded by underscore (_) characters, and it is always
        lower case.

        Returns:
            str: The nice name value.
        """
        # also set the nice_name
        # if self._nice_name is None or self._nice_name == "":
        self._nice_name = self._format_nice_name(self.name)
        return self._nice_name

    @validates("created_by")
    def _validate_created_by(self, key, created_by):
        """Validate the given created_by value.

        Args:
            key (str): The name of the validated column.
            created_by (Union[None, User]): The created_by value to be validated.

        Raises:
            TypeError: If the created_by value is not None and not a
                :class:`stalker.models.auth.User` instance.

        Returns:
            Union [None, User]: The validated created_by value.
        """
        from stalker.models.auth import User

        if created_by is not None:
            if not isinstance(created_by, User):
                raise TypeError(
                    f"{self.__class__.__name__}.created_by should be a "
                    "stalker.models.auth.User instance, "
                    f"not {created_by.__class__.__name__}: '{created_by}'"
                )
        return created_by

    @validates("updated_by")
    def _validate_updated_by(self, key, updated_by):
        """Validate the given updated_by value.

        Args:
            key (str): The name of the validated column.
            updated_by (Union[None, User]): The updated_by value to be validated.

        Raises:
            TypeError: If the updated_by value is not None and not a
                :class:`stalker.models.auth.User` instance.

        Returns:
            Union [None, User]: The validated updated_by value.
        """
        from stalker.models.auth import User

        if updated_by is None:
            # set it to what created_by attribute has
            updated_by = self.created_by

        if updated_by is not None:
            if not isinstance(updated_by, User):
                raise TypeError(
                    f"{self.__class__.__name__}.updated_by should be a "
                    "stalker.models.auth.User instance, "
                    f"not {updated_by.__class__.__name__}: '{updated_by}'"
                )
        return updated_by

    @validates("date_created")
    def _validate_date_created(self, key, date_created):
        """Validate the given date_created value.

        Args:
            key (str): The name of the validated column.
            date_created (datetime.datetime): The value to be validated.

        Raises:
            TypeError: If the given date_created value is None or not a datetime
                instance.

        Returns:
            datetime.datetime: The validated date_created value.
        """
        if date_created is None:
            raise TypeError(f"{self.__class__.__name__}.date_created can not be None")

        if not isinstance(date_created, datetime.datetime):
            raise TypeError(
                f"{self.__class__.__name__}.date_created should be a "
                "datetime.datetime instance, "
                f"not {date_created.__class__.__name__}: '{date_created}'"
            )

        return date_created

    @validates("date_updated")
    def _validate_date_updated(self, key, date_updated):
        """Validate the given date_updated.

        Args:
            key (str): The name of the validated column.
            date_updated (datetime.datetime): The date_updated to be validated.

        Raises:
            TypeError: If the date_updated value is ``None`` or date_updated is
                not a ``datetime.datetime`` instance.
            ValueError: If the date_updated is before than the date_created.

        Returns:
            datetime.datetime: The validated datetime_updated value.
        """
        # it is None
        if date_updated is None:
            raise TypeError(f"{self.__class__.__name__}.date_updated can not be None")

        # it is not a datetime.datetime instance
        if not isinstance(date_updated, datetime.datetime):
            raise TypeError(
                f"{self.__class__.__name__}.date_updated should be a "
                "datetime.datetime instance, "
                f"not {date_updated.__class__.__name__}: '{date_updated}'"
            )

        # lower than date_created
        if date_updated < self.date_created:
            raise ValueError(
                "{class_name}.date_updated could not be set to a date before "
                "{class_name}.date_created, try setting the ``date_created`` "
                "first.".format(class_name=self.__class__.__name__)
            )
        return date_updated

    @validates("type")
    def _validate_type(self, key, type_):
        """Validate the given type value.

        Args:
            key (str): The name of the validated column.
            type_ (Type): The type value to be validated.

        Raises:
            TypeError: If this class is a strictly typed class and the type_ is not
                None and not a Type instance.

        Returns:
            Type: The validated type_ value.
        """
        if self.__strictly_typed__ or type_ is not None:
            from stalker.models.type import Type

            if not isinstance(type_, Type):
                raise TypeError(
                    f"{self.__class__.__name__}.type must be a "
                    "stalker.models.type.Type instance, "
                    f"not {type_.__class__.__name__}: '{type_}'"
                )
        return type_

    @validates("thumbnail")
    def _validate_thumbnail(self, key, thumb):
        """Validate the given thumb value.

        Args:
            key (str): The name of the validated column.
            thumb (Link): The thumb value to be validated.

        Raises:
            TypeError: If the given thumb value is not None and not a Link instance.

        Returns:
            Union[None, Link]: The validated thumb value.
        """
        if thumb is not None:
            from stalker import Link

            if not isinstance(thumb, Link):
                raise TypeError(
                    f"{self.__class__.__name__}.thumbnail should be a "
                    "stalker.models.link.Link instance, "
                    f"not {thumb.__class__.__name__}: '{thumb}'"
                )
        return thumb

    @property
    def tjp_id(self):
        """Return TaskJuggler compatible id.

        Returns:
            str: The TaskJuggler compatible id.
        """
        return f"{self.__class__.__name__}_{self.id}"

    @property
    def to_tjp(self):
        """Render a TaskJuggler compliant str used for TaskJuggler integration.

        Needs to be overridden in inherited classes.

        Raises:
            NotImplementedError: Always.
        """
        raise NotImplementedError(
            f"This property is not implemented in {self.__class__.__name__}"
        )

    @validates("html_style")
    def _validate_html_style(self, key, html_style):
        """Validate the given html_style value.

        Args:
            key (str): The name of the validated column.
            html_style (str): The html_style to be validated.

        Raises:
            TypeError: If the given html_style is not a str.

        Returns:
            str: The validated html_style value.
        """
        if html_style is None:
            html_style = ""

        if not isinstance(html_style, string_types):
            raise TypeError(
                f"{self.__class__.__name__}.html_style should be a basestring "
                f"instance, not {html_style.__class__.__name__}: '{html_style}'"
            )
        return html_style

    @validates("html_class")
    def _validate_html_class(self, key, html_class):
        """Validate the given html_class value.

        Args:
            key (str): The name of the validated column.
            html_class (str): The html_class to be validated.

        Raises:
            TypeError: If the html_class is not a str.

        Returns:
            str: The validated html_class value.
        """
        if html_class is None:
            html_class = ""

        if not isinstance(html_class, string_types):
            raise TypeError(
                f"{self.__class__.__name__}.html_class should be a basestring "
                f"instance, not {html_class.__class__.__name__}: '{html_class}'"
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
    entity_id = Column("id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True)

    tags = relationship(
        "Tag",
        secondary="Entity_Tags",
        backref="entities",
        doc="""A list of tags attached to this object.

        It is a list of :class:`.Tag` instances which shows
        the tags of this object""",
    )

    notes = relationship(
        "Note",
        secondary="Entity_Notes",
        backref="entities",
        doc="""All the :class:`.Notes` s attached to this entity.

        It is a list of :class:`.Note` instances or an
        empty list, setting it to None will raise a TypeError.
        """,
    )

    def __init__(self, tags=None, notes=None, **kwargs):
        super(Entity, self).__init__(**kwargs)

        if tags is None:
            tags = []

        if notes is None:
            notes = []

        self.tags = tags
        self.notes = notes

    @validates("notes")
    def _validate_notes(self, key, note):
        """Validate the given note value.

        Args:
            key (str): The name of the validated column.
            note (Note): The note value to be validated.

        Raises:
            TypeError: If the given note value is not a Note instance.

        Returns:
            Note: The validated note value.
        """
        from stalker.models.note import Note

        if not isinstance(note, Note):
            raise TypeError(
                f"{self.__class__.__name__}.note should be a stalker.models.note.Note "
                f"instance, not {note.__class__.__name__}: '{note}'"
            )
        return note

    @validates("tags")
    def _validate_tags(self, key, tag):
        """Validate the given tag value.

        Args:
            key (str): The name of the validated column.
            tag (Tag): The tag value to be validated.

        Raises:
            TypeError: If the given tag value is not a Tag instance.

        Returns:
            Tag: The validated tag value.
        """
        from stalker.models.tag import Tag

        if not isinstance(tag, Tag):
            raise TypeError(
                f"{self.__class__.__name__}.tag should be a stalker.models.tag.Tag "
                f"instance, not {tag.__class__.__name__}: '{tag}'"
            )
        return tag

    def __eq__(self, other):
        """Check if the other object is equal to this one.

        Args:
            other (object): An object.

        Returns:
            bool: True if the other object is also an Entity instance and has the same
                basic attribute values.
        """
        return super(Entity, self).__eq__(other) and isinstance(other, Entity)

    def __hash__(self):
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(Entity, self).__hash__()


class EntityGroup(Entity):
    """Groups a wide variety of objects together to let one easily reach them.

    :class:`.EntityGroup` helps to group different types of entities together to let one
    easily reach to them.
    """

    __auto_name__ = True
    __tablename__ = "EntityGroups"
    __mapper_args__ = {"polymorphic_identity": "EntityGroup"}
    entity_group_id = Column("id", Integer, ForeignKey("Entities.id"), primary_key=True)

    entities = relationship(
        "SimpleEntity",
        secondary="EntityGroup_Entities",
        post_update=True,
        backref="entity_groups",
        doc="""All the :class:`.SimpleEntity`s grouped in this EntityGroup.
        """,
    )

    def __init__(self, entities=None, **kwargs):
        super(Entity, self).__init__(**kwargs)

        if entities is None:
            entities = []

        self.entities = entities

    @validates("entities")
    def _validate_entities(self, key, entity):
        """Validate the given entity value.

        Args:
            key (str): The name of the validated column.
            entity (Entity): The entity value to be validated.

        Raises:
            TypeError: If the entity is not a SimpleEntity instance.

        Returns:
            SimpleEntity: The validated entity value.
        """
        if not isinstance(entity, SimpleEntity):
            raise TypeError(
                f"{self.__class__.__name__}.entities should be a list of "
                f"SimpleEntities, not {entity.__class__.__name__}: '{entity}'"
            )

        return entity

    def __eq__(self, other):
        """Check if the other is equal to this instance.

        Args:
            other (EntityGroup): The other EntityGroup to check the equality of.

        Returns:
            bool: True if the other is also a EntityGroup instance and has the same
                attribute values.
        """
        return super(SimpleEntity, self).__eq__(other) and isinstance(
            other, EntityGroup
        )

    def __hash__(self):
        """Return the hash value of this instance.

        Because the __eq__ is overridden the __hash__ also needs to be overridden.

        Returns:
            int: The hash value.
        """
        return super(SimpleEntity, self).__hash__()


# Entity Tags
Entity_Tags = Table(
    "Entity_Tags",
    Base.metadata,
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
    ),
)

# Entity Notes
Entity_Notes = Table(
    "Entity_Notes",
    Base.metadata,
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
    ),
)

# SimpleEntity Generic Data
SimpleEntity_GenericData = Table(
    "SimpleEntity_GenericData",
    Base.metadata,
    Column(
        "simple_entity_id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True
    ),
    Column(
        "other_simple_entity_id",
        Integer,
        ForeignKey("SimpleEntities.id"),
        primary_key=True,
    ),
)

# EntityGroup Entities
EntityGroup_Entities = Table(
    "EntityGroup_Entities",
    Base.metadata,
    Column("entity_group_id", Integer, ForeignKey("EntityGroups.id"), primary_key=True),
    Column(
        "other_entity_id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True
    ),
)