# -*- coding: utf-8 -*-

import pytest

from sqlalchemy import Column, ForeignKey, Integer, Table

from stalker import SimpleEntity
from stalker.db.declarative import Base
from stalker.models.mixins import create_secondary_table


@pytest.fixture(scope="function")
def setup_test_class():
    """Create a test class."""

    class TestEntity(SimpleEntity):
        """Test class."""

        __tablename__ = "TestEntities"
        __table_args__ = {"extend_existing": True}
        __mapper_args__ = {"polymorphic_identity": "TestEntity"}
        test_entity_id = Column(
            "id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True
        )

    yield TestEntity


def test_primary_cls_name_is_none(setup_test_class):
    """primary_cls_name is None raises TypeError."""
    _ = setup_test_class
    with pytest.raises(TypeError) as cm:
        create_secondary_table(
            None,  # "TestEntity",
            "Link",
            "TestEntities",
            "Links",
            "TestEntity_References",
        )

    assert str(cm.value) == (
        "primary_cls_name should be a str containing the primary class name, "
        "not NoneType: 'None'"
    )


def test_primary_cls_name_is_not_a_string(setup_test_class):
    """primary_cls_name is not str raises TypeError."""
    _ = setup_test_class
    with pytest.raises(TypeError) as cm:
        create_secondary_table(
            1234,  # "TestEntity",
            "Link",
            "TestEntities",
            "Links",
            "TestEntity_References",
        )

    assert str(cm.value) == (
        "primary_cls_name should be a str containing the primary class name, "
        "not int: '1234'"
    )


def test_primary_cls_name_is_empty_string(setup_test_class):
    """primary_cls_name is an empty str raises ValueError."""
    _ = setup_test_class
    with pytest.raises(ValueError) as cm:
        create_secondary_table(
            "",  # "TestEntity",
            "Link",
            "TestEntities",
            "Links",
            "TestEntity_References",
        )

    assert str(cm.value) == (
        "primary_cls_name should be a str containing the primary class name, not: ''"
    )


def test_secondary_cls_name_is_none(setup_test_class):
    """secondary_cls_name is None raises TypeError."""
    _ = setup_test_class
    with pytest.raises(TypeError) as cm:
        create_secondary_table(
            "TestEntity",
            None,  # "Link",
            "TestEntities",
            "Links",
            "TestEntity_References",
        )

    assert str(cm.value) == (
        "secondary_cls_name should be a str containing the secondary class name, "
        "not NoneType: 'None'"
    )


def test_secondary_cls_name_is_not_a_string(setup_test_class):
    """secondary_cls_name is not str raises TypeError."""
    _ = setup_test_class
    with pytest.raises(TypeError) as cm:
        create_secondary_table(
            "TestEntity",
            1234,  # "Link",
            "TestEntities",
            "Links",
            "TestEntity_References",
        )

    assert str(cm.value) == (
        "secondary_cls_name should be a str containing the secondary class name, "
        "not int: '1234'"
    )


def test_secondary_cls_name_is_empty_string(setup_test_class):
    """secondary_cls_name is an empty str raises ValueError."""
    _ = setup_test_class
    with pytest.raises(ValueError) as cm:
        create_secondary_table(
            "TestEntity",
            "",  # "Link",
            "TestEntities",
            "Links",
            "TestEntity_References",
        )

    assert str(cm.value) == (
        "secondary_cls_name should be a str containing the secondary class name, "
        "not: ''"
    )


def test_secondary_cls_name_is_converted_to_plural(setup_test_class):
    """secondary_cls_name is converted to plural."""
    return_value = create_secondary_table(
        "TestEntity",
        "Link",
        "TestEntities",
        "Links",
        None,  # "TestEntity_References"
    )
    assert return_value.name == "TestEntity_Links"


def test_primary_cls_table_name_is_none(setup_test_class):
    """primary_cls_table_name is None raises TypeError."""
    _ = setup_test_class
    with pytest.raises(TypeError) as cm:
        create_secondary_table(
            "TestEntity",
            "Link",
            None,  # "TestEntities",
            "Links",
            "TestEntity_References",
        )

    assert str(cm.value) == (
        "primary_cls_table_name should be a str containing the primary class table "
        "name, not NoneType: 'None'"
    )


def test_primary_cls_table_name_is_not_a_string(setup_test_class):
    """primary_cls_table_name is not str raises TypeError."""
    _ = setup_test_class
    with pytest.raises(TypeError) as cm:
        create_secondary_table(
            "TestEntity",
            "Link",
            1234,  # "TestEntities",
            "Links",
            "TestEntity_References",
        )

    assert str(cm.value) == (
        "primary_cls_table_name should be a str containing the primary class table "
        "name, not int: '1234'"
    )


def test_primary_cls_table_name_is_empty_string(setup_test_class):
    """primary_cls_table_name is an empty str raises ValueError."""
    _ = setup_test_class
    with pytest.raises(ValueError) as cm:
        create_secondary_table(
            "TestEntity",
            "Link",
            "",  # "TestEntities",
            "Links",
            "TestEntity_References",
        )

    assert str(cm.value) == (
        "primary_cls_table_name should be a str containing the primary class table "
        "name, not: ''"
    )


def test_secondary_cls_table_name_is_none(setup_test_class):
    """secondary_cls_table_name is None raises TypeError."""
    _ = setup_test_class
    with pytest.raises(TypeError) as cm:
        create_secondary_table(
            "TestEntity",
            "Link",
            "TestEntities",
            None,  # "Links",
            "TestEntity_References",
        )

    assert str(cm.value) == (
        "secondary_cls_table_name should be a str containing the secondary class table "
        "name, not NoneType: 'None'"
    )


def test_secondary_cls_table_name_is_not_a_string(setup_test_class):
    """secondary_cls_table_name is not str raises TypeError."""
    _ = setup_test_class
    with pytest.raises(TypeError) as cm:
        create_secondary_table(
            "TestEntity",
            "Link",
            "TestEntities",
            1234,  # "Links",
            "TestEntity_References",
        )

    assert str(cm.value) == (
        "secondary_cls_table_name should be a str containing the secondary class table "
        "name, not int: '1234'"
    )


def test_secondary_cls_table_name_is_empty_string(setup_test_class):
    """secondary_cls_table_name is an empty str raises ValueError."""
    _ = setup_test_class
    with pytest.raises(ValueError) as cm:
        create_secondary_table(
            "TestEntity",
            "Link",
            "TestEntities",
            "",  # "Links",
            "TestEntity_References",
        )

    assert str(cm.value) == (
        "secondary_cls_table_name should be a str containing the secondary class table "
        "name, not: ''"
    )


def test_secondary_table_name_can_be_none(setup_test_class):
    """secondary_table_name can be None."""
    return_value = create_secondary_table(
        "TestEntity",
        "Link",
        "TestEntities",
        "Links",
        None,  # "TestEntity_References"
    )
    assert return_value.name == "TestEntity_Links"


def test_secondary_table_name_is_not_a_str(setup_test_class):
    """secondary_table_name is not str raises TypeError."""
    with pytest.raises(TypeError) as cm:
        _ = create_secondary_table(
            "TestEntity",
            "Link",
            "TestEntities",
            "Links",
            1234,  # "TestEntity_References"
        )
    assert str(cm.value) == (
        "secondary_table_name should be a str containing the secondary table name, "
        "or it can be None or an empty string to let Stalker to auto generate one, "
        "not int: '1234'"
    )


def test_secondary_table_name_is_an_empty_str(setup_test_class):
    """secondary_table_name is an empty string generates new name from class names."""
    return_value = create_secondary_table(
        "TestEntity",
        "Link",
        "TestEntities",
        "Links",
        "",  # "TestEntity_References"
    )
    assert return_value.name == "TestEntity_Links"


def test_secondary_table_name_already_exists_in_base_metadata(setup_test_class):
    """secondary_table_name already exists will use that table."""
    assert "TestEntity_References" not in Base.metadata
    return_value_1 = create_secondary_table(
        "TestEntity", "Link", "TestEntities", "Links", "TestEntity_References"
    )
    assert "TestEntity_References" in Base.metadata
    # should not generate any errors
    return_value_2 = create_secondary_table(
        "TestEntity", "Link", "TestEntities", "Links", "TestEntity_References"
    )
    # and return the same table
    assert return_value_2.name == "TestEntity_References"
    assert return_value_1 == return_value_2


def test_returns_a_table(setup_test_class):
    """create_secondary_table returns a table."""
    return_value = create_secondary_table(
        "TestEntity", "Link", "TestEntities", "Links", "TestEntity_References"
    )
    assert isinstance(return_value, Table)
