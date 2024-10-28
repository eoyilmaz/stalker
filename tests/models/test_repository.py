# -*- coding: utf-8 -*-
"""Tests related to the Repository class."""

import os
import platform

import pytest

from stalker import CodeMixin, Repository, Tag, defaults
from stalker.db.session import DBSession

from tests.utils import PlatformPatcher


@pytest.fixture(scope="function")
def setup_repository_db_tests(setup_postgresql_db):
    """Set up the tests for the Repository class with a DB."""
    data = dict()
    data["patcher"] = PlatformPatcher()

    # create a couple of test tags
    data["test_tag1"] = Tag(name="test tag 1")
    data["test_tag2"] = Tag(name="test tag 2")

    data["kwargs"] = {
        "name": "a repository",
        "code": "R1",
        "description": "this is for testing purposes",
        "tags": [data["test_tag1"], data["test_tag2"]],
        "linux_path": "/mnt/M/Projects",
        "osx_path": "/Volumes/M/Projects",
        "windows_path": "M:/Projects",
    }

    repo = Repository(**data["kwargs"])
    data["test_repo"] = repo
    DBSession.add(data["test_repo"])
    DBSession.commit()
    yield data
    data["patcher"].restore()


def test_code_mixin_as_super(setup_repository_db_tests):
    """CodeMixin is one of the supers of the Repository class."""
    data = setup_repository_db_tests
    repo = Repository(**data["kwargs"])
    assert isinstance(repo, CodeMixin)


def test___auto_name__class_attribute_is_set_to_false():
    """__auto_name__ class attribute is set to False for Repository class."""
    assert Repository.__auto_name__ is False


@pytest.mark.parametrize("test_value", [123123, 123.1231, [], {}])
def test_linux_path_argument_accepts_only_strings(
    test_value, setup_repository_db_tests
):
    """linux_path argument accepts only string values."""
    data = setup_repository_db_tests
    data["kwargs"]["linux_path"] = test_value
    with pytest.raises(TypeError):
        Repository(**data["kwargs"])


@pytest.mark.parametrize("test_value", [123123, 123.1231, [], {}])
def test_linux_path_attribute_accepts_only_strings(
    test_value, setup_repository_db_tests
):
    """linux_path attribute accepts only string values."""
    data = setup_repository_db_tests
    with pytest.raises(TypeError):
        data["test_repo"].linux_path = test_value


def test_linux_path_attribute_is_working_properly(setup_repository_db_tests):
    """linux_path attribute is working properly."""
    data = setup_repository_db_tests
    test_value = "~/newRepoPath/Projects/"
    data["test_repo"].linux_path = test_value
    assert data["test_repo"].linux_path == test_value


def test_linux_path_attribute_finishes_with_a_slash(setup_repository_db_tests):
    """linux_path attr is finished with a slash even it is not supplied by default."""
    data = setup_repository_db_tests
    test_value = "/mnt/T"
    expected_value = "/mnt/T/"
    data["test_repo"].linux_path = test_value
    assert data["test_repo"].linux_path == expected_value


@pytest.mark.parametrize("test_value", [123123, 123.1231, [], {}])
def test_windows_path_argument_accepts_only_strings(
    test_value, setup_repository_db_tests
):
    """windows_path argument accepts only string values."""
    data = setup_repository_db_tests
    data["kwargs"]["windows_path"] = test_value
    with pytest.raises(TypeError):
        Repository(**data["kwargs"])


def test_windows_path_attribute_accepts_only_strings(setup_repository_db_tests):
    """windows_path attribute accepts only string values."""
    data = setup_repository_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_repo"].windows_path = 123123

    assert (
        str(cm.value)
        == "Repository.windows_path should be an instance of string not int"
    )


def test_windows_path_attribute_is_working_properly(setup_repository_db_tests):
    """windows_path attribute is working properly."""
    data = setup_repository_db_tests
    test_value = "~/newRepoPath/Projects/"
    data["test_repo"].windows_path = test_value
    assert data["test_repo"].windows_path == test_value


def test_windows_path_attribute_finishes_with_a_slash(setup_repository_db_tests):
    """windows_path attr is finished with a slash even it is not supplied by default."""
    data = setup_repository_db_tests
    test_value = "T:"
    expected_value = "T:/"
    data["test_repo"].windows_path = test_value
    assert data["test_repo"].windows_path == expected_value


def test_osx_path_argument_accepts_only_strings(setup_repository_db_tests):
    """osx_path argument accepts only string values."""
    data = setup_repository_db_tests
    data["kwargs"]["osx_path"] = 123123
    with pytest.raises(TypeError) as cm:
        Repository(**data["kwargs"])

    assert (
        str(cm.value) == "Repository.osx_path should be an instance of string not int"
    )


def test_osx_path_attribute_accepts_only_strings(setup_repository_db_tests):
    """osx_path attribute accepts only string values."""
    data = setup_repository_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_repo"].osx_path = 123123

    assert (
        str(cm.value) == "Repository.osx_path should be an instance of string not int"
    )


def test_osx_path_attribute_is_working_properly(setup_repository_db_tests):
    """osx_path attribute is working properly."""
    data = setup_repository_db_tests
    test_value = "~/newRepoPath/Projects/"
    data["test_repo"].osx_path = test_value
    assert data["test_repo"].osx_path == test_value


def test_osx_path_attribute_finishes_with_a_slash(setup_repository_db_tests):
    """osx_path attr is finished with a slash even it is not supplied by default."""
    data = setup_repository_db_tests
    test_value = "/Volumes/T"
    expected_value = "/Volumes/T/"
    data["test_repo"].osx_path = test_value
    assert data["test_repo"].osx_path == expected_value


def test_path_returns_properly_for_windows(setup_repository_db_tests):
    """path returns the correct value for the os."""
    data = setup_repository_db_tests
    data["patcher"].patch("Windows")
    assert data["test_repo"].path == data["test_repo"].windows_path


def test_path_returns_properly_for_linux(setup_repository_db_tests):
    """path returns the correct value for the os."""
    data = setup_repository_db_tests
    data["patcher"].patch("Linux")
    assert data["test_repo"].path == data["test_repo"].linux_path


def test_path_returns_properly_for_osx(setup_repository_db_tests):
    """path returns the correct value for the os."""
    data = setup_repository_db_tests
    data["patcher"].patch("Darwin")
    assert data["test_repo"].path == data["test_repo"].osx_path


def test_path_attribute_sets_correct_path_for_windows(setup_repository_db_tests):
    """path property sets the correct attribute in windows."""
    data = setup_repository_db_tests
    data["patcher"].patch("Windows")
    test_value = "S:/Projects/"
    assert data["test_repo"].path != test_value
    assert data["test_repo"].windows_path != test_value
    data["test_repo"].path = test_value
    assert data["test_repo"].windows_path == test_value
    assert data["test_repo"].path == test_value


def test_path_attribute_sets_correct_path_for_linux(setup_repository_db_tests):
    """path property sets the correct attribute in linux."""
    data = setup_repository_db_tests
    data["patcher"].patch("Linux")
    test_value = "/mnt/S/Projects/"
    assert data["test_repo"].path != test_value
    assert data["test_repo"].linux_path != test_value
    data["test_repo"].path = test_value
    assert data["test_repo"].linux_path == test_value
    assert data["test_repo"].path == test_value


def test_path_attribute_sets_correct_path_for_osx(setup_repository_db_tests):
    """path property sets the correct attribute in osx."""
    data = setup_repository_db_tests
    data["patcher"].patch("Darwin")
    test_value = "/Volumes/S/Projects/"
    assert data["test_repo"].path != test_value
    assert data["test_repo"].osx_path != test_value
    data["test_repo"].path = test_value
    assert data["test_repo"].osx_path == test_value
    assert data["test_repo"].path == test_value


def test_equality(setup_repository_db_tests):
    """equality of two repositories."""
    data = setup_repository_db_tests
    repo1 = Repository(**data["kwargs"])
    repo2 = Repository(**data["kwargs"])

    data["kwargs"].update(
        {
            "name": "a repository",
            "description": "this is the commercial repository",
            "linux_path": "/mnt/commercialServer/Projects",
            "osx_path": "/Volumes/commercialServer/Projects",
            "windows_path": "Z:\\Projects",
        }
    )

    repo3 = Repository(**data["kwargs"])

    assert repo1 == repo2
    assert not repo1 == repo3


def test_inequality(setup_repository_db_tests):
    """inequality of two repositories."""
    data = setup_repository_db_tests
    repo1 = Repository(**data["kwargs"])
    repo2 = Repository(**data["kwargs"])

    data["kwargs"].update(
        {
            "name": "a repository",
            "description": "this is the commercial repository",
            "linux_path": "/mnt/commercialServer/Projects",
            "osx_path": "/Volumes/commercialServer/Projects",
            "windows_path": "Z:\\Projects",
        }
    )

    repo3 = Repository(**data["kwargs"])

    assert not repo1 != repo2
    assert repo1 != repo3


def test_plural_class_name(setup_repository_db_tests):
    """plural name of Repository class."""
    data = setup_repository_db_tests
    assert data["test_repo"].plural_class_name == "Repositories"


def test_linux_path_argument_backward_slashes_are_converted_to_forward_slashes(
    setup_repository_db_tests,
):
    """backward slashes are converted to forward slashes in the linux_path argument."""
    data = setup_repository_db_tests
    data["kwargs"]["linux_path"] = r"\mnt\M\Projects"
    new_repo = Repository(**data["kwargs"])
    assert "\\" not in new_repo.linux_path
    assert new_repo.linux_path == "/mnt/M/Projects/"


def test_linux_path_attribute_backward_slashes_are_converted_to_forward_slashes(
    setup_repository_db_tests,
):
    """backward slashes are converted to forward slashes in the linux_path attribute."""
    data = setup_repository_db_tests
    data["test_repo"].linux_path = r"\mnt\M\Projects"
    assert "\\" not in data["test_repo"].linux_path
    assert data["test_repo"].linux_path == "/mnt/M/Projects/"


def test_osx_path_argument_backward_slashes_are_converted_to_forward_slashes(
    setup_repository_db_tests,
):
    """backward slashes are converted to forward slashes in the osx_path argument."""
    data = setup_repository_db_tests
    data["kwargs"]["osx_path"] = r"\Volumes\M\Projects"
    new_repo = Repository(**data["kwargs"])
    assert "\\" not in new_repo.linux_path
    assert new_repo.osx_path == "/Volumes/M/Projects/"


def test_osx_path_attribute_backward_slashes_are_converted_to_forward_slashes(
    setup_repository_db_tests,
):
    """backward slashes are converted to forward slashes in the osx_path attribute."""
    data = setup_repository_db_tests
    data["test_repo"].osx_path = r"\Volumes\M\Projects"
    assert "\\" not in data["test_repo"].osx_path
    assert data["test_repo"].osx_path == "/Volumes/M/Projects/"


def test_windows_path_argument_backward_slashes_are_converted_to_forward_slashes(
    setup_repository_db_tests,
):
    """backward slashes are converted to forward slashes in the windows_path arg."""
    data = setup_repository_db_tests
    data["kwargs"]["windows_path"] = r"M:\Projects"
    new_repo = Repository(**data["kwargs"])
    assert "\\" not in new_repo.linux_path
    assert new_repo.windows_path == "M:/Projects/"


def test_windows_path_attribute_backward_slashes_are_converted_to_forward_slashes(
    setup_repository_db_tests,
):
    """backward slashes are converted to forward slashes in the windows_path attr."""
    data = setup_repository_db_tests
    data["test_repo"].windows_path = r"M:\Projects"
    assert "\\" not in data["test_repo"].windows_path
    assert data["test_repo"].windows_path == "M:/Projects/"


def test_windows_path_with_more_than_one_slashes_converted_to_single_slash_1(
    setup_repository_db_tests,
):
    """windows_path is set with more than one slashes is converted to single slash."""
    data = setup_repository_db_tests
    data["test_repo"].windows_path = r"M://"
    assert data["test_repo"].windows_path == "M:/"


def test_windows_path_with_more_than_one_slashes_converted_to_single_slash_2(
    setup_repository_db_tests,
):
    """windows_path is set with more than one slashes is converted to single slash."""
    data = setup_repository_db_tests
    data["test_repo"].windows_path = r"M://////////"
    assert data["test_repo"].windows_path == "M:/"


def test_to_linux_path_returns_the_linux_version_of_the_given_windows_path(
    setup_repository_db_tests,
):
    """to_linux_path returns the linux version of the given windows path."""
    data = setup_repository_db_tests
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    test_windows_path = "T:/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    assert data["test_repo"].to_linux_path(test_windows_path) == test_linux_path


def test_to_linux_path_returns_the_linux_version_of_the_given_linux_path(
    setup_repository_db_tests,
):
    """to_linux_path returns the linux version of the given linux path."""
    data = setup_repository_db_tests
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    test_linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    assert data["test_repo"].to_linux_path(test_linux_path) == test_linux_path


def test_to_linux_path_returns_the_linux_version_of_the_given_osx_path(
    setup_repository_db_tests,
):
    """to_linux_path returns the linux version of the given osx path."""
    data = setup_repository_db_tests
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_osx_path = "/Volumes/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    assert data["test_repo"].to_linux_path(test_osx_path) == test_linux_path


def test_to_linux_path_returns_the_linux_version_of_the_given_reverse_windows_path(
    setup_repository_db_tests,
):
    """to_linux_path returns the linux version of the given reverse windows path."""
    data = setup_repository_db_tests
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    test_linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_windows_path_reverse = (
        "T:\\Stalker_Projects\\Sero\\Task1\\" "Task2\\Some_file.ma"
    )
    assert data["test_repo"].to_linux_path(test_windows_path_reverse) == test_linux_path


def test_to_linux_path_returns_the_linux_version_of_the_given_reverse_linux_path(
    setup_repository_db_tests,
):
    """to_linux_path returns the linux version of the given reverse linux path."""
    data = setup_repository_db_tests
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    test_linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_linux_path_reverse = (
        "\\mnt\\T\\Stalker_Projects\\Sero\\Task1\\" "Task2\\Some_file.ma"
    )
    assert data["test_repo"].to_linux_path(test_linux_path_reverse) == test_linux_path


def test_to_linux_path_returns_the_linux_version_of_the_given_reverse_osx_path(
    setup_repository_db_tests,
):
    """to_linux_path returns the linux version of the given reverse osx path."""
    data = setup_repository_db_tests
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_osx_path_reverse = (
        "\\Volumes\\T\\Stalker_Projects\\Sero\\" "Task1\\Task2\\Some_file.ma"
    )
    assert data["test_repo"].to_linux_path(test_osx_path_reverse) == test_linux_path


def test_to_linux_path_returns_the_linux_version_of_the_given_path_with_env_vars(
    setup_repository_db_tests,
):
    """to_linux_path returns the linux version of the given path contains env vars."""
    data = setup_repository_db_tests
    data["test_repo"].id = 1
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    os.environ["REPO1"] = "/mnt/T/Stalker_Projects"
    test_linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_path_with_env_var = "$REPO1/Sero/Task1/Task2/Some_file.ma"
    assert data["test_repo"].to_linux_path(test_path_with_env_var) == test_linux_path


def test_to_linux_path_raises_type_error_if_path_is_none(setup_repository_db_tests):
    """to_linux_path raises TypeError if path is None."""
    data = setup_repository_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_repo"].to_linux_path(None)
    assert str(cm.value) == "Repository.path can not be None"


def test_to_linux_path_raises_type_error_if_path_is_not_a_string(
    setup_repository_db_tests,
):
    """to_linux_path raises TypeError if path is None."""
    data = setup_repository_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_repo"].to_linux_path(123)
    assert str(cm.value) == "Repository.path should be a string, not int"


def test_to_windows_path_returns_the_windows_version_of_the_given_windows_path(
    setup_repository_db_tests,
):
    """to_windows_path returns the windows version of the given windows path."""
    data = setup_repository_db_tests
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    test_windows_path = "T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma"
    assert data["test_repo"].to_windows_path(test_windows_path) == test_windows_path


def test_to_windows_path_returns_the_windows_version_of_the_given_linux_path(
    setup_repository_db_tests,
):
    """to_windows_path returns the windows version of the given linux path."""
    data = setup_repository_db_tests
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    test_linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_windows_path = "T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma"
    assert data["test_repo"].to_windows_path(test_linux_path) == test_windows_path


def test_to_windows_path_returns_the_windows_version_of_the_given_osx_path(
    setup_repository_db_tests,
):
    """to_windows_path returns the windows version of the given osx path."""
    data = setup_repository_db_tests
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_osx_path = "/Volumes/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_windows_path = "T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma"
    assert data["test_repo"].to_windows_path(test_osx_path) == test_windows_path


def test_to_windows_path_returns_the_windows_version_of_the_given_reverse_windows_path(
    setup_repository_db_tests,
):
    """to_windows_path returns the windows version of the given reverse windows path."""
    data = setup_repository_db_tests
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    test_windows_path = "T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma"
    test_windows_path_reverse = (
        "T:\\Stalker_Projects\\Sero\\Task1\\" "Task2\\Some_file.ma"
    )
    assert (
        data["test_repo"].to_windows_path(test_windows_path_reverse)
        == test_windows_path
    )


def test_to_windows_path_returns_the_windows_version_of_the_given_reverse_linux_path(
    setup_repository_db_tests,
):
    """to_windows_path returns the windows version of the given reverse linux path."""
    data = setup_repository_db_tests
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    test_windows_path = "T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma"
    test_linux_path_reverse = (
        "\\mnt\\T\\Stalker_Projects\\Sero\\Task1\\" "Task2\\Some_file.ma"
    )
    assert (
        data["test_repo"].to_windows_path(test_linux_path_reverse) == test_windows_path
    )


def test_to_windows_path_returns_the_windows_version_of_the_given_reverse_osx_path(
    setup_repository_db_tests,
):
    """to_windows_path returns the windows version of the given reverse osx path."""
    data = setup_repository_db_tests
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_windows_path = "T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma"
    test_osx_path_reverse = (
        "\\Volumes\\T\\Stalker_Projects\\Sero\\" "Task1\\Task2\\Some_file.ma"
    )
    assert data["test_repo"].to_windows_path(test_osx_path_reverse) == test_windows_path


def test_to_windows_path_returns_the_windows_version_of_the_given_path_with_env_vars(
    setup_repository_db_tests,
):
    """to_windows_path returns the windows version of the given path which env vars."""
    data = setup_repository_db_tests
    data["test_repo"].id = 1
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    os.environ["REPO1"] = data["test_repo"].linux_path
    test_windows_path = "T:/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_path_with_env_var = "$REPO1/Sero/Task1/Task2/Some_file.ma"
    assert (
        data["test_repo"].to_windows_path(test_path_with_env_var) == test_windows_path
    )


def test_to_windows_path_raises_type_error_if_path_is_none(setup_repository_db_tests):
    """to_windows_path raises TypeError if path is None."""
    data = setup_repository_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_repo"].to_windows_path(None)
    assert str(cm.value) == "Repository.path can not be None"


def test_to_windows_path_raises_type_error_if_path_is_not_a_string(
    setup_repository_db_tests,
):
    """to_windows_path raises TypeError if path is None."""
    data = setup_repository_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_repo"].to_windows_path(123)
    assert str(cm.value) == "Repository.path should be a string, not int"


def test_to_osx_path_returns_the_osx_version_of_the_given_windows_path(
    setup_repository_db_tests,
):
    """to_osx_path returns the osx version of the given windows path."""
    data = setup_repository_db_tests
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_windows_path = "T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma"
    test_osx_path = "/Volumes/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    assert data["test_repo"].to_osx_path(test_windows_path) == test_osx_path


def test_to_osx_path_returns_the_osx_version_of_the_given_linux_path(
    setup_repository_db_tests,
):
    """to_osx_path returns the osx version of the given linux path."""
    data = setup_repository_db_tests
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_osx_path = "/Volumes/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    assert data["test_repo"].to_osx_path(test_linux_path) == test_osx_path


def test_to_osx_path_returns_the_osx_version_of_the_given_osx_path(
    setup_repository_db_tests,
):
    """to_osx_path returns the osx version of the given osx path."""
    data = setup_repository_db_tests
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_osx_path = "/Volumes/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    assert data["test_repo"].to_osx_path(test_osx_path) == test_osx_path


def test_to_osx_path_returns_the_osx_version_of_the_given_reverse_windows_path(
    setup_repository_db_tests,
):
    """to_osx_path returns the osx version of the given reverse windows path."""
    data = setup_repository_db_tests
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_osx_path = "/Volumes/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_windows_path_reverse = (
        "T:\\Stalker_Projects\\Sero\\Task1\\" "Task2\\Some_file.ma"
    )
    assert data["test_repo"].to_osx_path(test_windows_path_reverse) == test_osx_path


def test_to_osx_path_returns_the_osx_version_of_the_given_reverse_linux_path(
    setup_repository_db_tests,
):
    """to_osx_path returns the osx version of the given reverse linux path."""
    data = setup_repository_db_tests
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_osx_path = "/Volumes/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_linux_path_reverse = (
        "\\mnt\\T\\Stalker_Projects\\Sero\\Task1\\" "Task2\\Some_file.ma"
    )
    assert data["test_repo"].to_osx_path(test_linux_path_reverse) == test_osx_path


def test_to_osx_path_returns_the_osx_version_of_the_given_reverse_osx_path(
    setup_repository_db_tests,
):
    """to_osx_path returns the osx version of the given reverse osx path."""
    data = setup_repository_db_tests
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_osx_path = "/Volumes/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_osx_path_reverse = (
        "\\Volumes\\T\\Stalker_Projects\\Sero\\" "Task1\\Task2\\Some_file.ma"
    )
    assert data["test_repo"].to_osx_path(test_osx_path_reverse) == test_osx_path


def test_to_osx_path_returns_the_osx_version_of_the_given_path(
    setup_repository_db_tests,
):
    """to_osx_path returns the osx version of the given path."""
    data = setup_repository_db_tests
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"

    test_windows_path = "T:/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_osx_path = "/Volumes/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"

    test_windows_path_reverse = (
        "T:\\Stalker_Projects\\Sero\\Task1\\" "Task2\\Some_file.ma"
    )
    test_linux_path_reverse = (
        "\\mnt\\T\\Stalker_Projects\\Sero\\Task1\\" "Task2\\Some_file.ma"
    )
    test_osx_path_reverse = (
        "\\Volumes\\T\\Stalker_Projects\\Sero\\" "Task1\\Task2\\Some_file.ma"
    )

    assert data["test_repo"].to_osx_path(test_windows_path) == test_osx_path
    assert data["test_repo"].to_osx_path(test_linux_path) == test_osx_path
    assert data["test_repo"].to_osx_path(test_osx_path) == test_osx_path
    assert data["test_repo"].to_osx_path(test_windows_path_reverse) == test_osx_path
    assert data["test_repo"].to_osx_path(test_linux_path_reverse) == test_osx_path
    assert data["test_repo"].to_osx_path(test_osx_path_reverse) == test_osx_path


def test_to_osx_path_returns_the_osx_version_of_the_given_path_with_env_vars(
    setup_repository_db_tests,
):
    """to_osx_path returns the osx version of the given path which contains env vars."""
    data = setup_repository_db_tests
    data["test_repo"].id = 1
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    os.environ["REPO1"] = data["test_repo"].windows_path
    test_windows_path = "/Volumes/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_path_with_env_var = "$REPO1/Sero/Task1/Task2/Some_file.ma"
    assert data["test_repo"].to_osx_path(test_path_with_env_var) == test_windows_path


def test_to_osx_path_raises_type_error_if_path_is_none(setup_repository_db_tests):
    """to_osx_path raises TypeError if path is None."""
    data = setup_repository_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_repo"].to_osx_path(None)
    assert str(cm.value) == "Repository.path can not be None"


def test_to_osx_path_raises_type_error_if_path_is_not_a_string(
    setup_repository_db_tests,
):
    """to_osx_path raises TypeError if path is None."""
    data = setup_repository_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_repo"].to_osx_path(123)
    assert str(cm.value) == "Repository.path should be a string, not int"


def test_to_native_path_returns_the_native_version_of_the_given_linux_path(
    setup_repository_db_tests,
):
    """to_native_path returns the native version of the given linux path."""
    data = setup_repository_db_tests
    data["patcher"].patch("Linux")
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    assert data["test_repo"].to_native_path(test_linux_path) == test_linux_path


def test_to_native_path_returns_the_native_version_of_the_given_windows_path(
    setup_repository_db_tests,
):
    """to_native_path returns the native version of the given windows path."""
    data = setup_repository_db_tests
    data["patcher"].patch("Linux")
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_windows_path = "T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma"
    assert (
        data["test_repo"].to_native_path(test_windows_path)
        == "/mnt/T/Stalker_Projects/Sero/Task1/Task2/Some_file.ma"
    )


def test_to_native_path_returns_the_native_version_of_the_given_osx_path(
    setup_repository_db_tests,
):
    """to_native_path returns the native version of the given osx path."""
    data = setup_repository_db_tests
    data["patcher"].patch("Linux")
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_osx_path = "/Volumes/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    assert data["test_repo"].to_native_path(test_osx_path) == test_linux_path


def test_to_native_path_returns_the_native_version_of_the_given_reverse_windows_path(
    setup_repository_db_tests,
):
    """to_native_path returns the native version of the given reverse windows path."""
    data = setup_repository_db_tests
    data["patcher"].patch("Linux")
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    test_windows_path_reverse = (
        "T:\\Stalker_Projects\\Sero\\Task1\\" "Task2\\Some_file.ma"
    )
    test_linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    assert (
        data["test_repo"].to_native_path(test_windows_path_reverse) == test_linux_path
    )


def test_to_native_path_returns_the_native_version_of_the_given_reverse_linux_path(
    setup_repository_db_tests,
):
    """to_native_path returns the native version of the given reverse linux path."""
    data = setup_repository_db_tests
    data["patcher"].patch("Linux")
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    test_linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_linux_path_reverse = (
        "\\mnt\\T\\Stalker_Projects\\Sero\\Task1\\" "Task2\\Some_file.ma"
    )
    assert data["test_repo"].to_native_path(test_linux_path_reverse) == test_linux_path


def test_to_native_path_returns_the_native_version_of_the_given_reverse_osx_path(
    setup_repository_db_tests,
):
    """to_native_path returns the native version of the
    given reverse osx path
    """
    data = setup_repository_db_tests
    data["patcher"].patch("Linux")
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    test_osx_path_reverse = (
        "\\Volumes\\T\\Stalker_Projects\\Sero\\" "Task1\\Task2\\Some_file.ma"
    )
    assert data["test_repo"].to_native_path(test_osx_path_reverse) == test_linux_path


def test_to_native_path_raises_type_error_if_path_is_none(setup_repository_db_tests):
    """to_native_path raises TypeError if path is None."""
    data = setup_repository_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_repo"].to_native_path(None)
    assert str(cm.value) == "Repository.path can not be None"


def test_to_native_path_raises_type_error_if_path_is_not_a_string(
    setup_repository_db_tests,
):
    """to_native_path raises TypeError if path is None."""
    data = setup_repository_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_repo"].to_native_path(123)
    assert str(cm.value) == "Repository.path should be a string, not int"


def test_is_in_repo_returns_true_if_the_given_linux_path_is_in_this_repo(
    setup_repository_db_tests,
):
    """is_in_repo returns True if linux path is in this repo or False otherwise."""
    data = setup_repository_db_tests
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    test_linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    assert data["test_repo"].is_in_repo(test_linux_path)


def test_is_in_repo_returns_true_if_the_given_linux_reverse_path_is_in_this_repo(
    setup_repository_db_tests,
):
    """is_in_repo returns True if linux path with reverse slashes is in this repo."""
    data = setup_repository_db_tests
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    test_linux_path_reverse = (
        "\\mnt\\T\\Stalker_Projects\\Sero\\Task1\\" "Task2\\Some_file.ma"
    )
    assert data["test_repo"].is_in_repo(test_linux_path_reverse)


def test_is_in_repo_returns_false_if_the_given_linux_path_is_not_in_this_repo(
    setup_repository_db_tests,
):
    """is_in_repo returns False if linux path is not in this repo or False otherwise."""
    data = setup_repository_db_tests
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    test_not_in_path_linux_path = (
        "/mnt/T/Other_Projects/Sero/Task1/" "Task2/Some_file.ma"
    )
    assert data["test_repo"].is_in_repo(test_not_in_path_linux_path) is False


def test_is_in_repo_returns_true_if_the_given_windows_path_is_in_this_repo(
    setup_repository_db_tests,
):
    """is_in_repo returns True if windows path is in this repo or False otherwise."""
    data = setup_repository_db_tests
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    test_windows_path = "T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma"
    assert data["test_repo"].is_in_repo(test_windows_path)


def test_is_in_repo_returns_true_if_the_given_windows_reverse_path_is_in_this_repo(
    setup_repository_db_tests,
):
    """is_in_repo returns True if windows path is in this repo or False otherwise."""
    data = setup_repository_db_tests
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    test_windows_path_reverse = (
        "T:\\Stalker_Projects\\Sero\\Task1\\" "Task2\\Some_file.ma"
    )
    assert data["test_repo"].is_in_repo(test_windows_path_reverse)


def test_is_in_repo_is_case_insensitive_under_windows(setup_repository_db_tests):
    """is_in_repo is case-insensitive under windows."""
    data = setup_repository_db_tests
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    test_windows_path_reverse = (
        "t:\\stalKer_ProjectS\\sErO\\task1\\" "Task2\\Some_file.ma"
    )
    assert data["test_repo"].is_in_repo(test_windows_path_reverse)


def test_is_in_repo_returns_false_if_the_given_windows_path_is_not_in_this_repo(
    setup_repository_db_tests,
):
    """is_in_repo returns False if windows path is not in this repo."""
    data = setup_repository_db_tests
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    test_not_in_path_windows_path = "T:/Other_Projects/Sero/Task1/Task2/" "Some_file.ma"
    assert data["test_repo"].is_in_repo(test_not_in_path_windows_path) is False


def test_is_in_repo_returns_true_if_the_given_osx_path_is_in_this_repo(
    setup_repository_db_tests,
):
    """is_in_repo returns True if the given osx path is in this repo."""
    data = setup_repository_db_tests
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_osx_path = "/Volumes/T/Stalker_Projects/Sero/Task1/Task2/" "Some_file.ma"
    assert data["test_repo"].is_in_repo(test_osx_path)


def test_is_in_repo_returns_true_if_the_given_osx_reverse_path_is_in_this_repo(
    setup_repository_db_tests,
):
    """is_in_repo returns True if the osx reverse path is in this repo."""
    data = setup_repository_db_tests
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_osx_path_reverse = (
        "\\Volumes\\T\\Stalker_Projects\\Sero\\" "Task1\\Task2\\Some_file.ma"
    )
    assert data["test_repo"].is_in_repo(test_osx_path_reverse)


def test_is_in_repo_returns_false_if_the_given_osx_path_is_not_in_this_repo(
    setup_repository_db_tests,
):
    """is_in_repo returns False if osx path is not in this repo."""
    data = setup_repository_db_tests
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    test_not_in_path_osx_path = (
        "/Volumes/T/Other_Projects/Sero/Task1/" "Task2/Some_file.ma"
    )
    assert not data["test_repo"].is_in_repo(test_not_in_path_osx_path)


def test_make_relative_method_converts_the_given_linux_path_to_relative_to_repo_root(
    setup_repository_db_tests,
):
    """make_relative() will convert the Linux path to repository root relative path."""
    data = setup_repository_db_tests
    # a Linux Path
    linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/Some_file.ma"
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    result = data["test_repo"].make_relative(linux_path)
    assert result == "Sero/Task1/Task2/Some_file.ma"


def test_make_relative_method_converts_the_given_osx_path_to_relative_to_repo_root(
    setup_repository_db_tests,
):
    """make_relative() will convert OSX path to repository root relative path."""
    data = setup_repository_db_tests
    # an OSX Path
    osx_path = "/Volumes/T/Stalker_Projects/Sero/Task1/Task2/Some_file.ma"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    result = data["test_repo"].make_relative(osx_path)
    assert result == "Sero/Task1/Task2/Some_file.ma"


def test_make_relative_method_converts_the_given_windows_path_to_relative_to_repo_root(
    setup_repository_db_tests,
):
    """make_relative() will convert Windows path to repository root relative path."""
    data = setup_repository_db_tests
    # a Windows Path
    windows_path = "T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma"
    data["test_repo"].osx_path = "T:/Stalker_Projects"
    result = data["test_repo"].make_relative(windows_path)
    assert result == "Sero/Task1/Task2/Some_file.ma"


def test_make_relative_method_converts_the_given_path_with_env_variable_to_native_path(
    setup_repository_db_tests,
):
    """make_relative() converts path with env vars to repository root relative path."""
    data = setup_repository_db_tests
    # so we should have the env var to be configured
    # now create a path with env var
    path = "$REPO{}/Sero/Task1/Task2/Some_file.ma".format(data["test_repo"].code)
    result = data["test_repo"].make_relative(path)
    assert result == "Sero/Task1/Task2/Some_file.ma"


def test_make_relative_method_converts_the_given_path_with_old_env_variable_to_native_path(
    setup_repository_db_tests,
):
    """make_relative() converts path with old env var to repo root relative path."""
    data = setup_repository_db_tests
    # so we should have the env var to be configured
    # now create a path with env var
    path = "$REPO{}/Sero/Task1/Task2/Some_file.ma".format(data["test_repo"].id)
    result = data["test_repo"].make_relative(path)
    assert result == "Sero/Task1/Task2/Some_file.ma"


def test_to_os_independent_path_is_working_properly(setup_repository_db_tests):
    """to_os_independent_path class method is working properly."""
    data = setup_repository_db_tests
    DBSession.add(data["test_repo"])
    DBSession.commit()
    relative_part = "some/path/to/a/file.ma"
    test_path = "%s/%s" % (data["test_repo"].path, relative_part)
    assert Repository.to_os_independent_path(test_path) == "$REPO%s/%s" % (
        data["test_repo"].code,
        relative_part,
    )


def test_to_os_independent_path_for_old_environment_vars(setup_repository_db_tests):
    """to_os_independent_path with paths that contain old env vars."""
    data = setup_repository_db_tests
    DBSession.add(data["test_repo"])
    DBSession.commit()
    relative_part = "some/path/to/a/file.ma"
    test_path = "$REPO{}/{}".format(data["test_repo"].id, relative_part)
    assert Repository.to_os_independent_path(test_path) == "$REPO{}/{}".format(
        data["test_repo"].code,
        relative_part,
    )


def test_to_os_independent_path_method_converts_the_given_linux_path_to_universal(
    setup_repository_db_tests,
):
    """to_os_independent_path() converts Linux path to an OS independent path."""
    data = setup_repository_db_tests
    # a Linux Path
    linux_path = "/mnt/T/Stalker_Projects/Sero/Task1/Task2/Some_file.ma"
    data["test_repo"].linux_path = "/mnt/T/Stalker_Projects"
    data["test_repo"].windows_path = "T:/Stalker_Projects"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    result = data["test_repo"].to_os_independent_path(linux_path)
    assert result == "$REPO%s/Sero/Task1/Task2/Some_file.ma" % data["test_repo"].code


def test_to_os_independent_path_method_converts_the_given_osx_path_to_universal(
    setup_repository_db_tests,
):
    """to_os_independent_path() converts OSX path to an os independent path."""
    data = setup_repository_db_tests
    # an OSX Path
    osx_path = "/Volumes/T/Stalker_Projects/Sero/Task1/Task2/Some_file.ma"
    data["test_repo"].osx_path = "/Volumes/T/Stalker_Projects"
    result = data["test_repo"].to_os_independent_path(osx_path)
    assert result == "$REPO%s/Sero/Task1/Task2/Some_file.ma" % data["test_repo"].code


def test_to_os_independent_path_method_converts_the_given_windows_path_to_universal(
    setup_repository_db_tests,
):
    """to_os_independent_path() converts Windows path to an os independent path."""
    data = setup_repository_db_tests
    # a Windows Path
    windows_path = "T:/Stalker_Projects/Sero/Task1/Task2/Some_file.ma"
    data["test_repo"].osx_path = "T:/Stalker_Projects"
    result = data["test_repo"].to_os_independent_path(windows_path)
    assert result == "$REPO{}/Sero/Task1/Task2/Some_file.ma".format(
        data["test_repo"].code
    )


def test_to_os_independent_path_method_not_change_the_path_with_env_variable(
    setup_repository_db_tests,
):
    """to_os_independent_path() do not change the given path with env var."""
    data = setup_repository_db_tests
    # so we should have the env var to be configured
    # now create a path with env var
    path = "$REPO{}/Sero/Task1/Task2/Some_file.ma".format(data["test_repo"].code)
    result = data["test_repo"].to_os_independent_path(path)
    assert result == "$REPO{}/Sero/Task1/Task2/Some_file.ma".format(
        data["test_repo"].code
    )


def test_to_os_independent_path_method_converts_the_given_path_with_old_env_variable_new_env_variable(
    setup_repository_db_tests,
):
    """to_os_independent_path converts path with old env var to new env var."""
    data = setup_repository_db_tests
    # so we should have the env var to be configured
    # now create a path with env var
    path = "$REPO{}/Sero/Task1/Task2/Some_file.ma".format(data["test_repo"].id)
    result = data["test_repo"].to_os_independent_path(path)
    assert result == "$REPO{}/Sero/Task1/Task2/Some_file.ma".format(
        data["test_repo"].code
    )


def test_find_repo_is_working_properly(setup_repository_db_tests):
    """find_repo class method is working properly."""
    data = setup_repository_db_tests
    DBSession.add(data["test_repo"])
    DBSession.commit()

    # add some other repositories
    new_repo1 = Repository(
        name="New Repository",
        code="NR",
        linux_path="/mnt/T/Projects",
        osx_path="/Volumes/T/Projects",
        windows_path="T:/Projects",
    )
    DBSession.add(new_repo1)
    DBSession.commit()

    test_path = "%s/some/path/to/a/file.ma" % data["test_repo"].path
    assert Repository.find_repo(test_path) == data["test_repo"]

    test_path = "%s/some/path/to/a/file.ma" % new_repo1.windows_path
    assert Repository.find_repo(test_path) == new_repo1


def test_find_repo_is_case_insensitive_under_windows(setup_repository_db_tests):
    """find_repo class method is case-insensitive under windows."""
    data = setup_repository_db_tests
    if platform.platform() != "Windows":
        pytest.skip("Test under Windows only!")

    DBSession.add(data["test_repo"])
    DBSession.commit()

    # add some other repositories
    new_repo1 = Repository(
        name="New Repository",
        code="NR",
        linux_path="/mnt/T/Projects",
        osx_path="/Volumes/T/Projects",
        windows_path="T:/Projects",
    )
    DBSession.add(new_repo1)
    DBSession.commit()

    test_path = "%s/some/path/to/a/file.ma" % data["test_repo"].path.lower()
    assert Repository.find_repo(test_path) == data["test_repo"]

    test_path = "%s/some/path/to/a/file.ma" % new_repo1.windows_path.lower()
    assert Repository.find_repo(test_path) == new_repo1


def test_find_repo_is_working_properly_with_reverse_slashes(setup_repository_db_tests):
    """find_repo class will work properly with paths that contains reverse slashes."""
    data = setup_repository_db_tests
    DBSession.add(data["test_repo"])
    DBSession.commit()

    # add some other repositories
    new_repo1 = Repository(
        name="New Repository",
        code="NR",
        linux_path="/mnt/T/Projects",
        osx_path="/Volumes/T/Projects",
        windows_path="T:/Projects",
    )
    DBSession.add(new_repo1)
    DBSession.commit()

    test_path = "%s\\some\\path\\to\\a\\file.ma" % data["test_repo"].path
    test_path.replace("/", "\\")
    assert Repository.find_repo(test_path) == data["test_repo"]

    test_path = "%s\\some\\path\\to\\a\\file.ma" % new_repo1.windows_path.lower()
    test_path.replace("/", "\\")
    assert Repository.find_repo(test_path) == new_repo1


def test_find_repo_is_working_properly_with_env_vars(setup_repository_db_tests):
    """find_repo class method is working properly with paths containing env vars."""
    data = setup_repository_db_tests
    DBSession.add(data["test_repo"])
    DBSession.commit()

    # add some other repositories
    new_repo1 = Repository(
        name="New Repository",
        code="NR",
        linux_path="/mnt/T/Projects",
        osx_path="/Volumes/T/Projects",
        windows_path="T:/Projects",
    )
    DBSession.add(new_repo1)
    DBSession.commit()

    # Test with env var
    test_path = "$REPO{}/some/path/to/a/file.ma".format(data["test_repo"].code)
    assert Repository.find_repo(test_path) == data["test_repo"]

    test_path = f"$REPO{new_repo1.code}/some/path/to/a/file.ma"
    assert Repository.find_repo(test_path) == new_repo1

    # Test with old env var
    test_path = "$REPO{}/some/path/to/a/file.ma".format(data["test_repo"].id)
    assert Repository.find_repo(test_path) == data["test_repo"]

    test_path = "$REPO{}/some/path/to/a/file.ma".format(new_repo1.id)
    assert Repository.find_repo(test_path) == new_repo1


def test_env_var_property_is_working_properly(setup_repository_db_tests):
    """env_var property is working properly."""
    data = setup_repository_db_tests
    assert data["test_repo"].env_var == "REPOR1"


def test_creating_and_committing_a_new_repository_instance_will_create_env_var(
    setup_repository_db_tests,
):
    """environment variable is created if a new repository is created."""
    repo = Repository(
        name="Test Repo",
        code="TR",
        linux_path="/mnt/T",
        osx_path="/Volumes/T",
        windows_path="T:/",
    )
    DBSession.add(repo)
    DBSession.commit()

    assert defaults.repo_env_var_template.format(code=repo.code) in os.environ

    # check the old ID based env var
    assert os.environ[defaults.repo_env_var_template_old.format(id=repo.id)] == repo.path


def test_updating_a_repository_will_update_repo_path(setup_repository_db_tests):
    """environment variable is updated if the repository path is updated."""
    repo = Repository(
        name="Test Repo",
        code="TR",
        linux_path="/mnt/T",
        osx_path="/Volumes/T",
        windows_path="T:/",
    )
    DBSession.add(repo)
    DBSession.commit()

    assert defaults.repo_env_var_template.format(code=repo.code) in os.environ
    assert defaults.repo_env_var_template_old.format(id=repo.id) in os.environ

    # now update the repository
    test_value = "/mnt/S/"
    repo.path = test_value

    # expect the environment variable is also updated
    assert (
        os.environ[defaults.repo_env_var_template.format(code=repo.code)] == test_value
    )
    assert (
        os.environ[defaults.repo_env_var_template_old.format(id=repo.id)] == test_value
    )


def test_updating_windows_path_only_update_repo_path_if_on_windows(
    setup_repository_db_tests,
):
    """updating the windows path will only update the path if the system is windows."""
    data = setup_repository_db_tests
    data["patcher"].patch("Linux")
    repo = Repository(
        name="Test Repo",
        code="TR",
        linux_path="/mnt/T",
        osx_path="/Volumes/T",
        windows_path="T:/",
    )
    DBSession.add(repo)
    DBSession.commit()

    assert defaults.repo_env_var_template.format(code=repo.code) in os.environ
    assert defaults.repo_env_var_template_old.format(id=repo.id) in os.environ

    # now update the repository
    test_value = "S:/"
    repo.windows_path = test_value

    # expect the environment variable not updated
    assert (
        os.environ[defaults.repo_env_var_template.format(code=repo.code)] != test_value
    )
    assert (
        os.environ[defaults.repo_env_var_template.format(code=repo.code)]
        == repo.linux_path
    )

    assert (
        os.environ[defaults.repo_env_var_template_old.format(id=repo.id)] != test_value
    )
    assert (
        os.environ[defaults.repo_env_var_template_old.format(id=repo.id)]
        == repo.linux_path
    )

    # make it windows
    data["patcher"].patch("Windows")

    # now update the repository
    test_value = "S:/"
    repo.windows_path = test_value

    # expect the environment variable not updated
    assert (
        os.environ[defaults.repo_env_var_template.format(code=repo.code)] == test_value
    )
    assert (
        os.environ[defaults.repo_env_var_template.format(code=repo.code)]
        == repo.windows_path
    )
    assert (
        os.environ[defaults.repo_env_var_template_old.format(id=repo.id)] == test_value
    )
    assert (
        os.environ[defaults.repo_env_var_template_old.format(id=repo.id)]
        == repo.windows_path
    )


def test_updating_osx_path_only_update_repo_path_if_on_osx(setup_repository_db_tests):
    """updating the osx path will only update the path if the system is osx."""
    data = setup_repository_db_tests
    data["patcher"].patch("Windows")

    repo = Repository(
        name="Test Repo",
        code="TR",
        linux_path="/mnt/T",
        osx_path="/Volumes/T",
        windows_path="T:/",
    )
    DBSession.add(repo)
    DBSession.commit()

    assert defaults.repo_env_var_template.format(code=repo.code) in os.environ
    assert defaults.repo_env_var_template_old.format(id=repo.id) in os.environ

    # now update the repository
    test_value = "/Volumes/S/"
    repo.osx_path = test_value

    # expect the environment variable not updated
    assert (
        os.environ[defaults.repo_env_var_template.format(code=repo.code)] != test_value
    )
    assert (
        os.environ[defaults.repo_env_var_template.format(code=repo.code)]
        == repo.windows_path
    )

    assert (
        os.environ[defaults.repo_env_var_template_old.format(id=repo.id)] != test_value
    )
    assert (
        os.environ[defaults.repo_env_var_template_old.format(id=repo.id)]
        == repo.windows_path
    )

    # make it osx
    data["patcher"].patch("Darwin")

    # now update the repository
    test_value = "/Volumes/S/"
    repo.osx_path = test_value

    # expect the environment variable not updated
    assert (
        os.environ[defaults.repo_env_var_template.format(code=repo.code)] == test_value
    )
    assert (
        os.environ[defaults.repo_env_var_template.format(code=repo.code)]
        == repo.osx_path
    )

    assert (
        os.environ[defaults.repo_env_var_template_old.format(id=repo.id)] == test_value
    )
    assert (
        os.environ[defaults.repo_env_var_template_old.format(id=repo.id)]
        == repo.osx_path
    )


def test_updating_linux_path_only_update_repo_path_if_on_linux(
    setup_repository_db_tests,
):
    """updating the linux path will only update the path if the system is linux."""
    data = setup_repository_db_tests
    data["patcher"].patch("Darwin")

    repo = Repository(
        name="Test Repo",
        code="TR",
        linux_path="/mnt/T",
        osx_path="/Volumes/T",
        windows_path="T:/",
    )
    DBSession.add(repo)
    DBSession.commit()

    assert defaults.repo_env_var_template.format(code=repo.code) in os.environ
    assert defaults.repo_env_var_template_old.format(id=repo.id) in os.environ

    # now update the repository
    test_value = "/mnt/S/"
    repo.linux_path = test_value

    # expect the environment variable not updated
    assert (
        os.environ[defaults.repo_env_var_template.format(code=repo.code)] != test_value
    )
    assert (
        os.environ[defaults.repo_env_var_template.format(code=repo.code)]
        == repo.osx_path
    )

    assert (
        os.environ[defaults.repo_env_var_template_old.format(id=repo.id)] != test_value
    )
    assert (
        os.environ[defaults.repo_env_var_template_old.format(id=repo.id)]
        == repo.osx_path
    )

    # make it linux
    data["patcher"].patch("Linux")

    # now update the repository
    test_value = "/mnt/S/"
    repo.linux_path = test_value

    # expect the environment variable not updated
    assert (
        os.environ[defaults.repo_env_var_template.format(code=repo.code)] == test_value
    )
    assert (
        os.environ[defaults.repo_env_var_template.format(code=repo.code)]
        == repo.linux_path
    )

    # expect the environment variable not updated
    assert (
        os.environ[defaults.repo_env_var_template_old.format(id=repo.id)] == test_value
    )
    assert (
        os.environ[defaults.repo_env_var_template_old.format(id=repo.id)]
        == repo.linux_path
    )
