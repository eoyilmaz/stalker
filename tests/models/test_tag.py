# -*- coding: utf-8 -*-

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
