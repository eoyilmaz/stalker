# -*- coding: utf-8 -*-
"""Wiki related functions and classes are situated here."""
from typing import Union

from six import string_types

from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import validates

from stalker import Entity, ProjectMixin


class Page(Entity, ProjectMixin):
    """A simple Wiki page implementation.

    Wiki in Stalker are managed per Project. That is, all Wiki pages are
    related to a Project.

    Stalker wiki pages are very simple in terms of data it holds. It has only
    one :attr:`.title` and one :attr:`.content` an some usual audit info coming
    from :class:`.SimpleEntity` and a :attr:`.project` coming from
    :class:`.ProjectMixin`.

    :param str title: The title of this Page
    :param str content: The content of this page. Can contain any kind of
      string literals including HTML tags etc.
    """

    __auto_name__ = True
    __tablename__ = "Pages"
    __mapper_args__ = {"polymorphic_identity": "Page"}
    page_id = Column("id", Integer, ForeignKey("Entities.id"), primary_key=True)

    title = Column(Text)
    content = Column(Text)

    def __init__(self, title="", content="", project=None, **kwargs):
        kwargs["project"] = project
        super(Page, self).__init__(**kwargs)
        ProjectMixin.__init__(self, **kwargs)

        self.title = title
        self.content = content

    @validates("title")
    def _validate_title(self, key: str, title: str) -> str:
        """Validate the given title value.

        Args:
            key (str): The name of the validated column.
            title (str): The title value to be validated.

        Raises:
            TypeError: If the given title is not a string.
            ValueError: If the title is an empty string.

        Returns:
            str: The validated title value.
        """
        if not isinstance(title, string_types):
            raise TypeError(
                "{}.title should be a string, not {}: '{}'".format(
                    self.__class__.__name__, title.__class__.__name__, title
                )
            )

        if not title:
            raise ValueError(f"{self.__class__.__name__}.title can not be empty")

        return title

    @validates("content")
    def _validate_content(self, key: str, content: Union[None, str]) -> str:
        """Validate the given content value.

        Args:
            key (str): The name of the validated column.
            content (Union[None, str]): The content value to be validated.

        Raises:
            TypeError: If the content is not None and not str.

        Returns:
            str: The validated content value.
        """
        content = "" if content is None else content
        if not isinstance(content, string_types):
            raise TypeError(
                "{}.content should be a string, not {}: '{}'".format(
                    self.__class__.__name__, content.__class__.__name__, content
                )
            )
        return content