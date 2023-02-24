# -*- coding: utf-8 -*-

import os

import pytest

from stalker import Link, Type


@pytest.fixture(scope="function")
def setup_link_tests():
    """Set up the test for the Link class."""
    data = dict()

    # create a mock LinkType object
    data["test_link_type1"] = Type(
        name="Test Type 1",
        code="test type1",
        target_entity_type="Link",
    )
    data["test_link_type2"] = Type(
        name="Test Type 2",
        code="test type2",
        target_entity_type="Link",
    )

    data["kwargs"] = {
        "name": "An Image Link",
        "full_path": "C:/A_NEW_PROJECT/td/dsdf/22-fdfffsd-32342-dsf2332-dsfd-3.exr",
        "original_filename": "this_is_an_image.jpg",
        "type": data["test_link_type1"],
    }

    data["test_link"] = Link(**data["kwargs"])
    return data


def test___auto_name__class_attribute_is_set_to_true():
    """__auto_name__ class attribute is set to False for Link class."""
    assert Link.__auto_name__ is True


def test_full_path_argument_is_none(setup_link_tests):
    """full_path argument is None is set the full_path attribute to an empty string."""
    data = setup_link_tests
    data["kwargs"]["full_path"] = None
    new_link = Link(**data["kwargs"])
    assert new_link.full_path == ""


def test_full_path_attribute_is_set_to_none(setup_link_tests):
    """full_path attr to None is set its value to an empty string."""
    data = setup_link_tests
    data["test_link"].full_path = ""


def test_full_path_argument_is_empty_an_empty_string(setup_link_tests):
    """full_path attr is set to an empty str if full_path arg is an empty string."""
    data = setup_link_tests
    data["kwargs"]["full_path"] = ""
    new_link = Link(**data["kwargs"])
    assert new_link.full_path == ""


def test_full_path_attribute_is_set_to_empty_string(setup_link_tests):
    """full_path attr value is set to an empty string."""
    data = setup_link_tests
    data["test_link"].full_path = ""
    assert data["test_link"].full_path == ""


def test_full_path_argument_is_not_a_string(setup_link_tests):
    """TypeError is raised if the full_path argument is not a string."""
    data = setup_link_tests
    test_value = 1
    data["kwargs"]["full_path"] = test_value
    with pytest.raises(TypeError) as cm:
        Link(**data["kwargs"])
    assert str(cm.value) == "Link.full_path should be an instance of string not int"


def test_full_path_attribute_is_not_a_string(setup_link_tests):
    """TypeError is raised if the full_path attribute is not a string instance."""
    data = setup_link_tests
    test_value = 1
    with pytest.raises(TypeError) as cm:
        data["test_link"].full_path = test_value

    assert str(cm.value) == "Link.full_path should be an instance of string not int"


def test_full_path_windows_to_other_conversion(setup_link_tests):
    """full_path is stored in internal format."""
    data = setup_link_tests
    windows_path = "M:\\path\\to\\object"
    expected_result = "M:/path/to/object"
    data["test_link"].full_path = windows_path
    assert data["test_link"].full_path == expected_result


def test_original_filename_argument_is_none(setup_link_tests):
    """original_filename arg is None will set the attr to filename of the full_path."""
    data = setup_link_tests
    data["kwargs"]["original_filename"] = None
    new_link = Link(**data["kwargs"])
    filename = os.path.basename(new_link.full_path)
    assert new_link.original_filename == filename


def test_original_filename_attribute_is_set_to_none(setup_link_tests):
    """original_filename is equal to the filename of the full_path if it is None."""
    data = setup_link_tests
    data["test_link"].original_filename = None
    filename = os.path.basename(data["test_link"].full_path)
    assert data["test_link"].original_filename == filename


def test_original_filename_argument_is_empty_string(setup_link_tests):
    """original_filename arg is empty str, attr is set to filename of the full_path."""
    data = setup_link_tests
    data["kwargs"]["original_filename"] = ""
    new_link = Link(**data["kwargs"])
    filename = os.path.basename(new_link.full_path)
    assert new_link.original_filename == filename


def test_original_filename_attribute_set_to_empty_string(setup_link_tests):
    """original_filename attr is empty str, attr is set to filename of the full_path."""
    data = setup_link_tests
    data["test_link"].original_filename = ""
    filename = os.path.basename(data["test_link"].full_path)
    assert data["test_link"].original_filename == filename


def test_original_filename_argument_accepts_string_only(setup_link_tests):
    """original_filename arg accepts str only and raises TypeError for other types."""
    data = setup_link_tests
    test_value = 1
    data["kwargs"]["original_filename"] = test_value
    with pytest.raises(TypeError) as cm:
        Link(**data["kwargs"])

    assert (
        str(cm.value)
        == "Link.original_filename should be an instance of str and not int"
    )


def test_original_filename_attribute_accepts_string_only(setup_link_tests):
    """original_filename attr accepts str only and raises TypeError for other types."""
    data = setup_link_tests
    test_value = 1.1
    with pytest.raises(TypeError) as cm:
        data["test_link"].original_filename = test_value

    assert (
        str(cm.value)
        == "Link.original_filename should be an instance of str and not float"
    )


def test_original_filename_argument_is_working_properly(setup_link_tests):
    """original_filename argument is working properly."""
    data = setup_link_tests
    assert data["kwargs"]["original_filename"] == data["test_link"].original_filename


def test_original_filename_attribute_is_working_properly(setup_link_tests):
    """original_filename attribute is working properly."""
    data = setup_link_tests
    new_value = "this_is_the_original_filename.jpg"
    assert data["test_link"].original_filename != new_value
    data["test_link"].original_filename = new_value
    assert data["test_link"].original_filename == new_value


def test_equality_of_two_links(setup_link_tests):
    """Equality operator."""
    data = setup_link_tests
    # with same parameters
    mock_link1 = Link(**data["kwargs"])
    assert data["test_link"] == mock_link1

    # with different parameters
    data["kwargs"]["type"] = data["test_link_type2"]
    mock_link2 = Link(**data["kwargs"])

    assert not data["test_link"] == mock_link2


def test_inequality_of_two_links(setup_link_tests):
    """Inequality operator."""
    data = setup_link_tests
    # with same parameters
    mock_link1 = Link(**data["kwargs"])
    assert data["test_link"] == mock_link1

    # with different parameters
    data["kwargs"]["type"] = data["test_link_type2"]
    mock_link2 = Link(**data["kwargs"])

    assert not data["test_link"] != mock_link1
    assert data["test_link"] != mock_link2


def test_plural_class_name(setup_link_tests):
    """Plural name of Link class."""
    data = setup_link_tests
    assert data["test_link"].plural_class_name == "Links"


def test_path_attribute_is_set_to_none(setup_link_tests):
    """TypeError is raised if the path attribute is set to None."""
    data = setup_link_tests
    with pytest.raises(TypeError) as cm:
        data["test_link"].path = None
    assert str(cm.value) == "Link.path can not be set to None"


def test_path_attribute_is_set_to_empty_string(setup_link_tests):
    """ValueError is raised if the path attribute is set to an empty string."""
    data = setup_link_tests
    with pytest.raises(ValueError) as cm:
        data["test_link"].path = ""
    assert str(cm.value) == "Link.path can not be an empty string"


def test_path_attribute_is_set_to_a_value_other_then_string(setup_link_tests):
    """TypeError is raised if the path attribute is set to a value other than string."""
    data = setup_link_tests
    with pytest.raises(TypeError) as cm:
        data["test_link"].path = 1
    assert str(cm.value) == "Link.path should be an instance of str, not int"


def test_path_attribute_value_comes_from_full_path(setup_link_tests):
    """path attribute value is calculated from the full_path attribute."""
    data = setup_link_tests
    assert data["test_link"].path == "C:/A_NEW_PROJECT/td/dsdf"


def test_path_attribute_updates_the_full_path_attribute(setup_link_tests):
    """path attribute is updating the full_path attribute properly."""
    data = setup_link_tests
    test_value = "/mnt/some/new/path"
    expected_full_path = "/mnt/some/new/path/" "22-fdfffsd-32342-dsf2332-dsfd-3.exr"

    assert data["test_link"].path != test_value
    data["test_link"].path = test_value
    assert data["test_link"].path == test_value
    assert data["test_link"].full_path == expected_full_path


def test_filename_attribute_is_set_to_none(setup_link_tests):
    """filename attribute is an empty string if it is set a None."""
    data = setup_link_tests
    data["test_link"].filename = None
    assert data["test_link"].filename == ""


def test_filename_attribute_is_set_to_a_value_other_then_string(setup_link_tests):
    """TypeError is raised if the filename attr is set to a value other than string."""
    data = setup_link_tests
    with pytest.raises(TypeError) as cm:
        data["test_link"].filename = 3
    assert str(cm.value) == "Link.filename should be an instance of str, not int"


def test_filename_attribute_is_set_to_empty_string(setup_link_tests):
    """filename value can be set to an empty string."""
    data = setup_link_tests
    data["test_link"].filename = ""
    assert data["test_link"].filename == ""


def test_filename_attribute_value_comes_from_full_path(setup_link_tests):
    """filename attribute value is calculated from the full_path attribute."""
    data = setup_link_tests
    assert data["test_link"].filename == "22-fdfffsd-32342-dsf2332-dsfd-3.exr"


def test_filename_attribute_updates_the_full_path_attribute(setup_link_tests):
    """filename attribute is updating the full_path attribute properly."""
    data = setup_link_tests
    test_value = "new_filename.tif"
    assert data["test_link"].filename != test_value
    data["test_link"].filename = test_value
    assert data["test_link"].filename == test_value
    assert data["test_link"].full_path == "C:/A_NEW_PROJECT/td/dsdf/new_filename.tif"


def test_filename_attribute_changes_also_the_extension(setup_link_tests):
    """filename attribute also changes the extension attribute."""
    data = setup_link_tests
    assert data["test_link"].extension != ".an_extension"
    data["test_link"].filename = "some_filename_and.an_extension"
    assert data["test_link"].extension == ".an_extension"


def test_extension_attribute_is_set_to_none(setup_link_tests):
    """extension is an empty string if it is set to None."""
    data = setup_link_tests
    data["test_link"].extension = None
    assert data["test_link"].extension == ""


def test_extension_attribute_is_set_to_empty_string(setup_link_tests):
    """extension attr can be set to an empty string."""
    data = setup_link_tests
    data["test_link"].extension = ""
    assert data["test_link"].extension == ""


def test_extension_attribute_is_set_to_a_value_other_then_string(setup_link_tests):
    """TypeError is raised if the extension attr is not str."""
    data = setup_link_tests
    with pytest.raises(TypeError) as cm:
        data["test_link"].extension = 123
    assert str(cm.value) == "Link.extension should be an instance of str, not int"


def test_extension_attribute_value_comes_from_full_path(setup_link_tests):
    """extension attribute value is calculated from the full_path attribute."""
    data = setup_link_tests
    assert data["test_link"].extension == ".exr"


def test_extension_attribute_updates_the_full_path_attribute(setup_link_tests):
    """extension attribute is updating the full_path attribute properly."""
    data = setup_link_tests
    test_value = ".iff"
    assert data["test_link"].extension != test_value
    data["test_link"].extension = test_value
    assert data["test_link"].extension == test_value
    assert (
        data["test_link"].full_path
        == "C:/A_NEW_PROJECT/td/dsdf/22-fdfffsd-32342-dsf2332-dsfd-3.iff"
    )


def test_extension_attribute_updates_the_full_path_attribute_with_the_dot(
    setup_link_tests,
):
    """full_path attr updated properly with the extension that doesn't have a dot."""
    data = setup_link_tests
    test_value = "iff"
    expected_value = ".iff"
    assert data["test_link"].extension != test_value
    data["test_link"].extension = test_value
    assert data["test_link"].extension == expected_value
    assert (
        data["test_link"].full_path
        == "C:/A_NEW_PROJECT/td/dsdf/22-fdfffsd-32342-dsf2332-dsfd-3.iff"
    )


def test_extension_attribute_is_also_change_the_filename_attribute(setup_link_tests):
    """extension attribute is updating the filename attribute."""
    data = setup_link_tests
    test_value = ".targa"
    expected_value = "22-fdfffsd-32342-dsf2332-dsfd-3.targa"
    assert data["test_link"].filename != expected_value
    data["test_link"].extension = test_value
    assert data["test_link"].filename == expected_value
