# -*- coding: utf-8 -*-
"""Tests for the SimpleEntity class."""
import json
import datetime

import pytest

import pytz

import stalker

from stalker import (
    Department,
    Link,
    Project,
    Repository,
    SimpleEntity,
    Structure,
    Type,
    User,
)
from stalker.db.session import DBSession


# create a new class deriving from the SimpleEntity
class NewClass(SimpleEntity):
    __strictly_typed__ = True


@pytest.fixture(scope="function")
def setup_simple_entity_tests():
    """Set up some proper values for SimpleEntity tests."""
    # create a user
    data = dict()
    data["test_user"] = User(
        name="Test User",
        login="testuser",
        email="test@user.com",
        password="test",
        generic_text=json.dumps({"Phone number": "123"}, sort_keys=True),
    )

    data["date_created"] = datetime.datetime(2010, 10, 21, 3, 8, 0, tzinfo=pytz.utc)
    data["date_updated"] = data["date_created"]

    data["kwargs"] = {
        "name": "Test Entity",
        "code": "TstEnt",
        "description": "This is a test entity, and this is a proper description for it",
        "created_by": data["test_user"],
        "updated_by": data["test_user"],
        "date_created": data["date_created"],
        "date_updated": data["date_updated"],
        "generic_text": json.dumps({"Phone number": "123"}, sort_keys=True),
    }

    # create a proper SimpleEntity to use it later in the tests
    data["test_simple_entity"] = SimpleEntity(**data["kwargs"])

    data["test_type"] = Type(
        name="Test Type", code="test", target_entity_type="SimpleEntity"
    )

    return data


def test___auto_name__attr_is_true():
    """__auto_name__ class attr is set to True."""
    assert SimpleEntity.__auto_name__ is True


def test_name_arg_is_none(setup_simple_entity_tests):
    """name attr automatically generated if the name arg is None."""
    data = setup_simple_entity_tests
    data["kwargs"]["name"] = None
    new_simple_entity = SimpleEntity(**data["kwargs"])
    assert new_simple_entity.name is not None


def test_name_attr_is_set_to_none(setup_simple_entity_tests):
    """name attr set to an automatic value if it is set to None."""
    data = setup_simple_entity_tests
    data["test_simple_entity"].name = ""
    assert data["test_simple_entity"].name is not None


def test_name_attr_is_set_to_none_2(setup_simple_entity_tests):
    """name attr set to an automatic value if it is set to None."""
    data = setup_simple_entity_tests
    assert data["test_simple_entity"].name != ""


def test_name_arg_is_empty_string(setup_simple_entity_tests):
    """name attr set to an automatic value if the name arg is an empty string."""
    data = setup_simple_entity_tests
    data["kwargs"]["name"] = ""
    new_simple_entity = SimpleEntity(**data["kwargs"])
    assert new_simple_entity.name != ""


def test_name_attr_is_set_to_empty_string(setup_simple_entity_tests):
    """name attr set to an automatic value if it is set to an automatic value."""
    data = setup_simple_entity_tests
    data["test_simple_entity"].name = ""
    assert data["test_simple_entity"].name != ""


@pytest.mark.parametrize("test_value", [12132, [1, "name"], {"a": "name"}])
def test_name_arg_is_not_a_string_instance_or_none(
    test_value, setup_simple_entity_tests
):
    """TypeError raised if the name arg is not a string or None."""
    data = setup_simple_entity_tests
    data["kwargs"]["name"] = test_value
    with pytest.raises(TypeError) as _:
        SimpleEntity(**data["kwargs"])


@pytest.mark.parametrize("test_value", [12132, [1, "name"], {"a": "name"}])
def test_name_attr_is_not_string_or_none(test_value, setup_simple_entity_tests):
    """TypeError raised if the name attr is not a string or None."""
    data = setup_simple_entity_tests
    with pytest.raises(TypeError) as _:
        data["test_simple_entity"].name = test_value


@pytest.mark.parametrize(
    "test_value",
    [
        ("testName", "testName"),
        ("test-Name", "test-Name"),
        ("1testName", "1testName"),
        ("_testName", "_testName"),
        ("2423$+^^+^'%+%%&_testName", "2423$+^^+^'%+%%&_testName"),
        ("2423$+^^+^'%+%%&_testName_35", "2423$+^^+^'%+%%&_testName_35"),
        ("2423$ +^^+^ '%+%%&_ testName_ 35", "2423$ +^^+^ '%+%%&_ testName_ 35"),
        ("SH001", "SH001"),
        ("46-BJ-3A", "46-BJ-3A"),
        ("304-sb-0403-0040", "304-sb-0403-0040"),
        ("Ozgur    Yilmaz\n\n\n", "Ozgur Yilmaz"),
        ("     Ozgur Yilmaz    ", "Ozgur Yilmaz"),
    ],
)
def test_name_attr_is_formatted_correctly(test_value, setup_simple_entity_tests):
    """name is formatted correctly"""
    data = setup_simple_entity_tests
    # set the new name
    data["test_simple_entity"].name = test_value[0]
    assert data["test_simple_entity"].name == test_value[1]


@pytest.mark.parametrize(
    "test_value",
    [
        ("testName", "testName"),
        ("1testName", "1testName"),
        ("_testName", "testName"),
        ("2423$+^^+^'%+%%&_testName", "2423_testName"),
        ("2423$+^^+^'%+%%&_testName_35", "2423_testName_35"),
        ("2423$ +^^+^ '%+%%&_ testName_ 35", "2423_testName_35"),
        ("SH001", "SH001"),
        ("My name is Ozgur", "My_name_is_Ozgur"),
        (" this is another name for an asset", "this_is_another_name_for_an_asset"),
        ("Ozgur    Yilmaz\n\n\n", "Ozgur_Yilmaz"),
    ],
)
def test_nice_name_attr_is_formatted_correctly(test_value, setup_simple_entity_tests):
    """nice name attr is formatted correctly."""
    data = setup_simple_entity_tests
    data["test_simple_entity"].name = test_value[0]
    assert data["test_simple_entity"].nice_name == test_value[1]


def test_nice_name_attr_is_read_only(setup_simple_entity_tests):
    """nice name attr is read-only."""
    data = setup_simple_entity_tests
    with pytest.raises(AttributeError) as cm:
        data["test_simple_entity"].nice_name = "a text"
    assert str(cm.value) == "can't set attribute 'nice_name'"


def test_description_arg_none(setup_simple_entity_tests):
    """description property converted to an empty string if description arg is None."""
    data = setup_simple_entity_tests
    data["kwargs"]["description"] = None
    new_simple_entity = SimpleEntity(**data["kwargs"])
    assert new_simple_entity.description == ""


def test_description_attr_none(setup_simple_entity_tests):
    """description attr converted to an empty string if it is set to None."""
    data = setup_simple_entity_tests
    data["test_simple_entity"].description = None
    assert data["test_simple_entity"].description == ""


def test_description_arg_is_not_a_string(setup_simple_entity_tests):
    """TypeError raised if the description arg value is not a string."""
    data = setup_simple_entity_tests
    data["kwargs"]["description"] = {"a": "description"}
    with pytest.raises(TypeError) as cm:
        SimpleEntity(**data["kwargs"])

    assert str(cm.value) == "SimpleEntity.description should be a string, not dict"


def test_description_attr_is_not_a_string(setup_simple_entity_tests):
    """TypeError raised if the description attr value is not a str."""
    data = setup_simple_entity_tests
    with pytest.raises(TypeError) as cm:
        data["test_simple_entity"].description = ["a description"]
    assert str(cm.value) == "SimpleEntity.description should be a string, not list"


def test_generic_text_arg_none(setup_simple_entity_tests):
    """generic_text value converted to an empty string if generic_text arg is None."""
    data = setup_simple_entity_tests
    data["kwargs"]["generic_text"] = None
    new_simple_entity = SimpleEntity(**data["kwargs"])
    assert new_simple_entity.generic_text == ""


def test_generic_text_attr_none(setup_simple_entity_tests):
    """generic_text attr converted to an empty string if it is set to None."""
    data = setup_simple_entity_tests
    data["test_simple_entity"].generic_text = None
    assert data["test_simple_entity"].generic_text == ""


def test_generic_text_arg_is_not_a_string(setup_simple_entity_tests):
    """TypeError raised if the generic_text arg value is not a string."""
    data = setup_simple_entity_tests
    data["kwargs"]["generic_text"] = {"a": "generic_text"}
    with pytest.raises(TypeError) as cm:
        SimpleEntity(**data["kwargs"])

    assert str(cm.value) == "SimpleEntity.generic_text should be a string, not dict"


def test_generic_text_attr_is_not_a_string(setup_simple_entity_tests):
    """TypeError raised if the generic_text attr is set not to a str."""
    data = setup_simple_entity_tests
    with pytest.raises(TypeError) as _:
        data["test_simple_entity"].generic_text = ["a generic_text"]


def test_equality(setup_simple_entity_tests):
    """equality of two simple entities."""
    # create two simple entities with same parameters and check for equality
    data = setup_simple_entity_tests
    se1 = SimpleEntity(**data["kwargs"])
    se2 = SimpleEntity(**data["kwargs"])

    data["kwargs"]["name"] = "a different simple entity"
    data["kwargs"]["description"] = "no description"
    se3 = SimpleEntity(**data["kwargs"])
    assert se1 == se2
    assert not se1 == se3


def test_inequality(setup_simple_entity_tests):
    """inequality of two simple entities."""
    data = setup_simple_entity_tests
    # create two simple entities with same parameters and check for
    # equality
    se1 = SimpleEntity(**data["kwargs"])
    se2 = SimpleEntity(**data["kwargs"])

    data["kwargs"]["name"] = "a different simple entity"
    data["kwargs"]["description"] = "no description"
    se3 = SimpleEntity(**data["kwargs"])

    assert not se1 != se2
    assert se1 != se3


def test_created_by_arg_is_not_a_user_instance(setup_simple_entity_tests):
    """TypeError is raised if created_by arg is not a User instance."""
    data = setup_simple_entity_tests
    # the created_by arg should be an instance of User class, in any
    # other case it should raise a TypeError
    test_value = "A User Name"

    # be sure that the test value is not an instance of User
    assert not isinstance(test_value, User)

    # check the value
    with pytest.raises(TypeError) as cm:
        data["test_simple_entity"].created_by = test_value

    assert str(cm.value) == (
        "SimpleEntity.created_by should be a stalker.models.auth.User instance, not str"
    )


def test_created_by_attr_instance_of_user(setup_simple_entity_tests):
    """TypeError is raised if created_by attr is set to a value other than a User."""
    data = setup_simple_entity_tests
    # the created_by attr should be an instance of User class, in any
    # other case it should raise a TypeError
    test_value = "A User Name"

    # be sure that the test value is not an instance of User
    assert not isinstance(test_value, User)

    # check the value
    with pytest.raises(TypeError) as cm:
        data["test_simple_entity"].created_by = test_value

    assert str(cm.value) == (
        "SimpleEntity.created_by should be a stalker.models.auth.User instance, not str"
    )


def test_updated_by_arg_instance_of_user(setup_simple_entity_tests):
    """TypeError is raised if updated_by arg is not a User instance."""
    data = setup_simple_entity_tests
    # the updated_by arg should be an instance of User class, in any
    # other case it should raise a TypeError
    test_value = "A User Name"

    # be sure that the test value is not an instance of User
    assert not isinstance(test_value, User)

    # check the value
    with pytest.raises(TypeError) as cm:
        data["test_simple_entity"].updated_by = test_value

    assert str(cm.value) == (
        "SimpleEntity.updated_by should be a stalker.models.auth.User instance, not str"
    )


def test_updated_by_attr_instance_of_user(setup_simple_entity_tests):
    """TypeError is raised if update_by attr set to a value other than a User."""
    data = setup_simple_entity_tests
    # the updated_by attr should be an instance of User class, in any
    # other case it should raise a TypeError
    test_value = "A User Name"

    # be sure that the test value is not an instance of User
    assert not isinstance(test_value, User)

    # check the value
    with pytest.raises(TypeError) as cm:
        data["test_simple_entity"].updated_by = test_value

    assert str(cm.value) == (
        "SimpleEntity.updated_by should be a stalker.models.auth.User instance, not str"
    )


def test_updated_by_arg_empty(setup_simple_entity_tests):
    """updated_by arg is None it is equal to created_by arg."""
    data = setup_simple_entity_tests
    data["kwargs"]["updated_by"] = None
    new_simple_entity = SimpleEntity(**data["kwargs"])
    # now check if they are same
    assert new_simple_entity.created_by == new_simple_entity.updated_by


def test_date_created_arg_accepts_datetime_only(setup_simple_entity_tests):
    """TypeError raised if the date_created arg is not a datetime instance."""
    data = setup_simple_entity_tests
    # the date_created arg should be an instance of datetime.datetime
    # try to set something else and expect a TypeError
    test_value = "a string date time 2010-10-26 etc."

    # be sure that the test_value is not an instance of datetime.datetime
    assert not isinstance(test_value, datetime.datetime)

    with pytest.raises(TypeError) as cm:
        data["test_simple_entity"].date_created = test_value

    assert str(cm.value) == (
        "SimpleEntity.date_created should be a datetime.datetime instance"
    )


def test_date_created_attr_accepts_datetime_only(setup_simple_entity_tests):
    """TypeError raised if the date_created attr is not a datetime instance."""
    data = setup_simple_entity_tests
    # the date_created attr should be an instance of datetime.datetime
    # try to set something else and expect a TypeError
    test_value = "a string date time 2010-10-26 etc."
    # be sure that the test_value is not an instance of datetime.datetime
    assert not isinstance(test_value, datetime.datetime)
    with pytest.raises(TypeError) as cm:
        data["test_simple_entity"].date_created = test_value

    assert str(cm.value) == (
        "SimpleEntity.date_created should be a datetime.datetime instance"
    )


def test_date_created_attr_being_empty(setup_simple_entity_tests):
    """TypeError is raised if the date_created attr is set to None."""
    data = setup_simple_entity_tests
    with pytest.raises(TypeError) as cm:
        data["test_simple_entity"].date_created = None

    assert str(cm.value) == "SimpleEntity.date_created can not be None"


def test_date_updated_arg_accepts_datetime_only(setup_simple_entity_tests):
    """TypeError raised if the date_updated arg is not a datetime instance."""
    data = setup_simple_entity_tests
    # try to set it to something else and expect a TypeError
    test_value = "a string date time 2010-10-26 etc."

    # be sure that the test_value is not an instance of datetime.datetime
    assert not isinstance(test_value, datetime.datetime)

    with pytest.raises(TypeError) as cm:
        data["test_simple_entity"].date_updated = test_value

    assert str(cm.value) == (
        "SimpleEntity.date_updated should be a datetime.datetime instance"
    )


def test_date_updated_attr_being_datetime(setup_simple_entity_tests):
    """TypeError raised if the date_updated attr is not a datetime instance."""
    data = setup_simple_entity_tests
    # try to set something else and expect a TypeError
    test_value = "a string date time 2010-10-26 etc."

    # be sure that the test_value is not an instance of datetime.datetime
    assert not isinstance(test_value, datetime.datetime)

    with pytest.raises(TypeError) as cm:
        data["test_simple_entity"].date_updated = test_value

    assert str(cm.value) == (
        "SimpleEntity.date_updated should be a datetime.datetime instance"
    )


def test_date_updated_attr_is_set_to_none(setup_simple_entity_tests):
    """TypeError is raised if the date_updated attr is set to None."""
    data = setup_simple_entity_tests
    with pytest.raises(TypeError) as cm:
        data["test_simple_entity"].date_updated = "date_updated"
    assert str(cm.value) == (
        "SimpleEntity.date_updated should be a datetime.datetime instance"
    )


def test_date_updated_attr_is_working_properly(setup_simple_entity_tests):
    """date_updated attr is working properly."""
    data = setup_simple_entity_tests
    test_value = datetime.datetime.now(pytz.utc)
    data["test_simple_entity"].date_updated = test_value
    assert data["test_simple_entity"].date_updated == test_value


def test_date_created_is_before_date_updated(setup_simple_entity_tests):
    """ValueError raised if date_updated is set to a time before date_created."""
    data = setup_simple_entity_tests
    data["kwargs"]["date_created"] = datetime.datetime(
        2000, 1, 1, 1, 1, 1, tzinfo=pytz.utc
    )
    data["kwargs"]["date_updated"] = datetime.datetime(
        1990, 1, 1, 1, 1, 1, tzinfo=pytz.utc
    )

    # create a new entity with these dates
    # and expect a ValueError
    with pytest.raises(ValueError) as cm:
        SimpleEntity(**data["kwargs"])

    assert str(cm.value) == (
        "SimpleEntity.date_updated could not be set to a date before "
        "SimpleEntity.date_created, try setting the ``date_created`` first."
    )


def test___repr__(setup_simple_entity_tests):
    """__repr__ works properly."""
    data = setup_simple_entity_tests
    assert data["test_simple_entity"].__repr__() == "<{} ({})>".format(
        data["test_simple_entity"].name,
        data["test_simple_entity"].entity_type,
    )


def test_type_arg_is_none(setup_simple_entity_tests):
    """nothing will happen the type arg is None."""
    data = setup_simple_entity_tests
    data["kwargs"]["type"] = None
    new_simple_entity = SimpleEntity(**data["kwargs"])
    assert isinstance(new_simple_entity, SimpleEntity)


def test_type_attr_is_set_to_none(setup_simple_entity_tests):
    """nothing happened if the type attr is set to None."""
    data = setup_simple_entity_tests
    data["test_simple_entity"].type = None


@pytest.mark.parametrize("test_value", [1, 1.2, "a type"])
def test_type_arg_accepts_only_type_instances(test_value, setup_simple_entity_tests):
    """TypeError raised if type attr is not a Type instance."""
    data = setup_simple_entity_tests
    data["kwargs"]["type"] = test_value
    with pytest.raises(TypeError):
        SimpleEntity(**data["kwargs"])


def test_type_arg_accepts_type_instances(setup_simple_entity_tests):
    """no error raised if the type arg is a Type instance."""
    data = setup_simple_entity_tests
    # test with a proper Type
    data["kwargs"]["type"] = data["test_type"]
    # no error is expected
    new_simple_entity = SimpleEntity(**data["kwargs"])
    assert isinstance(new_simple_entity, SimpleEntity)


@pytest.mark.parametrize("test_value", [1, 1.2, "a type"])
def test_type_attr_accepts_only_type_instances(test_value, setup_simple_entity_tests):
    """TypeError raised type attr is not Type instance."""
    data = setup_simple_entity_tests
    with pytest.raises(TypeError):
        data["test_simple_entity"].type = test_value


def test_type_attr_accepts_type_instances(setup_simple_entity_tests):
    """no error raised if the type attr is set to Type instance."""
    data = setup_simple_entity_tests
    # test with a proper Type
    data["test_simple_entity"].type = data["test_type"]


def test___strictly_typed___class_attr_is_init_as_false(setup_simple_entity_tests):
    """__strictly_typed__ class attr is initialized as False."""
    data = setup_simple_entity_tests
    assert data["test_simple_entity"].__strictly_typed__ is False


def test___strictly_typed___attr_set_to_true_and_no_type_arg(setup_simple_entity_tests):
    """TypeError raised if __strictly_typed__ is True but no Type arg given."""
    data = setup_simple_entity_tests
    # create a new class deriving from the SimpleEntity
    assert NewClass.__strictly_typed__ is True

    # create a new instance and skip the Type attr and expect a
    # TypeError
    if "type" in data["kwargs"]:
        data["kwargs"].pop("type")

    with pytest.raises(TypeError) as cm:
        NewClass(**data["kwargs"])

    assert str(cm.value) == (
        "NewClass.type must be a stalker.models.type.Type instance, not None"
    )


def test___strictly_typed___attr_set_to_true_and_type_arg_is_none(
    setup_simple_entity_tests,
):
    """TypeError raised if __strictly_typed__ attr is True but Type arg is None."""
    data = setup_simple_entity_tests
    # set it to None and expect a TypeError
    data["kwargs"]["type"] = None
    with pytest.raises(TypeError) as cm:
        NewClass(**data["kwargs"])

    assert str(cm.value) == (
        "NewClass.type must be a stalker.models.type.Type instance, not None"
    )


@pytest.mark.parametrize("test_value", [1, 1.2, ["a", "list"], {"a": "dict"}])
def test___strictly_typed___attr_set_to_true_and_type_arg_is_not_type(
    test_value,
    setup_simple_entity_tests,
):
    """TypeError raised __strictly_typed__ is True but the type arg is not a str."""
    data = setup_simple_entity_tests
    data["kwargs"]["type"] = test_value
    with pytest.raises(TypeError):
        NewClass(**data["kwargs"])


def test___stalker_version__attr_is_automatically_set_to_the_current_stalker_version(
    setup_simple_entity_tests,
):
    """__stalker_version__ is automatically set for the newly created SimpleEntities."""
    data = setup_simple_entity_tests
    new_simple_entity = SimpleEntity(**data["kwargs"])
    assert new_simple_entity.__stalker_version__ == stalker.__version__

    # update stalker.__version__ to a test value
    current_version = stalker.__version__

    test_version = "test_version"
    stalker.__version__ = test_version

    # test if it is updated
    assert stalker.__version__ == test_version

    # create a new SimpleEntity and check if it is following the version
    new_simple_entity2 = SimpleEntity(**data["kwargs"])
    assert new_simple_entity2.__stalker_version__ == test_version

    # restore the stalker.__version__
    stalker.__version__ = current_version


def test_thumbnail_arg_is_skipped(setup_simple_entity_tests):
    """thumbnail attr None if the thumbnail arg is skipped."""
    data = setup_simple_entity_tests
    try:
        data["kwargs"].pop("thumbnail")
    except KeyError:
        pass

    new_simple_entity = SimpleEntity(**data["kwargs"])
    assert new_simple_entity.thumbnail is None


def test_thumbnail_arg_is_none(setup_simple_entity_tests):
    """thumbnail arg can be None."""
    data = setup_simple_entity_tests
    data["kwargs"]["thumbnail"] = None
    new_simple_entity = SimpleEntity(**data["kwargs"])
    assert new_simple_entity.thumbnail is None


def test_thumbnail_attr_is_none(setup_simple_entity_tests):
    """thumbnail attr can be set to None."""
    data = setup_simple_entity_tests
    data["test_simple_entity"].thumbnail = None
    assert data["test_simple_entity"].thumbnail is None


def test_thumbnail_arg_is_not_a_link_instance(setup_simple_entity_tests):
    """TypeError raised if the thumbnail arg is not a Link instance."""
    data = setup_simple_entity_tests
    data["kwargs"]["thumbnail"] = "not a Link"
    with pytest.raises(TypeError) as cm:
        SimpleEntity(**data["kwargs"])

    assert str(cm.value) == (
        "SimpleEntity.thumbnail should be a stalker.models.link.Link instance, not str"
    )


def test_thumbnail_attr_is_not_a_link_instance(setup_simple_entity_tests):
    """TypeError raised if the thumbnail is not a Link instance."""
    data = setup_simple_entity_tests
    with pytest.raises(TypeError) as cm:
        data["test_simple_entity"].thumbnail = "not a Link"

    assert str(cm.value) == (
        "SimpleEntity.thumbnail should be a stalker.models.link.Link instance, not str"
    )


def test_thumbnail_arg_is_working_properly(setup_simple_entity_tests):
    """thumbnail arg value is passed to the thumbnail attr correctly."""
    data = setup_simple_entity_tests
    thumb = Link(full_path="some path")
    data["kwargs"]["thumbnail"] = thumb
    new_simple_entity = SimpleEntity(**data["kwargs"])
    assert new_simple_entity.thumbnail == thumb


def test_thumbnail_attr_is_working_properly(setup_simple_entity_tests):
    """thumbnail attr is working properly."""
    data = setup_simple_entity_tests
    thumb = Link(full_path="some path")
    assert not data["test_simple_entity"].thumbnail == thumb
    data["test_simple_entity"].thumbnail = thumb
    assert data["test_simple_entity"].thumbnail == thumb


def test_html_style_arg_is_skipped(setup_simple_entity_tests):
    """html_style arg is skipped the html_style attr an empty string."""
    data = setup_simple_entity_tests
    if "html_style" in data["kwargs"]:
        data["kwargs"].pop("html_style")
    se = SimpleEntity(**data["kwargs"])
    assert se.html_style == ""


def test_html_style_arg_is_none(setup_simple_entity_tests):
    """html_style arg is set to None the html_style attr an empty string."""
    data = setup_simple_entity_tests
    data["kwargs"]["html_style"] = None
    se = SimpleEntity(**data["kwargs"])
    assert se.html_style == ""


def test_html_style_attr_is_set_to_none(setup_simple_entity_tests):
    """html_style attr is set to None it an empty string."""
    data = setup_simple_entity_tests
    data["test_simple_entity"].html_style = None
    assert data["test_simple_entity"].html_style == ""


def test_html_style_arg_is_not_a_string(setup_simple_entity_tests):
    """TypeError raised if the html_style arg is not a string."""
    data = setup_simple_entity_tests
    data["kwargs"]["html_style"] = 123
    with pytest.raises(TypeError) as cm:
        SimpleEntity(**data["kwargs"])
    assert str(cm.value) == (
        "SimpleEntity.html_style should be a basestring instance, not int"
    )


def test_html_style_attr_is_not_set_to_a_string(setup_simple_entity_tests):
    """TypeError raised if the html_style attr is not set to a string."""
    data = setup_simple_entity_tests
    with pytest.raises(TypeError) as cm:
        data["test_simple_entity"].html_style = 34324
    assert str(cm.value) == (
        "SimpleEntity.html_style should be a basestring instance, not int"
    )


def test_html_style_arg_is_working_properly(setup_simple_entity_tests):
    """html_style arg value is correctly passed to the html_style attr."""
    data = setup_simple_entity_tests
    test_value = "width: 100px; color: purple; background-color: black"
    data["kwargs"]["html_style"] = test_value
    se = SimpleEntity(**data["kwargs"])
    assert se.html_style == test_value


def test_html_style_attr_is_working_properly(setup_simple_entity_tests):
    """html_style attr is working properly."""
    data = setup_simple_entity_tests
    test_value = "width: 100px; color: purple; background-color: black"
    data["test_simple_entity"].html_style = test_value
    assert data["test_simple_entity"].html_style == test_value


def test_html_class_arg_is_skipped(setup_simple_entity_tests):
    """html_class arg is skipped the html_class attr an empty string."""
    data = setup_simple_entity_tests
    if "html_class" in data["kwargs"]:
        data["kwargs"].pop("html_class")
    se = SimpleEntity(**data["kwargs"])
    assert se.html_class == ""


def test_html_class_arg_is_none(setup_simple_entity_tests):
    """html_class arg is set to None the html_class attr an empty string."""
    data = setup_simple_entity_tests
    data["kwargs"]["html_class"] = None
    se = SimpleEntity(**data["kwargs"])
    assert se.html_class == ""


def test_html_class_attr_is_set_to_none(setup_simple_entity_tests):
    """html_class attr is set to None it an empty string."""
    data = setup_simple_entity_tests
    data["test_simple_entity"].html_class = None
    assert data["test_simple_entity"].html_class == ""


def test_html_class_arg_is_not_a_string(setup_simple_entity_tests):
    """TypeError raised if the html_class arg is not a string."""
    data = setup_simple_entity_tests
    data["kwargs"]["html_class"] = 123
    with pytest.raises(TypeError) as cm:
        SimpleEntity(**data["kwargs"])
    assert str(cm.value) == (
        "SimpleEntity.html_class should be a basestring instance, not int"
    )


def test_html_class_attr_is_not_set_to_a_string(setup_simple_entity_tests):
    """TypeError raised if the html_class attr is not set to a string."""
    data = setup_simple_entity_tests
    with pytest.raises(TypeError) as cm:
        data["test_simple_entity"].html_class = 34324
    assert str(cm.value) == (
        "SimpleEntity.html_class should be a basestring instance, not int"
    )


def test_html_class_arg_is_working_properly(setup_simple_entity_tests):
    """html_class arg value is correctly passed to the html_class attr."""
    data = setup_simple_entity_tests
    test_value = "purple"
    data["kwargs"]["html_class"] = test_value
    se = SimpleEntity(**data["kwargs"])
    assert se.html_class == test_value


def test_html_class_attr_is_working_properly(setup_simple_entity_tests):
    """html_class attr is working properly."""
    data = setup_simple_entity_tests
    test_value = "purple"
    data["test_simple_entity"].html_class = test_value
    assert data["test_simple_entity"].html_class == test_value


def test_to_tjp_wil_raise_a_not_implemented_error(setup_simple_entity_tests):
    """calling to_tjp() method will raise a NotImplementedError."""
    data = setup_simple_entity_tests
    with pytest.raises(NotImplementedError):
        data["test_simple_entity"].to_tjp()


@pytest.fixture(scope="function")
def setup_simple_entity_db_tests(setup_postgresql_db):
    """set up the SimpleEntity tests wit a db."""
    data = dict()
    data["test_user"] = User(
        name="Test User",
        login="testuser",
        email="test@user.com",
        password="test",
        generic_text=json.dumps({"Phone number": "123"}, sort_keys=True),
    )
    DBSession.add(data["test_user"])
    DBSession.commit()

    data["date_created"] = datetime.datetime(2010, 10, 21, 3, 8, 0, tzinfo=pytz.utc)
    data["date_updated"] = data["date_created"]

    data["kwargs"] = {
        "name": "Test Entity",
        "code": "TstEnt",
        "description": "This is a test entity, and this is a proper \
        description for it",
        "created_by": data["test_user"],
        "updated_by": data["test_user"],
        "date_created": data["date_created"],
        "date_updated": data["date_updated"],
        "generic_text": json.dumps({"Phone number": "123"}, sort_keys=True),
    }
    return data


def test_generic_data_attr_can_hold_a_wide_variety_of_object_types(
    setup_simple_entity_db_tests,
):
    """generic_data attr can hold any kind of object as a list."""
    data = setup_simple_entity_db_tests
    new_simple_entity = SimpleEntity(**data["kwargs"])
    test_user = User(
        name="email",
        login="email",
        email="email@email.com",
        password="email",
    )

    test_department = Department(name="department1")

    test_repo = Repository(
        name="Test Repository",
        code="TR",
    )

    test_struct = Structure(name="Test Project Structure")

    test_proj = Project(
        name="Test Project 1",
        code="tp1",
        repository=test_repo,
        structure=test_struct,
    )

    new_simple_entity.generic_data.extend(
        [test_proj, test_struct, test_repo, test_department, test_user]
    )

    # now check if it is added to the database correctly
    del new_simple_entity

    new_simple_entity_db = SimpleEntity.query.filter_by(
        name=data["kwargs"]["name"]
    ).first()

    assert test_proj in new_simple_entity_db.generic_data
    assert test_struct in new_simple_entity_db.generic_data
    assert test_repo in new_simple_entity_db.generic_data
    assert test_department in new_simple_entity_db.generic_data
    assert test_user in new_simple_entity_db.generic_data
