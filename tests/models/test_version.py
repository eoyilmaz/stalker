# -*- coding: utf-8 -*-
import logging
import sys

import pytest

from stalker import (
    Asset,
    FilenameTemplate,
    Link,
    Project,
    Repository,
    Sequence,
    Shot,
    Status,
    StatusList,
    Structure,
    Task,
    Type,
    Version,
    defaults,
    log,
)
from stalker.db.session import DBSession
from stalker.exceptions import CircularDependencyError

from tests.utils import PlatformPatcher

logger = logging.getLogger("stalker.models.version.Version")
logger.setLevel(log.logging_level)


VARIANT_NAME_TEST_VALUES = [
    ["Variant Name", "Variant_Name"],
    ["VariantName", "VariantName"],
    ["variant name", "variant_name"],
    ["  variant_name", "variant_name"],
    ["variant_name   ", "variant_name"],
    ["   variant   name   ", "variant_name"],
    ["VariantName", "VariantName"],
    ["Variant___Name", "Variant___Name"],
    ["Variant@Name", "Variant@Name"],
]


@pytest.fixture(scope="function")
def setup_version_db_tests(setup_postgresql_db):
    """Set up the tests for the Version class with a DB."""
    data = dict()
    data["patcher"] = PlatformPatcher()
    # statuses
    data["test_status1"] = Status(name="Status1", code="STS1")
    data["test_status2"] = Status(name="Status2", code="STS2")
    data["test_status3"] = Status(name="Status3", code="STS3")
    data["test_status4"] = Status(name="Status4", code="STS4")
    data["test_status5"] = Status(name="Status5", code="STS5")
    DBSession.add_all(
        [
            data["test_status1"],
            data["test_status2"],
            data["test_status3"],
            data["test_status4"],
            data["test_status5"],
        ]
    )
    DBSession.commit()

    # repository
    data["test_repo"] = Repository(
        name="Test Repository",
        code="TR",
        linux_path="/mnt/T/",
        windows_path="T:/",
        macos_path="/Volumes/T/",
    )
    DBSession.add(data["test_repo"])

    # a project type
    data["test_project_type"] = Type(
        name="Test",
        code="test",
        target_entity_type="Project",
    )
    DBSession.add(data["test_project_type"])

    # create a structure
    data["test_structure"] = Structure(name="Test Project Structure")
    DBSession.add(data["test_structure"])

    # create a project
    data["test_project"] = Project(
        name="Test Project",
        code="tp",
        type=data["test_project_type"],
        repositories=[data["test_repo"]],
        structure=data["test_structure"],
    )
    DBSession.add(data["test_project"])
    DBSession.commit()

    # create a sequence
    data["test_sequence"] = Sequence(
        name="Test Sequence",
        code="SEQ1",
        project=data["test_project"],
    )
    DBSession.add(data["test_sequence"])
    DBSession.commit()

    # create a shot
    data["test_shot1"] = Shot(
        name="SH001",
        code="SH001",
        project=data["test_project"],
        sequences=[data["test_sequence"]],
    )
    DBSession.add(data["test_shot1"])
    DBSession.commit()

    # create a group of Tasks for the shot
    data["test_task1"] = Task(name="Task1", parent=data["test_shot1"])
    DBSession.add(data["test_task1"])
    DBSession.commit()

    # a Link for the input file
    data["test_input_link1"] = Link(
        name="Input Link 1",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_beauty_v001.###.exr",
    )
    DBSession.add(data["test_input_link1"])

    data["test_input_link2"] = Link(
        name="Input Link 2",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_occ_v001.###.exr",
    )
    DBSession.add(data["test_input_link2"])

    # a Link for the output file
    data["test_output_link1"] = Link(
        name="Output Link 1",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_beauty_v001.###.exr",
    )
    DBSession.add(data["test_output_link1"])

    data["test_output_link2"] = Link(
        name="Output Link 2",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_occ_v001.###.exr",
    )
    DBSession.add(data["test_output_link2"])
    DBSession.commit()

    # now create a version for the Task
    data["kwargs"] = {
        "variant_name": "TestVariant",
        "inputs": [data["test_input_link1"], data["test_input_link2"]],
        "outputs": [data["test_output_link1"], data["test_output_link2"]],
        "task": data["test_task1"],
        "created_with": "Houdini",
    }

    # and the Version
    data["test_version"] = Version(**data["kwargs"])
    DBSession.add(data["test_version"])

    # set the published to False
    data["test_version"].is_published = False
    DBSession.commit()
    yield data
    # clean up test
    data["patcher"].restore()


def test___auto_name__class_attribute_is_set_to_true():
    """__auto_name__ class attribute is set to True for Version class."""
    assert Version.__auto_name__ is True


def test_variant_name_argument_is_skipped_defaults_to_default_value(
    setup_version_db_tests,
):
    """variant_name arg is skipped variant_name attr equals defaults.DEFAULT_VERSION_VARIANT_NAME."""
    data = setup_version_db_tests
    data["kwargs"].pop("variant_name")
    new_version = Version(**data["kwargs"])
    assert new_version.variant_name == defaults.version_variant_name


def test_variant_name_argument_is_none(setup_version_db_tests):
    """TypeError raised if the variant_name argument is None."""
    data = setup_version_db_tests
    data["kwargs"]["variant_name"] = None
    with pytest.raises(TypeError) as cm:
        Version(**data["kwargs"])
    assert (
        str(cm.value) == "Version.variant_name should be a string, not NoneType: 'None'"
    )


def test_variant_name_attribute_is_none(setup_version_db_tests):
    """TypeError raised if the variant_name attribute is set to None."""
    data = setup_version_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_version"].variant_name = None

    assert (
        str(cm.value) == "Version.variant_name should be a string, not NoneType: 'None'"
    )


def test_variant_name_argument_is_empty_string(setup_version_db_tests):
    """ValueError raised if the variant_name arg is given as an empty string."""
    data = setup_version_db_tests
    data["kwargs"]["variant_name"] = ""
    with pytest.raises(ValueError) as cm:
        Version(**data["kwargs"])
    assert str(cm.value) == "Version.variant_name cannot be an empty string"


def test_variant_name_attribute_is_empty_string(setup_version_db_tests):
    """ValueError raised if the variant_name attribute is set to an empty string."""
    data = setup_version_db_tests
    with pytest.raises(ValueError) as cm:
        data["test_version"].variant_name = ""
    assert str(cm.value) == "Version.variant_name cannot be an empty string"


@pytest.mark.parametrize("test_value", [[1, 1.2, ["a list"], {"a": "dict"}]])
def test_variant_name_argument_is_not_a_string(setup_version_db_tests, test_value):
    """TypeError raised if the given variant_name argument is not a string."""
    data = setup_version_db_tests
    data["kwargs"]["variant_name"] = test_value
    with pytest.raises(TypeError) as cm:
        Version(**data["kwargs"])

    assert str(cm.value) == (
        "Version.variant_name should be a string, not {}: '{}'".format(
            test_value.__class__.__name__,
            test_value,
        )
    )


@pytest.mark.parametrize("test_value", [1, 1.2, ["a list"], {"a": "dict"}])
def test_variant_name_attribute_is_not_a_string(test_value, setup_version_db_tests):
    """TypeError raised if the variant_name attr is set to a value other than a str."""
    data = setup_version_db_tests
    with pytest.raises(TypeError):
        data["test_version"].variant_name = test_value


def test_variant_name_argument_is_formatted_to_empty_string(setup_version_db_tests):
    """ValueError raised if the variant_name arg is formatted to an empty str."""
    data = setup_version_db_tests
    data["kwargs"]["variant_name"] = "##$½#$"
    with pytest.raises(ValueError) as cm:
        _ = Version(**data["kwargs"])
    assert str(cm.value) == "Version.variant_name cannot be an empty string"


def test_variant_name_attribute_is_formatted_to_empty_string(setup_version_db_tests):
    """ValueError raised if the variant_name arg is formatted to an empty str."""
    data = setup_version_db_tests
    with pytest.raises(ValueError) as cm:
        data["test_version"].variant_name = "##$½#$"
    assert str(cm.value) == "Version.variant_name cannot be an empty string"


@pytest.mark.parametrize("variant_name, expected_result", VARIANT_NAME_TEST_VALUES)
def test_variant_name_argument_is_formatted_correctly(
    setup_version_db_tests, variant_name, expected_result
):
    """variant_name argument value is formatted correctly."""
    data = setup_version_db_tests
    data["kwargs"]["variant_name"] = variant_name
    new_version = Version(**data["kwargs"])
    assert new_version.variant_name == expected_result


@pytest.mark.parametrize("variant_name, expected_result", VARIANT_NAME_TEST_VALUES)
def test_variant_name_attribute_is_formatted_correctly(
    setup_version_db_tests, variant_name, expected_result
):
    """variant_name attribute value is formatted correctly."""
    data = setup_version_db_tests
    data["test_version"].variant_name = variant_name
    assert data["test_version"].variant_name == expected_result


def test_task_argument_is_skipped(setup_version_db_tests):
    """TypeError raised if the task argument is skipped."""
    data = setup_version_db_tests
    data["kwargs"].pop("task")
    with pytest.raises(TypeError) as cm:
        Version(**data["kwargs"])
    assert str(cm.value) == "Version.task cannot be None"


def test_task_argument_is_none(setup_version_db_tests):
    """TypeError raised if the task argument is None."""
    data = setup_version_db_tests
    data["kwargs"]["task"] = None
    with pytest.raises(TypeError) as cm:
        Version(**data["kwargs"])
    assert str(cm.value) == "Version.task cannot be None"


def test_task_attribute_is_none(setup_version_db_tests):
    """TypeError raised if the task attribute is None."""
    data = setup_version_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_version"].task = None
    assert str(cm.value) == "Version.task cannot be None"


def test_task_argument_is_not_a_task(setup_version_db_tests):
    """TypeError raised if the task argument is not a Task instance."""
    data = setup_version_db_tests
    data["kwargs"]["task"] = "a task"
    with pytest.raises(TypeError) as cm:
        Version(**data["kwargs"])
    assert str(cm.value) == (
        "Version.task should be a stalker.models.task.Task instance, not str: 'a task'"
    )


def test_task_attribute_is_not_a_task(setup_version_db_tests):
    """TypeError raised if the task attribute is not a Task instance."""
    data = setup_version_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_version"].task = "a task"
    assert str(cm.value) == (
        "Version.task should be a stalker.models.task.Task instance, not str: 'a task'"
    )


def test_task_attribute_is_working_as_expected(setup_version_db_tests):
    """task attribute is working as expected."""
    data = setup_version_db_tests
    new_task = Task(
        name="New Test Task",
        parent=data["test_shot1"],
    )
    assert data["test_version"].task is not new_task
    data["test_version"].task = new_task
    assert data["test_version"].task is new_task


def test_version_number_attribute_is_automatically_generated(setup_version_db_tests):
    """version_number attribute is automatically generated."""
    data = setup_version_db_tests
    assert data["test_version"].version_number == 1
    DBSession.add(data["test_version"])
    DBSession.commit()

    new_version = Version(**data["kwargs"])
    DBSession.add(new_version)
    DBSession.commit()

    assert data["test_version"].task == new_version.task
    assert data["test_version"].variant_name == new_version.variant_name

    assert new_version.version_number == 2

    new_version = Version(**data["kwargs"])
    DBSession.add(new_version)
    DBSession.commit()

    assert data["test_version"].task == new_version.task
    assert data["test_version"].variant_name == new_version.variant_name

    assert new_version.version_number == 3

    new_version = Version(**data["kwargs"])
    DBSession.add(new_version)
    DBSession.commit()

    assert data["test_version"].task == new_version.task
    assert data["test_version"].variant_name == new_version.variant_name

    assert new_version.version_number == 4


def test_version_number_attribute_is_starting_from_1(setup_version_db_tests):
    """version_number attribute is starting from 1."""
    data = setup_version_db_tests
    assert data["test_version"].version_number == 1


def test_version_number_attribute_is_set_to_a_lower_then_it_should_be(
    setup_version_db_tests,
):
    """version_number attr is set to unique number if it smaller than what it
    should be."""
    data = setup_version_db_tests
    data["test_version"].version_number = -1
    assert data["test_version"].version_number == 1

    data["test_version"].version_number = -10
    assert data["test_version"].version_number == 1

    DBSession.add(data["test_version"])
    DBSession.commit()

    data["test_version"].version_number = -100
    # it should be 1 again
    assert data["test_version"].version_number == 1

    new_version = Version(**data["kwargs"])
    assert new_version.version_number == 2

    new_version.version_number = 1
    assert new_version.version_number == 2

    new_version.version_number = 100
    assert new_version.version_number == 100


def test_inputs_argument_is_skipped(setup_version_db_tests):
    """inputs attribute an empty list if the inputs argument is skipped."""
    data = setup_version_db_tests
    data["kwargs"].pop("inputs")
    new_version = Version(**data["kwargs"])
    assert new_version.inputs == []


def test_inputs_argument_is_none(setup_version_db_tests):
    """inputs attribute an empty list if the inputs argument is None."""
    data = setup_version_db_tests
    data["kwargs"]["inputs"] = None
    new_version = Version(**data["kwargs"])
    assert new_version.inputs == []


def test_inputs_attribute_is_none(setup_version_db_tests):
    """TypeError raised if the inputs argument is set to None."""
    data = setup_version_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_version"].inputs = None
    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_inputs_argument_is_not_a_list_of_link_instances(setup_version_db_tests):
    """TypeError raised if the inputs attr is not a Link instance."""
    data = setup_version_db_tests
    test_value = [132, "231123"]
    data["kwargs"]["inputs"] = test_value
    with pytest.raises(TypeError) as cm:
        Version(**data["kwargs"])

    assert (
        str(cm.value) == "All elements in Version.inputs should be all "
        "stalker.models.link.Link instances, not int: '132'"
    )


def test_inputs_attribute_is_not_a_list_of_link_instances(setup_version_db_tests):
    """TypeError raised if the inputs attr is set to something other than a Link."""
    data = setup_version_db_tests
    test_value = [132, "231123"]
    with pytest.raises(TypeError) as cm:
        data["test_version"].inputs = test_value

    assert (
        str(cm.value) == "All elements in Version.inputs should be all "
        "stalker.models.link.Link instances, not int: '132'"
    )


def test_inputs_attribute_is_working_as_expected(setup_version_db_tests):
    """inputs attribute is working as expected."""
    data = setup_version_db_tests
    data["kwargs"].pop("inputs")
    new_version = Version(**data["kwargs"])
    assert data["test_input_link1"] not in new_version.inputs
    assert data["test_input_link2"] not in new_version.inputs

    new_version.inputs = [data["test_input_link1"], data["test_input_link2"]]
    assert data["test_input_link1"] in new_version.inputs
    assert data["test_input_link2"] in new_version.inputs


def test_outputs_argument_is_skipped(setup_version_db_tests):
    """outputs attribute an empty list if the outputs argument is skipped."""
    data = setup_version_db_tests
    data["kwargs"].pop("outputs")
    new_version = Version(**data["kwargs"])
    assert new_version.outputs == []


def test_outputs_argument_is_none(setup_version_db_tests):
    """outputs attribute an empty list if the outputs argument is None."""
    data = setup_version_db_tests
    data["kwargs"]["outputs"] = None
    new_version = Version(**data["kwargs"])
    assert new_version.outputs == []


def test_outputs_attribute_is_none(setup_version_db_tests):
    """TypeError raised if the outputs argument is set to None."""
    data = setup_version_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_version"].outputs = None
    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_outputs_argument_is_not_a_list_of_link_instances(setup_version_db_tests):
    """TypeError raised if the outputs attr is not a Link instance."""
    data = setup_version_db_tests
    test_value = [132, "231123"]
    data["kwargs"]["outputs"] = test_value
    with pytest.raises(TypeError) as cm:
        Version(**data["kwargs"])

    assert (
        str(cm.value) == "All elements in Version.outputs should be all "
        "stalker.models.link.Link instances, not int: '132'"
    )


def test_outputs_attribute_is_not_a_list_of_link_instances(setup_version_db_tests):
    """TypeError raised if the outputs attr is not a Link instance."""
    data = setup_version_db_tests
    test_value = [132, "231123"]
    with pytest.raises(TypeError) as cm:
        data["test_version"].outputs = test_value

    assert (
        str(cm.value) == "All elements in Version.outputs should be all "
        "stalker.models.link.Link instances, not int: '132'"
    )


def test_outputs_attribute_is_working_as_expected(setup_version_db_tests):
    """outputs attribute is working as expected."""
    data = setup_version_db_tests
    data["kwargs"].pop("outputs")
    new_version = Version(**data["kwargs"])
    assert data["test_output_link1"] not in new_version.outputs
    assert data["test_output_link2"] not in new_version.outputs

    new_version.outputs = [data["test_output_link1"], data["test_output_link2"]]
    assert data["test_output_link1"] in new_version.outputs
    assert data["test_output_link2"] in new_version.outputs


def test_is_published_attribute_is_false_by_default(setup_version_db_tests):
    """is_published attribute is False by default."""
    data = setup_version_db_tests
    assert data["test_version"].is_published is False


def test_is_published_attribute_is_working_as_expected(setup_version_db_tests):
    """is_published attribute is working as expected."""
    data = setup_version_db_tests
    data["test_version"].is_published = True
    assert data["test_version"].is_published is True
    data["test_version"].is_published = False
    assert data["test_version"].is_published is False


def test_parent_argument_is_skipped(setup_version_db_tests):
    """parent attribute None if the parent argument is skipped."""
    data = setup_version_db_tests
    try:
        data["kwargs"].pop("parent")
    except KeyError:
        pass
    new_version = Version(**data["kwargs"])
    assert new_version.parent is None


def test_parent_argument_is_none(setup_version_db_tests):
    """parent attribute None if the parent argument is skipped."""
    data = setup_version_db_tests
    data["kwargs"]["parent"] = None
    new_version = Version(**data["kwargs"])
    assert new_version.parent is None


def test_parent_attribute_is_none(setup_version_db_tests):
    """parent attribute value None if it is set to None."""
    data = setup_version_db_tests
    data["test_version"].parent = None
    assert data["test_version"].parent is None


def test_parent_argument_is_not_a_version_instance(setup_version_db_tests):
    """TypeError raised if the parent argument is not a Version instance."""
    data = setup_version_db_tests
    data["kwargs"]["parent"] = "not a version instance"
    with pytest.raises(TypeError) as cm:
        Version(**data["kwargs"])

    assert str(cm.value) == (
        "Version.parent should be an instance of Version class or "
        "derivative, not str: 'not a version instance'"
    )


def test_parent_attribute_is_not_set_to_a_version_instance(setup_version_db_tests):
    """TypeError raised if the parent attribute is not set to a Version instance."""
    data = setup_version_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_version"].parent = "not a version instance"

    assert str(cm.value) == (
        "Version.parent should be an instance of Version class or "
        "derivative, not str: 'not a version instance'"
    )


def test_parent_argument_is_working_as_expected(setup_version_db_tests):
    """parent argument is working as expected."""
    data = setup_version_db_tests
    data["kwargs"]["parent"] = data["test_version"]
    new_version = Version(**data["kwargs"])
    assert new_version.parent == data["test_version"]


def test_parent_attribute_is_working_as_expected(setup_version_db_tests):
    """parent attribute is working as expected."""
    data = setup_version_db_tests
    data["kwargs"]["parent"] = None
    new_version = Version(**data["kwargs"])
    assert new_version.parent != data["test_version"]
    new_version.parent = data["test_version"]
    assert new_version.parent == data["test_version"]


def test_parent_argument_updates_the_children_attribute(setup_version_db_tests):
    """parent argument updates the children attribute of the parent Version."""
    data = setup_version_db_tests
    data["kwargs"]["parent"] = data["test_version"]
    new_version = Version(**data["kwargs"])
    assert new_version in data["test_version"].children


def test_parent_attribute_updates_the_children_attribute(setup_version_db_tests):
    """parent attr updates the children attribute of the parent Version."""
    data = setup_version_db_tests
    data["kwargs"]["parent"] = None
    new_version = Version(**data["kwargs"])
    assert new_version.parent != data["test_version"]
    new_version.parent = data["test_version"]
    assert new_version in data["test_version"].children


def test_parent_attribute_will_not_allow_circular_dependencies(setup_version_db_tests):
    """CircularDependency raised if parent attr is a child of the current Version."""
    data = setup_version_db_tests
    data["kwargs"]["parent"] = data["test_version"]
    version1 = Version(**data["kwargs"])
    with pytest.raises(CircularDependencyError) as cm:
        data["test_version"].parent = version1

    assert (
        str(cm.value) == "<tp_SH001_Task1_TestVariant_v001 (Version)> (Version) and "
        "<tp_SH001_Task1_TestVariant_v002 (Version)> (Version) creates a "
        'circular dependency in their "children" attribute'
    )


def test_parent_attribute_will_not_allow_deeper_circular_dependencies(
    setup_version_db_tests,
):
    """CircularDependency raised if the Version is a parent of the current parent."""
    data = setup_version_db_tests
    data["kwargs"]["parent"] = data["test_version"]
    version1 = Version(**data["kwargs"])

    data["kwargs"]["parent"] = version1
    version2 = Version(**data["kwargs"])

    # now create circular dependency
    with pytest.raises(CircularDependencyError) as cm:
        data["test_version"].parent = version2

    assert (
        str(cm.value) == "<tp_SH001_Task1_TestVariant_v001 (Version)> (Version) and "
        "<tp_SH001_Task1_TestVariant_v002 (Version)> (Version) creates a "
        'circular dependency in their "children" attribute'
    )


def test_children_attribute_is_set_to_none(setup_version_db_tests):
    """TypeError raised if the children attribute is set to None."""
    data = setup_version_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_version"].children = None

    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_children_attribute_is_not_set_to_a_list(setup_version_db_tests):
    """TypeError raised if the children attribute is not set to a list."""
    data = setup_version_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_version"].children = "not a list of Version instances"

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_children_attribute_is_not_set_to_a_list_of_version_instances(
    setup_version_db_tests,
):
    """TypeError raised if the children attr is not all Version instances."""
    data = setup_version_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_version"].children = ["not a Version instance", 3]

    assert str(cm.value) == (
        "Version.children should be a list of Version (or derivative) "
        "instances, not str: 'not a Version instance'"
    )


def test_children_attribute_is_working_as_expected(setup_version_db_tests):
    """children attribute is working as expected."""
    data = setup_version_db_tests
    data["kwargs"]["parent"] = None
    new_version1 = Version(**data["kwargs"])
    data["test_version"].children = [new_version1]
    assert new_version1 in data["test_version"].children

    new_version2 = Version(**data["kwargs"])
    data["test_version"].children.append(new_version2)
    assert new_version2 in data["test_version"].children


def test_children_attribute_updates_parent_attribute(setup_version_db_tests):
    """children attribute updates the parent attribute of the children Versions."""
    data = setup_version_db_tests
    data["kwargs"]["parent"] = None
    new_version1 = Version(**data["kwargs"])
    data["test_version"].children = [new_version1]
    assert new_version1.parent == data["test_version"]

    new_version2 = Version(**data["kwargs"])
    data["test_version"].children.append(new_version2)
    assert new_version2.parent == data["test_version"]


def test_children_attribute_will_not_allow_circular_dependencies(
    setup_version_db_tests,
):
    """CircularDependency error raised if a parent is set as a child to its child."""
    data = setup_version_db_tests
    data["kwargs"]["parent"] = None
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()
    new_version2 = Version(**data["kwargs"])
    DBSession.add(new_version2)
    DBSession.commit()

    new_version1.parent = new_version2
    with pytest.raises(CircularDependencyError) as cm:
        new_version1.children.append(new_version2)

    assert (
        str(cm.value) == "<tp_SH001_Task1_TestVariant_v003 (Version)> (Version) and "
        "<tp_SH001_Task1_TestVariant_v002 (Version)> (Version) creates a "
        'circular dependency in their "children" attribute'
    )


def test_children_attribute_will_not_allow_deeper_circular_dependencies(
    setup_version_db_tests,
):
    """CircularDependency error raised if a parent Version of a parent Version is set as
    a children to its grand child."""
    data = setup_version_db_tests
    data["kwargs"]["parent"] = None
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()
    new_version2 = Version(**data["kwargs"])
    DBSession.add(new_version2)
    DBSession.commit()
    new_version3 = Version(**data["kwargs"])
    DBSession.add(new_version2)
    DBSession.commit()

    new_version1.parent = new_version2
    new_version2.parent = new_version3

    with pytest.raises(CircularDependencyError) as cm:
        new_version1.children.append(new_version3)

    assert (
        str(cm.value) == "<tp_SH001_Task1_TestVariant_v004 (Version)> (Version) and "
        "<tp_SH001_Task1_TestVariant_v002 (Version)> (Version) creates a "
        'circular dependency in their "children" attribute'
    )


def test_update_paths_will_render_the_appropriate_template_from_the_related_project(
    setup_version_db_tests,
):
    """update_paths method updates Version.full_path by rendering the related Project
    FilenameTemplate.."""
    data = setup_version_db_tests
    # create a FilenameTemplate for Task instances

    # A Template for Assets
    # ......../Assets/{{asset.type.name}}/{{asset.nice_name}}/{{task.type.name}}/
    #
    # Project1/Assets/Character/Sero/Modeling/Sero_Modeling_Main_v001.ma
    #
    # + Project1
    # |
    # +-+ Assets (Task)
    # | |
    # | +-+ Characters
    # |   |
    # |   +-+ Sero (Asset)
    # |     |
    # |     +-> Version 1
    # |     |
    # |     +-+ Modeling (Task)
    # |       |
    # |       +-+ Body Modeling (Task)
    # |         |
    # |         +-+ Coarse Modeling (Task)
    # |         | |
    # |         | +-> Version 1 (Version)
    # |         |
    # |         +-+ Fine Modeling (Task)
    # |           |
    # |           +-> Version 1 (Version): Fine_Modeling_Main_v001.ma
    # |                                  Assets/Characters/Sero/Modeling/Body_Modeling/Fine_Modeling/Fine_Modeling_Main_v001.ma
    # |
    # +-+ Shots (Task)
    #   |
    #   +-+ Shot 10 (Shot)
    #   | |
    #   | +-+ Layout (Task)
    #   |   |
    #   |   +-> Version 1 (Version): Layout_v001.ma
    #   |                            Shots/Shot_1/Layout/Layout_Main_v001.ma
    #   |
    #   +-+ Shot 2 (Shot)
    #     |
    #     +-+ FX (Task)
    #       |
    #       +-> Version 1 (Version)

    ft = FilenameTemplate(
        name="Task Filename Template",
        target_entity_type="Task",
        path="{{project.code}}/{%- for parent_task in parent_tasks -%}"
        "{{parent_task.nice_name}}/{%- endfor -%}",
        filename="{{task.nice_name}}_{{version.variant_name}}"
        '_v{{"%03d"|format(version.version_number)}}{{extension}}',
    )
    data["test_project"].structure.templates.append(ft)
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()
    new_version1.update_paths()
    assert new_version1.path == "tp/SH001/Task1"

    new_version1.extension = ".ma"
    assert new_version1.filename == "Task1_TestVariant_v002.ma"


def test_update_paths_will_preserve_extension(setup_version_db_tests):
    """update_paths method will preserve the extension."""
    data = setup_version_db_tests
    # create a FilenameTemplate for Task instances
    ft = FilenameTemplate(
        name="Task Filename Template",
        target_entity_type="Task",
        path="{{project.code}}/{%- for parent_task in parent_tasks -%}"
        "{{parent_task.nice_name}}/{%- endfor -%}",
        filename="{{task.nice_name}}_{{version.variant_name}}"
        '_v{{"%03d"|format(version.version_number)}}{{extension}}',
    )
    data["test_project"].structure.templates.append(ft)
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()
    new_version1.update_paths()
    assert new_version1.path == "tp/SH001/Task1"

    extension = ".ma"
    new_version1.extension = extension
    assert new_version1.filename == "Task1_TestVariant_v002.ma"

    # rename the task and update the paths
    data["test_task1"].name = "Task2"

    # now call update_paths and expect the extension to be preserved
    new_version1.update_paths()
    assert new_version1.filename == "Task2_TestVariant_v002.ma"
    assert new_version1.extension == extension


def test_update_paths_will_raise_a_runtime_error_if_there_is_no_suitable_filename_template(
    setup_version_db_tests,
):
    """update_paths method raises a RuntimeError if there is no suitable
    FilenameTemplate instance found."""
    data = setup_version_db_tests
    data["kwargs"]["parent"] = None
    new_version1 = Version(**data["kwargs"])
    with pytest.raises(RuntimeError) as cm:
        new_version1.update_paths()

    assert (
        str(cm.value)
        == "There are no suitable FilenameTemplate (target_entity_type == "
        "'Task') defined in the Structure of the related Project "
        "instance, please create a new "
        "stalker.models.template.FilenameTemplate instance with its "
        "'target_entity_type' attribute is set to 'Task' and assign it "
        "to the `templates` attribute of the structure of the project"
    )


def test_template_variables_project(setup_version_db_tests):
    """project in template variables is correct."""
    data = setup_version_db_tests
    kwargs = data["test_version"]._template_variables()
    assert kwargs["project"] == data["test_version"].task.project


def test_template_variables_sequences(setup_version_db_tests):
    """sequences in template variables is correct."""
    data = setup_version_db_tests
    kwargs = data["test_version"]._template_variables()
    assert kwargs["sequences"] == []


def test_template_variables_scenes(setup_version_db_tests):
    """scenes in template variables is correct."""
    data = setup_version_db_tests
    kwargs = data["test_version"]._template_variables()
    assert kwargs["scenes"] == []


def test_template_variables_shot(setup_version_db_tests):
    """shot in template variables is correct."""
    data = setup_version_db_tests
    kwargs = data["test_version"]._template_variables()
    assert kwargs["shot"] == data["test_version"].task


def test_template_variables_asset(setup_version_db_tests):
    """asset in template variables is correct."""
    data = setup_version_db_tests
    kwargs = data["test_version"]._template_variables()
    assert kwargs["asset"] == data["test_version"].task


def test_template_variables_task(setup_version_db_tests):
    """task in template variables is correct."""
    data = setup_version_db_tests
    kwargs = data["test_version"]._template_variables()
    assert kwargs["task"] == data["test_version"].task


def test_template_variables_parent_tasks(setup_version_db_tests):
    """parent_tasks in template variables is correct."""
    data = setup_version_db_tests
    kwargs = data["test_version"]._template_variables()
    parents = data["test_version"].task.parents
    parents.append(data["test_version"].task)
    assert kwargs["parent_tasks"] == parents


def test_template_variables_version(setup_version_db_tests):
    """version in template variables is correct."""
    data = setup_version_db_tests
    kwargs = data["test_version"]._template_variables()
    assert kwargs["version"] == data["test_version"]


def test_template_variables_type(setup_version_db_tests):
    """type in template variables is correct."""
    data = setup_version_db_tests
    kwargs = data["test_version"]._template_variables()
    assert kwargs["type"] == data["test_version"].type


def test_absolute_full_path_works_as_expected(setup_version_db_tests):
    """absolute_full_path attribute works as expected."""
    data = setup_version_db_tests
    data["patcher"].patch("Linux")
    ft = FilenameTemplate(
        name="Task Filename Template",
        target_entity_type="Task",
        path="{{project.repositories[0].path}}/{{project.code}}/"
        "{%- for parent_task in parent_tasks -%}"
        "{{parent_task.nice_name}}/"
        "{%- endfor -%}",
        filename="{{task.nice_name}}_{{version.variant_name}}"
        '_v{{"%03d"|format(version.version_number)}}{{extension}}',
    )
    data["test_project"].structure.templates.append(ft)
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()

    new_version1.variant_name = "TestVariant@BBOX"

    new_version1.update_paths()
    new_version1.extension = ".ma"
    assert new_version1.extension == ".ma"

    assert (
        new_version1.absolute_full_path
        == "/mnt/T/tp/SH001/Task1/Task1_TestVariant@BBOX_v002.ma"
    )


def test_latest_published_version_is_read_only(setup_version_db_tests):
    """latest_published_version is a read only attribute."""
    data = setup_version_db_tests
    with pytest.raises(AttributeError) as cm:
        data["test_version"].latest_published_version = True

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'latest_published_version'",
    }.get(
        sys.version_info.minor,
        "property 'latest_published_version' of 'Version' object has no setter",
    )

    assert str(cm.value) == error_message


def test_latest_published_version_is_working_as_expected(setup_version_db_tests):
    """is_latest_published_version is working as expected."""
    data = setup_version_db_tests
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()

    new_version2 = Version(**data["kwargs"])
    DBSession.add(new_version2)
    DBSession.commit()

    new_version3 = Version(**data["kwargs"])
    DBSession.add(new_version3)
    DBSession.commit()

    new_version4 = Version(**data["kwargs"])
    DBSession.add(new_version4)
    DBSession.commit()

    new_version5 = Version(**data["kwargs"])
    DBSession.add(new_version5)
    DBSession.commit()

    new_version1.is_published = True
    new_version3.is_published = True
    new_version4.is_published = True

    assert new_version1.latest_published_version == new_version4
    assert new_version2.latest_published_version == new_version4
    assert new_version3.latest_published_version == new_version4
    assert new_version4.latest_published_version == new_version4
    assert new_version5.latest_published_version == new_version4


def test_is_latest_published_version_is_working_as_expected(setup_version_db_tests):
    """is_latest_published_version is working as expected."""
    data = setup_version_db_tests
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()

    new_version2 = Version(**data["kwargs"])
    DBSession.add(new_version2)
    DBSession.commit()

    new_version3 = Version(**data["kwargs"])
    DBSession.add(new_version3)
    DBSession.commit()

    new_version4 = Version(**data["kwargs"])
    DBSession.add(new_version4)
    DBSession.commit()

    new_version5 = Version(**data["kwargs"])
    DBSession.add(new_version5)
    DBSession.commit()

    new_version1.is_published = True
    new_version3.is_published = True
    new_version4.is_published = True

    assert not new_version1.is_latest_published_version()
    assert not new_version2.is_latest_published_version()
    assert not new_version3.is_latest_published_version()
    assert new_version4.is_latest_published_version()
    assert not new_version5.is_latest_published_version()


def test_equality_operator(setup_version_db_tests):
    """equality of two Version instances."""
    data = setup_version_db_tests
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()

    new_version2 = Version(**data["kwargs"])
    DBSession.add(new_version2)
    DBSession.commit()

    new_version3 = Version(**data["kwargs"])
    DBSession.add(new_version3)
    DBSession.commit()

    new_version4 = Version(**data["kwargs"])
    DBSession.add(new_version4)
    DBSession.commit()

    new_version5 = Version(**data["kwargs"])
    DBSession.add(new_version5)
    DBSession.commit()

    new_version1.is_published = True
    new_version3.is_published = True
    new_version4.is_published = True

    assert not new_version1 == new_version2
    assert not new_version1 == new_version3
    assert not new_version1 == new_version4
    assert not new_version1 == new_version5

    assert not new_version2 == new_version3
    assert not new_version2 == new_version4
    assert not new_version2 == new_version5

    assert not new_version3 == new_version4
    assert not new_version3 == new_version5

    assert not new_version4 == new_version5


def test_inequality_operator(setup_version_db_tests):
    """inequality of two Version instances."""
    data = setup_version_db_tests
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()

    new_version2 = Version(**data["kwargs"])
    DBSession.add(new_version2)
    DBSession.commit()

    new_version3 = Version(**data["kwargs"])
    DBSession.add(new_version3)
    DBSession.commit()

    new_version4 = Version(**data["kwargs"])
    DBSession.add(new_version4)
    DBSession.commit()

    new_version5 = Version(**data["kwargs"])
    DBSession.add(new_version5)
    DBSession.commit()

    new_version1.is_published = True
    new_version3.is_published = True
    new_version4.is_published = True

    assert new_version1 != new_version2
    assert new_version1 != new_version3
    assert new_version1 != new_version4
    assert new_version1 != new_version5

    assert new_version2 != new_version3
    assert new_version2 != new_version4
    assert new_version2 != new_version5

    assert new_version3 != new_version4
    assert new_version3 != new_version5

    assert new_version4 != new_version5


def test_created_with_argument_can_be_skipped(setup_version_db_tests):
    """created_with argument can be skipped."""
    data = setup_version_db_tests
    data["kwargs"].pop("created_with")
    Version(**data["kwargs"])


def test_created_with_argument_can_be_none(setup_version_db_tests):
    """created_with argument can be None."""
    data = setup_version_db_tests
    data["kwargs"]["created_with"] = None
    Version(**data["kwargs"])


def test_created_with_attribute_can_be_set_to_none(setup_version_db_tests):
    """created with attribute can be set to None."""
    data = setup_version_db_tests
    data["test_version"].created_with = None


def test_created_with_argument_accepts_only_string_or_none(setup_version_db_tests):
    """TypeError raised if the created_with arg is not a string or None."""
    data = setup_version_db_tests
    data["kwargs"]["created_with"] = 234
    with pytest.raises(TypeError) as cm:
        Version(**data["kwargs"])
    assert str(cm.value) == (
        "Version.created_with should be an instance of str, not int: '234'"
    )


def test_created_with_attribute_accepts_only_string_or_none(setup_version_db_tests):
    """TypeError raised if the created_with attr is not a str or None."""
    data = setup_version_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_version"].created_with = 234

    assert str(cm.value) == (
        "Version.created_with should be an instance of str, not int: '234'"
    )


def test_created_with_argument_is_working_as_expected(setup_version_db_tests):
    """created_with argument value is passed to created_with attribute."""
    data = setup_version_db_tests
    test_value = "Maya"
    data["kwargs"]["created_with"] = test_value
    test_version = Version(**data["kwargs"])
    assert test_version.created_with == test_value


def test_created_with_attribute_is_working_as_expected(setup_version_db_tests):
    """created_with attribute is working as expected."""
    data = setup_version_db_tests
    test_value = "Maya"
    assert data["test_version"].created_with != test_value
    data["test_version"].created_with = test_value
    assert data["test_version"].created_with == test_value


def test_max_version_number_attribute_is_read_only(setup_version_db_tests):
    """max_version_number attribute is read only."""
    data = setup_version_db_tests
    with pytest.raises(AttributeError) as cm:
        data["test_version"].max_version_number = 20

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'max_version_number'",
    }.get(
        sys.version_info.minor,
        "property 'max_version_number' of 'Version' object has no setter",
    )

    assert str(cm.value) == error_message


def test_max_version_number_attribute_is_working_as_expected(setup_version_db_tests):
    """max_version_number attribute is working as expected."""
    data = setup_version_db_tests
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()

    new_version2 = Version(**data["kwargs"])
    DBSession.add(new_version2)
    DBSession.commit()

    new_version3 = Version(**data["kwargs"])
    DBSession.add(new_version3)
    DBSession.commit()

    new_version4 = Version(**data["kwargs"])
    DBSession.add(new_version4)
    DBSession.commit()

    new_version5 = Version(**data["kwargs"])
    DBSession.add(new_version5)
    DBSession.commit()

    assert new_version5.version_number == 6

    assert new_version1.max_version_number == 6
    assert new_version2.max_version_number == 6
    assert new_version3.max_version_number == 6
    assert new_version4.max_version_number == 6
    assert new_version5.max_version_number == 6


def test_latest_version_attribute_is_read_only(setup_version_db_tests):
    """last_version attribute is a read only attribute."""
    data = setup_version_db_tests
    with pytest.raises(AttributeError) as cm:
        data["test_version"].latest_version = 3453

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'latest_version'",
    }.get(
        sys.version_info.minor,
        "property 'latest_version' of 'Version' object has no setter",
    )

    assert str(cm.value) == error_message


def test_latest_version_attribute_is_working_as_expected(setup_version_db_tests):
    """last_version attribute is working as expected."""
    data = setup_version_db_tests
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()

    new_version2 = Version(**data["kwargs"])
    DBSession.add(new_version2)
    DBSession.commit()

    new_version3 = Version(**data["kwargs"])
    DBSession.add(new_version3)
    DBSession.commit()

    new_version4 = Version(**data["kwargs"])
    DBSession.add(new_version4)
    DBSession.commit()

    new_version5 = Version(**data["kwargs"])
    DBSession.add(new_version5)
    DBSession.commit()

    assert new_version5.version_number == 6

    assert new_version1.latest_version == new_version5
    assert new_version2.latest_version == new_version5
    assert new_version3.latest_version == new_version5
    assert new_version4.latest_version == new_version5
    assert new_version5.latest_version == new_version5


def test_naming_parents_attribute_is_a_read_only_property(setup_version_db_tests):
    """naming_parents attribute is a read only property."""
    data = setup_version_db_tests
    with pytest.raises(AttributeError) as cm:
        data["test_version"].naming_parents = [data["test_task1"]]

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'naming_parents'",
    }.get(
        sys.version_info.minor,
        "property 'naming_parents' of 'Version' object has no setter",
    )

    assert str(cm.value) == error_message


def test_naming_parents_attribute_is_working_as_expected(setup_version_db_tests):
    """naming_parents attribute is working as expected."""
    data = setup_version_db_tests
    # for data["test_version"]
    assert data["test_version"].naming_parents == [
        data["test_shot1"],
        data["test_task1"],
    ]

    # for a new version of a task
    task1 = Task(
        name="Test Task 1",
        project=data["test_project"],
    )

    task2 = Task(
        name="Test Task 2",
        parent=task1,
    )

    task3 = Task(
        name="Test Task 3",
        parent=task2,
    )
    DBSession.add_all([task1, task2, task3])
    DBSession.commit()

    version1 = Version(task=task3)
    DBSession.add(version1)
    DBSession.commit()

    assert version1.naming_parents == [task1, task2, task3]

    # for an asset version
    character_type = Type(target_entity_type="Asset", name="Character", code="Char")
    asset1 = Asset(name="Asset1", code="Asset1", parent=task1, type=character_type)
    DBSession.add(asset1)
    DBSession.commit()

    version2 = Version(task=asset1)
    assert version2.naming_parents == [asset1]

    # for a version of a task of a shot
    shot2 = Shot(
        name="SH002",
        code="SH002",
        parent=task3,
    )
    DBSession.add(shot2)
    DBSession.commit()

    task4 = Task(
        name="Test Task 4",
        parent=shot2,
    )
    DBSession.add(task4)
    DBSession.commit()

    version3 = Version(task=task4)

    assert version3.naming_parents == [shot2, task4]

    # for an asset of a shot
    asset2 = Asset(name="Asset2", code="Asset2", parent=shot2, type=character_type)
    DBSession.add(asset2)
    DBSession.commit()

    version4 = Version(task=asset2)
    assert version4.naming_parents == [asset2]


def test_nice_name_attribute_is_working_as_expected(setup_version_db_tests):
    """nice_name attribute is working as expected."""
    data = setup_version_db_tests
    # for data["test_version"]
    assert data["test_version"].naming_parents == [
        data["test_shot1"],
        data["test_task1"],
    ]

    # for a new version of a task
    task1 = Task(
        name="Test Task 1",
        project=data["test_project"],
    )

    task2 = Task(
        name="Test Task 2",
        parent=task1,
    )

    task3 = Task(
        name="Test Task 3",
        parent=task2,
    )
    DBSession.add_all([task1, task2, task3])
    DBSession.commit()

    version1 = Version(task=task3, variant_name="Variant1@Main")
    DBSession.add(version1)
    DBSession.commit()

    assert version1.nice_name == "{}_{}_{}_{}".format(
        task1.nice_name,
        task2.nice_name,
        task3.nice_name,
        version1.variant_name,
    )

    # for an asset version
    character_type = Type(target_entity_type="Asset", name="Character", code="Char")
    asset1 = Asset(name="Asset1", code="Asset1", parent=task1, type=character_type)
    DBSession.add(asset1)
    DBSession.commit()

    version2 = Version(task=asset1)
    assert version2.nice_name == "{}_{}".format(asset1.nice_name, version2.variant_name)

    # for a version of a task of a shot
    shot2 = Shot(
        name="SH002",
        code="SH002",
        parent=task3,
    )
    DBSession.add(shot2)
    DBSession.commit()

    task4 = Task(
        name="Test Task 4",
        parent=shot2,
    )
    DBSession.add(task4)
    DBSession.commit()

    version3 = Version(task=task4)

    assert version3.nice_name == "{}_{}_{}".format(
        shot2.nice_name,
        task4.nice_name,
        version3.variant_name,
    )

    # for an asset of a shot
    asset2 = Asset(name="Asset2", code="Asset2", parent=shot2, type=character_type)
    DBSession.add(asset2)
    DBSession.commit()

    version4 = Version(task=asset2)
    assert version4.nice_name == "{}_{}".format(asset2.nice_name, version4.variant_name)


def test_string_representation_is_a_little_bit_meaningful(setup_version_db_tests):
    """__str__ or __repr__ result is meaningful."""
    data = setup_version_db_tests
    assert "<tp_SH001_Task1_TestVariant_v001 (Version)>" == f'{data["test_version"]}'


def test_walk_hierarchy_is_working_as_expected_in_dfs_mode(setup_version_db_tests):
    """walk_hierarchy() method is working in DFS mode correctly."""
    data = setup_version_db_tests
    v1 = Version(task=data["test_task1"])
    v2 = Version(task=data["test_task1"], parent=v1)
    v3 = Version(task=data["test_task1"], parent=v2)
    v4 = Version(task=data["test_task1"], parent=v3)
    v5 = Version(task=data["test_task1"], parent=v1)
    expected_result = [v1, v2, v3, v4, v5]
    visited_versions = []
    for v in v1.walk_hierarchy():
        visited_versions.append(v)
    assert expected_result == visited_versions


def test_walk_inputs_is_working_as_expected_in_dfs_mode(setup_version_db_tests):
    """walk_inputs() method is working in DFS mode correctly."""
    data = setup_version_db_tests
    v1 = Version(task=data["test_task1"])
    v2 = Version(task=data["test_task1"])
    v3 = Version(task=data["test_task1"])
    v4 = Version(task=data["test_task1"])
    v5 = Version(task=data["test_task1"])

    v5.inputs = [v4]
    v4.inputs = [v3, v2]
    v3.inputs = [v1]
    v2.inputs = [v1]

    expected_result = [v5, v4, v3, v1, v2, v1]
    visited_versions = []
    for v in v5.walk_inputs():
        visited_versions.append(v)

    assert expected_result == visited_versions


# def test_path_attribute_value_is_calculated_on_init(setup_version_db_tests):
#     """path attribute value is automatically calculated on
#     Version instance initialize
#     """
#     ft = FilenameTemplate(
#         name='Task Filename Template',
#         target_entity_type='Task',
#         path='{{project.code}}/{%- for p in parent_tasks -%}'
#              '{{p.nice_name}}/{%- endfor -%}',
#         filename='{{version.nice_name}}_v{{"%03d"|format(version.version_number)}}{{extension}}'
#     )
#     data["test_project"].structure.templates.append(ft)
#     DBSession.add(data["test_project"])
#     DBSession.commit()
#
#     print('entity_type: {}'.format(data["test_task1"].entity_type))
#
#     # v1 = Version(task=data["test_task1"])
#     # assert 'tp/SH001/task1/task1_Main_v001' == v1.path
#     data["fail"]()


@pytest.fixture(scope="function")
def setup_version_tests():
    """Set up non-DB related tests of Version class."""
    data = dict()
    data["patcher"] = PlatformPatcher()

    # statuses
    data["test_status1"] = Status(name="Status1", code="STS1")
    data["test_status2"] = Status(name="Status2", code="STS2")
    data["test_status3"] = Status(name="Status3", code="STS3")
    data["test_status4"] = Status(name="Status4", code="STS4")
    data["test_status5"] = Status(name="Status5", code="STS5")

    # status lists
    data["test_task_status_list"] = StatusList(
        name="Task Status List",
        statuses=[
            data["test_status1"],
            data["test_status2"],
            data["test_status3"],
            data["test_status4"],
            data["test_status5"],
        ],
        target_entity_type="Task",
    )

    data["test_asset_status_list"] = StatusList(
        name="Asset Status List",
        statuses=[
            data["test_status1"],
            data["test_status2"],
            data["test_status3"],
            data["test_status4"],
            data["test_status5"],
        ],
        target_entity_type="Asset",
    )

    data["test_shot_status_list"] = StatusList(
        name="Shot Status List",
        statuses=[
            data["test_status1"],
            data["test_status2"],
            data["test_status3"],
            data["test_status4"],
            data["test_status5"],
        ],
        target_entity_type="Shot",
    )

    data["test_sequence_status_list"] = StatusList(
        name="Sequence Status List",
        statuses=[
            data["test_status1"],
            data["test_status2"],
            data["test_status3"],
            data["test_status4"],
            data["test_status5"],
        ],
        target_entity_type="Sequence",
    )

    data["test_project_status_list"] = StatusList(
        name="Project Status List",
        statuses=[
            data["test_status1"],
            data["test_status2"],
            data["test_status3"],
            data["test_status4"],
            data["test_status5"],
        ],
        target_entity_type="Project",
    )

    # repository
    data["test_repo"] = Repository(
        name="Test Repository",
        code="TR",
        linux_path="/mnt/T/",
        windows_path="T:/",
        macos_path="/Volumes/T/",
    )

    # a project type
    data["test_project_type"] = Type(
        name="Test",
        code="test",
        target_entity_type="Project",
    )

    # create a structure
    data["test_structure"] = Structure(name="Test Project Structure")

    # create a project
    data["test_project"] = Project(
        name="Test Project",
        code="tp",
        type=data["test_project_type"],
        status_list=data["test_project_status_list"],
        repositories=[data["test_repo"]],
        structure=data["test_structure"],
    )

    # create a sequence
    data["test_sequence"] = Sequence(
        name="Test Sequence",
        code="SEQ1",
        project=data["test_project"],
        status_list=data["test_sequence_status_list"],
    )

    # create a shot
    data["test_shot1"] = Shot(
        name="SH001",
        code="SH001",
        project=data["test_project"],
        sequences=[data["test_sequence"]],
        status_list=data["test_shot_status_list"],
    )

    # create a group of Tasks for the shot
    data["test_task1"] = Task(
        name="Task1",
        parent=data["test_shot1"],
        status_list=data["test_task_status_list"],
    )

    # a Link for the input file
    data["test_input_link1"] = Link(
        name="Input Link 1",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_beauty_v001.###.exr",
    )

    data["test_input_link2"] = Link(
        name="Input Link 2",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_occ_v001.###.exr",
    )

    # a Link for the output file
    data["test_output_link1"] = Link(
        name="Output Link 1",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_beauty_v001.###.exr",
    )

    data["test_output_link2"] = Link(
        name="Output Link 2",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_occ_v001.###.exr",
    )

    # now create a version for the Task
    data["kwargs"] = {
        "variant_name": "TestVariant",
        "inputs": [data["test_input_link1"], data["test_input_link2"]],
        "outputs": [data["test_output_link1"], data["test_output_link2"]],
        "task": data["test_task1"],
        "created_with": "Houdini",
    }

    # and the Version
    data["test_version"] = Version(**data["kwargs"])

    # set the published to False
    data["test_version"].is_published = False
    yield data
    # clean up test
    data["patcher"].restore()


def test_children_attribute_will_not_allow_circular_dependencies_2(
    setup_version_tests,
):
    """CircularDependency error raised if a parent is set as a child to its child."""
    data = setup_version_tests
    data["kwargs"]["parent"] = None
    new_version1 = Version(**data["kwargs"])
    new_version2 = Version(**data["kwargs"])

    new_version1.parent = new_version2
    with pytest.raises(CircularDependencyError) as cm:
        new_version1.children.append(new_version2)

    assert (
        str(cm.value) == "<tp_SH001_Task1_TestVariant_v003 (Version)> (Version) and "
        "<tp_SH001_Task1_TestVariant_v002 (Version)> (Version) creates a "
        'circular dependency in their "children" attribute'
    )


def test_children_attribute_will_not_allow_deeper_circular_dependencies_2(
    setup_version_tests,
):
    """CircularDependency error raised if the parent of a parent Version is set as a
    children to its grand child."""
    data = setup_version_tests
    data["kwargs"]["parent"] = None
    new_version1 = Version(**data["kwargs"])
    new_version2 = Version(**data["kwargs"])
    new_version3 = Version(**data["kwargs"])

    new_version1.parent = new_version2
    new_version2.parent = new_version3

    with pytest.raises(CircularDependencyError) as cm:
        new_version1.children.append(new_version3)

    assert (
        str(cm.value) == "<tp_SH001_Task1_TestVariant_v004 (Version)> (Version) and "
        "<tp_SH001_Task1_TestVariant_v002 (Version)> (Version) creates a "
        'circular dependency in their "children" attribute'
    )
