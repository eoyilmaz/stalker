# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import validates
from stalker import ProjectMixin, Entity


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
    __tablename__ = 'Pages'
    __mapper_args__ = {'polymorphic_identity': 'Page'}
    page_id = Column('id', Integer, ForeignKey('Entities.id'),
                     primary_key=True)

    title = Column(Text)
    content = Column(Text)

    def __init__(self, title='', content='', project=None, **kwargs):
        kwargs['project'] = project
        super(Page, self).__init__(**kwargs)
        ProjectMixin.__init__(self, **kwargs)

        self.title = title
        self.content = content

    @validates('title')
    def _validate_title(self, key, title):
        """validates the given title value
        """
        from stalker import __string_types__
        if not isinstance(title, __string_types__):
            raise TypeError(
                '%(class)s.title should be a string, not %(title_class)s' %
                {
                    'class': self.__class__.__name__,
                    'title_class': title.__class__.__name__
                }
            )

        if not title:
            raise ValueError(
                '%(class)s.title can not be empty' %
                {
                    'class': self.__class__.__name__
                }
            )

        return title

    @validates('content')
    def _validate_content(self, key, content):
        """validates the given content value
        """
        if content is None:
            content = ''

        from stalker import __string_types__
        if not isinstance(content, __string_types__):
            raise TypeError(
                '%(class)s.content should be a string, not %(content_class)s' %
                {
                    'class': self.__class__.__name__,
                    'content_class': content.__class__.__name__
                }
            )

        return content
