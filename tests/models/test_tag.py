# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2017 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# Stalker is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# Stalker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with Stalker.  If not, see <http://www.gnu.org/licenses/>

from stalker import Tag, SimpleEntity


def test___auto_name__class_attribute_is_set_to_false():
    """testing if the __auto_name__ class attribute is set to False for Tag
    class
    """
    assert Tag.__auto_name__ is False


def test_tag_init():
    """testing if tag inits properly
    """
    # this should work without any error
    tag = Tag(
        name="a test tag",
        description="this is a test tag"
    )
    assert isinstance(tag, Tag)


def test_equality():
    """testing the equality of two Tags
    """
    kwargs = dict(
        name="a test tag",
        description="this is a test tag"
    )

    simple_entity = SimpleEntity(**kwargs)

    a_tag_object1 = Tag(**kwargs)
    a_tag_object2 = Tag(**kwargs)

    kwargs["name"] = "a new test Tag"
    kwargs["description"] = "this is a new test Tag"

    a_tag_object3 = Tag(**kwargs)

    assert a_tag_object1 == a_tag_object2
    assert not a_tag_object1 == a_tag_object3
    assert not a_tag_object1 == simple_entity


def test_inequality():
    """testing the inequality of two Tags
    """
    kwargs = dict(
        name="a test tag",
        description="this is a test tag"
    )

    simple_entity = SimpleEntity(**kwargs)

    a_tag_object1 = Tag(**kwargs)
    a_tag_object2 = Tag(**kwargs)

    kwargs["name"] = "a new test Tag"
    kwargs["description"] = "this is a new test Tag"

    a_tag_object3 = Tag(**kwargs)

    assert not a_tag_object1 != a_tag_object2
    assert a_tag_object1 != a_tag_object3
    assert a_tag_object1 != simple_entity


def test_plural_class_name():
    """testing the plural name of Tag class
    """
    kwargs = dict(
        name="a test tag",
        description="this is a test tag"
    )
    test_tag = Tag(**kwargs)
    assert test_tag.plural_class_name == "Tags"
