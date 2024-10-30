# -*- coding: utf-8 -*-
"""Tests for the Project class."""

import datetime
import logging
import sys

from jinja2 import Template

import pytest

import pytz

from stalker import (
    log,
    Asset,
    Entity,
    Client,
    ImageFormat,
    Link,
    Project,
    Repository,
    Sequence,
    Shot,
    StatusList,
    Structure,
    Task,
    Ticket,
    TimeLog,
    Type,
    User,
)
from stalker.db.session import DBSession
from stalker.models.ticket import FIXED, CANTFIX, INVALID

logger = logging.getLogger("stalker.models.project")
log.register_logger(logger)


@pytest.fixture(scope="function")
def setup_project_db_test(setup_postgresql_db):
    """Set up the Project class tests."""
    data = dict()

    # create test objects
    data["start"] = datetime.datetime(2016, 11, 17, tzinfo=pytz.utc)
    data["end"] = data["start"] + datetime.timedelta(days=20)

    data["test_lead"] = User(
        name="lead", login="lead", email="lead@lead.com", password="lead"
    )

    data["test_user1"] = User(
        name="User1", login="user1", email="user1@users.com", password="123456"
    )

    data["test_user2"] = User(
        name="User2", login="user2", email="user2@users.com", password="123456"
    )

    data["test_user3"] = User(
        name="User3", login="user3", email="user3@users.com", password="123456"
    )

    data["test_user4"] = User(
        name="User4", login="user4", email="user4@users.com", password="123456"
    )

    data["test_user5"] = User(
        name="User5", login="user5", email="user5@users.com", password="123456"
    )

    data["test_user6"] = User(
        name="User6", login="user6", email="user6@users.com", password="123456"
    )

    data["test_user7"] = User(
        name="User7", login="user7", email="user7@users.com", password="123456"
    )

    data["test_user8"] = User(
        name="User8", login="user8", email="user8@users.com", password="123456"
    )

    data["test_user9"] = User(
        name="user9", login="user9", email="user9@users.com", password="123456"
    )

    data["test_user10"] = User(
        name="User10", login="user10", email="user10@users.com", password="123456"
    )

    data["test_user_client"] = User(
        name="User Client",
        login="userClient",
        email="user@client.com",
        password="123456",
    )
    DBSession.save(
        [
            data["test_lead"],
            data["test_user1"],
            data["test_user2"],
            data["test_user3"],
            data["test_user4"],
            data["test_user5"],
            data["test_user6"],
            data["test_user7"],
            data["test_user8"],
            data["test_user9"],
            data["test_user10"],
            data["test_user_client"],
        ]
    )

    data["test_image_format"] = ImageFormat(
        name="HD",
        width=1920,
        height=1080,
    )

    # type for project
    data["test_project_type"] = Type(
        name="Project Type 1", code="projt1", target_entity_type="Project"
    )

    data["test_project_type2"] = Type(
        name="Project Type 2", code="projt2", target_entity_type="Project"
    )

    # type for structure
    data["test_structure_type1"] = Type(
        name="Structure Type 1", code="struct1", target_entity_type="Structure"
    )

    data["test_structure_type2"] = Type(
        name="Structure Type 2", code="struct2", target_entity_type="Structure"
    )

    data["test_project_structure"] = Structure(
        name="Project Structure 1",
        type=data["test_structure_type1"],
    )

    data["test_project_structure2"] = Structure(
        name="Project Structure 2",
        type=data["test_structure_type2"],
    )

    data["test_repo1"] = Repository(
        name="Commercials Repository 1",
        code="CR1",
    )

    data["test_repo2"] = Repository(name="Commercials Repository 2", code="CR2")

    data["test_client"] = Client(name="Test Company", users=[data["test_user_client"]])
    DBSession.save(
        [
            data["test_image_format"],
            data["test_project_type"],
            data["test_project_type2"],
            data["test_structure_type1"],
            data["test_structure_type2"],
            data["test_project_structure"],
            data["test_project_structure2"],
            data["test_repo1"],
            data["test_repo2"],
            data["test_client"],
        ]
    )

    # create a project object
    data["kwargs"] = {
        "name": "Test Project",
        "code": "tp",
        "description": "This is a project object for testing purposes",
        "image_format": data["test_image_format"],
        "fps": 25,
        "type": data["test_project_type"],
        "structure": data["test_project_structure"],
        "repositories": [data["test_repo1"], data["test_repo2"]],
        "is_stereoscopic": False,
        "display_width": 15,
        "start": data["start"],
        "end": data["end"],
        "clients": [data["test_client"]],
    }

    data["test_project"] = Project(**data["kwargs"])
    DBSession.add(data["test_project"])
    DBSession.commit()

    # sequences without tasks
    data["test_seq1"] = Sequence(
        name="Seq1",
        code="Seq1",
        project=data["test_project"],
        resources=[data["test_user1"]],
        responsible=[data["test_user1"]],
    )

    data["test_seq2"] = Sequence(
        name="Seq2",
        code="Seq2",
        project=data["test_project"],
        resources=[data["test_user2"]],
        responsible=[data["test_user2"]],
    )

    data["test_seq3"] = Sequence(
        name="Seq3",
        code="Seq3",
        project=data["test_project"],
        resources=[data["test_user3"]],
        responsible=[data["test_user1"]],
    )

    # sequences with tasks
    data["test_seq4"] = Sequence(
        name="Seq4",
        code="Seq4",
        project=data["test_project"],
        responsible=[data["test_user1"]],
    )

    data["test_seq5"] = Sequence(
        name="Seq5",
        code="Seq5",
        project=data["test_project"],
        responsible=[data["test_user1"]],
    )

    # sequences without tasks but with shots
    data["test_seq6"] = Sequence(
        name="Seq6",
        code="Seq6",
        project=data["test_project"],
        responsible=[data["test_user1"]],
    )

    data["test_seq7"] = Sequence(
        name="Seq7",
        code="Seq7",
        project=data["test_project"],
        responsible=[data["test_user1"]],
    )

    # shots
    data["test_shot1"] = Shot(
        code="SH001",
        project=data["test_project"],
        sequences=[data["test_seq6"]],
        responsible=[data["test_lead"]],
    )

    data["test_shot2"] = Shot(
        code="SH002",
        project=data["test_project"],
        sequences=[data["test_seq6"]],
        responsible=[data["test_lead"]],
    )

    data["test_shot3"] = Shot(
        code="SH003",
        project=data["test_project"],
        sequences=[data["test_seq7"]],
        responsible=[data["test_lead"]],
    )

    data["test_shot4"] = Shot(
        code="SH004",
        project=data["test_project"],
        sequences=[data["test_seq7"]],
        responsible=[data["test_lead"]],
    )

    # asset types
    data["asset_type"] = Type(
        name="Character",
        code="char",
        target_entity_type="Asset",
    )

    # assets without tasks
    data["test_asset1"] = Asset(
        name="Test Asset 1",
        code="ta1",
        type=data["asset_type"],
        project=data["test_project"],
        resources=[data["test_user2"]],
        responsible=[data["test_lead"]],
    )

    data["test_asset2"] = Asset(
        name="Test Asset 2",
        code="ta2",
        type=data["asset_type"],
        project=data["test_project"],
        responsible=[data["test_lead"]],
    )

    data["test_asset3"] = Asset(
        name="Test Asset 3",
        code="ta3",
        type=data["asset_type"],
        project=data["test_project"],
        responsible=[data["test_lead"]],
    )

    # assets with tasks
    data["test_asset4"] = Asset(
        name="Test Asset 4",
        code="ta4",
        type=data["asset_type"],
        project=data["test_project"],
        responsible=[data["test_lead"]],
    )

    data["test_asset5"] = Asset(
        name="Test Asset 5",
        code="ta5",
        type=data["asset_type"],
        project=data["test_project"],
    )

    # for project
    data["test_task1"] = Task(
        name="Test Task 1",
        project=data["test_project"],
        resources=[data["test_user1"]],
    )

    data["test_task2"] = Task(
        name="Test Task 2",
        project=data["test_project"],
        resources=[data["test_user2"]],
    )

    data["test_task3"] = Task(
        name="Test Task 3",
        project=data["test_project"],
        resources=[data["test_user3"]],
    )

    # for sequence4
    data["test_task4"] = Task(
        name="Test Task 4",
        parent=data["test_seq4"],
        resources=[data["test_user4"]],
    )

    data["test_task5"] = Task(
        name="Test Task 5",
        parent=data["test_seq4"],
        resources=[data["test_user5"]],
    )

    data["test_task6"] = Task(
        name="Test Task 6",
        parent=data["test_seq4"],
        resources=[data["test_user6"]],
    )

    # for sequence5
    data["test_task7"] = Task(
        name="Test Task 7",
        parent=data["test_seq5"],
        resources=[data["test_user7"]],
    )

    data["test_task8"] = Task(
        name="Test Task 8",
        parent=data["test_seq5"],
        resources=[data["test_user8"]],
    )

    data["test_task9"] = Task(
        name="Test Task 9",
        parent=data["test_seq5"],
        resources=[data["test_user9"]],
    )

    # for shot1 of sequence6
    data["test_task10"] = Task(
        name="Test Task 10",
        parent=data["test_shot1"],
        resources=[data["test_user10"]],
        schedule_timing=10,
    )

    data["test_task11"] = Task(
        name="Test Task 11",
        parent=data["test_shot1"],
        resources=[data["test_user1"], data["test_user2"]],
    )

    data["test_task12"] = Task(
        name="Test Task 12",
        parent=data["test_shot1"],
        resources=[data["test_user3"], data["test_user4"]],
    )

    # for shot2 of sequence6
    data["test_task13"] = Task(
        name="Test Task 13",
        parent=data["test_shot2"],
        resources=[data["test_user5"], data["test_user6"]],
    )

    data["test_task14"] = Task(
        name="Test Task 14",
        parent=data["test_shot2"],
        resources=[data["test_user7"], data["test_user8"]],
    )

    data["test_task15"] = Task(
        name="Test Task 15",
        parent=data["test_shot2"],
        resources=[data["test_user9"], data["test_user10"]],
    )

    # for shot3 of sequence7
    data["test_task16"] = Task(
        name="Test Task 16",
        parent=data["test_shot3"],
        resources=[data["test_user1"], data["test_user2"], data["test_user3"]],
    )

    data["test_task17"] = Task(
        name="Test Task 17",
        parent=data["test_shot3"],
        resources=[data["test_user4"], data["test_user5"], data["test_user6"]],
    )

    data["test_task18"] = Task(
        name="Test Task 18",
        parent=data["test_shot3"],
        resources=[data["test_user7"], data["test_user8"], data["test_user9"]],
    )

    # for shot4 of sequence7
    data["test_task19"] = Task(
        name="Test Task 19",
        parent=data["test_shot4"],
        resources=[data["test_user10"], data["test_user1"], data["test_user2"]],
    )

    data["test_task20"] = Task(
        name="Test Task 20",
        parent=data["test_shot4"],
        resources=[data["test_user3"], data["test_user4"], data["test_user5"]],
    )

    data["test_task21"] = Task(
        name="Test Task 21",
        parent=data["test_shot4"],
        resources=[data["test_user6"], data["test_user7"], data["test_user8"]],
    )

    # for asset4
    data["test_task22"] = Task(
        name="Test Task 22",
        parent=data["test_asset4"],
        resources=[data["test_user9"], data["test_user10"], data["test_user1"]],
    )

    data["test_task23"] = Task(
        name="Test Task 23",
        parent=data["test_asset4"],
        resources=[data["test_user2"], data["test_user3"]],
    )

    data["test_task24"] = Task(
        name="Test Task 24",
        parent=data["test_asset4"],
        resources=[data["test_user4"], data["test_user5"]],
    )

    # for asset5
    data["test_task25"] = Task(
        name="Test Task 25",
        parent=data["test_asset5"],
        resources=[data["test_user6"], data["test_user7"]],
    )

    data["test_task26"] = Task(
        name="Test Task 26",
        parent=data["test_asset5"],
        resources=[data["test_user8"], data["test_user9"]],
    )

    data["test_task27"] = Task(
        name="Test Task 27",
        parent=data["test_asset5"],
        resources=[data["test_user10"], data["test_user1"]],
    )

    # final task hierarchy
    # test_seq1
    # test_seq2
    # test_seq3
    #
    # test_seq4
    #     test_task4
    #     test_task5
    #     test_task6
    # test_seq5
    #     test_task7
    #     test_task8
    #     test_task9
    # test_seq6
    # test_seq7
    #
    # test_shot1
    #     test_task10
    #     test_task11
    #     test_task12
    # test_shot2
    #     test_task13
    #     test_task14
    #     test_task15
    # test_shot3
    #     test_task16
    #     test_task17
    #     test_task18
    # test_shot4
    #     test_task19
    #     test_task20
    #     test_task21
    #
    # test_asset1
    # test_asset2
    # test_asset3
    # test_asset4
    #     test_task22
    #     test_task23
    #     test_task24
    # test_asset5
    #     test_task25
    #     test_task26
    #     test_task27
    #
    # test_task1
    # test_task2
    # test_task3

    DBSession.add(data["test_project"])
    DBSession.commit()
    return data


def test___auto_name__class_attribute_is_set_to_false():
    """__auto_name__ class attribute is set to False for Project class."""
    assert Project.__auto_name__ is False


def test_setup_is_working_correctly(setup_project_db_test):
    """Setup is done correctly."""
    data = setup_project_db_test
    assert isinstance(data["test_project_type"], Type)
    assert isinstance(data["test_project_type2"], Type)


def test_sequences_attribute_is_read_only(setup_project_db_test):
    """Sequence attribute is read-only."""
    data = setup_project_db_test
    with pytest.raises(AttributeError) as cm:
        data["test_project"].sequences = ["some non sequence related data"]

    error_message = (
        "can't set attribute 'sequences'"
        if sys.version_info.minor < 11
        else "property 'sequences' of 'Project' object has no setter"
    )

    assert str(cm.value) == error_message


def test_assets_attribute_is_read_only(setup_project_db_test):
    """assets attribute is read only."""
    data = setup_project_db_test
    with pytest.raises(AttributeError) as _:
        data["test_project"].assets = ["some list"]


def test_image_format_argument_is_skipped(setup_project_db_test):
    """image_format attribute is None if the image_format argument is skipped."""
    data = setup_project_db_test
    data["kwargs"].pop("image_format")
    new_project = Project(**data["kwargs"])
    assert new_project.image_format is None


def test_image_format_argument_is_none(setup_project_db_test):
    """nothing is going to happen if the image_format is set to None."""
    data = setup_project_db_test
    data["kwargs"]["image_format"] = None
    new_project = Project(**data["kwargs"])
    assert new_project.image_format is None


def test_image_format_attribute_is_set_to_none(setup_project_db_test):
    """nothing will happen if the image_format attribute is set to None."""
    data = setup_project_db_test
    data["test_project"].image_format = None


def test_image_format_argument_accepts_image_format_only(setup_project_db_test):
    """TypeError is raised if the image_format argument value is not an ImageFormat."""
    data = setup_project_db_test
    data["kwargs"]["image_format"] = "a str"
    with pytest.raises(TypeError) as cm:
        Project(**data["kwargs"])

    assert str(cm.value) == (
        "Project.image_format should be an instance of "
        "stalker.models.format.ImageFormat, not str: 'a str'"
    )


def test_image_format_argument_is_working_properly(setup_project_db_test):
    """image_format argument value is correctly passed to the image_format attribute."""
    data = setup_project_db_test
    # and a proper image format
    data["kwargs"]["image_format"] = data["test_image_format"]
    new_project = Project(**data["kwargs"])
    assert new_project.image_format == data["test_image_format"]


def test_image_format_attribute_accepts_image_format_only(setup_project_db_test):
    """TypeError is raised if the image_format attr set not to an ImageFormat."""
    data = setup_project_db_test
    test_values = [1, 1.2, "a str", ["a", "list"], {"a": "dict"}]
    for test_value in test_values:
        with pytest.raises(TypeError) as cm:
            data["test_project"].image_format = test_value

    # and a proper image format
    data["test_project"].image_format = data["test_image_format"]


def test_image_format_attribute_works_properly(setup_project_db_test):
    """image_format attribute is working properly."""
    data = setup_project_db_test
    new_image_format = ImageFormat(name="Foo Image Format", width=10, height=10)
    data["test_project"].image_format = new_image_format
    assert data["test_project"].image_format == new_image_format


def test_fps_argument_is_skipped(setup_project_db_test):
    """Default value is used if fps is skipped."""
    data = setup_project_db_test
    data["kwargs"].pop("fps")
    new_project = Project(**data["kwargs"])
    assert new_project.fps == 25.0


def test_fps_attribute_is_set_to_none(setup_project_db_test):
    """TypeError is raised if the fps attribute is set to None."""
    data = setup_project_db_test
    data["kwargs"]["fps"] = None
    with pytest.raises(TypeError) as cm:
        Project(**data["kwargs"])

    assert str(cm.value) == (
        "Project.fps should be a positive float or int, not NoneType: 'None'"
    )


def test_fps_argument_is_given_as_non_float_or_integer_1(setup_project_db_test):
    """TypeError is raised if the fps arg is not a float, int."""
    data = setup_project_db_test
    data["kwargs"]["fps"] = "a str"
    with pytest.raises(TypeError) as cm:
        Project(**data["kwargs"])

    assert str(cm.value) == (
        "Project.fps should be a positive float or int, not str: 'a str'"
    )


def test_fps_argument_is_given_as_non_float_or_integer_2(setup_project_db_test):
    """TypeError is raised if the fps arg not a float or int."""
    data = setup_project_db_test
    data["kwargs"]["fps"] = ["a", "list"]
    with pytest.raises(TypeError) as cm:
        Project(**data["kwargs"])

    assert str(cm.value) == (
        "Project.fps should be a positive float or int, not list: '['a', 'list']'"
    )


def test_fps_attribute_is_given_as_non_float_or_integer_1(setup_project_db_test):
    """TypeError is raised if the fps attr set not to a float, int."""
    data = setup_project_db_test
    with pytest.raises(TypeError) as cm:
        data["test_project"].fps = "a str"

    assert str(cm.value) == (
        "Project.fps should be a positive float or int, not str: 'a str'"
    )


def test_fps_attribute_is_given_as_non_float_or_integer_2(setup_project_db_test):
    """TypeError is raised if the fps attr set not to a float, int."""
    data = setup_project_db_test
    with pytest.raises(TypeError) as cm:
        data["test_project"].fps = ["a", "list"]

    assert str(cm.value) == (
        "Project.fps should be a positive float or int, not list: '['a', 'list']'"
    )


def test_fps_argument_string_to_float_conversion(setup_project_db_test):
    """TypeError is raised if a string containing a float has been passed."""
    data = setup_project_db_test
    data["kwargs"]["fps"] = "2.3"
    with pytest.raises(TypeError) as cm:
        Project(**data["kwargs"])

    assert str(cm.value) == (
        "Project.fps should be a positive float or int, not str: '2.3'"
    )


def test_fps_attribute_string_to_float_conversion(setup_project_db_test):
    """TypeError is raised if the fps attr is set to a string containing a float."""
    data = setup_project_db_test
    with pytest.raises(TypeError) as cm:
        data["test_project"].fps = "2.3"

    assert str(cm.value) == (
        "Project.fps should be a positive float or int, not str: '2.3'"
    )


def test_fps_attribute_float_conversion(setup_project_db_test):
    """fps attr is converted to float if the float argument is given as an integer."""
    data = setup_project_db_test
    test_value = 1
    data["kwargs"]["fps"] = test_value
    new_project = Project(**data["kwargs"])
    assert isinstance(new_project.fps, float)
    assert new_project.fps == float(test_value)


def test_fps_attribute_float_conversion_2(setup_project_db_test):
    """fps attribute is converted to float if it is set to an integer value."""
    data = setup_project_db_test
    test_value = 1
    data["test_project"].fps = test_value
    assert isinstance(data["test_project"].fps, float)
    assert data["test_project"].fps == float(test_value)


def test_fps_argument_is_zero(setup_project_db_test):
    """ValueError is raised if the fps is 0."""
    data = setup_project_db_test
    data["kwargs"]["fps"] = 0
    with pytest.raises(ValueError) as cm:
        Project(**data["kwargs"])
    assert str(cm.value) == "Project.fps should be a positive float or int, not 0.0"


def test_fps_attribute_is_set_to_zero(setup_project_db_test):
    """value error is raised if the fps attribute is set to zero."""
    data = setup_project_db_test
    with pytest.raises(ValueError) as cm:
        data["test_project"].fps = 0
    assert str(cm.value) == "Project.fps should be a positive float or int, not 0.0"


def test_fps_argument_is_negative(setup_project_db_test):
    """ValueError is raised if the fps argument is negative."""
    data = setup_project_db_test
    data["kwargs"]["fps"] = -1.0
    with pytest.raises(ValueError) as cm:
        Project(**data["kwargs"])
    assert str(cm.value) == "Project.fps should be a positive float or int, not -1.0"


def test_fps_attribute_is_negative(setup_project_db_test):
    """ValueError is raised if the fps attribute is set to a negative value."""
    data = setup_project_db_test
    with pytest.raises(ValueError) as cm:
        data["test_project"].fps = -1
    assert str(cm.value) == "Project.fps should be a positive float or int, not -1.0"


def test_repositories_argument_is_skipped(setup_project_db_test):
    """repositories attr is an empty list if the repositories argument is skipped."""
    data = setup_project_db_test
    data["kwargs"].pop("repositories")
    p = Project(**data["kwargs"])
    assert p.repositories == []


def test_repositories_argument_is_none(setup_project_db_test):
    """the repositories attr is an empty list if the repositories argument is None."""
    data = setup_project_db_test
    data["kwargs"]["repositories"] = None
    p = Project(**data["kwargs"])
    assert p.repositories == []


def test_repositories_attribute_is_set_to_none(setup_project_db_test):
    """TypeError is raised if the repositories attribute is set to None."""
    data = setup_project_db_test
    with pytest.raises(TypeError) as cm:
        data["test_project"].repositories = None

    assert str(cm.value) == "'NoneType' object is not iterable"


def test_repositories_argument_is_not_a_list(setup_project_db_test):
    """TypeError is raised if the repositories argument value is not a list."""
    data = setup_project_db_test
    data["kwargs"]["repositories"] = "not a list"
    with pytest.raises(TypeError) as cm:
        Project(**data["kwargs"])

    assert (
        str(cm.value) == "ProjectRepository.repositories should be a list of "
        "stalker.models.repository.Repository instances or derivatives, "
        "not str: 'n'"
    )


def test_repositories_attribute_is_not_a_list(setup_project_db_test):
    """TypeError raised if the repositories attr is set to not a list."""
    data = setup_project_db_test
    with pytest.raises(TypeError) as cm:
        data["test_project"].repositories = "not a list"

    assert str(cm.value) == (
        "ProjectRepository.repositories should be a list of "
        "stalker.models.repository.Repository instances or derivatives, "
        "not str: 'n'"
    )


def test_repositories_argument_is_not_a_list_of_repository_instances(
    setup_project_db_test,
):
    """TypeError raised if the repositories arg is not Repository instances."""
    data = setup_project_db_test
    data["kwargs"]["repositories"] = ["not", 1, "list", "of", Repository, "instances"]
    with pytest.raises(TypeError) as cm:
        Project(**data["kwargs"])

    assert (
        str(cm.value) == "ProjectRepository.repositories should be a list of "
        "stalker.models.repository.Repository instances or derivatives, "
        "not str: 'not'"
    )


def test_repositories_attribute_is_not_a_list_of_repository_instances(
    setup_project_db_test,
):
    """TypeError raised if the repositories attr is set to a list of non Repository."""
    data = setup_project_db_test
    with pytest.raises(TypeError) as cm:
        data["test_project"].repositories = [
            "not",
            1,
            "list",
            "of",
            Repository,
            "instances",
        ]

    assert str(cm.value) == (
        "ProjectRepository.repositories should be a list of "
        "stalker.models.repository.Repository instances or derivatives, not str: 'not'"
    )


def test_repositories_argument_is_working_properly(setup_project_db_test):
    """repositories argument value is properly passed to the repositories attr."""
    data = setup_project_db_test
    assert data["test_project"].repositories == data["kwargs"]["repositories"]


def test_repositories_attribute_is_working_properly(setup_project_db_test):
    """repository attribute is working properly."""
    data = setup_project_db_test
    new_repo1 = Repository(
        name="Some Random Repo",
        code="SRP",
        linux_path="/mnt/S/random/repo",
        windows_path="S:/random/repo",
        osx_path="/Volumes/S/random/repo",
    )

    assert data["test_project"].repositories != [new_repo1]
    data["test_project"].repositories = [new_repo1]
    assert data["test_project"].repositories == [new_repo1]


def test_repositories_attribute_value_order_is_not_changing(setup_project_db_test):
    """Order of the repositories attribute is preserved."""
    data = setup_project_db_test
    repo1 = Repository(name="Repo1", code="R1")
    repo2 = Repository(name="Repo2", code="R1")
    repo3 = Repository(name="Repo3", code="R1")

    DBSession.add_all([repo1, repo2, repo3])
    DBSession.commit()

    test_value = [repo3, repo1, repo2]
    data["test_project"].repositories = test_value
    DBSession.commit()

    for i in range(10):
        db_proj = Project.query.first()
        assert db_proj.repositories == test_value
        DBSession.commit()


def test_is_stereoscopic_argument_skipped(setup_project_db_test):
    """is_stereoscopic will set the is_stereoscopic attribute to False."""
    data = setup_project_db_test
    data["kwargs"].pop("is_stereoscopic")
    new_project = Project(**data["kwargs"])
    assert new_project.is_stereoscopic is False


@pytest.mark.parametrize("test_value", [0, 1, 1.2, "", "str", ["a", "list"]])
def test_is_stereoscopic_argument_bool_conversion(test_value, setup_project_db_test):
    """is_stereoscopic arg is converted to a bool value."""
    data = setup_project_db_test
    data["kwargs"]["is_stereoscopic"] = test_value
    new_project = Project(**data["kwargs"])
    assert new_project.is_stereoscopic == bool(test_value)


@pytest.mark.parametrize("test_value", [0, 1, 1.2, "", "str", ["a", "list"]])
def test_is_stereoscopic_attribute_bool_conversion(test_value, setup_project_db_test):
    """is_stereoscopic attr is converted to a bool value correctly."""
    data = setup_project_db_test
    data["test_project"].is_stereoscopic = test_value
    assert data["test_project"].is_stereoscopic == bool(test_value)


def test_structure_argument_is_none(setup_project_db_test):
    """structure argument can be None."""
    data = setup_project_db_test
    data["kwargs"]["structure"] = None
    new_project = Project(**data["kwargs"])
    assert isinstance(new_project, Project)


def test_structure_attribute_is_none(setup_project_db_test):
    """structure attribute can be set to None."""
    data = setup_project_db_test
    data["test_project"].structure = None


def test_structure_argument_not_instance_of_structure(setup_project_db_test):
    """TypeError is raised if the structure argument is not an instance of Structure."""
    data = setup_project_db_test
    data["kwargs"]["structure"] = 1.215
    with pytest.raises(TypeError) as cm:
        Project(**data["kwargs"])

    assert (
        str(cm.value) == "Project.structure should be an instance of "
        "stalker.models.structure.Structure, not float: '1.215'"
    )


def test_structure_attribute_not_instance_of_structure(setup_project_db_test):
    """TypeError raised if the structure attr is not a Structure."""
    data = setup_project_db_test
    with pytest.raises(TypeError) as cm:
        data["test_project"].structure = 1.2

    assert (
        str(cm.value) == "Project.structure should be an instance of "
        "stalker.models.structure.Structure, not float: '1.2'"
    )


def test_structure_attribute_is_working_properly(setup_project_db_test):
    """structure attribute is working properly."""
    data = setup_project_db_test
    data["test_project"].structure = data["test_project_structure2"]
    assert data["test_project"].structure == data["test_project_structure2"]


def test_equality(setup_project_db_test):
    """Equality of two projects."""
    data = setup_project_db_test
    # create a new project with the same arguments
    new_project1 = Project(**data["kwargs"])

    # create a new entity with the same arguments
    new_entity = Entity(**data["kwargs"])

    # create another project with different name
    data["kwargs"]["name"] = "a different project"
    new_project2 = Project(**data["kwargs"])

    assert not data["test_project"] != new_project1
    assert data["test_project"] != new_project2
    assert data["test_project"] != new_entity


def test_inequality(setup_project_db_test):
    """Inequality of two projects"""
    data = setup_project_db_test
    # create a new project with the same arguments
    new_project1 = Project(**data["kwargs"])

    # create a new entity with the same arguments
    new_entity = Entity(**data["kwargs"])

    # create another project with different name
    data["kwargs"]["name"] = "a different project"
    new_project2 = Project(**data["kwargs"])

    assert not data["test_project"] != new_project1
    assert data["test_project"] != new_project2
    assert data["test_project"] != new_entity


def test_reference_mixin_initialization(setup_project_db_test):
    """ReferenceMixin part is initialized correctly."""
    data = setup_project_db_test
    link_type_1 = Type(name="Image", code="image", target_entity_type="Link")

    link1 = Link(
        name="Artwork 1",
        full_path="/mnt/M/JOBs/TEST_PROJECT",
        filename="a.jpg",
        type=link_type_1,
    )

    link2 = Link(
        name="Artwork 2",
        full_path="/mnt/M/JOBs/TEST_PROJECT",
        filename="b.jbg",
        type=link_type_1,
    )

    references = [link1, link2]

    data["kwargs"]["references"] = references
    new_project = Project(**data["kwargs"])
    assert new_project.references == references


def test_status_mixin_initialization(setup_project_db_test):
    """StatusMixin part is initialized correctly."""
    data = setup_project_db_test
    status_list = StatusList.query.filter_by(target_entity_type="Project").first()
    data["kwargs"]["status"] = 0
    data["kwargs"]["status_list"] = status_list
    new_project = Project(**data["kwargs"])
    assert new_project.status_list == status_list


def test_schedule_mixin_initialization(setup_project_db_test):
    """DateRangeMixin part is initialized correctly."""
    data = setup_project_db_test
    start = datetime.datetime(2013, 3, 22, 4, 0, tzinfo=pytz.utc) + datetime.timedelta(
        days=25
    )
    end = start + datetime.timedelta(days=12)

    data["kwargs"]["start"] = start
    data["kwargs"]["end"] = end

    new_project = Project(**data["kwargs"])
    assert new_project.start == start
    assert new_project.end == end
    assert new_project.duration == end - start


def test___strictly_typed___is_false(setup_project_db_test):
    """__strictly_typed__ is True for Project class."""
    assert Project.__strictly_typed__ is False


def test___strictly_typed___not_forces_type_initialization(setup_project_db_test):
    """Project can not be created without defining a type for it."""
    data = setup_project_db_test
    data["kwargs"].pop("type")
    Project(**data["kwargs"])  # should be possible


@pytest.mark.parametrize(
    "test_data",
    [
        "test_task1",
        "test_task2",
        "test_task3",
        "test_task4",
        "test_task5",
        "test_task6",
        "test_task7",
        "test_task8",
        "test_task9",
        "test_task10",
        "test_task11",
        "test_task12",
        "test_task13",
        "test_task14",
        "test_task15",
        "test_task16",
        "test_task17",
        "test_task18",
        "test_task19",
        "test_task20",
        "test_task21",
        "test_task22",
        "test_task23",
        "test_task24",
        "test_task25",
        "test_task26",
        "test_task27",
        "test_seq1",
        "test_seq2",
        "test_seq3",
        "test_seq4",
        "test_seq5",
        "test_seq6",
        "test_seq7",
        "test_asset1",
        "test_asset2",
        "test_asset3",
        "test_asset4",
        "test_asset5",
        "test_shot1",
        "test_shot2",
        "test_shot3",
        "test_shot4",
    ],
)
def test_tasks_attribute_returns_the_tasks_instances_related_to_this_project(
    test_data, setup_project_db_test
):
    """tasks attr returns a list of Task instances related to this Project instance."""
    data = setup_project_db_test
    # test if we are going to get all the Tasks for project.tasks
    assert len(data["test_project"].tasks) == 43
    assert data[test_data] in data["test_project"].tasks


@pytest.mark.parametrize(
    "test_data",
    [
        "test_task1",
        "test_task2",
        "test_task3",
        "test_seq1",
        "test_seq2",
        "test_seq3",
        "test_seq4",
        "test_seq5",
        "test_seq6",
        "test_seq7",
        "test_asset1",
        "test_asset2",
        "test_asset3",
        "test_asset4",
        "test_asset5",
        "test_shot1",
        "test_shot2",
        "test_shot3",
        "test_shot4",
    ],
)
def test_root_tasks_attribute_returns_the_tasks_instances_with_no_parent_in_this_project(
    test_data, setup_project_db_test
):
    """root_tasks attr returns Task instances on this Project that has no parent."""
    data = setup_project_db_test
    # test if we are going to get all the Tasks for project.tasks
    root_tasks = data["test_project"].root_tasks
    assert len(root_tasks) == 19
    assert data[test_data] in root_tasks


def test_users_argument_is_skipped(setup_project_db_test):
    """users attribute is an empty list if the users argument is skipped."""
    data = setup_project_db_test
    data["kwargs"]["name"] = "New Project Name"
    try:
        data["kwargs"].pop("users")
    except KeyError:
        pass
    new_project = Project(**data["kwargs"])
    assert new_project.users == []


def test_users_argument_is_none(setup_project_db_test):
    """the users attribute is an empty list if the users argument is set to None."""
    data = setup_project_db_test
    data["kwargs"]["name"] = "New Project Name"
    data["kwargs"]["users"] = None
    new_project = Project(**data["kwargs"])
    assert new_project.users == []


def test_users_attribute_is_set_to_none(setup_project_db_test):
    """TypeError is raised if the users attribute is set to None."""
    data = setup_project_db_test
    with pytest.raises(TypeError) as cm:
        data["test_project"].users = None

    assert str(cm.value) == "'NoneType' object is not iterable"


def test_users_argument_is_not_a_list_of_user_instances(setup_project_db_test):
    """TypeError is raised if the users argument is not a list of Users."""
    data = setup_project_db_test
    data["kwargs"]["name"] = "New Project Name"
    data["kwargs"]["users"] = ["not a list of User instances"]
    with pytest.raises(TypeError) as cm:
        Project(**data["kwargs"])

    assert (
        str(cm.value) == "ProjectUser.user should be a stalker.models.auth.User "
        "instance, not str: 'not a list of User instances'"
    )


def test_users_attribute_is_set_to_a_value_which_is_not_a_list_of_User_instances(
    setup_project_db_test,
):
    """TypeError raised if the user attribute is set to not a list of User instances."""
    data = setup_project_db_test
    with pytest.raises(TypeError) as cm:
        data["test_project"].users = ["not a list of Users"]

    assert (
        str(cm.value) == "ProjectUser.user should be a stalker.models.auth.User "
        "instance, not str: 'not a list of Users'"
    )


def test_users_argument_is_working_properly(setup_project_db_test):
    """users argument value is passed to the users attribute properly."""
    data = setup_project_db_test
    data["kwargs"]["users"] = [
        data["test_user1"],
        data["test_user2"],
        data["test_user3"],
    ]
    new_proj = Project(**data["kwargs"])
    assert sorted(data["kwargs"]["users"], key=lambda x: x.name) == sorted(
        new_proj.users, key=lambda x: x.name
    )


def test_users_attribute_is_working_properly(setup_project_db_test):
    """users attribute is working properly."""
    data = setup_project_db_test
    users = [data["test_user1"], data["test_user2"], data["test_user3"]]
    data["test_project"].users = users
    assert sorted(users, key=lambda x: x.name) == sorted(
        data["test_project"].users, key=lambda x: x.name
    )


def test_tjp_id_is_working_properly(setup_project_db_test):
    """tjp_id attribute is working properly."""
    data = setup_project_db_test
    data["test_project"].id = 654654
    assert data["test_project"].tjp_id == "Project_654654"


@pytest.mark.parametrize(
    "get_data_file", ["project_to_tjp_output.jinja2"], indirect=True
)
def test_to_tjp_is_working_properly(get_data_file, setup_project_db_test):
    """to_tjp attribute is working properly."""
    data = setup_project_db_test
    data_file_path = get_data_file
    with open(data_file_path, "r") as f:
        template_content = f.read()

    expected_tjp_temp = Template(template_content)
    expected_tjp = expected_tjp_temp.render(
        {
            "project": data["test_project"],
            "task1": data["test_task1"],
            "task2": data["test_task2"],
            "task3": data["test_task3"],
            "task4": data["test_task4"],
            "task5": data["test_task5"],
            "task6": data["test_task6"],
            "task7": data["test_task7"],
            "task8": data["test_task8"],
            "task9": data["test_task9"],
            "task10": data["test_task10"],
            "task11": data["test_task11"],
            "task12": data["test_task12"],
            "task13": data["test_task13"],
            "task14": data["test_task14"],
            "task15": data["test_task15"],
            "task16": data["test_task16"],
            "task17": data["test_task17"],
            "task18": data["test_task18"],
            "task19": data["test_task19"],
            "task20": data["test_task20"],
            "task21": data["test_task21"],
            "task22": data["test_task22"],
            "task23": data["test_task23"],
            "task24": data["test_task24"],
            "task25": data["test_task25"],
            "task26": data["test_task26"],
            "task27": data["test_task27"],
            "asset1": data["test_asset1"],
            "asset2": data["test_asset2"],
            "asset3": data["test_asset3"],
            "asset4": data["test_asset4"],
            "asset5": data["test_asset5"],
            "shot1": data["test_shot1"],
            "shot2": data["test_shot2"],
            "shot3": data["test_shot3"],
            "shot4": data["test_shot4"],
            "sequence1": data["test_seq1"],
            "sequence2": data["test_seq2"],
            "sequence3": data["test_seq3"],
            "sequence4": data["test_seq4"],
            "sequence5": data["test_seq5"],
            "sequence6": data["test_seq6"],
            "sequence7": data["test_seq7"],
            "user1": data["test_user1"],
            "user2": data["test_user2"],
            "user3": data["test_user3"],
            "user4": data["test_user4"],
            "user5": data["test_user5"],
            "user6": data["test_user6"],
            "user7": data["test_user7"],
            "user8": data["test_user8"],
            "user9": data["test_user9"],
            "user10": data["test_user10"],
        }
    )

    # print(expected_tjp)
    # print("-----------------")
    # print(data["test_project"].to_tjp)

    assert data["test_project"].to_tjp == expected_tjp


def test_active_attribute_is_true_by_default(setup_project_db_test):
    """active attribute is True by default."""
    data = setup_project_db_test
    new_project = Project(**data["kwargs"])
    assert new_project.active is True


def test_is_active_is_read_only(setup_project_db_test):
    """is_active is a read only property."""
    data = setup_project_db_test
    with pytest.raises(AttributeError) as cm:
        data["test_project"].is_active = True

    error_message = (
        "can't set attribute 'is_active'"
        if sys.version_info.minor < 11
        else "property 'is_active' of 'Project' object has no setter"
    )

    assert str(cm.value) == error_message


def test_is_active_is_working_properly(setup_project_db_test):
    """is_active is working properly."""
    data = setup_project_db_test
    data["test_project"].active = True
    assert data["test_project"].is_active is True
    data["test_project"].active = False
    assert data["test_project"].is_active is False


def test_total_logged_seconds_attribute_is_read_only(setup_project_db_test):
    """total_logged_seconds attribute is a read-only attribute."""
    data = setup_project_db_test
    with pytest.raises(AttributeError) as cm:
        data["test_project"].total_logged_seconds = 32.3

    error_message = (
        "can't set attribute 'total_logged_seconds'"
        if sys.version_info.minor < 11
        else "property 'total_logged_seconds' of 'Project' object has no setter"
    )

    assert str(cm.value) == error_message


def test_total_logged_seconds_is_0_for_a_project_with_no_child_tasks(
    setup_project_db_test,
):
    """total_logged_seconds."""
    data = setup_project_db_test
    new_project = Project(**data["kwargs"])
    DBSession.add(new_project)
    DBSession.commit()
    assert new_project.total_logged_seconds == 0


def test_total_logged_seconds_attribute_is_working_properly(setup_project_db_test):
    """total_logged_seconds attribute is working properly."""
    data = setup_project_db_test
    # create some time logs
    TimeLog(
        task=data["test_task1"],
        resource=data["test_task1"].resources[0],
        start=datetime.datetime(2013, 8, 1, 1, 0, tzinfo=pytz.utc),
        duration=datetime.timedelta(hours=1),
    )
    DBSession.commit()
    assert data["test_project"].total_logged_seconds == 3600

    # add more time logs
    TimeLog(
        task=data["test_seq1"],
        resource=data["test_seq1"].resources[0],
        start=datetime.datetime(2013, 8, 1, 2, 0, tzinfo=pytz.utc),
        duration=datetime.timedelta(hours=1),
    )
    DBSession.commit()
    assert data["test_project"].total_logged_seconds == 7200

    # create more deeper time logs
    TimeLog(
        task=data["test_task10"],
        resource=data["test_task10"].resources[0],
        start=datetime.datetime(2013, 8, 1, 3, 0, tzinfo=pytz.utc),
        duration=datetime.timedelta(hours=3),
    )
    DBSession.commit()
    assert data["test_project"].total_logged_seconds == 18000

    # create a time log for one asset
    TimeLog(
        task=data["test_asset1"],
        resource=data["test_asset1"].resources[0],
        start=datetime.datetime(2013, 8, 1, 6, 0, tzinfo=pytz.utc),
        duration=datetime.timedelta(hours=10),
    )
    DBSession.commit()
    assert data["test_project"].total_logged_seconds == 15 * 3600


def test_schedule_seconds_attribute_is_read_only(setup_project_db_test):
    """schedule_seconds is a read-only attribute."""
    data = setup_project_db_test
    with pytest.raises(AttributeError) as cm:
        data["test_project"].schedule_seconds = 3

    error_message = (
        "can't set attribute 'schedule_seconds'"
        if sys.version_info.minor < 11
        else "property 'schedule_seconds' of 'Project' object has no setter"
    )

    assert str(cm.value) == error_message


def test_schedule_seconds_attribute_value_is_0_for_a_project_with_no_tasks(
    setup_project_db_test,
):
    """schedule_seconds attribute value is 0 for a project with no tasks."""
    data = setup_project_db_test
    new_project = Project(**data["kwargs"])
    DBSession.add(new_project)
    DBSession.commit()
    assert new_project.schedule_seconds == 0


@pytest.mark.parametrize(
    "test_entity,expected_value",
    [
        ["test_seq1", 3600],
        ["test_seq2", 3600],
        ["test_seq3", 3600],
        ["test_seq4", 3 * 3600],
        ["test_seq5", 3 * 3600],
        ["test_seq6", 3600],
        ["test_seq7", 3600],
        ["test_shot1", 12 * 3600],
        ["test_shot2", 3 * 3600],
        ["test_shot3", 3 * 3600],
        ["test_shot4", 3 * 3600],
        ["test_asset1", 3600],
        ["test_asset2", 3600],
        ["test_asset3", 3600],
        ["test_asset4", 3 * 3600],
        ["test_asset5", 3 * 3600],
        ["test_task1", 3600],
        ["test_task2", 3600],
        ["test_task3", 3600],
        ["test_task4", 3600],
        ["test_task5", 3600],
        ["test_task6", 3600],
        ["test_task7", 3600],
        ["test_task8", 3600],
        ["test_task9", 3600],
        ["test_task10", 10 * 3600],
        ["test_task11", 3600],
        ["test_task12", 3600],
        ["test_task13", 3600],
        ["test_task14", 3600],
        ["test_task15", 3600],
        ["test_task16", 3600],
        ["test_task17", 3600],
        ["test_task18", 3600],
        ["test_task19", 3600],
        ["test_task20", 3600],
        ["test_task21", 3600],
        ["test_task22", 3600],
        ["test_task23", 3600],
        ["test_task24", 3600],
        ["test_task25", 3600],
        ["test_task26", 3600],
        ["test_task27", 3600],
        ["test_project", 44 * 3600],
    ],
)
def test_schedule_seconds_attribute_is_working_properly(
    test_entity, expected_value, setup_project_db_test
):
    """schedule_seconds attribute value is gathered from the child tasks."""
    data = setup_project_db_test
    assert data["test_shot1"].is_container
    assert data["test_task10"].parent == data["test_shot1"]

    assert data[test_entity].schedule_seconds == expected_value


def test_percent_complete_attribute_is_read_only(setup_project_db_test):
    """percent_complete is a read-only attribute."""
    data = setup_project_db_test
    with pytest.raises(AttributeError) as cm:
        data["test_project"].percent_complete = 32.3

    error_message = (
        "can't set attribute 'percent_complete'"
        if sys.version_info.minor < 11
        else "property 'percent_complete' of 'Project' object has no setter"
    )

    assert str(cm.value) == error_message


def test_percent_complete_is_0_for_a_project_with_no_tasks(setup_project_db_test):
    """percent_complete attribute value is 0 for a project with no tasks."""
    data = setup_project_db_test
    new_project = Project(**data["kwargs"])
    DBSession.add(new_project)
    DBSession.commit()
    assert new_project.percent_complete == 0


def test_percent_complete_attribute_is_working_properly(setup_project_db_test):
    """percent_complete attribute is working properly"""
    data = setup_project_db_test
    assert data["test_project"].percent_complete == 0
    assert data["test_shot1"].is_container is True
    assert data["test_task10"].parent == data["test_shot1"]
    assert data["test_task10"].schedule_seconds == 36000
    assert data["test_task11"].schedule_seconds == 3600
    assert data["test_task12"].schedule_seconds == 3600
    assert data["test_shot1"].schedule_seconds == 12 * 3600

    # create some time logs
    t = TimeLog(
        task=data["test_task1"],
        resource=data["test_task1"].resources[0],
        start=datetime.datetime(2013, 8, 1, 1, 0, tzinfo=pytz.utc),
        duration=datetime.timedelta(hours=1),
    )
    DBSession.add(t)
    DBSession.commit()

    assert data["test_project"].percent_complete == (1.0 / 44.0 * 100)


def test_clients_argument_is_skipped(setup_project_db_test):
    """clients attribute is set to None if the clients argument is skipped."""
    data = setup_project_db_test
    data["kwargs"]["name"] = "New Project Name"
    try:
        data["kwargs"].pop("clients")
    except KeyError:
        pass
    new_project = Project(**data["kwargs"])
    assert new_project.clients == []


def test_clients_argument_is_none(setup_project_db_test):
    """clients argument can be None."""
    data = setup_project_db_test
    data["kwargs"]["clients"] = None
    new_project = Project(**data["kwargs"])
    assert new_project.clients == []


def test_clients_attribute_is_set_to_none(setup_project_db_test):
    """it a TypeError is raised if the clients attribute is set to None."""
    data = setup_project_db_test
    with pytest.raises(TypeError) as cm:
        data["test_project"].clients = None

    assert str(cm.value) == "'NoneType' object is not iterable"


def test_clients_argument_is_given_as_something_other_than_a_client(
    setup_project_db_test,
):
    """TypeError raised if the client arg is not a Client."""
    data = setup_project_db_test
    data["kwargs"]["clients"] = "a user"
    with pytest.raises(TypeError) as cm:
        Project(**data["kwargs"])

    assert str(cm.value) == (
        "ProjectClient.client should be an instance of "
        "stalker.models.auth.Client, not str: 'a'"
    )


def test_clients_attribute_is_not_a_client_instance(setup_project_db_test):
    """TypeError raised if the client attribute is not a Client."""
    data = setup_project_db_test
    with pytest.raises(TypeError) as cm:
        data["test_project"].clients = "a user"

    assert str(cm.value) == (
        "ProjectClient.client should be an instance of stalker.models.auth.Client, "
        "not str: 'a'"
    )


# def test_client_argument_is_working_properly(setup_project_db_test):
#     """client argument value is correctly passed to the client attribute."""
#     data = setup_project_db_test
#     assert data["test_project"].client == data["kwargs"]['client']


def test_clients_attribute_is_working_properly(setup_project_db_test):
    """clients attribute value can be updated correctly."""
    data = setup_project_db_test
    new_client = Client(name="New Client")
    assert data["test_project"].clients != [new_client]
    data["test_project"].clients = [new_client]
    assert data["test_project"].clients == [new_client]


@pytest.fixture(scope="function")
def setup_project_tickets_db_tests(setup_postgresql_db):
    """Set up the tests for the Project <-> Ticket relation."""
    data = dict()

    # create test objects
    data["start"] = datetime.datetime(2016, 11, 17, tzinfo=pytz.utc)
    data["end"] = data["start"] + datetime.timedelta(days=20)

    data["test_lead"] = User(
        name="lead", login="lead", email="lead@lead.com", password="lead"
    )

    data["test_user1"] = User(
        name="User1", login="user1", email="user1@users.com", password="123456"
    )

    data["test_user2"] = User(
        name="User2", login="user2", email="user2@users.com", password="123456"
    )

    data["test_user3"] = User(
        name="User3", login="user3", email="user3@users.com", password="123456"
    )

    data["test_user4"] = User(
        name="User4", login="user4", email="user4@users.com", password="123456"
    )

    data["test_user5"] = User(
        name="User5", login="user5", email="user5@users.com", password="123456"
    )

    data["test_user6"] = User(
        name="User6", login="user6", email="user6@users.com", password="123456"
    )

    data["test_user7"] = User(
        name="User7", login="user7", email="user7@users.com", password="123456"
    )

    data["test_user8"] = User(
        name="User8", login="user8", email="user8@users.com", password="123456"
    )

    data["test_user9"] = User(
        name="user9", login="user9", email="user9@users.com", password="123456"
    )

    data["test_user10"] = User(
        name="User10", login="user10", email="user10@users.com", password="123456"
    )

    data["test_image_format"] = ImageFormat(
        name="HD",
        width=1920,
        height=1080,
    )

    # type for project
    data["test_project_type"] = Type(
        name="Project Type 1", code="projt1", target_entity_type="Project"
    )

    data["test_project_type2"] = Type(
        name="Project Type 2", code="projt2", target_entity_type="Project"
    )

    # type for structure
    data["test_structure_type1"] = Type(
        name="Structure Type 1", code="struct1", target_entity_type="Structure"
    )

    data["test_structure_type2"] = Type(
        name="Structure Type 2", code="struct2", target_entity_type="Structure"
    )

    data["test_project_structure"] = Structure(
        name="Project Structure 1",
        type=data["test_structure_type1"],
    )

    data["test_project_structure2"] = Structure(
        name="Project Structure 2",
        type=data["test_structure_type2"],
    )

    data["test_repo"] = Repository(
        name="Commercials Repository",
        code="CR",
    )

    # create a project object
    data["kwargs"] = {
        "name": "Test Project",
        "code": "tp",
        "description": "This is a project object for testing purposes",
        "image_format": data["test_image_format"],
        "fps": 25,
        "type": data["test_project_type"],
        "structure": data["test_project_structure"],
        "repository": data["test_repo"],
        "is_stereoscopic": False,
        "display_width": 15,
        "start": data["start"],
        "end": data["end"],
    }

    data["test_project"] = Project(**data["kwargs"])

    # *********************************************************************
    # Tickets
    # *********************************************************************

    # no need to create status list for tickets cause we have a database
    # set up an running so it is automatically linked

    # tickets for version1
    data["test_ticket1"] = Ticket(project=data["test_project"])

    DBSession.add(data["test_ticket1"])
    # set it to closed
    data["test_ticket1"].resolve()
    DBSession.commit()

    # create a new ticket and leave it open
    data["test_ticket2"] = Ticket(project=data["test_project"])
    DBSession.add(data["test_ticket2"])
    DBSession.commit()

    # create a new ticket and close and then reopen it
    data["test_ticket3"] = Ticket(project=data["test_project"])
    DBSession.add(data["test_ticket3"])
    data["test_ticket3"].resolve()
    data["test_ticket3"].reopen()
    DBSession.commit()

    # *********************************************************************
    # tickets for version2
    # create a new ticket and leave it open
    data["test_ticket4"] = Ticket(project=data["test_project"])
    DBSession.add(data["test_ticket4"])
    DBSession.commit()

    # create a new Ticket and close it
    data["test_ticket5"] = Ticket(project=data["test_project"])
    DBSession.add(data["test_ticket5"])
    data["test_ticket5"].resolve()
    DBSession.commit()

    # create a new Ticket and close it
    data["test_ticket6"] = Ticket(project=data["test_project"])
    DBSession.add(data["test_ticket6"])
    data["test_ticket6"].resolve()
    DBSession.commit()

    # *********************************************************************
    # tickets for version3
    # create a new ticket and close it
    data["test_ticket7"] = Ticket(project=data["test_project"])
    DBSession.add(data["test_ticket7"])
    data["test_ticket7"].resolve()
    DBSession.commit()

    # create a new ticket and close it
    data["test_ticket8"] = Ticket(project=data["test_project"])
    DBSession.add(data["test_ticket8"])
    data["test_ticket8"].resolve()
    DBSession.commit()

    # *********************************************************************
    # tickets for version4
    # create a new ticket and close it
    data["test_ticket9"] = Ticket(project=data["test_project"])
    DBSession.add(data["test_ticket9"])

    data["test_ticket9"].resolve()
    DBSession.commit()

    # *********************************************************************

    DBSession.add(data["test_project"])
    DBSession.commit()
    return data


def test_tickets_attribute_is_an_empty_list_by_default(setup_project_tickets_db_tests):
    """Project.tickets is an empty list by default."""
    data = setup_project_tickets_db_tests
    project1 = Project(**data["kwargs"])
    assert project1.tickets == []


def test_open_tickets_attribute_is_an_empty_list_by_default(
    setup_project_tickets_db_tests,
):
    """Project.open_tickets is an empty list by default."""
    data = setup_project_tickets_db_tests
    project1 = Project(**data["kwargs"])
    DBSession.add(project1)
    DBSession.commit()
    assert project1.open_tickets == []


def test_open_tickets_attribute_is_read_only(setup_project_tickets_db_tests):
    """Project.open_tickets attribute is a read only attribute."""
    data = setup_project_tickets_db_tests
    with pytest.raises(AttributeError) as cm:
        data["test_project"].open_tickets = []

    error_message = (
        "can't set attribute 'open_tickets'"
        if sys.version_info.minor < 11
        else "property 'open_tickets' of 'Project' object has no setter"
    )

    assert str(cm.value) == error_message


def test_tickets_attribute_returns_all_tickets_in_this_project(
    setup_project_tickets_db_tests,
):
    """Project.tickets returns all the tickets in this project."""
    data = setup_project_tickets_db_tests
    # there should be tickets in this project already
    assert data["test_project"].tickets != []

    # now we should have some tickets
    assert len(data["test_project"].tickets) > 0

    # now check for exact items
    assert sorted(data["test_project"].tickets, key=lambda x: x.name) == sorted(
        [
            data["test_ticket1"],
            data["test_ticket2"],
            data["test_ticket3"],
            data["test_ticket4"],
            data["test_ticket5"],
            data["test_ticket6"],
            data["test_ticket7"],
            data["test_ticket8"],
            data["test_ticket9"],
        ],
        key=lambda x: x.name,
    )


def test_open_tickets_attribute_returns_all_open_tickets_owned_by_this_user(
    setup_project_tickets_db_tests,
):
    """User.open_tickets returns all the open tickets owned by this user."""
    data = setup_project_tickets_db_tests
    # there should be tickets in this project already
    assert data["test_project"].open_tickets != []

    # assign the user to some tickets
    data["test_ticket1"].reopen(data["test_user1"])
    data["test_ticket2"].reopen(data["test_user1"])
    data["test_ticket3"].reopen(data["test_user1"])
    data["test_ticket4"].reopen(data["test_user1"])
    data["test_ticket5"].reopen(data["test_user1"])
    data["test_ticket6"].reopen(data["test_user1"])
    data["test_ticket7"].reopen(data["test_user1"])
    data["test_ticket8"].reopen(data["test_user1"])

    # be careful not all of these are open tickets
    data["test_ticket1"].reassign(data["test_user1"], data["test_user1"])
    data["test_ticket2"].reassign(data["test_user1"], data["test_user1"])
    data["test_ticket3"].reassign(data["test_user1"], data["test_user1"])
    data["test_ticket4"].reassign(data["test_user1"], data["test_user1"])
    data["test_ticket5"].reassign(data["test_user1"], data["test_user1"])
    data["test_ticket6"].reassign(data["test_user1"], data["test_user1"])
    data["test_ticket7"].reassign(data["test_user1"], data["test_user1"])
    data["test_ticket8"].reassign(data["test_user1"], data["test_user1"])

    # now we should have some open tickets
    assert len(data["test_project"].open_tickets) > 0

    # now check for exact items
    assert sorted(data["test_project"].open_tickets, key=lambda x: x.name) == sorted(
        [
            data["test_ticket1"],
            data["test_ticket2"],
            data["test_ticket3"],
            data["test_ticket4"],
            data["test_ticket5"],
            data["test_ticket6"],
            data["test_ticket7"],
            data["test_ticket8"],
        ],
        key=lambda x: x.name,
    )

    # close a couple of them
    data["test_ticket1"].resolve(data["test_user1"], FIXED)
    data["test_ticket2"].resolve(data["test_user1"], INVALID)
    data["test_ticket3"].resolve(data["test_user1"], CANTFIX)

    # new check again
    assert sorted(data["test_project"].open_tickets, key=lambda x: x.name) == sorted(
        [
            data["test_ticket4"],
            data["test_ticket5"],
            data["test_ticket6"],
            data["test_ticket7"],
            data["test_ticket8"],
        ],
        key=lambda x: x.name,
    )
