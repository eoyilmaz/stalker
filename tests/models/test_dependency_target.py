# -*- coding: utf-8 -*-
"""DependencyTarget related tests are here."""
from enum import Enum
import sys

import pytest

from stalker.models.enum import DependencyTarget


@pytest.mark.parametrize(
    "target",
    [
        DependencyTarget.OnStart,
        DependencyTarget.OnEnd,
    ],
)
def test_it_is_an_enum(target):
    """DependencyTarget is an Enum."""
    assert isinstance(target, Enum)


@pytest.mark.parametrize(
    "target,expected_value",
    [
        [DependencyTarget.OnStart, "onstart"],
        [DependencyTarget.OnEnd, "onend"],
    ],
)
def test_enum_values(target, expected_value):
    """Test enum values."""
    assert target.value == expected_value


@pytest.mark.parametrize(
    "target,expected_name",
    [
        [DependencyTarget.OnStart, "OnStart"],
        [DependencyTarget.OnEnd, "OnEnd"],
    ],
)
def test_enum_names(target, expected_name):
    """Test enum names."""
    assert target.name == expected_name


@pytest.mark.parametrize(
    "target,expected_value",
    [
        [DependencyTarget.OnStart, "onstart"],
        [DependencyTarget.OnEnd, "onend"],
    ],
)
def test_enum_as_str(target, expected_value):
    """Test enum names."""
    assert str(target) == expected_value


def test_to_target_target_is_skipped():
    """DependencyTarget.to_target() target is skipped."""
    with pytest.raises(TypeError) as cm:
        _ = DependencyTarget.to_target()

    py_error_message = {
        8: "to_target() missing 1 required positional argument: 'target'",
        9: "to_target() missing 1 required positional argument: 'target'",
        10: "DependencyTarget.to_target() missing 1 required positional argument: 'target'",
        11: "DependencyTarget.to_target() missing 1 required positional argument: 'target'",
        12: "DependencyTarget.to_target() missing 1 required positional argument: 'target'",
        13: "DependencyTarget.to_target() missing 1 required positional argument: 'target'",
    }[sys.version_info.minor]
    assert str(cm.value) == py_error_message


def test_to_target_target_is_none():
    """DependencyTarget.to_target() target is None."""
    with pytest.raises(TypeError) as cm:
        _ = DependencyTarget.to_target(None)
    assert str(cm.value) == (
        "target should be a DependencyTarget enum value or one of ['OnStart', 'OnEnd', 'onstart', 'onend'], not NoneType: 'None'"
    )


def test_to_target_target_is_not_a_str():
    """DependencyTarget.to_target() target is not a str."""
    with pytest.raises(TypeError) as cm:
        _ = DependencyTarget.to_target(12334.123)

    assert str(cm.value) == (
        "target should be a DependencyTarget enum value or one of ['OnStart', 'OnEnd', 'onstart', 'onend'], not float: '12334.123'"
    )


def test_to_target_target_is_not_a_valid_str():
    """DependencyTarget.to_target() target is not a valid str."""
    with pytest.raises(ValueError) as cm:
        _ = DependencyTarget.to_target("not a valid value")

    assert str(cm.value) == (
        "target should be a DependencyTarget enum value or one of ['OnStart', "
        "'OnEnd', 'onstart', 'onend'], not 'not a valid value'"
    )


@pytest.mark.parametrize(
    "target_name,target",
    [
        # OnStart
        ["OnStart", DependencyTarget.OnStart],
        ["onstart", DependencyTarget.OnStart],
        ["ONSTART", DependencyTarget.OnStart],
        ["oNsTART", DependencyTarget.OnStart],
        # OnEnd
        ["OnEnd", DependencyTarget.OnEnd],
        ["onend", DependencyTarget.OnEnd],
        ["ONEND", DependencyTarget.OnEnd],
        ["oNeNd", DependencyTarget.OnEnd],
        ["OnEnD", DependencyTarget.OnEnd],
    ],
)
def test_to_target_is_working_properly(target_name, target):
    """DependencyTarget can parse dependency target names."""
    assert DependencyTarget.to_target(target_name) == target
