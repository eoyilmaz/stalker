# -*- coding: utf-8 -*-
"""ReferenceMixin related tests."""

import pytest

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from stalker import Entity, Link, ReferenceMixin, SimpleEntity, Type


class RefMixFooClass(SimpleEntity, ReferenceMixin):
    """class for ReferenceMixin tests."""

    __tablename__ = "RefMixFooClasses"
    __mapper_args__ = {"polymorphic_identity": "RefMixFooClass"}
    refMixFooClass_id: Mapped[int] = mapped_column(
        "id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True
    )

    def __init__(self, **kwargs):
        super(RefMixFooClass, self).__init__(**kwargs)


@pytest.fixture(scope="function")
def setup_reference_mixin_tester():
    """Set up the tests for the ReferenceMixin.

    Returns:
        dict: test data.
    """
    # link type
    data = dict()
    data["test_link_type"] = Type(
        name="Test Link Type",
        code="testlink",
        target_entity_type=Link,
    )

    # create a couple of Link objects
    data["test_link1"] = Link(
        name="Test Link 1",
        type=data["test_link_type"],
        full_path="test_path",
        filename="test_filename",
    )

    data["test_link2"] = Link(
        name="Test Link 2",
        type=data["test_link_type"],
        full_path="test_path",
        filename="test_filename",
    )

    data["test_link3"] = Link(
        name="Test Link 3",
        type=data["test_link_type"],
        full_path="test_path",
        filename="test_filename",
    )

    data["test_link4"] = Link(
        name="Test Link 4",
        type=data["test_link_type"],
        full_path="test_path",
        filename="test_filename",
    )

    data["test_entity1"] = Entity(
        name="Test Entity 1",
    )

    data["test_entity2"] = Entity(
        name="Test Entity 2",
    )

    data["test_links"] = [
        data["test_link1"],
        data["test_link2"],
        data["test_link3"],
        data["test_link4"],
    ]

    data["test_foo_obj"] = RefMixFooClass(name="Ref Mixin Test")
    return data


def test_references_attribute_accepting_empty_list(setup_reference_mixin_tester):
    """references attribute accepting empty lists."""
    data = setup_reference_mixin_tester
    data["test_foo_obj"].references = []


def test_references_attribute_only_accepts_list_like_objects(
    setup_reference_mixin_tester,
):
    """references attribute accepts only list-like objects."""
    data = setup_reference_mixin_tester
    with pytest.raises(TypeError) as cm:
        data["test_foo_obj"].references = "a string"

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_references_attribute_accepting_only_lists_of_link_instances(
    setup_reference_mixin_tester,
):
    """references attribute accepting only lists of Links."""
    data = setup_reference_mixin_tester
    test_value = [1, 2.2, "some references"]

    with pytest.raises(TypeError) as cm:
        data["test_foo_obj"].references = test_value

    assert str(cm.value) == (
        "All the items in the RefMixFooClass.references should be "
        "stalker.models.link.Link instances, not int: '1'"
    )


def test_references_attribute_elements_accepts_links_only(setup_reference_mixin_tester):
    """TypeError is raised if non Link assigned to references attribute."""
    data = setup_reference_mixin_tester
    with pytest.raises(TypeError) as cm:
        data["test_foo_obj"].references = [data["test_entity1"], data["test_entity2"]]

    assert str(cm.value) == (
        "All the items in the RefMixFooClass.references should be "
        "stalker.models.link.Link instances, not Entity: '<Test Entity 1 (Entity)>'"
    )


def test_references_attribute_is_working_as_expected(setup_reference_mixin_tester):
    """references attribute working as expected."""
    data = setup_reference_mixin_tester
    data["test_foo_obj"].references = data["test_links"]
    assert data["test_foo_obj"].references == data["test_links"]

    test_value = [data["test_link1"], data["test_link2"]]
    data["test_foo_obj"].references = test_value
    assert sorted(data["test_foo_obj"].references, key=lambda x: x.name) == sorted(
        test_value, key=lambda x: x.name
    )


def test_references_application_test(setup_reference_mixin_tester):
    """example of ReferenceMixin usage."""

    class GreatEntity(SimpleEntity, ReferenceMixin):
        __tablename__ = "GreatEntities"
        __mapper_args__ = {"polymorphic_identity": "GreatEntity"}
        ge_id: Mapped[int] = mapped_column(
            "id", ForeignKey("SimpleEntities.id"), primary_key=True
        )

    my_ge = GreatEntity(name="Test")
    # we should have a references attribute right now
    _ = my_ge.references
    image_link_type = Type(name="Image", code="image", target_entity_type="Link")
    new_link = Link(
        name="NewTestLink",
        full_path="nopath",
        filename="nofilename",
        type=image_link_type,
    )
    test_value = [new_link]
    my_ge.references = test_value
    assert my_ge.references == test_value
