# -*- coding: utf-8 -*-

import os
import sys

import pytest

from stalker import File, Repository, Type
from stalker.db.session import DBSession
from tests.utils import PlatformPatcher


@pytest.fixture(scope="function")
def setup_file_tests():
    """Set up the test for the File class."""
    data = dict()
    data["patcher"] = PlatformPatcher()

    # create a test Repository
    data["test_repo"] = Repository(
        name="Projects Repository",
        code="PR1",
        windows_path="M:/Projects",
        linux_path="/mnt/projects_server/Projects",
        macos_path="/Volumes/projects_server/Projects",
    )

    # create a Type object for Files
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

    image_sequence_type = Type(
        name="Image Sequence",
        code="ImSeq",
        target_entity_type="File",
    )

    # a File for the input file
    data["test_input_file1"] = File(
        name="Input File 1",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_beauty_v001.###.exr",
        type=image_sequence_type,
    )

    data["test_input_file2"] = File(
        name="Input File 2",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_occ_v001.###.exr",
        type=image_sequence_type,
    )

    data["kwargs"] = {
        "name": "An Image File",
        "full_path": "C:/A_NEW_PROJECT/td/dsdf/22-fdfffsd-32342-dsf2332-dsfd-3.exr",
        "references": [data["test_input_file1"], data["test_input_file2"]],
        "original_filename": "this_is_an_image.jpg",
        "type": data["test_file_type1"],
        "created_with": "Houdini",
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
    assert str(cm.value) == ("File.full_path should be a str, not int: '1'")


def test_full_path_attribute_is_not_a_string(setup_file_tests):
    """TypeError is raised if the full_path attribute is not a string instance."""
    data = setup_file_tests
    test_value = 1
    with pytest.raises(TypeError) as cm:
        data["test_file"].full_path = test_value

    assert str(cm.value) == ("File.full_path should be a str, not int: '1'")


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

    assert str(cm.value) == ("File.original_filename should be a str, not int: '1'")


def test_original_filename_attribute_accepts_string_only(setup_file_tests):
    """original_filename attr accepts str only and raises TypeError for other types."""
    data = setup_file_tests
    test_value = 1.1
    with pytest.raises(TypeError) as cm:
        data["test_file"].original_filename = test_value

    assert str(cm.value) == ("File.original_filename should be a str, not float: '1.1'")


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
    assert str(cm.value) == "File.path should be a str, not int: '1'"


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
    assert str(cm.value) == "File.filename should be a str, not int: '3'"


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
    assert str(cm.value) == ("File.extension should be a str, not int: '123'")


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


def test_references_arg_is_skipped(setup_file_tests):
    """references attr is an empty list if the references argument is skipped."""
    data = setup_file_tests
    data["kwargs"].pop("references")
    new_version = File(**data["kwargs"])
    assert new_version.references == []


def test_references_arg_is_none(setup_file_tests):
    """references attr is an empty list if the references argument is None."""
    data = setup_file_tests
    data["kwargs"]["references"] = None
    new_file = File(**data["kwargs"])
    assert new_file.references == []


def test_references_attr_is_none(setup_file_tests):
    """TypeError raised if the references attr is set to None."""
    data = setup_file_tests
    with pytest.raises(TypeError) as cm:
        data["test_file"].references = None
    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_references_arg_is_not_a_list_of_file_instances(setup_file_tests):
    """TypeError raised if the references arg is not a File instance."""
    data = setup_file_tests
    test_value = [132, "231123"]
    data["kwargs"]["references"] = test_value
    with pytest.raises(TypeError) as cm:
        File(**data["kwargs"])

    assert str(cm.value) == (
        "File.references should only contain instances of "
        "stalker.models.file.File, not int: '132'"
    )


def test_references_attr_is_not_a_list_of_file_instances(setup_file_tests):
    """TypeError raised if the references attr is set to something other than a File."""
    data = setup_file_tests
    test_value = [132, "231123"]
    with pytest.raises(TypeError) as cm:
        data["test_file"].references = test_value

    assert str(cm.value) == (
        "File.references should only contain instances of "
        "stalker.models.file.File, not int: '132'"
    )


def test_references_attr_is_working_as_expected(setup_file_tests):
    """references attr is working as expected."""
    data = setup_file_tests
    data["kwargs"].pop("references")
    new_file = File(**data["kwargs"])
    assert data["test_input_file1"] not in new_file.references
    assert data["test_input_file2"] not in new_file.references

    new_file.references = [data["test_input_file1"], data["test_input_file2"]]
    assert data["test_input_file1"] in new_file.references
    assert data["test_input_file2"] in new_file.references


def test_created_with_argument_can_be_skipped(setup_file_tests):
    """created_with argument can be skipped."""
    data = setup_file_tests
    data["kwargs"].pop("created_with")
    File(**data["kwargs"])


def test_created_with_argument_can_be_none(setup_file_tests):
    """created_with argument can be None."""
    data = setup_file_tests
    data["kwargs"]["created_with"] = None
    File(**data["kwargs"])


def test_created_with_attribute_can_be_set_to_none(setup_file_tests):
    """created with attribute can be set to None."""
    data = setup_file_tests
    data["test_file"].created_with = None


def test_created_with_argument_accepts_only_string_or_none(setup_file_tests):
    """TypeError raised if the created_with arg is not a string or None."""
    data = setup_file_tests
    data["kwargs"]["created_with"] = 234
    with pytest.raises(TypeError) as cm:
        File(**data["kwargs"])
    assert str(cm.value) == (
        "File.created_with should be an instance of str, not int: '234'"
    )


def test_created_with_attribute_accepts_only_string_or_none(setup_file_tests):
    """TypeError raised if the created_with attr is not a str or None."""
    data = setup_file_tests
    with pytest.raises(TypeError) as cm:
        data["test_file"].created_with = 234

    assert str(cm.value) == (
        "File.created_with should be an instance of str, not int: '234'"
    )


def test_created_with_argument_is_working_as_expected(setup_file_tests):
    """created_with argument value is passed to created_with attribute."""
    data = setup_file_tests
    test_value = "Maya"
    data["kwargs"]["created_with"] = test_value
    test_file = File(**data["kwargs"])
    assert test_file.created_with == test_value


def test_created_with_attribute_is_working_as_expected(setup_file_tests):
    """created_with attribute is working as expected."""
    data = setup_file_tests
    test_value = "Maya"
    assert data["test_file"].created_with != test_value
    data["test_file"].created_with = test_value
    assert data["test_file"].created_with == test_value


def test_walk_references_is_working_as_expected_in_dfs_mode(setup_file_tests):
    """walk_references() method is working in DFS mode correctly."""
    # data = setup_file_tests

    repr_type = Type(name="Representation", code="Repr", target_entity_type="File")
    # DBSession.add(repr_type)
    # DBSession.commit()

    # File 1
    # v1 = Version(task=data["test_task1"])
    v1_base_repr = File(
        name="Base Repr.",
        # full_path=str(v1.generate_path().with_suffix(".ma")),
        type=repr_type,
    )
    # v1.files.append(v1_base_repr)

    # Version 2
    # v2 = Version(task=data["test_task1"])
    v2_base_repr = File(
        name="Base Repr.",
        # full_path=str(v2.generate_path().with_suffix(".ma")),
        type=repr_type,
    )
    # v2.files.append(v2_base_repr)

    # Version 3
    # v3 = Version(task=data["test_task1"])
    v3_base_repr = File(
        name="Base Repr.",
        # full_path=str(v3.generate_path().with_suffix(".ma")),
        type=repr_type,
    )
    # v3.files.append(v3_base_repr)

    # v4 = Version(task=data["test_task1"])
    v4_base_repr = File(
        name="Base Repr.",
        # full_path=str(v4.generate_path().with_suffix(".ma")),
        type=repr_type,
    )
    # v4.files.append(v4_base_repr)

    # v5 = Version(task=data["test_task1"])
    v5_base_repr = File(
        name="Base Repr.",
        # full_path=str(v5.generate_path().with_suffix(".ma")),
        type=repr_type,
    )
    # v5.files.append(v5_base_repr)

    v5_base_repr.references = [v4_base_repr]
    v4_base_repr.references = [v3_base_repr, v2_base_repr]
    v3_base_repr.references = [v1_base_repr]
    v2_base_repr.references = [v1_base_repr]

    expected_result = [
        v5_base_repr,
        v4_base_repr,
        v3_base_repr,
        v1_base_repr,
        v2_base_repr,
        v1_base_repr,
    ]
    visited_versions = []
    for v in v5_base_repr.walk_references():
        visited_versions.append(v)

    assert expected_result == visited_versions


def test_absolute_path_is_read_only(setup_file_tests):
    """absolute_path property is read-only."""
    data = setup_file_tests
    with pytest.raises(AttributeError) as cm:
        data["test_file"].absolute_path = "C:/A_NEW_PROJECT/td/dsdf"
    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'absolute_path'",
        11: "property 'absolute_path' of 'File' object has no setter",
    }.get(sys.version_info.minor, "property 'absolute_path' of 'File' object has no setter")
    assert str(cm.value) == error_message


def test_absolute_path_returns_the_absolute_path(setup_file_tests):
    """absolute_path property returns the absolute path of the full_path attribute."""
    data = setup_file_tests
    data["patcher"].patch("Darwin")
    file = data["test_file"]
    file.full_path = "$REPOPR1/A_NEW_PROJECT/td/dsdf/22-fdfffsd-32342-dsf2332-dsfd-3.exr"
    expected_result = "/Volumes/projects_server/Projects/A_NEW_PROJECT/td/dsdf"
    assert data["test_file"].absolute_path == expected_result


def test_absolute_full_path_is_read_only(setup_file_tests):
    """absolute_full_path property is read-only."""
    data = setup_file_tests
    with pytest.raises(AttributeError) as cm:
        data["test_file"].absolute_full_path = "C:/A_NEW_PROJECT/td/dsdf"
    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'absolute_full_path'",
        11: "property 'absolute_full_path' of 'File' object has no setter",
    }.get(sys.version_info.minor, "property 'absolute_full_path' of 'File' object has no setter")
    assert str(cm.value) == error_message


def test_absolute_full_path_returns_the_absolute_full_path(setup_file_tests):
    """absolute_full_path property returns the absolute path of the full_path attribute."""
    data = setup_file_tests
    data["patcher"].patch("Darwin")
    file = data["test_file"]
    file.full_path = "$REPOPR1/A_NEW_PROJECT/td/dsdf/22-fdfffsd-32342-dsf2332-dsfd-3.exr"
    expected_result = "/Volumes/projects_server/Projects/A_NEW_PROJECT/td/dsdf/22-fdfffsd-32342-dsf2332-dsfd-3.exr"
    assert data["test_file"].absolute_full_path == expected_result
