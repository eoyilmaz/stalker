# -*- coding: utf-8 -*-
"""Asset class related tests."""

import pytest

from stalker import (
    Asset,
    Entity,
    Link,
    Project,
    Repository,
    Sequence,
    Shot,
    Status,
    StatusList,
    Task,
    Type,
    User,
)
from stalker.db.session import DBSession


@pytest.fixture(scope="function")
def setup_asset_tests(setup_postgresql_db):
    """Set up tests for the Asset class.

    Args:
        setup_postgresql_db: pytest.fixture.

    Returns:
        dict: Test data.
    """
    data = dict()
    # users
    data["test_user1"] = User(
        name="User1", login="user1", password="12345", email="user1@user1.com"
    )
    DBSession.add(data["test_user1"])
    data["test_user2"] = User(
        name="User2", login="user2", password="12345", email="user2@user2.com"
    )
    DBSession.add(data["test_user2"])
    DBSession.commit()
    # statuses
    data["status_wip"] = Status.query.filter_by(code="WIP").first()
    data["status_cmpl"] = Status.query.filter_by(code="CMPL").first()
    # types
    data["commercial_project_type"] = Type(
        name="Commercial Project",
        code="commproj",
        target_entity_type="Project",
    )
    DBSession.add(data["commercial_project_type"])
    data["asset_type1"] = Type(
        name="Character", code="char", target_entity_type="Asset"
    )
    DBSession.add(data["asset_type1"])
    data["asset_type2"] = Type(
        name="Environment", code="env", target_entity_type="Asset"
    )
    DBSession.add(data["asset_type2"])
    data["repository_type"] = Type(
        name="Test Repository Type",
        code="testrepo",
        target_entity_type="Repository",
    )
    DBSession.add(data["repository_type"])
    # repository
    data["repository"] = Repository(
        name="Test Repository",
        code="TR",
        type=data["repository_type"],
    )
    DBSession.add(data["repository"])
    # project
    data["project1"] = Project(
        name="Test Project1",
        code="tp1",
        type=data["commercial_project_type"],
        repositories=[data["repository"]],
    )
    DBSession.add(data["project1"])
    DBSession.commit()
    # sequence
    data["seq1"] = Sequence(
        name="Test Sequence",
        code="tseq",
        project=data["project1"],
        responsible=[data["test_user1"]],
    )
    DBSession.add(data["seq1"])
    # shots
    data["shot1"] = Shot(
        code="TestSH001",
        project=data["project1"],
        sequence=data["seq1"],
        responsible=[data["test_user1"]],
    )
    DBSession.add(data["shot1"])
    data["shot2"] = Shot(
        code="TestSH002",
        project=data["project1"],
        sequence=data["seq1"],
        responsible=[data["test_user1"]],
    )
    DBSession.add(data["shot2"])
    data["shot3"] = Shot(
        code="TestSH003",
        project=data["project1"],
        sequence=data["seq1"],
        responsible=[data["test_user1"]],
    )
    DBSession.add(data["shot3"])
    data["shot4"] = Shot(
        code="TestSH004",
        project=data["project1"],
        sequence=data["seq1"],
        responsible=[data["test_user1"]],
    )
    DBSession.add(data["shot4"])
    data["kwargs"] = {
        "name": "Test Asset",
        "code": "ta",
        "description": "This is a test Asset object",
        "project": data["project1"],
        "type": data["asset_type1"],
        "status": 0,
        "responsible": [data["test_user1"]],
    }
    data["asset1"] = Asset(**data["kwargs"])
    DBSession.add(data["asset1"])
    # tasks
    data["task1"] = Task(
        name="Task1",
        parent=data["asset1"],
    )
    DBSession.add(data["task1"])
    data["task2"] = Task(
        name="Task2",
        parent=data["asset1"],
    )
    DBSession.add(data["task2"])
    data["task3"] = Task(
        name="Task3",
        parent=data["asset1"],
    )
    DBSession.add(data["task3"])
    DBSession.commit()
    return data


def test_auto_name_class_attribute_is_set_to_false():
    """__auto_name__ class attribute is set to False for Asset class."""
    assert Asset.__auto_name__ is False


def test_name_cannot_be_set_to_none(setup_asset_tests):
    """name arg cannot be set to None."""
    data = setup_asset_tests
    data["kwargs"]["name"] = None
    with pytest.raises(TypeError) as cm:
        _ = Asset(**data["kwargs"])

    assert str(cm.value) == "Asset.name cannot be None"


def test_name_cannot_be_set_to_empty_string(setup_asset_tests):
    """name arg cannot be set to None."""
    data = setup_asset_tests
    data["kwargs"]["name"] = ""
    with pytest.raises(ValueError) as cm:
        _ = Asset(**data["kwargs"])

    assert str(cm.value) == "Asset.name cannot be an empty string"


def test_equality(setup_asset_tests):
    """Equality of two Asset objects."""
    data = setup_asset_tests
    new_asset1 = Asset(**data["kwargs"])
    new_asset2 = Asset(**data["kwargs"])
    new_entity1 = Entity(**data["kwargs"])
    data["kwargs"]["type"] = data["asset_type2"]
    new_asset3 = Asset(**data["kwargs"])
    data["kwargs"]["name"] = "another name"
    new_asset4 = Asset(**data["kwargs"])
    assert new_asset1 == new_asset2
    assert not new_asset1 == new_asset3
    assert not new_asset1 == new_asset4
    assert not new_asset3 == new_asset4
    assert not new_asset1 == new_entity1


def test_inequality(setup_asset_tests):
    """Inequality of two Asset objects."""
    data = setup_asset_tests
    new_asset1 = Asset(**data["kwargs"])
    new_asset2 = Asset(**data["kwargs"])
    new_entity1 = Entity(**data["kwargs"])
    data["kwargs"]["type"] = data["asset_type2"]
    new_asset3 = Asset(**data["kwargs"])
    data["kwargs"]["name"] = "another name"
    new_asset4 = Asset(**data["kwargs"])
    assert not new_asset1 != new_asset2
    assert new_asset1 != new_asset3
    assert new_asset1 != new_asset4
    assert new_asset3 != new_asset4
    assert new_asset1 != new_entity1


def test_reference_mixin_initialization(setup_asset_tests):
    """ReferenceMixin part is initialized correctly."""
    data = setup_asset_tests
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
    data["kwargs"]["code"] = "SH12314"
    data["kwargs"]["references"] = references
    new_asset = Asset(**data["kwargs"])
    assert new_asset.references == references


def test_status_mixin_initialization(setup_asset_tests):
    """StatusMixin part is initialized correctly."""
    data = setup_asset_tests
    status_list = StatusList.query.filter_by(target_entity_type="Asset").first()
    data["kwargs"]["code"] = "SH12314"
    data["kwargs"]["status"] = 0
    data["kwargs"]["status_list"] = status_list
    new_asset = Asset(**data["kwargs"])
    assert new_asset.status_list == status_list


def test_task_mixin_initialization(setup_asset_tests):
    """TaskMixin part is initialized correctly."""
    data = setup_asset_tests
    commercial_project_type = Type(
        name="Commercial",
        code="comm",
        target_entity_type="Project",
    )
    new_project = Project(
        name="Commercial",
        code="COM",
        type=commercial_project_type,
        repository=data["repository"],
    )
    character_asset_type = Type(
        name="Character", code="char", target_entity_type="Asset"
    )
    new_asset = Asset(
        name="test asset",
        type=character_asset_type,
        code="tstasset",
        project=new_project,
        responsible=[data["test_user1"]],
    )
    task1 = Task(name="Modeling", parent=new_asset)
    task2 = Task(name="Lighting", parent=new_asset)
    tasks = [task1, task2]

    assert sorted(new_asset.tasks, key=lambda x: x.name) == sorted(
        tasks, key=lambda x: x.name
    )


def test_plural_class_name(setup_asset_tests):
    """Default plural name of the Asset class."""
    data = setup_asset_tests
    assert data["asset1"].plural_class_name == "Assets"


def test_strictly_typed_is_true():
    """__strictly_typed__ class attribute is True."""
    assert Asset.__strictly_typed__ is True


def test_hash_value(setup_asset_tests):
    """__hash__ returns the hash of the Asset instance."""
    data = setup_asset_tests
    result = hash(data["asset1"])
    assert isinstance(result, int)


def test_template_variables_for_asset_related_task(setup_asset_tests):
    """_template_variables() for an asset related task returns correct data."""
    data = setup_asset_tests
    assert data["task2"]._template_variables() == {
        "asset": data["asset1"],
        "parent_tasks": [data["asset1"], data["task2"]],
        "project": data["project1"],
        "scenes": [],
        "sequence": None,
        "shot": None,
        "task": data["task2"],
        "type": None
    }


def test_template_variables_for_asset_itself(setup_asset_tests):
    """_template_variables() for an asset itself returns correct data."""
    data = setup_asset_tests
    assert data["asset1"]._template_variables() == {
        "asset": data["asset1"],
        "parent_tasks": [data["asset1"]],
        "project": data["project1"],
        "scenes": [],
        "sequence": None,
        "shot": None,
        "task": data["asset1"],
        "type": data["asset_type1"]
    }
