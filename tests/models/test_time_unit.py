# -*- coding: utf-8 -*-
"""TimeUnit related tests are here."""
from enum import Enum
import sys

import pytest

from stalker.models.enum import TimeUnit


@pytest.mark.parametrize(
    "unit",
    [
        TimeUnit.Minute,
        TimeUnit.Hour,
        TimeUnit.Day,
        TimeUnit.Week,
        TimeUnit.Month,
        TimeUnit.Year,
    ],
)
def test_it_is_an_enum(unit):
    """TimeUnit is an Enum."""
    assert isinstance(unit, Enum)


@pytest.mark.parametrize(
    "unit,expected_value",
    [
        [TimeUnit.Minute, "min"],
        [TimeUnit.Hour, "h"],
        [TimeUnit.Day, "d"],
        [TimeUnit.Week, "w"],
        [TimeUnit.Month, "m"],
        [TimeUnit.Year, "y"],
    ],
)
def test_enum_values(unit, expected_value):
    """Test enum values."""
    assert unit.value == expected_value


@pytest.mark.parametrize(
    "unit,expected_name",
    [
        [TimeUnit.Minute, "Minute"],
        [TimeUnit.Hour, "Hour"],
        [TimeUnit.Day, "Day"],
        [TimeUnit.Week, "Week"],
        [TimeUnit.Month, "Month"],
        [TimeUnit.Year, "Year"],
    ],
)
def test_enum_names(unit, expected_name):
    """Test enum names."""
    assert unit.name == expected_name


@pytest.mark.parametrize(
    "unit,expected_value",
    [
        [TimeUnit.Minute, "min"],
        [TimeUnit.Hour, "h"],
        [TimeUnit.Day, "d"],
        [TimeUnit.Week, "w"],
        [TimeUnit.Month, "m"],
        [TimeUnit.Year, "y"],
    ],
)
def test_enum_as_str(unit, expected_value):
    """Test enum names."""
    assert str(unit) == expected_value


def test_to_unit_unit_is_skipped():
    """TimeUnit.to_unit() unit is skipped."""
    with pytest.raises(TypeError) as cm:
        _ = TimeUnit.to_unit()

    py_error_message = {
        8: "to_unit() missing 1 required positional argument: 'unit'",
        9: "to_unit() missing 1 required positional argument: 'unit'",
        10: "TimeUnit.to_unit() missing 1 required positional argument: 'unit'",
        11: "TimeUnit.to_unit() missing 1 required positional argument: 'unit'",
        12: "TimeUnit.to_unit() missing 1 required positional argument: 'unit'",
        13: "TimeUnit.to_unit() missing 1 required positional argument: 'unit'",
    }[sys.version_info.minor]
    assert str(cm.value) == py_error_message


def test_to_unit_unit_is_none():
    """TimeUnit.to_unit() unit is None."""
    with pytest.raises(TypeError) as cm:
        _ = TimeUnit.to_unit(None)
    assert str(cm.value) == (
        "unit should be a TimeUnit enum value or one of ['Minute', 'Hour', "
        "'Day', 'Week', 'Month', 'Year', 'min', 'h', 'd', 'w', 'm', 'y'], "
        "not NoneType: 'None'"
    )


def test_to_unit_unit_is_not_a_str():
    """TimeUnit.to_unit() unit is not a str."""
    with pytest.raises(TypeError) as cm:
        _ = TimeUnit.to_unit(12334.123)

    assert str(cm.value) == (
        "unit should be a TimeUnit enum value or one of ['Minute', 'Hour', "
        "'Day', 'Week', 'Month', 'Year', 'min', 'h', 'd', 'w', 'm', 'y'], "
        "not float: '12334.123'"
    )


def test_to_unit_unit_is_not_a_valid_str():
    """TimeUnit.to_unit() unit is not a valid str."""
    with pytest.raises(ValueError) as cm:
        _ = TimeUnit.to_unit("not a valid value")

    assert str(cm.value) == (
        "unit should be a TimeUnit enum value or one of ['Minute', 'Hour', "
        "'Day', 'Week', 'Month', 'Year', 'min', 'h', 'd', 'w', 'm', 'y'], "
        "not 'not a valid value'"
    )


@pytest.mark.parametrize(
    "unit_name,unit",
    [
        # Minute
        ["Min", TimeUnit.Minute],
        ["min", TimeUnit.Minute],
        ["MIN", TimeUnit.Minute],
        ["MiN", TimeUnit.Minute],
        ["mIn", TimeUnit.Minute],
        ["Minute", TimeUnit.Minute],
        ["minute", TimeUnit.Minute],
        ["MINUTE", TimeUnit.Minute],
        ["MiNuTe", TimeUnit.Minute],
        ["mInUtE", TimeUnit.Minute],
        # Hour
        ["H", TimeUnit.Hour],
        ["h", TimeUnit.Hour],
        ["Hour", TimeUnit.Hour],
        ["hour", TimeUnit.Hour],
        ["HOUR", TimeUnit.Hour],
        ["HoUr", TimeUnit.Hour],
        ["hOuR", TimeUnit.Hour],
        # Day
        ["D", TimeUnit.Day],
        ["d", TimeUnit.Day],
        ["Day", TimeUnit.Day],
        ["day", TimeUnit.Day],
        ["DAY", TimeUnit.Day],
        ["DaY", TimeUnit.Day],
        ["dAy", TimeUnit.Day],
        # Week
        ["W", TimeUnit.Week],
        ["w", TimeUnit.Week],
        ["Week", TimeUnit.Week],
        ["week", TimeUnit.Week],
        ["WEEK", TimeUnit.Week],
        ["WeeK", TimeUnit.Week],
        ["wEEk", TimeUnit.Week],
        # Month
        ["M", TimeUnit.Month],
        ["m", TimeUnit.Month],
        ["Month", TimeUnit.Month],
        ["month", TimeUnit.Month],
        ["MONTH", TimeUnit.Month],
        ["MoNtH", TimeUnit.Month],
        ["mOnTh", TimeUnit.Month],
        # Year
        ["Y", TimeUnit.Year],
        ["y", TimeUnit.Year],
        ["Year", TimeUnit.Year],
        ["year", TimeUnit.Year],
        ["YEAR", TimeUnit.Year],
        ["YeAr", TimeUnit.Year],
        ["yEaR", TimeUnit.Year],
    ],
)
def test_schedule_unit_to_unit_is_working_properly(unit_name, unit):
    """TimeUnit can parse schedule unit names."""
    assert TimeUnit.to_unit(unit_name) == unit
