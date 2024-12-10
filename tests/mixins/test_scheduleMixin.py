# -*- coding: utf-8 -*-
"""ScheduleMixin related tests."""
import datetime

import pytest

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

import stalker
from stalker import ScheduleMixin, SimpleEntity, defaults
from stalker.models.mixins import TimeUnit


class MixedInClass(SimpleEntity, ScheduleMixin):
    """class derived from SimpleEntity and mixed in with ScheduleMixin for testing."""

    __tablename__ = "ScheduleMixFooMixedInClasses"
    __mapper_args__ = {"polymorphic_identity": "ScheduleMixFooMixedInClass"}
    schedMixFooMixedInClass_id: Mapped[int] = mapped_column(
        "id", ForeignKey("SimpleEntities.id"), primary_key=True
    )

    def __init__(self, **kwargs):
        SimpleEntity.__init__(self, **kwargs)
        ScheduleMixin.__init__(self, **kwargs)


@pytest.fixture(scope="function")
def setup_schedule_mixin_tests():
    """Set up the tests for the ScheduleMixin.

    Yields:
        dict: Test data.
    """
    stalker.defaults.config_values = stalker.defaults.default_config_values.copy()
    stalker.defaults["timing_resolution"] = datetime.timedelta(hours=1)
    data = dict()
    data["kwargs"] = {
        "name": "Test Object",
        "schedule_timing": 1,
        "schedule_unit": TimeUnit.Hour,
        "schedule_model": "effort",
        "schedule_constraint": 0,
    }
    data["test_obj"] = MixedInClass(**data["kwargs"])
    yield data
    stalker.defaults.config_values = stalker.defaults.default_config_values.copy()
    stalker.defaults["timing_resolution"] = datetime.timedelta(hours=1)


def test_schedule_model_attribute_is_effort_by_default(setup_schedule_mixin_tests):
    """schedule_model is effort by default."""
    data = setup_schedule_mixin_tests
    assert data["test_obj"].schedule_model == "effort"


def test_schedule_model_argument_is_none(setup_schedule_mixin_tests):
    """schedule model is 'effort' if the schedule_model argument is set to None."""
    data = setup_schedule_mixin_tests
    data["kwargs"]["schedule_model"] = None
    new_task = MixedInClass(**data["kwargs"])
    assert new_task.schedule_model == "effort"


def test_schedule_model_attribute_is_set_to_none(setup_schedule_mixin_tests):
    """schedule_model will be 'effort' if it is set to None."""
    data = setup_schedule_mixin_tests
    data["test_obj"].schedule_model = None
    assert data["test_obj"].schedule_model == "effort"


def test_schedule_model_argument_is_not_a_string(setup_schedule_mixin_tests):
    """TypeError is raised if the schedule_model argument is not a string."""
    data = setup_schedule_mixin_tests
    data["kwargs"]["schedule_model"] = 234
    with pytest.raises(TypeError) as cm:
        MixedInClass(**data["kwargs"])

    assert str(cm.value) == (
        "MixedInClass.schedule_model should be one of ['effort', 'length', "
        "'duration'], not int: '234'"
    )


def test_schedule_model_attribute_is_not_a_string(setup_schedule_mixin_tests):
    """TypeError is raised if the schedule_model attribute is not a string."""
    data = setup_schedule_mixin_tests
    with pytest.raises(TypeError) as cm:
        data["test_obj"].schedule_model = 2343

    assert str(cm.value) == (
        "MixedInClass.schedule_model should be one of ['effort', 'length', "
        "'duration'], not int: '2343'"
    )


def test_schedule_model_argument_is_not_in_correct_value(setup_schedule_mixin_tests):
    """ValueError is raised if the schedule_model argument is not valid."""
    data = setup_schedule_mixin_tests
    data["kwargs"]["schedule_model"] = "not in the list"
    with pytest.raises(ValueError) as cm:
        MixedInClass(**data["kwargs"])

    assert str(cm.value) == (
        "MixedInClass.schedule_model should be one of ['effort', 'length', "
        "'duration'], not str: 'not in the list'"
    )


def test_schedule_model_attribute_is_not_in_correct_value(setup_schedule_mixin_tests):
    """ValueError is raised if the schedule_model attribute is not valid."""
    data = setup_schedule_mixin_tests
    with pytest.raises(ValueError) as cm:
        data["test_obj"].schedule_model = "not in the list"

    assert str(cm.value) == (
        "MixedInClass.schedule_model should be one of ['effort', 'length', "
        "'duration'], not str: 'not in the list'"
    )


def test_schedule_model_argument_is_working_as_expected(setup_schedule_mixin_tests):
    """schedule_model arg is passed to the schedule_model attribute."""
    data = setup_schedule_mixin_tests
    test_value = "duration"
    data["kwargs"]["schedule_model"] = test_value
    new_task = MixedInClass(**data["kwargs"])
    assert new_task.schedule_model == test_value


def test_schedule_model_attribute_is_working_as_expected(setup_schedule_mixin_tests):
    """schedule_model attribute is working as expected."""
    data = setup_schedule_mixin_tests
    test_value = "duration"
    assert data["test_obj"].schedule_model != test_value
    data["test_obj"].schedule_model = test_value
    assert data["test_obj"].schedule_model == test_value


def test_schedule_constraint_is_0_by_default(setup_schedule_mixin_tests):
    """schedule_constraint attribute is None by default."""
    data = setup_schedule_mixin_tests
    assert data["test_obj"].schedule_constraint == 0


def test_schedule_constraint_argument_is_skipped(setup_schedule_mixin_tests):
    """schedule_constraint attribute is 0 if schedule_constraint is skipped."""
    data = setup_schedule_mixin_tests
    try:
        data["kwargs"].pop("schedule_constraint")
    except KeyError:
        pass
    new_task = MixedInClass(**data["kwargs"])
    assert new_task.schedule_constraint == 0


def test_schedule_constraint_argument_is_none(setup_schedule_mixin_tests):
    """schedule_constraint attribute will be 0 if schedule_constraint is None."""
    data = setup_schedule_mixin_tests
    data["kwargs"]["schedule_constraint"] = None
    new_task = MixedInClass(**data["kwargs"])
    assert new_task.schedule_constraint == 0


def test_schedule_constraint_attribute_is_set_to_none(setup_schedule_mixin_tests):
    """schedule_constraint attribute will be 0 if it is set to None."""
    data = setup_schedule_mixin_tests
    data["test_obj"].schedule_constraint = None
    assert data["test_obj"].schedule_constraint == 0


def test_schedule_constraint_argument_is_not_an_integer(setup_schedule_mixin_tests):
    """TypeError is raised if the schedule_constraint argument is not an int."""
    data = setup_schedule_mixin_tests
    data["kwargs"]["schedule_constraint"] = "not an int"
    with pytest.raises(ValueError) as cm:
        MixedInClass(**data["kwargs"])

    assert str(cm.value) == (
        "constraint should be a ScheduleConstraint enum value or one of "
        "['None', 'Start', 'End', 'Both'], not 'not an int'"
    )


def test_schedule_constraint_attribute_is_not_an_integer(setup_schedule_mixin_tests):
    """TypeError is raised if the schedule_constraint attribute is not an int."""
    data = setup_schedule_mixin_tests
    with pytest.raises(ValueError) as cm:
        data["test_obj"].schedule_constraint = "not an int"

    assert str(cm.value) == (
        "constraint should be a ScheduleConstraint enum value or one of "
        "['None', 'Start', 'End', 'Both'], not 'not an int'"
    )


def test_schedule_constraint_argument_is_working_as_expected(
    setup_schedule_mixin_tests,
):
    """schedule_constraint arg value is passed to schedule_constraint attribute."""
    data = setup_schedule_mixin_tests
    test_value = 2
    data["kwargs"]["schedule_constraint"] = test_value
    new_task = MixedInClass(**data["kwargs"])
    assert new_task.schedule_constraint == test_value


def test_schedule_constraint_attribute_is_working_as_expected(
    setup_schedule_mixin_tests,
):
    """schedule_constraint attribute value is correctly changed."""
    data = setup_schedule_mixin_tests
    test_value = 3
    data["test_obj"].schedule_constraint = test_value
    assert data["test_obj"].schedule_constraint == test_value


@pytest.mark.parametrize("test_value", [-1, 4])
def test_schedule_constraint_argument_value_is_out_of_range(
    setup_schedule_mixin_tests,
    test_value,
):
    """schedule_constraint is clamped to the [0-3] range if it is out of range."""
    data = setup_schedule_mixin_tests
    data["kwargs"]["schedule_constraint"] = test_value
    with pytest.raises(ValueError) as cm:
        _ = MixedInClass(**data["kwargs"])
    assert str(cm.value) == (f"{test_value} is not a valid ScheduleConstraint")


@pytest.mark.parametrize("test_value", [-1, 4])
def test_schedule_constraint_attribute_value_is_out_of_range(
    setup_schedule_mixin_tests,
    test_value,
):
    """schedule_constraint is clamped to the [0-3] range if it is out of range."""
    data = setup_schedule_mixin_tests
    with pytest.raises(ValueError) as cm:
        data["test_obj"].schedule_constraint = test_value

    assert str(cm.value) == (f"{test_value} is not a valid ScheduleConstraint")


def test_schedule_timing_argument_skipped(setup_schedule_mixin_tests):
    """schedule_timing is equal to 1h if the schedule_timing arg is skipped."""
    data = setup_schedule_mixin_tests
    data["kwargs"].pop("schedule_timing")
    new_task = MixedInClass(**data["kwargs"])

    assert new_task.schedule_timing == MixedInClass.__default_schedule_timing__


def test_schedule_timing_argument_is_none(setup_schedule_mixin_tests):
    """schedule_timing==Config.timing_resolution.seconds/60 if the schedule_timing arg is None."""
    data = setup_schedule_mixin_tests
    defaults["timing_resolution"] = datetime.timedelta(hours=1)
    data["kwargs"]["schedule_timing"] = None
    new_task = MixedInClass(**data["kwargs"])
    assert new_task.schedule_timing == defaults.timing_resolution.seconds / 60.0


def test_schedule_timing_attribute_is_set_to_none(setup_schedule_mixin_tests):
    """schedule_timing==Config.timing_resolution.seconds/60 if it is set to None."""
    data = setup_schedule_mixin_tests
    defaults["timing_resolution"] = datetime.timedelta(hours=1)
    data["test_obj"].schedule_timing = None
    assert data["test_obj"].schedule_timing == defaults.timing_resolution.seconds / 60.0


def test_schedule_timing_argument_is_not_an_integer_or_float(
    setup_schedule_mixin_tests,
):
    """TypeError is raised if the schedule_timing is not an int or float."""
    data = setup_schedule_mixin_tests
    data["kwargs"]["schedule_timing"] = "10d"
    with pytest.raises(TypeError) as cm:
        MixedInClass(**data["kwargs"])

    assert str(cm.value) == (
        "MixedInClass.schedule_timing should be an integer or float number showing the "
        "value of the schedule timing of this MixedInClass, not str: '10d'"
    )


def test_schedule_timing_attribute_is_not_an_int_or_float(
    setup_schedule_mixin_tests,
):
    """TypeError is raised if the schedule_timing attribute is not int or float."""
    data = setup_schedule_mixin_tests
    with pytest.raises(TypeError) as cm:
        data["test_obj"].schedule_timing = "10d"

    assert str(cm.value) == (
        "MixedInClass.schedule_timing should be an integer or float number showing the "
        "value of the schedule timing of this MixedInClass, not str: '10d'"
    )


def test_schedule_timing_attribute_is_working_as_expected(setup_schedule_mixin_tests):
    """schedule_timing attribute is working as expected."""
    data = setup_schedule_mixin_tests
    test_value = 18
    data["test_obj"].schedule_timing = test_value
    assert data["test_obj"].schedule_timing == test_value


def test_schedule_unit_argument_skipped(setup_schedule_mixin_tests):
    """schedule_unit attribute defaults if schedule_unit argument is skipped."""
    data = setup_schedule_mixin_tests
    data["kwargs"].pop("schedule_unit")
    new_task = MixedInClass(**data["kwargs"])
    assert new_task.schedule_unit == MixedInClass.__default_schedule_unit__


def test_schedule_unit_argument_is_none(setup_schedule_mixin_tests):
    """schedule_unit attribute defaults if the schedule_unit argument is None."""
    data = setup_schedule_mixin_tests
    data["kwargs"]["schedule_unit"] = None
    new_task = MixedInClass(**data["kwargs"])
    assert new_task.schedule_unit == MixedInClass.__default_schedule_unit__


def test_schedule_unit_attribute_is_set_to_none(setup_schedule_mixin_tests):
    """schedule_unit attribute will use the default value if it is set to None."""
    data = setup_schedule_mixin_tests
    data["test_obj"].schedule_unit = None
    assert data["test_obj"].schedule_unit == MixedInClass.__default_schedule_unit__


def test_schedule_unit_argument_is_not_a_string(setup_schedule_mixin_tests):
    """TypeError will be raised if the schedule_unit is not an int."""
    data = setup_schedule_mixin_tests
    data["kwargs"]["schedule_unit"] = 10
    with pytest.raises(TypeError) as cm:
        MixedInClass(**data["kwargs"])
    assert str(cm.value) == (
        "unit should be a TimeUnit enum value or one of ['Minute', 'Hour', "
        "'Day', 'Week', 'Month', 'Year', 'min', 'h', 'd', 'w', 'm', 'y'], "
        "not int: '10'"
    )


def test_schedule_unit_attribute_is_not_a_string(setup_schedule_mixin_tests):
    """TypeError is raised if schedule_unit attribute is not set to a string."""
    data = setup_schedule_mixin_tests
    with pytest.raises(TypeError) as cm:
        data["test_obj"].schedule_unit = 23
    assert str(cm.value) == (
        "unit should be a TimeUnit enum value or one of ['Minute', 'Hour', "
        "'Day', 'Week', 'Month', 'Year', 'min', 'h', 'd', 'w', 'm', 'y'], "
        "not int: '23'"
    )


def test_schedule_unit_attribute_is_working_as_expected(setup_schedule_mixin_tests):
    """schedule_unit attribute is working as expected."""
    data = setup_schedule_mixin_tests
    test_value = TimeUnit.Week
    data["test_obj"].schedule_unit = test_value
    assert data["test_obj"].schedule_unit == test_value


def test_schedule_unit_argument_value_is_not_in_defaults_datetime_units(
    setup_schedule_mixin_tests,
):
    """ValueError is raised if the schedule_unit is not in datetime_units list."""
    data = setup_schedule_mixin_tests
    data["kwargs"]["schedule_unit"] = "os"
    with pytest.raises(ValueError) as cm:
        MixedInClass(**data["kwargs"])

    assert str(cm.value) == (
        "unit should be a TimeUnit enum value or one of ['Minute', 'Hour', "
        "'Day', 'Week', 'Month', 'Year', 'min', 'h', 'd', 'w', 'm', 'y'], "
        "not 'os'"
    )


def test_schedule_unit_attribute_value_is_not_in_defaults_datetime_units(
    setup_schedule_mixin_tests,
):
    """ValueError is raised if schedule_unit not in datetime_units."""
    data = setup_schedule_mixin_tests
    with pytest.raises(ValueError) as cm:
        data["test_obj"].schedule_unit = "so"

    assert str(cm.value) == (
        "unit should be a TimeUnit enum value or one of ['Minute', 'Hour', "
        "'Day', 'Week', 'Month', 'Year', 'min', 'h', 'd', 'w', 'm', 'y'], "
        "not 'so'"
    )


@pytest.mark.parametrize(
    "input_value,expected_result",
    [
        [[60, True], (1, TimeUnit.Minute)],
        [[125, True], (2, TimeUnit.Minute)],
        [[1800, True], (30, TimeUnit.Minute)],
        [[3600, True], (1, TimeUnit.Hour)],
        [[5400, True], (90, TimeUnit.Minute)],
        [[6000, True], (100, TimeUnit.Minute)],
        [[7200, True], (2, TimeUnit.Hour)],
        [[9600, True], (160, TimeUnit.Minute)],
        [[10000, True], (166, TimeUnit.Minute)],
        [[12000, True], (200, TimeUnit.Minute)],
        [[14400, True], (4, TimeUnit.Hour)],
        [[15000, True], (250, TimeUnit.Minute)],
        [[18000, True], (5, TimeUnit.Hour)],
        [[32400, True], (1, TimeUnit.Day)],
        [[32400, False], (9, TimeUnit.Hour)],
        [[64800, True], (2, TimeUnit.Day)],
        [[64800, False], (18, TimeUnit.Hour)],
        [[86400, True], (24, TimeUnit.Hour)],
        [[86400, False], (1, TimeUnit.Day)],
        [[162000, True], (1, TimeUnit.Week)],
        [[162000, False], (45, TimeUnit.Hour)],
        [[604800, False], (1, TimeUnit.Week)],
        [[648000, True], (1, TimeUnit.Month)],
        [[648000, False], (180, TimeUnit.Hour)],
        [[8424000, True], (1, TimeUnit.Year)],
        [[8424000, False], (2340, TimeUnit.Hour)],
        [[2419200, False], (1, TimeUnit.Month)],
        [[31536000, False], (1, TimeUnit.Year)],
    ],
)
def test_least_meaningful_time_unit_is_working_as_expected(
    input_value, expected_result, setup_schedule_mixin_tests
):
    """least_meaningful_time_unit is working as expected."""
    data = setup_schedule_mixin_tests

    defaults["daily_working_hours"] = 9
    defaults["weekly_working_days"] = 5
    defaults["weekly_working_hours"] = 45
    defaults["yearly_working_days"] = 52.1428 * 5

    assert expected_result == data["test_obj"].least_meaningful_time_unit(*input_value)


@pytest.mark.parametrize(
    "schedule_model,schedule_timing,schedule_unit,expected_value",
    [
        # effort values
        ["effort", 1, "min", 60],
        ["effort", 1, "h", 3600],
        ["effort", 1, "d", 32400],
        ["effort", 1, "w", 162000],
        ["effort", 1, "m", 648000],
        ["effort", 1, "y", 8424000],
        ["effort", 1, TimeUnit.Minute, 60],
        ["effort", 1, TimeUnit.Hour, 3600],
        ["effort", 1, TimeUnit.Day, 32400],
        ["effort", 1, TimeUnit.Week, 162000],
        ["effort", 1, TimeUnit.Month, 648000],
        ["effort", 1, TimeUnit.Year, 8424000],
        # length values
        ["length", 1, "min", 60],
        ["length", 1, "h", 3600],
        ["length", 1, "d", 32400],
        ["length", 1, "w", 162000],
        ["length", 1, "m", 648000],
        ["length", 1, "y", 8424000],
        ["length", 1, TimeUnit.Minute, 60],
        ["length", 1, TimeUnit.Hour, 3600],
        ["length", 1, TimeUnit.Day, 32400],
        ["length", 1, TimeUnit.Week, 162000],
        ["length", 1, TimeUnit.Month, 648000],
        ["length", 1, TimeUnit.Year, 8424000],
        # duration values
        ["duration", 1, "min", 60],
        ["duration", 1, "h", 3600],
        ["duration", 1, "d", 86400],
        ["duration", 1, "w", 604800],
        ["duration", 1, "m", 2419200],
        ["duration", 1, "y", 31536000],
        ["duration", 1, TimeUnit.Minute, 60],
        ["duration", 1, TimeUnit.Hour, 3600],
        ["duration", 1, TimeUnit.Day, 86400],
        ["duration", 1, TimeUnit.Week, 604800],
        ["duration", 1, TimeUnit.Month, 2419200],
        ["duration", 1, TimeUnit.Year, 31536000],
    ],
)
def test_to_seconds_is_working_as_expected(
    schedule_model,
    schedule_timing,
    schedule_unit,
    expected_value,
    setup_schedule_mixin_tests,
):
    """to_seconds method is working as expected."""
    data = setup_schedule_mixin_tests

    defaults["daily_working_hours"] = 9
    defaults["weekly_working_days"] = 5
    defaults["weekly_working_hours"] = 45
    defaults["yearly_working_days"] = 52.1428 * 5

    data["test_obj"].schedule_model = schedule_model
    data["test_obj"].schedule_timing = schedule_timing
    data["test_obj"].schedule_unit = schedule_unit
    assert expected_value == data["test_obj"].to_seconds(
        data["test_obj"].schedule_timing,
        data["test_obj"].schedule_unit,
        data["test_obj"].schedule_model,
    )


def test_to_unit_unit_is_none(setup_schedule_mixin_tests):
    """to_unit method is working as expected."""
    data = setup_schedule_mixin_tests

    defaults["daily_working_hours"] = 9
    defaults["weekly_working_days"] = 5
    defaults["weekly_working_hours"] = 45
    defaults["yearly_working_days"] = 52.1428 * 5

    assert data["test_obj"].to_unit(10, None, "effort") is None


@pytest.mark.parametrize(
    "schedule_model,schedule_timing,schedule_unit,seconds",
    [
        # effort values
        ["effort", 1, "min", 60],
        ["effort", 10, "min", 600],
        ["effort", 20, "min", 1200],
        ["effort", 1, "h", 3600],
        ["effort", 1.01, "h", 3636],
        ["effort", 2, "h", 7200],
        ["effort", 1, "d", 32400],
        ["effort", 1, "w", 162000],
        ["effort", 1, "m", 648000],
        ["effort", 1, "y", 8424000],
        # length values
        ["length", 1, "min", 60],
        ["length", 540, "min", 32400],
        ["length", 1, "h", 3600],
        ["length", 1, "d", 32400],
        ["length", 1, "w", 162000],
        ["length", 1, "m", 648000],
        ["length", 1, "y", 8424000],
        # duration values
        ["duration", 1, "min", 60],
        ["duration", 60, "min", 3600],
        ["duration", 1440, "min", 86400],
        ["duration", 1, "h", 3600],
        ["duration", 1.5, "h", 5400],
        ["duration", 2, "h", 7200],
        ["duration", 1, "d", 86400],
        ["duration", 1, "w", 604800],
        ["duration", 1, "m", 2419200],
        ["duration", 1, "y", 31536000],
    ],
)
def test_to_unit_is_working_as_expected(
    schedule_model, schedule_timing, schedule_unit, seconds, setup_schedule_mixin_tests
):
    """to_unit method is working as expected."""
    data = setup_schedule_mixin_tests

    defaults["daily_working_hours"] = 9
    defaults["weekly_working_days"] = 5
    defaults["weekly_working_hours"] = 45
    defaults["yearly_working_days"] = 52.1428 * 5

    assert schedule_timing == data["test_obj"].to_unit(
        seconds, schedule_unit, schedule_model
    )


@pytest.mark.parametrize(
    "schedule_model,schedule_timing,schedule_unit,expected_value",
    [
        # effort values
        ["effort", 1, "min", 60],
        ["effort", 1, "h", 3600],
        ["effort", 1, "d", 32400],
        ["effort", 1, "w", 162000],
        ["effort", 1, "m", 648000],
        ["effort", 1, "y", 8424000],
        # length values
        ["length", 1, "min", 60],
        ["length", 1, "h", 3600],
        ["length", 1, "d", 32400],
        ["length", 1, "w", 162000],
        ["length", 1, "m", 648000],
        ["length", 1, "y", 8424000],
        # duration values
        ["duration", 1, "min", 60],
        ["duration", 1, "h", 3600],
        ["duration", 1, "d", 86400],
        ["duration", 1, "w", 604800],
        ["duration", 1, "m", 2419200],
        ["duration", 1, "y", 31536000],
    ],
)
def test_schedule_seconds_is_working_as_expected(
    schedule_model,
    schedule_timing,
    schedule_unit,
    expected_value,
    setup_schedule_mixin_tests,
):
    """schedule_seconds property is working as expected."""
    data = setup_schedule_mixin_tests

    defaults["daily_working_hours"] = 9
    defaults["weekly_working_days"] = 5
    defaults["weekly_working_hours"] = 45
    defaults["yearly_working_days"] = 52.1428 * 5

    data["test_obj"].schedule_model = schedule_model
    data["test_obj"].schedule_timing = schedule_timing
    data["test_obj"].schedule_unit = schedule_unit
    assert expected_value == data["test_obj"].schedule_seconds
