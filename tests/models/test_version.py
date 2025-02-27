# -*- coding: utf-8 -*-
import copy
import logging
from pathlib import Path
import sys

import pytest

from stalker import (
    Asset,
    FilenameTemplate,
    File,
    Project,
    Repository,
    Scene,
    Sequence,
    Shot,
    Status,
    StatusList,
    Structure,
    Task,
    Type,
    User,
    Variant,
    Version,
    defaults,
    log,
)
from stalker.db.session import DBSession
from stalker.exceptions import CircularDependencyError
from stalker.models.entity import Entity

from tests.utils import PlatformPatcher

logger = logging.getLogger("stalker.models.version.Version")
logger.setLevel(log.logging_level)


@pytest.fixture(scope="function")
def setup_version_db_tests(setup_postgresql_db):
    """Set up the tests for the Version class with a DB."""
    data = dict()
    data["patcher"] = PlatformPatcher()

    # Users
    data["test_user1"] = User(
        name="Test User 1",
        login="tuser1",
        email="tuser1@test.com",
        password="secret",
    )
    data["test_user2"] = User(
        name="Test User 2",
        login="tuser2",
        email="tuser2@test.com",
        password="secret",
    )

    # statuses
    data["status_wip"] = Status.query.filter_by(code="WIP").first()

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

    # create a filename template for Variants
    data["test_filename_template"] = FilenameTemplate(
        name="Variant Filename Template",
        target_entity_type="Variant",
        path="{{project.code}}/{%- for parent_task in parent_tasks -%}"
        "{{parent_task.nice_name}}/{%- endfor -%}",
        filename="{{version.nice_name}}"
        '_r{{"%02d"|format(version.revision_number)}}'
        '_v{{"%03d"|format(version.version_number)}}'
        "{{extension}}",
    )
    DBSession.add(data["test_filename_template"])
    DBSession.commit()
    # create a structure
    data["test_structure"] = Structure(
        name="Test Project Structure", templates=[data["test_filename_template"]]
    )
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

    data["test_scene"] = Scene(
        name="Test Scene",
        code="SC001",
        project=data["test_project"],
    )
    DBSession.add(data["test_scene"])
    DBSession.commit()

    # create a shot
    data["test_shot1"] = Shot(
        name="SH001",
        code="SH001",
        project=data["test_project"],
        sequence=data["test_sequence"],
        scene=data["test_scene"],
    )
    DBSession.add(data["test_shot1"])
    DBSession.commit()

    # create a group of Tasks for the shot
    data["test_task1"] = Task(name="FX", parent=data["test_shot1"])
    DBSession.add(data["test_task1"])
    DBSession.commit()

    data["test_variant1"] = Variant(name="Main", parent=data["test_task1"])
    DBSession.add(data["test_variant1"])
    DBSession.commit()

    # a File for the files attribute
    data["test_file1"] = File(
        name="File 1",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "SH001_FX_Main_r01_v001.ma",
    )
    DBSession.add(data["test_file1"])

    data["test_file2"] = File(
        name="File 2",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "SH001_FX_Main_r01_v002.ma",
    )
    DBSession.add(data["test_file2"])

    # a File for the input file
    data["test_input_file1"] = File(
        name="Input File 1",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_beauty_v001.###.exr",
    )
    DBSession.add(data["test_input_file1"])

    data["test_input_file2"] = File(
        name="Input File 2",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_occ_v001.###.exr",
    )
    DBSession.add(data["test_input_file2"])

    # a File for the output file
    data["test_output_file1"] = File(
        name="Output File 1",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_beauty_v001.###.exr",
    )
    DBSession.add(data["test_output_file1"])

    data["test_output_file2"] = File(
        name="Output File 2",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_occ_v001.###.exr",
    )
    DBSession.add(data["test_output_file2"])
    DBSession.commit()

    # now create a version for the Task
    data["kwargs"] = {
        "files": [data["test_file1"], data["test_file2"]],
        "task": data["test_variant1"],
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


def test_version_derives_from_entity():
    """Version class derives from Entity."""
    assert Entity == Version.__mro__[1]


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
        "Version.task should be a Task, Asset, Shot, Scene, Sequence or Variant "
        "instance, not str: 'a task'"
    )


def test_task_attribute_is_not_a_task(setup_version_db_tests):
    """TypeError raised if the task attribute is not a Task instance."""
    data = setup_version_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_version"].task = "a task"
    assert str(cm.value) == (
        "Version.task should be a Task, Asset, Shot, Scene, Sequence or Variant "
        "instance, not str: 'a task'"
    )


def test_task_attribute_is_working_as_expected(setup_version_db_tests):
    """task attribute is working as expected."""
    data = setup_version_db_tests
    new_task = Variant(
        name="New Test Variant",
        parent=data["test_shot1"],
    )
    DBSession.add(new_task)
    assert data["test_version"].task is not new_task
    data["test_version"].task = new_task
    assert data["test_version"].task is new_task


def test_revision_number_arg_is_skipped(setup_version_db_tests):
    """revision_number arg can be skipped."""
    data = setup_version_db_tests
    new_version = Version(**data["kwargs"])
    assert isinstance(new_version, Version)
    assert new_version.revision_number == 1


def test_revision_number_arg_is_none(setup_version_db_tests):
    """revision_number arg can be None."""
    data = setup_version_db_tests
    data["kwargs"]["revision_number"] = None
    new_version = Version(**data["kwargs"])
    assert isinstance(new_version, Version)
    assert new_version.revision_number == 1


def test_revision_number_attr_cannot_be_set_to_none(setup_version_db_tests):
    """revision_number can be None."""
    data = setup_version_db_tests
    data["kwargs"]["revision_number"] = 12
    new_version = Version(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_version.revision_number = None
    assert str(cm.value) == (
        "Version.revision_number should be a positive integer, not NoneType: 'None'"
    )


def test_revision_number_arg_is_not_an_integer(setup_version_db_tests):
    """revision_number arg is not an integer raises TypeError."""
    data = setup_version_db_tests
    data["kwargs"]["revision_number"] = "not an integer"
    with pytest.raises(TypeError) as cm:
        _ = Version(**data["kwargs"])
    assert str(cm.value) == (
        "Version.revision_number should be a positive integer, "
        "not str: 'not an integer'"
    )


def test_revision_number_attr_is_not_an_integer(setup_version_db_tests):
    """revision_number attr is not an integer raises TypeError."""
    data = setup_version_db_tests
    data["kwargs"]["revision_number"] = 14
    new_version = Version(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_version.revision_number = "not an integer"
    assert str(cm.value) == (
        "Version.revision_number should be a positive integer, "
        "not str: 'not an integer'"
    )


def test_revision_number_arg_is_not_a_positive_integer(setup_version_db_tests):
    """revision_number arg is not a positive integer raises ValueError."""
    data = setup_version_db_tests
    data["kwargs"]["revision_number"] = -109
    with pytest.raises(ValueError) as cm:
        _ = Version(**data["kwargs"])
    assert str(cm.value) == (
        "Version.revision_number should be a positive integer, " "not int: '-109'"
    )


def test_revision_number_attr_is_not_a_positive_integer(setup_version_db_tests):
    """revision_number attr is not a positive integer raises ValueError."""
    data = setup_version_db_tests
    data["kwargs"]["revision_number"] = 153
    new_version = Version(**data["kwargs"])
    with pytest.raises(ValueError) as cm:
        new_version.revision_number = -109
    assert str(cm.value) == (
        "Version.revision_number should be a positive integer, " "not int: '-109'"
    )


def test_revision_number_arg_can_be_non_sequential(setup_version_db_tests):
    """revision_number arg can be set to any positive number."""
    data = setup_version_db_tests
    data["kwargs"]["revision_number"] = 21
    new_version = Version(**data["kwargs"])
    assert isinstance(new_version, Version)
    assert new_version.revision_number == 21


def test_revision_number_attr_can_be_non_sequential(setup_version_db_tests):
    """revision_number attr can be set to any positive number."""
    data = setup_version_db_tests
    data["kwargs"]["revision_number"] = 21
    new_version = Version(**data["kwargs"])
    assert new_version.revision_number != 13
    new_version.revision_number = 13
    assert new_version.revision_number == 13


def test_revision_number_attr_changed_will_reset_version_number(setup_version_db_tests):
    """revision_number attr can be set to any positive number."""
    data = setup_version_db_tests
    data["kwargs"]["revision_number"] = 21
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert new_version.version_number == 1
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert new_version.version_number == 2
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert new_version.version_number == 3
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert new_version.version_number == 4
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert new_version.version_number == 5
    assert new_version.revision_number != 13
    new_version.revision_number = 13
    DBSession.save(new_version)
    assert new_version.revision_number == 13
    assert new_version.version_number == 1
    new_version.revision_number = 21
    assert new_version.version_number == 5


def test_revision_number_attr_not_changed_will_not_reset_version_number(
    setup_version_db_tests,
):
    """revision_number attr can be set to any positive number."""
    data = setup_version_db_tests
    data["kwargs"]["revision_number"] = 21
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    new_version.revision_number = 13
    DBSession.save(new_version)
    new_version.revision_number = 21
    DBSession.save(new_version)
    new_version.revision_number = 21
    assert new_version.version_number == 5


def test_revision_number_arg_value_is_passed_to_revision_number_attr(
    setup_version_db_tests,
):
    """revision_number arg value is passed to revision_number attr."""
    data = setup_version_db_tests
    data["kwargs"]["revision_number"] = 21
    new_version = Version(**data["kwargs"])
    assert isinstance(new_version, Version)
    assert new_version.revision_number == 21


def test_revision_number_arg_effects_version_number(setup_version_db_tests):
    """revision_number arg effects version_number value."""
    data = setup_version_db_tests
    data["kwargs"]["revision_number"] = 1
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert isinstance(new_version, Version)
    assert new_version.revision_number == 1
    assert new_version.version_number == 2

    # second version
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert isinstance(new_version, Version)
    assert new_version.revision_number == 1
    assert new_version.version_number == 3

    # third version
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert isinstance(new_version, Version)
    assert new_version.revision_number == 1
    assert new_version.version_number == 4

    # new revision_number series
    data["kwargs"]["revision_number"] = 2
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert isinstance(new_version, Version)
    assert new_version.revision_number == 2
    assert new_version.version_number == 1

    # second version
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert isinstance(new_version, Version)
    assert new_version.revision_number == 2
    assert new_version.version_number == 2

    # back to revision_number 1
    data["kwargs"]["revision_number"] = 1
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert isinstance(new_version, Version)
    assert new_version.revision_number == 1
    assert new_version.version_number == 5


def test_max_revision_number_returns_the_maximum_revision_number_in_the_db(
    setup_version_db_tests,
):
    """max_revision_number returns the maximum value of the revision_number in the db."""
    data = setup_version_db_tests
    data["kwargs"]["revision_number"] = 1
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert new_version.revision_number == 1
    assert new_version.version_number == 2
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert new_version.revision_number == 1
    assert new_version.version_number == 3
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert new_version.revision_number == 1
    assert new_version.version_number == 4

    # new revision_number series
    data["kwargs"]["revision_number"] = 2
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert new_version.revision_number == 2
    assert new_version.version_number == 1
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert new_version.revision_number == 2
    assert new_version.version_number == 2

    # back to revision_number 1
    data["kwargs"]["revision_number"] = 1
    new_version = Version(**data["kwargs"])
    DBSession.save(new_version)
    assert new_version.revision_number == 1

    assert new_version.max_revision_number == 2


def test_max_revision_number_returns_the_maximum_revision_number_in_the_db_when_no_version(
    setup_version_db_tests,
):
    """max_revision_number returns the maximum value of the revision_number in the db when no version is created."""
    data = setup_version_db_tests
    data["kwargs"]["revision_number"] = 1
    new_version = Version(**data["kwargs"])
    assert new_version.max_revision_number == 1


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
    assert new_version.version_number == 2

    new_version = Version(**data["kwargs"])
    DBSession.add(new_version)
    DBSession.commit()

    assert data["test_version"].task == new_version.task
    assert new_version.version_number == 3

    new_version = Version(**data["kwargs"])
    DBSession.add(new_version)
    DBSession.commit()

    assert data["test_version"].task == new_version.task
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


def test_files_argument_is_skipped(setup_version_db_tests):
    """files attribute an empty list if the files argument is skipped."""
    data = setup_version_db_tests
    data["kwargs"].pop("files")
    new_version = Version(**data["kwargs"])
    assert new_version.files == []


def test_files_argument_is_none(setup_version_db_tests):
    """files attribute an empty list if the files argument is None."""
    data = setup_version_db_tests
    data["kwargs"]["files"] = None
    new_version = Version(**data["kwargs"])
    assert new_version.files == []


def test_files_attribute_is_none(setup_version_db_tests):
    """TypeError raised if the files argument is set to None."""
    data = setup_version_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_version"].files = None
    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_files_argument_is_not_a_list_of_file_instances(setup_version_db_tests):
    """TypeError raised if the files attr is not a list of File instances."""
    data = setup_version_db_tests
    test_value = [132, "231123"]
    data["kwargs"]["files"] = test_value
    with pytest.raises(TypeError) as cm:
        Version(**data["kwargs"])

    assert (
        str(cm.value) == "Version.files should only contain instances of "
        "stalker.models.file.File, not int: '132'"
    )


def test_files_attribute_is_not_a_list_of_file_instances(setup_version_db_tests):
    """TypeError raised if the files attr is set to something other than a File."""
    data = setup_version_db_tests
    test_value = [132, "231123"]
    with pytest.raises(TypeError) as cm:
        data["test_version"].files = test_value

    assert (
        str(cm.value) == "Version.files should only contain instances of "
        "stalker.models.file.File, not int: '132'"
    )


def test_files_attribute_is_working_as_expected(setup_version_db_tests):
    """files attribute is working as expected."""
    data = setup_version_db_tests
    data["kwargs"].pop("files")
    new_version = Version(**data["kwargs"])
    assert data["test_file1"] not in new_version.files
    assert data["test_file2"] not in new_version.files

    new_version.files = [data["test_file1"], data["test_file2"]]
    assert data["test_file1"] in new_version.files
    assert data["test_file2"] in new_version.files


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
    DBSession.add(new_version)
    assert new_version in data["test_version"].children


def test_parent_attribute_updates_the_children_attribute(setup_version_db_tests):
    """parent attr updates the children attribute of the parent Version."""
    data = setup_version_db_tests
    data["kwargs"]["parent"] = None
    new_version = Version(**data["kwargs"])
    DBSession.add(new_version)
    assert new_version.parent != data["test_version"]
    new_version.parent = data["test_version"]
    assert new_version in data["test_version"].children


def test_parent_attribute_will_not_allow_circular_dependencies(setup_version_db_tests):
    """CircularDependency raised if parent attr is a child of the current Version."""
    data = setup_version_db_tests
    data["kwargs"]["parent"] = data["test_version"]
    version1 = Version(**data["kwargs"])
    DBSession.add(version1)
    with pytest.raises(CircularDependencyError) as cm:
        data["test_version"].parent = version1

    assert (
        str(cm.value) == "<tp_SH001_FX_Main_v001 (Version)> (Version) and "
        "<tp_SH001_FX_Main_v002 (Version)> (Version) are in a "
        'circular dependency in their "children" attribute'
    )


def test_parent_attribute_will_not_allow_deeper_circular_dependencies(
    setup_version_db_tests,
):
    """CircularDependency raised if the Version is a parent of the current parent."""
    data = setup_version_db_tests
    data["kwargs"]["parent"] = data["test_version"]
    version1 = Version(**data["kwargs"])
    DBSession.add(version1)

    data["kwargs"]["parent"] = version1
    version2 = Version(**data["kwargs"])
    DBSession.add(version2)

    # now create circular dependency
    with pytest.raises(CircularDependencyError) as cm:
        data["test_version"].parent = version2

    assert (
        str(cm.value) == "<tp_SH001_FX_Main_v001 (Version)> (Version) and "
        "<tp_SH001_FX_Main_v002 (Version)> (Version) are in a "
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
        "Version.children should only contain instances of "
        "Version (or derivative), not str: 'not a Version instance'"
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
        str(cm.value) == "<tp_SH001_FX_Main_v003 (Version)> (Version) and "
        "<tp_SH001_FX_Main_v002 (Version)> (Version) are in a "
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
        str(cm.value) == "<tp_SH001_FX_Main_v004 (Version)> (Version) and "
        "<tp_SH001_FX_Main_v002 (Version)> (Version) are in a "
        'circular dependency in their "children" attribute'
    )


def test_generate_path_extension_can_be_skipped(setup_version_db_tests):
    """generate_path() extension can be skipped."""
    data = setup_version_db_tests
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()
    # extension can be skipped
    _ = new_version1.generate_path()


def test_generate_path_extension_can_be_None(setup_version_db_tests):
    """generate_path() extension can be None."""
    data = setup_version_db_tests
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()
    # extension can be skipped
    path = new_version1.generate_path(extension=None)
    assert path.suffix == ""


def test_generate_path_extension_is_not_a_str(setup_version_db_tests):
    """generate_path() extension is not a str will raise a TypeError."""
    data = setup_version_db_tests
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()
    # extension is not str raises TypeError
    with pytest.raises(TypeError) as cm:
        _ = new_version1.generate_path(extension=1234)

    assert str(cm.value) == "extension should be a str, not int: '1234'"


def test_generate_path_extension_can_be_an_empty_str(setup_version_db_tests):
    """generate_path() extension can be an empty str."""
    data = setup_version_db_tests
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()
    # extension can be an empty string
    path = new_version1.generate_path(extension="")
    assert path.suffix == ""


def test_generate_path_will_render_the_appropriate_template_from_the_related_project(
    setup_version_db_tests,
):
    """generate_path() generates a Path by rendering the related Project FilenameTemplate."""
    data = setup_version_db_tests
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()
    path = new_version1.generate_path()
    assert isinstance(path, Path)
    assert str(path.parent) == "tp/SH001/FX/Main"

    path = path.with_suffix(".ma")
    assert str(path.name) == "SH001_FX_Main_r01_v002.ma"


def test_generate_path_will_use_the_given_extension(setup_version_db_tests):
    """generate_path method uses the given extension."""
    data = setup_version_db_tests
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()
    path = new_version1.generate_path(extension=".ma")
    assert isinstance(path, Path)
    assert str(path.parent) == "tp/SH001/FX/Main"
    assert str(path.name) == "SH001_FX_Main_r01_v002.ma"


def test_generate_path_will_raise_a_runtime_error_if_there_is_no_suitable_filename_template(
    setup_version_db_tests,
):
    """generate_path method raises a RuntimeError if there is no suitable
    FilenameTemplate instance found."""
    data = setup_version_db_tests
    data["test_structure"].templates.remove(data["test_filename_template"])
    DBSession.commit()

    DBSession.delete(data["test_filename_template"])
    DBSession.commit()
    data["kwargs"]["parent"] = None
    new_version1 = Version(**data["kwargs"])
    with pytest.raises(RuntimeError) as cm:
        new_version1.generate_path()

    assert (
        str(cm.value)
        == "There are no suitable FilenameTemplate (target_entity_type == "
        "'Variant') defined in the Structure of the related Project "
        "instance, please create a new "
        "stalker.models.template.FilenameTemplate instance with its "
        "'target_entity_type' attribute is set to 'Variant' and add it "
        "to the `templates` attribute of the structure of the project"
    )


def test_template_variables_project(setup_version_db_tests):
    """project in template variables is correct."""
    data = setup_version_db_tests
    kwargs = data["test_version"]._template_variables()
    assert kwargs["project"] == data["test_version"].task.project


def test_template_variables_sequence(setup_version_db_tests):
    """sequence in template variables is correct."""
    data = setup_version_db_tests
    kwargs = data["test_version"]._template_variables()
    assert kwargs["sequence"] == data["test_sequence"]


def test_template_variables_scene(setup_version_db_tests):
    """scene in template variables is correct."""
    data = setup_version_db_tests
    kwargs = data["test_version"]._template_variables()
    assert kwargs["scene"] == data["test_scene"]


def test_template_variables_shot(setup_version_db_tests):
    """shot in template variables is correct."""
    data = setup_version_db_tests
    kwargs = data["test_version"]._template_variables()
    assert kwargs["shot"] is None


def test_template_variables_asset(setup_version_db_tests):
    """asset in template variables is correct."""
    data = setup_version_db_tests
    kwargs = data["test_version"]._template_variables()
    assert kwargs["asset"] is None


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


def test_template_variables_for_a_shot_version_contains_scene(setup_version_db_tests):
    """template_variables for a Shot version contains scene."""
    data = setup_version_db_tests
    v = Version(task=data["test_shot1"])
    template_variables = v._template_variables()
    assert data["test_shot1"].scene is not None
    assert "scene" in template_variables
    assert template_variables["scene"] == data["test_shot1"].scene


def test_template_variables_for_a_shot_version_contains_sequence(
    setup_version_db_tests,
):
    """template_variables for a Shot version contains sequence."""
    data = setup_version_db_tests
    v = Version(task=data["test_shot1"])
    template_variables = v._template_variables()
    assert data["test_shot1"].sequence is not None
    assert "sequence" in template_variables
    assert template_variables["sequence"] == data["test_shot1"].sequence


def test_absolute_path_works_as_expected(setup_version_db_tests):
    """absolute_path attribute works as expected."""
    data = setup_version_db_tests
    # data["patcher"].patch("Linux")

    data["test_structure"].templates.remove(data["test_filename_template"])
    DBSession.delete(data["test_filename_template"])
    DBSession.commit()

    ft = FilenameTemplate(
        name="Task Filename Template",
        target_entity_type="Variant",
        path="$REPO{{project.repositories[0].code}}/{{project.code}}/"
        "{%- for parent_task in parent_tasks -%}"
        "{{parent_task.nice_name}}/"
        "{%- endfor -%}",
        filename="{{task.nice_name}}"
        '_r{{"%02d"|format(version.revision_number)}}'
        '_v{{"%03d"|format(version.version_number)}}',
    )
    data["test_project"].structure.templates.append(ft)
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()

    repo_path = data["test_repo"].path
    assert new_version1.absolute_path == Path(f"{repo_path}/tp/SH001/FX/Main")


def test_absolute_full_path_works_as_expected(setup_version_db_tests):
    """absolute_full_path attribute works as expected."""
    data = setup_version_db_tests
    # data["patcher"].patch("Linux")

    data["test_structure"].templates.remove(data["test_filename_template"])
    DBSession.delete(data["test_filename_template"])
    DBSession.commit()

    ft = FilenameTemplate(
        name="Task Filename Template",
        target_entity_type="Variant",
        path="$REPO{{project.repositories[0].code}}/{{project.code}}/"
        "{%- for parent_task in parent_tasks -%}"
        "{{parent_task.nice_name}}/"
        "{%- endfor -%}",
        filename="{{task.nice_name}}"
        '_r{{"%02d"|format(version.revision_number)}}'
        '_v{{"%03d"|format(version.version_number)}}',
    )
    data["test_project"].structure.templates.append(ft)
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()

    repo_path = data["test_repo"].path
    assert new_version1.absolute_full_path == Path(
        f"{repo_path}/tp/SH001/FX/Main/Main_r01_v002"
    )


def test_path_works_as_expected(setup_version_db_tests):
    """path attribute works as expected."""
    data = setup_version_db_tests
    data["patcher"].patch("Linux")

    data["test_structure"].templates.remove(data["test_filename_template"])
    DBSession.delete(data["test_filename_template"])
    DBSession.commit()

    ft = FilenameTemplate(
        name="Task Filename Template",
        target_entity_type="Variant",
        path="$REPO{{project.repositories[0].code}}/{{project.code}}/"
        "{%- for parent_task in parent_tasks -%}"
        "{{parent_task.nice_name}}/"
        "{%- endfor -%}",
        filename="{{task.nice_name}}"
        '_r{{"%02d"|format(version.revision_number)}}'
        '_v{{"%03d"|format(version.version_number)}}',
    )
    data["test_project"].structure.templates.append(ft)
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()

    assert new_version1.path == Path("$REPOTR/tp/SH001/FX/Main")


def test_full_path_works_as_expected(setup_version_db_tests):
    """full_path attribute works as expected."""
    data = setup_version_db_tests
    data["patcher"].patch("Linux")

    data["test_structure"].templates.remove(data["test_filename_template"])
    DBSession.delete(data["test_filename_template"])
    DBSession.commit()

    ft = FilenameTemplate(
        name="Task Filename Template",
        target_entity_type="Variant",
        path="$REPO{{project.repositories[0].code}}/{{project.code}}/"
        "{%- for parent_task in parent_tasks -%}"
        "{{parent_task.nice_name}}/"
        "{%- endfor -%}",
        filename="{{task.nice_name}}"
        '_r{{"%02d"|format(version.revision_number)}}'
        '_v{{"%03d"|format(version.version_number)}}',
    )
    data["test_project"].structure.templates.append(ft)
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()

    assert new_version1.full_path == Path("$REPOTR/tp/SH001/FX/Main/Main_r01_v002")


def test_filename_works_as_expected(setup_version_db_tests):
    """filename attribute works as expected."""
    data = setup_version_db_tests
    data["patcher"].patch("Linux")

    data["test_structure"].templates.remove(data["test_filename_template"])
    DBSession.delete(data["test_filename_template"])
    DBSession.commit()

    ft = FilenameTemplate(
        name="Task Filename Template",
        target_entity_type="Variant",
        path="$REPO{{project.repositories[0].code}}/{{project.code}}/"
        "{%- for parent_task in parent_tasks -%}"
        "{{parent_task.nice_name}}/"
        "{%- endfor -%}",
        filename="{{task.nice_name}}"
        '_r{{"%02d"|format(version.revision_number)}}'
        '_v{{"%03d"|format(version.version_number)}}',
    )
    data["test_project"].structure.templates.append(ft)
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()

    assert new_version1.filename == "Main_r01_v002"
    assert isinstance(new_version1.filename, str)


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
    DBSession.save(new_version1)

    new_version2 = Version(**data["kwargs"])
    DBSession.save(new_version2)

    new_version3 = Version(**data["kwargs"])
    DBSession.save(new_version3)

    new_version4 = Version(**data["kwargs"])
    DBSession.save(new_version4)

    new_version5 = Version(**data["kwargs"])
    DBSession.save(new_version5)

    # with new revision number
    data["kwargs"]["revision_number"] = 2
    new_version6 = Version(**data["kwargs"])
    DBSession.save(new_version6)
    new_version7 = Version(**data["kwargs"])
    DBSession.save(new_version7)
    new_version8 = Version(**data["kwargs"])
    DBSession.save(new_version8)

    new_version1.is_published = True
    new_version3.is_published = True
    new_version4.is_published = True

    new_version7.is_published = True

    assert new_version1.latest_published_version == new_version4
    assert new_version2.latest_published_version == new_version4
    assert new_version3.latest_published_version == new_version4
    assert new_version4.latest_published_version == new_version4
    assert new_version5.latest_published_version == new_version4

    assert new_version6.latest_published_version == new_version7
    assert new_version7.latest_published_version == new_version7
    assert new_version8.latest_published_version == new_version7


def test_is_latest_published_version_is_working_as_expected(setup_version_db_tests):
    """is_latest_published_version is working as expected."""
    data = setup_version_db_tests
    new_version1 = Version(**data["kwargs"])
    DBSession.save(new_version1)

    new_version2 = Version(**data["kwargs"])
    DBSession.save(new_version2)

    new_version3 = Version(**data["kwargs"])
    DBSession.save(new_version3)

    new_version4 = Version(**data["kwargs"])
    DBSession.save(new_version4)

    new_version5 = Version(**data["kwargs"])
    DBSession.save(new_version5)

    # with new revision number
    data["kwargs"]["revision_number"] = 2
    new_version6 = Version(**data["kwargs"])
    DBSession.save(new_version6)
    new_version7 = Version(**data["kwargs"])
    DBSession.save(new_version7)
    new_version8 = Version(**data["kwargs"])
    DBSession.save(new_version8)

    new_version1.is_published = True
    new_version3.is_published = True
    new_version4.is_published = True

    new_version7.is_published = True

    assert new_version1.is_latest_published_version() is False
    assert new_version2.is_latest_published_version() is False
    assert new_version3.is_latest_published_version() is False
    assert new_version4.is_latest_published_version() is True
    assert new_version5.is_latest_published_version() is False

    assert new_version6.is_latest_published_version() is False
    assert new_version7.is_latest_published_version() is True
    assert new_version8.is_latest_published_version() is False


def test_equality_operator(setup_version_db_tests):
    """equality of two Version instances."""
    data = setup_version_db_tests
    new_version1 = Version(**data["kwargs"])
    DBSession.save(new_version1)

    new_version2 = Version(**data["kwargs"])
    DBSession.save(new_version2)

    new_version3 = Version(**data["kwargs"])
    DBSession.save(new_version3)

    new_version4 = Version(**data["kwargs"])
    DBSession.save(new_version4)  #

    new_version5 = Version(**data["kwargs"])
    DBSession.save(new_version5)

    # with new revision number
    data["kwargs"]["revision_number"] = 2
    new_version6 = Version(**data["kwargs"])
    DBSession.save(new_version6)
    new_version7 = Version(**data["kwargs"])
    DBSession.save(new_version7)
    new_version8 = Version(**data["kwargs"])
    DBSession.save(new_version8)

    new_version1.is_published = True
    new_version3.is_published = True
    new_version4.is_published = True

    new_version7.is_published = True

    assert (new_version1 == new_version1) is True
    assert (new_version1 == new_version2) is False
    assert (new_version1 == new_version3) is False
    assert (new_version1 == new_version4) is False
    assert (new_version1 == new_version5) is False
    assert (new_version1 == new_version6) is False
    assert (new_version1 == new_version7) is False
    assert (new_version1 == new_version8) is False

    assert (new_version2 == new_version2) is True
    assert (new_version2 == new_version3) is False
    assert (new_version2 == new_version4) is False
    assert (new_version2 == new_version5) is False
    assert (new_version2 == new_version6) is False
    assert (new_version2 == new_version7) is False
    assert (new_version2 == new_version8) is False

    assert (new_version3 == new_version3) is True
    assert (new_version3 == new_version4) is False
    assert (new_version3 == new_version5) is False
    assert (new_version3 == new_version6) is False
    assert (new_version3 == new_version7) is False
    assert (new_version3 == new_version8) is False

    assert (new_version4 == new_version4) is True
    assert (new_version4 == new_version5) is False
    assert (new_version4 == new_version6) is False
    assert (new_version4 == new_version7) is False
    assert (new_version4 == new_version8) is False

    assert (new_version5 == new_version5) is True
    assert (new_version5 == new_version6) is False
    assert (new_version5 == new_version7) is False
    assert (new_version5 == new_version8) is False

    assert (new_version6 == new_version6) is True
    assert (new_version6 == new_version7) is False
    assert (new_version6 == new_version8) is False

    assert (new_version7 == new_version7) is True
    assert (new_version6 == new_version8) is False

    assert (new_version8 == new_version8) is True


def test_inequality_operator(setup_version_db_tests):
    """inequality of two Version instances."""
    data = setup_version_db_tests
    new_version1 = Version(**data["kwargs"])
    DBSession.save(new_version1)

    new_version2 = Version(**data["kwargs"])
    DBSession.save(new_version2)

    new_version3 = Version(**data["kwargs"])
    DBSession.save(new_version3)

    new_version4 = Version(**data["kwargs"])
    DBSession.save(new_version4)

    new_version5 = Version(**data["kwargs"])
    DBSession.save(new_version5)

    # with new revision number
    data["kwargs"]["revision_number"] = 2
    new_version6 = Version(**data["kwargs"])
    DBSession.save(new_version6)
    new_version7 = Version(**data["kwargs"])
    DBSession.save(new_version7)
    new_version8 = Version(**data["kwargs"])
    DBSession.save(new_version8)

    new_version1.is_published = True
    new_version3.is_published = True
    new_version4.is_published = True

    new_version7.is_published = True

    assert (new_version1 != new_version1) is False
    assert (new_version1 != new_version2) is True
    assert (new_version1 != new_version3) is True
    assert (new_version1 != new_version4) is True
    assert (new_version1 != new_version5) is True
    assert (new_version1 != new_version6) is True
    assert (new_version1 != new_version7) is True
    assert (new_version1 != new_version8) is True

    assert (new_version2 != new_version2) is False
    assert (new_version2 != new_version3) is True
    assert (new_version2 != new_version4) is True
    assert (new_version2 != new_version5) is True
    assert (new_version2 != new_version6) is True
    assert (new_version2 != new_version7) is True
    assert (new_version2 != new_version8) is True

    assert (new_version3 != new_version3) is False
    assert (new_version3 != new_version4) is True
    assert (new_version3 != new_version5) is True
    assert (new_version3 != new_version6) is True
    assert (new_version3 != new_version7) is True
    assert (new_version3 != new_version8) is True

    assert (new_version4 != new_version4) is False
    assert (new_version4 != new_version5) is True
    assert (new_version4 != new_version6) is True
    assert (new_version4 != new_version7) is True
    assert (new_version4 != new_version8) is True

    assert (new_version5 != new_version5) is False
    assert (new_version5 != new_version6) is True
    assert (new_version5 != new_version7) is True
    assert (new_version5 != new_version8) is True

    assert (new_version6 != new_version6) is False
    assert (new_version6 != new_version7) is True
    assert (new_version6 != new_version8) is True

    assert (new_version7 != new_version7) is False
    assert (new_version6 != new_version8) is True

    assert (new_version8 != new_version8) is False


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
    """latest_version attribute is a read only attribute."""
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
    """latest_version attribute is working as expected."""
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


def test_latest_version_attribute_is_working_as_expected_for_different_revision_numbers(
    setup_version_db_tests,
):
    """latest_version attribute is working as expected for different revision_numbers."""
    data = setup_version_db_tests
    data["kwargs"]["revision_number"] = 1
    new_version1 = Version(**data["kwargs"])
    DBSession.add(new_version1)
    DBSession.commit()

    new_version2 = Version(**data["kwargs"])
    DBSession.add(new_version2)
    DBSession.commit()

    data["kwargs"]["revision_number"] = 2
    new_version3 = Version(**data["kwargs"])
    DBSession.add(new_version3)
    DBSession.commit()

    new_version4 = Version(**data["kwargs"])
    DBSession.add(new_version4)
    DBSession.commit()

    data["kwargs"]["revision_number"] = 3
    new_version5 = Version(**data["kwargs"])
    DBSession.add(new_version5)
    DBSession.commit()

    assert new_version5.version_number == 1

    assert new_version1.latest_version == new_version2
    assert new_version2.latest_version == new_version2
    assert new_version3.latest_version == new_version4
    assert new_version4.latest_version == new_version4
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
        data["test_variant1"],
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
        data["test_variant1"],
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

    assert version1.nice_name == "{}_{}_{}".format(
        task1.nice_name,
        task2.nice_name,
        task3.nice_name,
    )

    # for an asset version
    character_type = Type(target_entity_type="Asset", name="Character", code="Char")
    asset1 = Asset(name="Asset1", code="Asset1", parent=task1, type=character_type)
    DBSession.add(asset1)
    DBSession.commit()

    version2 = Version(task=asset1)
    assert version2.nice_name == "{}".format(asset1.nice_name)

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

    assert version3.nice_name == "{}_{}".format(
        shot2.nice_name,
        task4.nice_name,
    )

    # for an asset of a shot
    asset2 = Asset(name="Asset2", code="Asset2", parent=shot2, type=character_type)
    DBSession.add(asset2)
    DBSession.commit()

    version4 = Version(task=asset2)
    assert version4.nice_name == "{}".format(asset2.nice_name)


def test_string_representation_is_a_little_bit_meaningful(setup_version_db_tests):
    """__str__ or __repr__ result is meaningful."""
    data = setup_version_db_tests
    assert "<tp_SH001_FX_Main_v001 (Version)>" == f'{data["test_version"]}'


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


def test_reviews_attribute_is_a_list_of_reviews(setup_version_db_tests):
    """Version.reviews attribute is filled with Review instances."""
    data = setup_version_db_tests
    data["test_variant1"].status = data["status_wip"]
    data["test_variant1"].responsible = [data["test_user1"], data["test_user2"]]
    version = Version(task=data["test_variant1"])

    # request a review
    reviews = data["test_variant1"].request_review(version=version)
    assert reviews[0].version == version
    assert reviews[1].version == version
    assert isinstance(version.reviews, list)
    assert len(version.reviews) == 2
    assert version.reviews == reviews


@pytest.fixture(scope="function")
def setup_version_tests():
    """Set up non-DB related tests of Version class."""
    data = dict()
    data["patcher"] = PlatformPatcher()

    # users
    # test users
    data["test_user1"] = User(
        name="Test User 1",
        login="tuser1",
        email="tuser1@test.com",
        password="secret",
    )
    data["test_user2"] = User(
        name="Test User 2",
        login="tuser2",
        email="tuser2@test.com",
        password="secret",
    )

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
        sequence=data["test_sequence"],
        status_list=data["test_shot_status_list"],
    )

    # create a group of Tasks for the shot
    data["test_task1"] = Task(
        name="Task1",
        parent=data["test_shot1"],
        status_list=data["test_task_status_list"],
    )

    data["test_task2"] = Task(
        name="Task2",
        parent=data["test_shot1"],
        status_list=data["test_task_status_list"],
    )

    # a File for the input file
    data["test_input_file1"] = File(
        name="Input File 1",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_beauty_v001.###.exr",
    )

    data["test_input_file2"] = File(
        name="Input File 2",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_occ_v001.###.exr",
    )

    # a File for the output file
    data["test_output_file1"] = File(
        name="Output File 1",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_beauty_v001.###.exr",
    )

    data["test_output_file2"] = File(
        name="Output File 2",
        full_path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/"
        "Outputs/SH001_occ_v001.###.exr",
    )

    # now create a version for the Task
    data["kwargs"] = {
        "task": data["test_task1"],
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
        str(cm.value) == "<tp_SH001_Task1_v003 (Version)> (Version) and "
        "<tp_SH001_Task1_v002 (Version)> (Version) are in a "
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
        str(cm.value) == "<tp_SH001_Task1_v004 (Version)> (Version) and "
        "<tp_SH001_Task1_v002 (Version)> (Version) are in a "
        'circular dependency in their "children" attribute'
    )


def test_version_number_without_a_db(setup_version_tests):
    """version_number without a db is not None."""
    data = setup_version_tests
    v = Version(task=data["test_task2"])
    assert v.version_number is not None


def test_version_number_without_a_db(setup_version_tests):
    """version_number without a db is not None."""
    data = setup_version_tests
    v1 = Version(task=data["test_task2"])
    assert v1.version_number == 1
    v2 = Version(task=data["test_task2"])
    assert v2.version_number == 2
    v3 = Version(task=data["test_task2"])
    assert v3.version_number == 3


def test_latest_version_without_a_db(setup_version_tests):
    """latest_version without a db returns self."""
    data = setup_version_tests
    v = Version(task=data["test_task2"])
    assert v.latest_version is v


def test_max_version_number_without_a_db(setup_version_tests):
    """max_version_number without a db returns self.version_number."""
    data = setup_version_tests
    v = Version(task=data["test_task2"])
    assert v.max_version_number == v.version_number


def test__hash__is_working_as_expected(setup_version_tests):
    """__hash__ is working as expected."""
    data = setup_version_tests
    v = Version(task=data["test_task2"])
    result = hash(v)
    assert isinstance(result, int)
    assert result == v.__hash__()


def test_request_review_method_calls_task_request_review_method(
    setup_version_tests, monkeypatch
):
    """request_review() calls Task.request_review() method."""
    data = setup_version_tests
    called = []

    def patched_request_review(self, version=None):
        """Patch the request review method."""
        called.append(version)

    data["test_task2"].responsible = [
        data["test_user1"],
        data["test_user2"],
    ]

    monkeypatch.setattr(
        "stalker.models.version.Task.request_review", patched_request_review
    )
    v = Version(task=data["test_task2"])

    assert len(called) == 0
    _ = v.request_review()
    assert len(called) == 1
    assert called[0] == v


def test_request_review_method_returns_reviews(setup_version_db_tests):
    """request_review() returns Reviews."""
    data = setup_version_db_tests
    task = data["test_variant1"]
    task.responsible = [
        data["test_user1"],
        data["test_user2"],
    ]
    task.status = data["status_wip"]
    v = Version(task=task)
    reviews = v.request_review()
    assert len(reviews) == 2
    from stalker.models.review import Review

    assert isinstance(reviews[0], Review)
    assert isinstance(reviews[1], Review)


def test_variant_name_attr_does_not_exist(setup_version_tests):
    """Version.variant_name does not exist anymore."""
    data = setup_version_tests
    assert hasattr(data["test_version"], "variant_name") is False
