# -*- coding: utf-8 -*-

import os

import pytest

from stalker import File, Type


@pytest.fixture(scope="function")
def setup_file_tests():
    """Set up the test for the File class."""
    data = dict()

    # create a mock FileType object
    data["test_file_type1"] = Type(
        name="Test Type 1",
        code="test type1",
        target_entity_type="File",
    )
    data["test_file_type2"] = Type(
        name="Test Type 2",
        code="test type2",
        target_entity_type="File",
    )

    data["kwargs"] = {
        "name": "An Image File",
        "full_path": "C:/A_NEW_PROJECT/td/dsdf/22-fdfffsd-32342-dsf2332-dsfd-3.exr",
        "original_filename": "this_is_an_image.jpg",
        "type": data["test_file_type1"],
    }

    data["test_file"] = File(**data["kwargs"])
    return data


def test___auto_name__class_attribute_is_set_to_true():
    """__auto_name__ class attribute is set to False for File class."""
    assert File.__auto_name__ is True


def test_full_path_argument_is_none(setup_file_tests):
    """full_path argument is None is set the full_path attribute to an empty string."""
    data = setup_file_tests
    data["kwargs"]["full_path"] = None
    new_file = File(**data["kwargs"])
    assert new_file.full_path == ""


def test_full_path_attribute_is_set_to_none(setup_file_tests):
    """full_path attr to None is set its value to an empty string."""
    data = setup_file_tests
    data["test_file"].full_path = ""


def test_full_path_argument_is_empty_an_empty_string(setup_file_tests):
    """full_path attr is set to an empty str if full_path arg is an empty string."""
    data = setup_file_tests
    data["kwargs"]["full_path"] = ""
    new_file = File(**data["kwargs"])
    assert new_file.full_path == ""


def test_full_path_attribute_is_set_to_empty_string(setup_file_tests):
    """full_path attr value is set to an empty string."""
    data = setup_file_tests
    data["test_file"].full_path = ""
    assert data["test_file"].full_path == ""


def test_full_path_argument_is_not_a_string(setup_file_tests):
    """TypeError is raised if the full_path argument is not a string."""
    data = setup_file_tests
    test_value = 1
    data["kwargs"]["full_path"] = test_value
    with pytest.raises(TypeError) as cm:
        File(**data["kwargs"])
    assert str(cm.value) == (
        "File.full_path should be an instance of string, not int: '1'"
    )


def test_full_path_attribute_is_not_a_string(setup_file_tests):
    """TypeError is raised if the full_path attribute is not a string instance."""
    data = setup_file_tests
    test_value = 1
    with pytest.raises(TypeError) as cm:
        data["test_file"].full_path = test_value

    assert str(cm.value) == (
        "File.full_path should be an instance of string, not int: '1'"
    )


def test_full_path_windows_to_other_conversion(setup_file_tests):
    """full_path is stored in internal format."""
    data = setup_file_tests
    windows_path = "M:\\path\\to\\object"
    expected_result = "M:/path/to/object"
    data["test_file"].full_path = windows_path
    assert data["test_file"].full_path == expected_result


def test_original_filename_argument_is_none(setup_file_tests):
    """original_filename arg is None will set the attr to filename of the full_path."""
    data = setup_file_tests
    data["kwargs"]["original_filename"] = None
    new_file = File(**data["kwargs"])
    filename = os.path.basename(new_file.full_path)
    assert new_file.original_filename == filename


def test_original_filename_attribute_is_set_to_none(setup_file_tests):
    """original_filename is equal to the filename of the full_path if it is None."""
    data = setup_file_tests
    data["test_file"].original_filename = None
    filename = os.path.basename(data["test_file"].full_path)
    assert data["test_file"].original_filename == filename


def test_original_filename_argument_is_empty_string(setup_file_tests):
    """original_filename arg is empty str, attr is set to filename of the full_path."""
    data = setup_file_tests
    data["kwargs"]["original_filename"] = ""
    new_file = File(**data["kwargs"])
    filename = os.path.basename(new_file.full_path)
    assert new_file.original_filename == filename


def test_original_filename_attribute_set_to_empty_string(setup_file_tests):
    """original_filename attr is empty str, attr is set to filename of the full_path."""
    data = setup_file_tests
    data["test_file"].original_filename = ""
    filename = os.path.basename(data["test_file"].full_path)
    assert data["test_file"].original_filename == filename


def test_original_filename_argument_accepts_string_only(setup_file_tests):
    """original_filename arg accepts str only and raises TypeError for other types."""
    data = setup_file_tests
    test_value = 1
    data["kwargs"]["original_filename"] = test_value
    with pytest.raises(TypeError) as cm:
        File(**data["kwargs"])

    assert str(cm.value) == (
        "File.original_filename should be an instance of string, not int: '1'"
    )


def test_original_filename_attribute_accepts_string_only(setup_file_tests):
    """original_filename attr accepts str only and raises TypeError for other types."""
    data = setup_file_tests
    test_value = 1.1
    with pytest.raises(TypeError) as cm:
        data["test_file"].original_filename = test_value

    assert str(cm.value) == (
        "File.original_filename should be an instance of string, not float: '1.1'"
    )


def test_original_filename_argument_is_working_as_expected(setup_file_tests):
    """original_filename argument is working as expected."""
    data = setup_file_tests
    assert data["kwargs"]["original_filename"] == data["test_file"].original_filename


def test_original_filename_attribute_is_working_as_expected(setup_file_tests):
    """original_filename attribute is working as expected."""
    data = setup_file_tests
    new_value = "this_is_the_original_filename.jpg"
    assert data["test_file"].original_filename != new_value
    data["test_file"].original_filename = new_value
    assert data["test_file"].original_filename == new_value


def test_equality_of_two_files(setup_file_tests):
    """Equality operator."""
    data = setup_file_tests
    # with same parameters
    mock_file1 = File(**data["kwargs"])
    assert data["test_file"] == mock_file1

    # with different parameters
    data["kwargs"]["type"] = data["test_file_type2"]
    mock_file2 = File(**data["kwargs"])

    assert not data["test_file"] == mock_file2


def test_inequality_of_two_files(setup_file_tests):
    """Inequality operator."""
    data = setup_file_tests
    # with same parameters
    mock_file1 = File(**data["kwargs"])
    assert data["test_file"] == mock_file1

    # with different parameters
    data["kwargs"]["type"] = data["test_file_type2"]
    mock_file2 = File(**data["kwargs"])

    assert not data["test_file"] != mock_file1
    assert data["test_file"] != mock_file2


def test_plural_class_name(setup_file_tests):
    """Plural name of File class."""
    data = setup_file_tests
    assert data["test_file"].plural_class_name == "Files"


def test_path_attribute_is_set_to_none(setup_file_tests):
    """TypeError is raised if the path attribute is set to None."""
    data = setup_file_tests
    with pytest.raises(TypeError) as cm:
        data["test_file"].path = None
    assert str(cm.value) == "File.path cannot be set to None"


def test_path_attribute_is_set_to_empty_string(setup_file_tests):
    """ValueError is raised if the path attribute is set to an empty string."""
    data = setup_file_tests
    with pytest.raises(ValueError) as cm:
        data["test_file"].path = ""
    assert str(cm.value) == "File.path cannot be an empty string"


def test_path_attribute_is_set_to_a_value_other_then_string(setup_file_tests):
    """TypeError is raised if the path attribute is set to a value other than string."""
    data = setup_file_tests
    with pytest.raises(TypeError) as cm:
        data["test_file"].path = 1
    assert str(cm.value) == "File.path should be an instance of str, not int: '1'"


def test_path_attribute_value_comes_from_full_path(setup_file_tests):
    """path attribute value is calculated from the full_path attribute."""
    data = setup_file_tests
    assert data["test_file"].path == "C:/A_NEW_PROJECT/td/dsdf"


def test_path_attribute_updates_the_full_path_attribute(setup_file_tests):
    """path attribute is updating the full_path attribute."""
    data = setup_file_tests
    test_value = "/mnt/some/new/path"
    expected_full_path = "/mnt/some/new/path/" "22-fdfffsd-32342-dsf2332-dsfd-3.exr"

    assert data["test_file"].path != test_value
    data["test_file"].path = test_value
    assert data["test_file"].path == test_value
    assert data["test_file"].full_path == expected_full_path


def test_filename_attribute_is_set_to_none(setup_file_tests):
    """filename attribute is an empty string if it is set a None."""
    data = setup_file_tests
    data["test_file"].filename = None
    assert data["test_file"].filename == ""


def test_filename_attribute_is_set_to_a_value_other_then_string(setup_file_tests):
    """TypeError is raised if the filename attr is set to a value other than string."""
    data = setup_file_tests
    with pytest.raises(TypeError) as cm:
        data["test_file"].filename = 3
    assert str(cm.value) == "File.filename should be an instance of str, not int: '3'"


def test_filename_attribute_is_set_to_empty_string(setup_file_tests):
    """filename value can be set to an empty string."""
    data = setup_file_tests
    data["test_file"].filename = ""
    assert data["test_file"].filename == ""


def test_filename_attribute_value_comes_from_full_path(setup_file_tests):
    """filename attribute value is calculated from the full_path attribute."""
    data = setup_file_tests
    assert data["test_file"].filename == "22-fdfffsd-32342-dsf2332-dsfd-3.exr"


def test_filename_attribute_updates_the_full_path_attribute(setup_file_tests):
    """filename attribute is updating the full_path attribute."""
    data = setup_file_tests
    test_value = "new_filename.tif"
    assert data["test_file"].filename != test_value
    data["test_file"].filename = test_value
    assert data["test_file"].filename == test_value
    assert data["test_file"].full_path == "C:/A_NEW_PROJECT/td/dsdf/new_filename.tif"


def test_filename_attribute_changes_also_the_extension(setup_file_tests):
    """filename attribute also changes the extension attribute."""
    data = setup_file_tests
    assert data["test_file"].extension != ".an_extension"
    data["test_file"].filename = "some_filename_and.an_extension"
    assert data["test_file"].extension == ".an_extension"


def test_extension_attribute_is_set_to_none(setup_file_tests):
    """extension is an empty string if it is set to None."""
    data = setup_file_tests
    data["test_file"].extension = None
    assert data["test_file"].extension == ""


def test_extension_attribute_is_set_to_empty_string(setup_file_tests):
    """extension attr can be set to an empty string."""
    data = setup_file_tests
    data["test_file"].extension = ""
    assert data["test_file"].extension == ""


def test_extension_attribute_is_set_to_a_value_other_then_string(setup_file_tests):
    """TypeError is raised if the extension attr is not str."""
    data = setup_file_tests
    with pytest.raises(TypeError) as cm:
        data["test_file"].extension = 123
    assert str(cm.value) == (
        "File.extension should be an instance of str, not int: '123'"
    )


def test_extension_attribute_value_comes_from_full_path(setup_file_tests):
    """extension attribute value is calculated from the full_path attribute."""
    data = setup_file_tests
    assert data["test_file"].extension == ".exr"


def test_extension_attribute_updates_the_full_path_attribute(setup_file_tests):
    """extension attribute is updating the full_path attribute."""
    data = setup_file_tests
    test_value = ".iff"
    assert data["test_file"].extension != test_value
    data["test_file"].extension = test_value
    assert data["test_file"].extension == test_value
    assert (
        data["test_file"].full_path
        == "C:/A_NEW_PROJECT/td/dsdf/22-fdfffsd-32342-dsf2332-dsfd-3.iff"
    )


def test_extension_attribute_updates_the_full_path_attribute_with_the_dot(
    setup_file_tests,
):
    """full_path attr updated with the extension that doesn't have a dot."""
    data = setup_file_tests
    test_value = "iff"
    expected_value = ".iff"
    assert data["test_file"].extension != test_value
    data["test_file"].extension = test_value
    assert data["test_file"].extension == expected_value
    assert (
        data["test_file"].full_path
        == "C:/A_NEW_PROJECT/td/dsdf/22-fdfffsd-32342-dsf2332-dsfd-3.iff"
    )


def test_extension_attribute_is_also_change_the_filename_attribute(setup_file_tests):
    """extension attribute is updating the filename attribute."""
    data = setup_file_tests
    test_value = ".targa"
    expected_value = "22-fdfffsd-32342-dsf2332-dsfd-3.targa"
    assert data["test_file"].filename != expected_value
    data["test_file"].extension = test_value
    assert data["test_file"].filename == expected_value


def test_format_path_converts_bytes_to_strings(setup_file_tests):
    """_format_path() converts bytes to strings."""
    data = setup_file_tests
    test_value = b"C:/A_NEW_PROJECT/td/dsdf/22-fdfffsd-32342-dsf2332-dsfd-3.iff"
    result = data["test_file"]._format_path(test_value)
    assert isinstance(result, str)
    assert result == test_value.decode("utf-8")


def test__hash__is_working_as_expected(setup_file_tests):
    """__hash__ is working as expected."""
    data = setup_file_tests
    result = hash(data["test_file"])
    assert isinstance(result, int)
    assert result == data["test_file"].__hash__()
