# -*- coding: utf-8 -*-
"""TraversalDirection related tests are here."""
from enum import IntEnum
import sys

import pytest

from stalker.models.enum import TraversalDirection


@pytest.mark.parametrize(
    "traversal_direction",
    [
        TraversalDirection.DepthFirst,
        TraversalDirection.BreadthFirst,
    ],
)
def test_it_is_an_int_enum(traversal_direction):
    """TraversalDirection is an IntEnum."""
    assert isinstance(traversal_direction, IntEnum)


@pytest.mark.parametrize(
    "traversal_direction,expected_value",
    [
        [TraversalDirection.DepthFirst, 0],
        [TraversalDirection.BreadthFirst, 1],
    ],
)
def test_enum_values(traversal_direction, expected_value):
    """Test enum values."""
    assert traversal_direction == expected_value


@pytest.mark.parametrize(
    "traversal_direction,expected_value",
    [
        [TraversalDirection.DepthFirst, "DepthFirst"],
        [TraversalDirection.BreadthFirst, "BreadthFirst"],
    ],
)
def test_enum_names(traversal_direction, expected_value):
    """Test enum names."""
    assert str(traversal_direction) == expected_value


def test_to_direction_direction_is_skipped():
    """TraversalDirection.to_direction() direction is skipped."""
    with pytest.raises(TypeError) as cm:
        _ = TraversalDirection.to_direction()

    py_error_message = {
        8: "to_direction() missing 1 required positional argument: 'direction'",
        9: "to_direction() missing 1 required positional argument: 'direction'",
        10: "TraversalDirection.to_direction() missing 1 required positional argument: 'direction'",
        11: "TraversalDirection.to_direction() missing 1 required positional argument: 'direction'",
        12: "TraversalDirection.to_direction() missing 1 required positional argument: 'direction'",
        13: "TraversalDirection.to_direction() missing 1 required positional argument: 'direction'",
    }[sys.version_info.minor]
    assert str(cm.value) == py_error_message


def test_to_direction_direction_is_none():
    """TraversalDirection.to_direction() direction is None."""
    with pytest.raises(TypeError) as cm:
        _ = TraversalDirection.to_direction(None)
    assert str(cm.value) == (
        "direction should be a TraversalDirection enum value or one "
        "of ['DepthFirst', 'BreadthFirst', 0, 1], not NoneType: 'None'"
    )


def test_to_direction_direction_is_not_a_str():
    """TraversalDirection.to_direction() direction is not an int or str."""
    with pytest.raises(TypeError) as cm:
        _ = TraversalDirection.to_direction(12334.123)

    assert str(cm.value) == (
        "direction should be a TraversalDirection enum value or one of "
        "['DepthFirst', 'BreadthFirst', 0, 1], not float: '12334.123'"
    )


def test_to_direction_direction_is_not_a_valid_str():
    """TraversalDirection.to_direction() direction is not a valid str."""
    with pytest.raises(ValueError) as cm:
        _ = TraversalDirection.to_direction("not a valid value")

    assert str(cm.value) == (
        "direction should be a TraversalDirection enum value or one of "
        "['DepthFirst', 'BreadthFirst', 0, 1], not 'not a valid value'"
    )


@pytest.mark.parametrize(
    "direction_name,direction",
    [
        # DepthFirst
        ["DepthFirst", TraversalDirection.DepthFirst],
        ["depthfirst", TraversalDirection.DepthFirst],
        ["DEPTHFIRST", TraversalDirection.DepthFirst],
        ["DePtHfIrSt", TraversalDirection.DepthFirst],
        ["dEpThFiRsT", TraversalDirection.DepthFirst],
        [0, TraversalDirection.DepthFirst],
        # BreadthFirst
        ["BreadthFirst", TraversalDirection.BreadthFirst],
        ["breadthfirst", TraversalDirection.BreadthFirst],
        ["BREADTHFIRST", TraversalDirection.BreadthFirst],
        ["BrEaDtHfIrSt", TraversalDirection.BreadthFirst],
        ["bReAdThFiRsT", TraversalDirection.BreadthFirst],
        [1, TraversalDirection.BreadthFirst],
    ],
)
def test_to_direction_is_working_properly(direction_name, direction):
    """TraversalDirection can parse schedule direction names."""
    assert TraversalDirection.to_direction(direction_name) == direction
