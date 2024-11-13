# -*- coding: utf-8 -*-
"""TargetEntityTypeMixin related tests."""

import sys
import pytest

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from stalker import Project, SimpleEntity
from stalker.models.mixins import TargetEntityTypeMixin


class TestClass(object):
    """A simple class for testing purposes."""

    pass


class TargetEntityTypeMixedClass(SimpleEntity, TargetEntityTypeMixin):
    """A simple class for TargetEntityTypeMixin tests."""

    __tablename__ = "TarEntMixClasses"
    __mapper_args__ = {"polymorphic_identity": "TarEntMixClass"}
    tarMixClass_id: Mapped[int] = mapped_column(
        "id", ForeignKey("SimpleEntities.id"), primary_key=True
    )

    def __init__(self, **kwargs):
        super(TargetEntityTypeMixedClass, self).__init__(**kwargs)
        TargetEntityTypeMixin.__init__(self, **kwargs)


@pytest.fixture(scope="function")
def setup_target_entity_mixin_tests():
    """Set up tests for the TargetEntityMixin.

    Returns:
        dict: Test data.
    """
    data = dict()
    data["kwargs"] = {"name": "Test object", "target_entity_type": Project}
    data["test_object"] = TargetEntityTypeMixedClass(**data["kwargs"])
    return data


def test_target_entity_type_argument_is_skipped(setup_target_entity_mixin_tests):
    """TypeError is raised if target_entity_type argument is skipped."""
    data = setup_target_entity_mixin_tests
    data["kwargs"].pop("target_entity_type")
    with pytest.raises(TypeError) as cm:
        TargetEntityTypeMixedClass(**data["kwargs"])

    assert (
        str(cm.value) == "TargetEntityTypeMixedClass.target_entity_type cannot be None"
    )


def test_target_entity_type_argument_being_empty_string(
    setup_target_entity_mixin_tests,
):
    """ValueError is raised if the target_entity_type argument is given as None."""
    data = setup_target_entity_mixin_tests
    data["kwargs"]["target_entity_type"] = ""
    with pytest.raises(ValueError) as cm:
        TargetEntityTypeMixedClass(**data["kwargs"])
    assert (
        str(cm.value) == "TargetEntityTypeMixedClass.target_entity_type cannot be empty"
    )


def test_target_entity_type_argument_being_none(setup_target_entity_mixin_tests):
    """TypeError is raised if target_entity_type argument is given as None."""
    data = setup_target_entity_mixin_tests
    data["kwargs"]["target_entity_type"] = None
    with pytest.raises(TypeError) as cm:
        TargetEntityTypeMixedClass(**data["kwargs"])
    assert (
        str(cm.value) == "TargetEntityTypeMixedClass.target_entity_type cannot be None"
    )


def test_target_entity_type_attribute_is_read_only(setup_target_entity_mixin_tests):
    """target_entity_type argument is read-only."""
    data = setup_target_entity_mixin_tests
    # try to set the target_entity_type attribute and expect AttributeError
    with pytest.raises(AttributeError) as cm:
        data["test_object"].target_entity_type = "Project"

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute",
        11: "property of 'TargetEntityTypeMixedClass' object has no setter",
        12: "property of 'TargetEntityTypeMixedClass' object has no setter",
    }.get(
        sys.version_info.minor,
        "property '_target_entity_type_getter' of 'TargetEntityTypeMixedClass' "
        "object has no setter",
    )

    assert str(cm.value) == error_message


def test_target_entity_type_argument_accepts_classes(setup_target_entity_mixin_tests):
    """target_entity_type argument accepts classes."""
    data = setup_target_entity_mixin_tests
    data["kwargs"]["target_entity_type"] = TestClass
    new_object = TargetEntityTypeMixedClass(**data["kwargs"])
    assert new_object.target_entity_type == "TestClass"
