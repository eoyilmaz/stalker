# -*- coding: utf-8 -*-
"""ScheduleConstraint related tests are here."""
from enum import IntEnum
import sys

import pytest

from stalker.models.mixins import ScheduleConstraint


@pytest.mark.parametrize(
    "schedule_constraint",
    [
        ScheduleConstraint.NONE,
        ScheduleConstraint.Start,
        ScheduleConstraint.End,
        ScheduleConstraint.Both,
    ],
)
def test_it_is_an_int_enum(schedule_constraint):
    """ScheduleConstraint is an IntEnum."""
    assert isinstance(schedule_constraint, IntEnum)


@pytest.mark.parametrize(
    "schedule_constraint,expected_value",
    [
        [ScheduleConstraint.NONE, 0],
        [ScheduleConstraint.Start, 1],
        [ScheduleConstraint.End, 2],
        [ScheduleConstraint.Both, 3],
    ],
)
def test_enum_values(schedule_constraint, expected_value):
    """Test enum values."""
    assert schedule_constraint == expected_value


@pytest.mark.parametrize(
    "schedule_constraint,expected_value",
    [
        [ScheduleConstraint.NONE, "None"],
        [ScheduleConstraint.Start, "Start"],
        [ScheduleConstraint.End, "End"],
        [ScheduleConstraint.Both, "Both"],
    ],
)
def test_enum_names(schedule_constraint, expected_value):
    """Test enum names."""
    assert str(schedule_constraint) == expected_value


def test_to_constraint_constraint_is_skipped():
    """ScheduleConstraint.to_constraint() constraint is skipped."""
    with pytest.raises(TypeError) as cm:
        _ = ScheduleConstraint.to_constraint()

    py_error_message = {
        8: "to_constraint() missing 1 required positional argument: 'constraint'",
        9: "to_constraint() missing 1 required positional argument: 'constraint'",
        10: "ScheduleConstraint.to_constraint() missing 1 required positional argument: 'constraint'",
        11: "ScheduleConstraint.to_constraint() missing 1 required positional argument: 'constraint'",
        12: "ScheduleConstraint.to_constraint() missing 1 required positional argument: 'constraint'",
        13: "ScheduleConstraint.to_constraint() missing 1 required positional argument: 'constraint'",
    }[sys.version_info.minor]
    assert str(cm.value) == py_error_message


def test_to_constraint_constraint_is_none():
    """ScheduleConstraint.to_constraint() constraint is None."""
    constraint = ScheduleConstraint.to_constraint(None)
    assert constraint == ScheduleConstraint.NONE


def test_to_constraint_constraint_is_not_a_str():
    """ScheduleConstraint.to_constraint() constraint is not an int or str."""
    with pytest.raises(TypeError) as cm:
        _ = ScheduleConstraint.to_constraint(12334.123)

    assert str(cm.value) == (
        "constraint should be a ScheduleConstraint enum value or an int or a "
        "str, not float: '12334.123'"
    )


def test_to_constraint_constraint_is_not_a_valid_str():
    """ScheduleConstraint.to_constraint() constraint is not a valid str."""
    with pytest.raises(ValueError) as cm:
        _ = ScheduleConstraint.to_constraint("not a valid value")

    assert str(cm.value) == (
        "constraint should be a ScheduleConstraint enum value or one of "
        "['None', 'Start', 'End', 'Both'], not 'not a valid value'"
    )


@pytest.mark.parametrize(
    "constraint_name,constraint",
    [
        # None
        ["None", ScheduleConstraint.NONE],
        ["none", ScheduleConstraint.NONE],
        ["NONE", ScheduleConstraint.NONE],
        ["NoNe", ScheduleConstraint.NONE],
        ["nONe", ScheduleConstraint.NONE],
        [0, ScheduleConstraint.NONE],
        # Start
        ["Start", ScheduleConstraint.Start],
        ["start", ScheduleConstraint.Start],
        ["START", ScheduleConstraint.Start],
        ["StaRt", ScheduleConstraint.Start],
        ["STaRt", ScheduleConstraint.Start],
        ["StARt", ScheduleConstraint.Start],
        [1, ScheduleConstraint.Start],
        # End
        ["End", ScheduleConstraint.End],
        ["end", ScheduleConstraint.End],
        ["END", ScheduleConstraint.End],
        ["eNd", ScheduleConstraint.End],
        ["eND", ScheduleConstraint.End],
        [2, ScheduleConstraint.End],
        # Both
        ["Both", ScheduleConstraint.Both],
        ["both", ScheduleConstraint.Both],
        ["BOTH", ScheduleConstraint.Both],
        ["bOth", ScheduleConstraint.Both],
        ["boTh", ScheduleConstraint.Both],
        ["BotH", ScheduleConstraint.Both],
        ["BOtH", ScheduleConstraint.Both],
        [3, ScheduleConstraint.Both],
    ],
)
def test_schedule_constraint_to_constraint_is_working_properly(
    constraint_name, constraint
):
    """ScheduleConstraint can parse schedule constraint names."""
    assert ScheduleConstraint.to_constraint(constraint_name) == constraint
