# -*- coding: utf-8 -*-
"""DateRangeMixin class related tests."""
import datetime
import logging
import sys

import pytest

import pytz

from sqlalchemy import Column, ForeignKey, Integer

import stalker
from stalker import DateRangeMixin, SimpleEntity, defaults, log
from stalker.db.session import DBSession
from stalker.models.studio import Studio

logger = log.get_logger(__name__)


class DateRangeMixFooMixedInClass(SimpleEntity, DateRangeMixin):
    """A class which derives from another which has and __init__ already."""

    __tablename__ = "DateRangeMixFooMixedInClasses"
    __mapper_args__ = {"polymorphic_identity": "DateRangeMixFooMixedInClass"}
    schedMixFooMixedInClass_id = Column(
        "id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True
    )

    def __init__(self, **kwargs):
        super(DateRangeMixFooMixedInClass, self).__init__(**kwargs)
        DateRangeMixin.__init__(self, **kwargs)


@pytest.fixture(scope="function")
def date_range_mixin_tester():
    """Fixture for the DateRangeMixin tests.

    Returns:
        dict: Test data.
    """
    # create mock objects
    stalker.defaults.config_values = stalker.defaults.default_config_values.copy()
    stalker.defaults["timing_resolution"] = datetime.timedelta(hours=1)
    data = dict()
    data["start"] = datetime.datetime(2013, 3, 22, 15, 15, tzinfo=pytz.utc)
    data["end"] = data["start"] + datetime.timedelta(days=20)
    data["duration"] = datetime.timedelta(days=10)

    data["kwargs"] = {
        "name": "Test Daterange Mixin",
        "description": "This is a simple entity object for testing " "DateRangeMixin",
        "start": data["start"],
        "end": data["end"],
        "duration": data["duration"],
    }
    data["test_foo_obj"] = DateRangeMixFooMixedInClass(**data["kwargs"])
    yield data
    stalker.defaults.config_values = stalker.defaults.default_config_values.copy()
    stalker.defaults["timing_resolution"] = datetime.timedelta(hours=1)


@pytest.mark.parametrize("test_value", [1, 1.2, "str", ["a", "date"]])
def test_start_argument_is_not_a_date_object(test_value, date_range_mixin_tester):
    """Default values are used if the start attribute is not a datetime object."""
    data = date_range_mixin_tester
    data["kwargs"]["start"] = test_value
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    assert new_foo_obj.start == new_foo_obj.end - new_foo_obj.duration


@pytest.mark.parametrize("test_value", [1, 1.2, "str", ["a", "date"]])
def test_start_attribute_is_not_a_date_object(test_value, date_range_mixin_tester):
    """Default values are used if start attribute is set not datetime object."""
    data = date_range_mixin_tester
    end = data["test_foo_obj"].end
    duration = data["test_foo_obj"].duration
    data["test_foo_obj"].start = test_value
    assert (
        data["test_foo_obj"].start
        == data["test_foo_obj"].end - data["test_foo_obj"].duration
    )
    # check if we still have the same end
    assert data["test_foo_obj"].end == end
    # check if we still have the same duration
    assert data["test_foo_obj"].duration == duration


def test_start_attribute_is_set_to_none_use_the_default_value(date_range_mixin_tester):
    """Setting the start attribute to None will update the start to today."""
    data = date_range_mixin_tester
    data["test_foo_obj"].start = None
    assert data["test_foo_obj"].start == datetime.datetime(
        2013, 3, 22, 15, 00, tzinfo=pytz.utc
    )
    assert isinstance(data["test_foo_obj"].start, datetime.datetime)


def test_start_attribute_works_properly(date_range_mixin_tester):
    """start attribute is working properly."""
    data = date_range_mixin_tester
    test_value = datetime.datetime(2011, 1, 1, tzinfo=pytz.utc)
    data["test_foo_obj"].start = test_value
    assert data["test_foo_obj"].start == test_value


@pytest.mark.parametrize(
    "test_value", [1, 1.2, "str", ["a", "date"], datetime.timedelta(days=100)]
)
def test_end_argument_is_not_a_date_object(test_value, date_range_mixin_tester):
    """Defaults used for the end attribute if due date not a datetime instance."""
    data = date_range_mixin_tester
    data["kwargs"]["end"] = test_value
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    assert new_foo_obj.end == new_foo_obj.start + new_foo_obj.duration


@pytest.mark.parametrize(
    "test_value", [1, 1.2, "str", ["a", "date"], datetime.timedelta(days=100)]
)
def test_end_attribute_is_not_a_date_object(test_value, date_range_mixin_tester):
    """Defaults used for the end attribute if it is not a datetime object."""
    data = date_range_mixin_tester
    data["test_foo_obj"].end = test_value
    assert (
        data["test_foo_obj"].end
        == data["test_foo_obj"].start + data["test_foo_obj"].duration
    )


def test_end_argument_is_tried_to_set_to_a_time_before_start(date_range_mixin_tester):
    """end attribute is updated to start+duration if end arg is a date before start."""
    data = date_range_mixin_tester
    data["kwargs"]["end"] = data["kwargs"]["start"] - datetime.timedelta(days=10)
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    assert new_foo_obj.end == new_foo_obj.start + new_foo_obj.duration


def test_end_attribute_is_tried_to_set_to_a_time_before_start(date_range_mixin_tester):
    """end attribute is updated to start+duration if end is a date before start."""
    data = date_range_mixin_tester
    new_end = data["test_foo_obj"].start - datetime.timedelta(days=10)
    data["test_foo_obj"].end = new_end
    assert (
        data["test_foo_obj"].end
        == data["test_foo_obj"].start + data["test_foo_obj"].duration
    )


def test_end_attribute_is_shifted_if_start_passes_it(date_range_mixin_tester):
    """end attribute is shifted if the start attribute passes it."""
    data = date_range_mixin_tester
    time_delta = data["test_foo_obj"].end - data["test_foo_obj"].start
    data["test_foo_obj"].start += 2 * time_delta
    assert data["test_foo_obj"].end - data["test_foo_obj"].start == time_delta


@pytest.mark.parametrize("test_value", [None, 1, 1.2, "10", "10 days"])
def test_duration_argument_is_not_an_instance_of_timedelta_no_problem_if_start_and_end_is_present(
    test_value, date_range_mixin_tester
):
    """No error raised if duration arg is not a datetime instance if start and end args are present."""
    data = date_range_mixin_tester
    data["kwargs"]["duration"] = test_value
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    assert new_foo_obj.duration == new_foo_obj.end - new_foo_obj.start


@pytest.mark.parametrize("test_value", [1, 1.2, "10", "10 days"])
def test_duration_argument_is_not_an_instance_of_date_if_start_argument_is_missing(
    test_value, date_range_mixin_tester
):
    """defaults.timing_resolution is used if duration arg is not a datetime if start arg is also missing."""
    data = date_range_mixin_tester
    data["kwargs"].pop("start")
    data["kwargs"]["duration"] = test_value
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    assert new_foo_obj.duration == defaults.timing_resolution


@pytest.mark.parametrize("test_value", [1, 1.2, "10", "10 days"])
def test_duration_argument_is_not_an_instance_of_date_if_end_argument_is_missing(
    test_value, date_range_mixin_tester
):
    """defaults.timing_resolution is used if the duration arg is not a datetime and if end arg is also missing."""
    data = date_range_mixin_tester
    defaults["timing_resolution"] = datetime.timedelta(hours=1)
    # some wrong values for the duration
    data["kwargs"].pop("end")
    data["kwargs"]["duration"] = test_value
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    assert new_foo_obj.duration == defaults.timing_resolution


def test_duration_argument_is_smaller_than_timing_resolution(date_range_mixin_tester):
    """defaults.timing_resolution is used for duration if duration arg is smaller than defaults.timing_resolution"""
    data = date_range_mixin_tester
    data["kwargs"].pop("end")
    data["kwargs"]["duration"] = datetime.timedelta(minutes=1)
    obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    assert obj.start == datetime.datetime(2013, 3, 22, 15, 0, tzinfo=pytz.utc)
    assert obj.end == datetime.datetime(2013, 3, 22, 16, 0, tzinfo=pytz.utc)


def test_duration_attribute_is_calculated_correctly(date_range_mixin_tester):
    """duration attribute is calculated correctly."""
    data = date_range_mixin_tester
    new_foo_entity = DateRangeMixFooMixedInClass(**data["kwargs"])
    new_foo_entity.start = datetime.datetime(2013, 3, 22, 15, 0, tzinfo=pytz.utc)
    new_foo_entity.end = new_foo_entity.start + datetime.timedelta(201)
    assert new_foo_entity.duration == datetime.timedelta(201)


@pytest.mark.parametrize("test_value", [None, 1, 1.2, "10", "10 days"])
def test_duration_attribute_is_set_to_not_an_instance_of_timedelta(
    test_value,
    date_range_mixin_tester,
):
    """duration attribute reset to a calculated value if it is not a timedelta."""
    data = date_range_mixin_tester
    # no problem if there are start and end arguments
    data["test_foo_obj"].duration = test_value
    # check the value
    assert (
        data["test_foo_obj"].duration
        == data["test_foo_obj"].end - data["test_foo_obj"].start
    )


def test_duration_attribute_expands_then_end_shifts(date_range_mixin_tester):
    """duration attribute is expanded then the end attribute is shifted."""
    data = date_range_mixin_tester
    _ = data["test_foo_obj"].end
    start = data["test_foo_obj"].start
    duration = data["test_foo_obj"].duration

    # change the duration
    new_duration = duration * 10
    data["test_foo_obj"].duration = new_duration

    # duration expanded
    assert data["test_foo_obj"].duration == new_duration

    # start is not changed
    assert data["test_foo_obj"].start == start

    # end is postponed
    assert data["test_foo_obj"].end == start + new_duration


def test_duration_attribute_contracts_then_end_shifts_back(date_range_mixin_tester):
    """duration attribute is contracted then the end attribute is shifted back."""
    data = date_range_mixin_tester
    _ = data["test_foo_obj"].end
    start = data["test_foo_obj"].start
    duration = data["test_foo_obj"].duration

    # change the duration
    new_duration = duration / 2
    data["test_foo_obj"].duration = new_duration

    # duration expanded
    assert data["test_foo_obj"].duration == new_duration

    # start is not changed
    assert data["test_foo_obj"].start == start

    # end is postponed
    assert data["test_foo_obj"].end == start + new_duration


def test_duration_attribute_is_smaller_then_timing_resolution(date_range_mixin_tester):
    """defaults.timing_resolution is used for the duration if it is smaller than it."""
    data = date_range_mixin_tester
    data["test_foo_obj"].duration = datetime.timedelta(minutes=10)
    assert data["test_foo_obj"].duration == defaults.timing_resolution


def test_duration_is_a_negative_timedelta(date_range_mixin_tester):
    """duration is a negative timedelta will set the duration to 1 days."""
    data = date_range_mixin_tester
    start = data["test_foo_obj"].start
    data["test_foo_obj"].duration = datetime.timedelta(-10)
    assert data["test_foo_obj"].duration == datetime.timedelta(1)
    assert data["test_foo_obj"].start == start


def test_init_all_parameters_skipped(date_range_mixin_tester):
    """Attributes are initialized to the following values.

    start = datetime.datetime.now(pytz.utc)
    duration = stalker.config.Config.timing_resolution
    end = start + duration
    """
    data = date_range_mixin_tester
    # self.fail("test is not implemented yet")
    data["kwargs"].pop("start")
    data["kwargs"].pop("end")
    data["kwargs"].pop("duration")

    new_foo_entity = DateRangeMixFooMixedInClass(**data["kwargs"])

    assert isinstance(new_foo_entity.start, datetime.datetime)
    # cannot check for start, just don't want to struggle with the round
    # thing
    # assert \
    #     new_foo_entity.start == \
    #     datetime.datetime(2013, 3, 22, 15, 30, tzinfo=pytz.utc)
    assert new_foo_entity.duration == defaults.timing_resolution
    assert new_foo_entity.end == new_foo_entity.start + new_foo_entity.duration


def test_init_only_start_argument_is_given(date_range_mixin_tester):
    """Attributes are initialized to the following values.

    duration = defaults.timing_resolution
    end = start + duration
    """
    data = date_range_mixin_tester
    data["kwargs"].pop("end")
    data["kwargs"].pop("duration")
    new_foo_entity = DateRangeMixFooMixedInClass(**data["kwargs"])
    assert new_foo_entity.duration == defaults.timing_resolution
    assert new_foo_entity.end == new_foo_entity.start + new_foo_entity.duration


def test_init_start_and_end_argument_is_given(date_range_mixin_tester):
    """Attributes are initialized to the following values.

    duration = end - start
    """
    data = date_range_mixin_tester
    data["kwargs"].pop("duration")
    new_foo_entity = DateRangeMixFooMixedInClass(**data["kwargs"])
    assert new_foo_entity.duration == new_foo_entity.end - new_foo_entity.start


def test_init_start_and_end_argument_is_given_but_duration_is_smaller_than_timing_resolution(
    date_range_mixin_tester,
):
    """Start is anchored and the end is updated if duration is smaller than timing_resolution.

    duration = end - start
    """
    data = date_range_mixin_tester
    data["kwargs"].pop("duration")
    data["kwargs"]["start"] = datetime.datetime(2013, 12, 22, 23, 8, tzinfo=pytz.utc)
    data["kwargs"]["end"] = datetime.datetime(2013, 12, 22, 23, 15, tzinfo=pytz.utc)
    obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    assert obj.start == datetime.datetime(2013, 12, 22, 23, 0, tzinfo=pytz.utc)
    assert obj.end == datetime.datetime(2013, 12, 23, 0, 0, tzinfo=pytz.utc)


def test_init_start_and_duration_argument_is_given(date_range_mixin_tester):
    """Attributes are initialized to:

    end = start + duration
    """
    data = date_range_mixin_tester
    data["kwargs"].pop("end")
    new_foo_entity = DateRangeMixFooMixedInClass(**data["kwargs"])
    assert new_foo_entity.end == new_foo_entity.start + new_foo_entity.duration


def test_init_all_arguments_are_given(date_range_mixin_tester):
    """Attributes are initialized to:

    duration = end - start
    """
    data = date_range_mixin_tester
    new_foo_entity = DateRangeMixFooMixedInClass(**data["kwargs"])
    assert new_foo_entity.duration == new_foo_entity.end - new_foo_entity.start


def test_init_end_and_duration_argument_is_given(date_range_mixin_tester):
    """Attributes are initialized to:

    start = end - duration
    """
    data = date_range_mixin_tester
    data["kwargs"].pop("start")
    new_foo_entity = DateRangeMixFooMixedInClass(**data["kwargs"])
    assert new_foo_entity.start == new_foo_entity.end - new_foo_entity.duration


def test_init_only_end_argument_is_given(date_range_mixin_tester):
    """Attributes are initialized to:

    duration = defaults.timing_resolution
    start = end - duration
    """
    data = date_range_mixin_tester
    data["kwargs"].pop("duration")
    data["kwargs"].pop("start")
    new_foo_entity = DateRangeMixFooMixedInClass(**data["kwargs"])
    assert new_foo_entity.duration == defaults.timing_resolution
    assert new_foo_entity.start == new_foo_entity.end - new_foo_entity.duration


def test_init_only_duration_argument_is_given(date_range_mixin_tester):
    """Attributes are initialized to:

    start = datetime.datetime.now(pytz.utc)
    end = start + duration
    """
    data = date_range_mixin_tester
    data["kwargs"].pop("end")
    data["kwargs"].pop("start")

    new_foo_entity = DateRangeMixFooMixedInClass(**data["kwargs"])

    # just check if it is an instance of datetime.datetime
    assert isinstance(new_foo_entity.start, datetime.datetime)
    # cannot check for start
    # assert new_foo_entity.start == \
    #        datetime.datetime(2013, 3, 22, 15, 30, tzinfo=pytz.utc
    assert new_foo_entity.end == new_foo_entity.start + new_foo_entity.duration


def test_start_end_and_duration_values_are_rounded_to_the_default_timing_resolution(
    date_range_mixin_tester,
):
    """start and end dates are rounded to the default timing_resolution (no Studio)."""
    data = date_range_mixin_tester
    data["kwargs"]["start"] = datetime.datetime(
        2013, 3, 22, 2, 38, 55, 531, tzinfo=pytz.utc
    )
    data["kwargs"]["end"] = datetime.datetime(
        2013, 3, 24, 16, 46, 32, 102, tzinfo=pytz.utc
    )
    defaults["timing_resolution"] = datetime.timedelta(minutes=5)

    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    # check the start
    expected_start = datetime.datetime(2013, 3, 22, 2, 40, tzinfo=pytz.utc)
    assert new_foo_obj.start == expected_start
    # check the end
    expected_end = datetime.datetime(2013, 3, 24, 16, 45, tzinfo=pytz.utc)
    assert new_foo_obj.end == expected_end
    # check the duration
    assert new_foo_obj.duration == expected_end - expected_start


def test_computed_start_is_none_for_a_non_scheduled_class(date_range_mixin_tester):
    """computed_start attribute is None for a non-scheduled class."""
    data = date_range_mixin_tester
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    assert new_foo_obj.computed_start is None


def test_computed_end_is_none_for_a_non_scheduled_class(date_range_mixin_tester):
    """computed_end attribute is None for a non-scheduled class."""
    data = date_range_mixin_tester
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    assert new_foo_obj.computed_end is None


def test_computed_duration_attribute_is_none_if_there_is_no_computed_start_and_no_computed_end(
    date_range_mixin_tester,
):
    """computed_start attr is None if there is no computed_start and no computed_end."""
    data = date_range_mixin_tester
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    new_foo_obj.computed_start = None
    new_foo_obj.computed_end = None
    assert new_foo_obj.computed_duration is None


def test_computed_duration_attribute_is_none_if_there_is_computed_start_but_no_computed_end(
    date_range_mixin_tester,
):
    """computed_start attr is None if there is computed_start but no computed_end."""
    data = date_range_mixin_tester
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    new_foo_obj.computed_start = datetime.datetime.now(pytz.utc)
    new_foo_obj.computed_end = None
    assert new_foo_obj.computed_duration is None


def test_computed_duration_attribute_is_none_if_there_is_no_computed_start_but_computed_end(
    date_range_mixin_tester,
):
    """computed_start attr is None if there is no computed_start but computed_end."""
    data = date_range_mixin_tester
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    new_foo_obj.computed_start = None
    new_foo_obj.computed_end = datetime.datetime.now(pytz.utc)
    assert new_foo_obj.computed_duration is None


def test_computed_duration_attribute_is_calculated_correctly_if_there_are_both_computed_start_and_computed_end(
    date_range_mixin_tester,
):
    """computed_duration is calculated correctly if both computed_start and computed_end given."""
    data = date_range_mixin_tester
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    new_foo_obj.computed_start = datetime.datetime.now(pytz.utc)
    new_foo_obj.computed_end = new_foo_obj.computed_start + datetime.timedelta(12)
    assert new_foo_obj.computed_duration == datetime.timedelta(12)


def test_computed_duration_is_read_only(date_range_mixin_tester):
    """computed_duration attribute is read-only."""
    data = date_range_mixin_tester
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    with pytest.raises(AttributeError) as cm:
        new_foo_obj.computed_duration = datetime.timedelta(10)

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'computed_duration'",
    }.get(
        sys.version_info.minor,
        "property 'computed_duration' of 'DateRangeMixFooMixedInClass' "
        "object has no setter"
    )

    assert str(cm.value) == error_message


def test_total_seconds_attribute_is_read_only(date_range_mixin_tester):
    """total_seconds is read only."""
    data = date_range_mixin_tester
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    with pytest.raises(AttributeError) as cm:
        new_foo_obj.total_seconds = 234234

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'total_seconds'",
    }.get(
        sys.version_info.minor,
        "property 'total_seconds' of 'DateRangeMixFooMixedInClass' "
        "object has no setter"
    )

    assert str(cm.value) == error_message


def test_total_seconds_attribute_is_working_properly(date_range_mixin_tester):
    """total_seconds is read only."""
    data = date_range_mixin_tester
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    new_foo_obj.start = datetime.datetime(2013, 5, 31, 10, 0, tzinfo=pytz.utc)
    new_foo_obj.end = datetime.datetime(2013, 5, 31, 18, 0, tzinfo=pytz.utc)
    assert new_foo_obj.total_seconds == 8 * 60 * 60


def test_computed_total_seconds_attribute_is_read_only(date_range_mixin_tester):
    """computed_total_seconds is read only."""
    data = date_range_mixin_tester
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    with pytest.raises(AttributeError) as cm:
        new_foo_obj.computed_total_seconds = 234234

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'computed_total_seconds'",
    }.get(
        sys.version_info.minor,
        "property 'computed_total_seconds' of 'DateRangeMixFooMixedInClass' "
        "object has no setter"
    )

    assert str(cm.value) == error_message


def test_computed_total_seconds_attribute_is_working_properly(date_range_mixin_tester):
    """computed_total_seconds is read only."""
    data = date_range_mixin_tester
    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    new_foo_obj.computed_start = datetime.datetime(2013, 5, 31, 10, 0, tzinfo=pytz.utc)
    new_foo_obj.computed_end = datetime.datetime(2013, 5, 31, 18, 0, tzinfo=pytz.utc)
    assert new_foo_obj.computed_total_seconds == 8 * 60 * 60


@pytest.fixture(scope="function")
def setup_date_range_mixin_db(setup_postgresql_db):
    """Set up the tests that needs a database.

    Returns:
        dict: Test data.
    """
    data = setup_postgresql_db

    # create mock objects
    data["start"] = datetime.datetime(2013, 3, 22, 15, 15, tzinfo=pytz.utc)
    data["end"] = data["start"] + datetime.timedelta(days=20)
    data["duration"] = datetime.timedelta(days=10)

    data["kwargs"] = {
        "name": "Test Daterange Mixin",
        "description": "This is a simple entity object for testing " "DateRangeMixin",
        "start": data["start"],
        "end": data["end"],
        "duration": data["duration"],
    }
    data["test_foo_obj"] = DateRangeMixFooMixedInClass(**data["kwargs"])
    return data


def test_start_end_and_duration_values_are_rounded_to_the_studio_timing_resolution(
    setup_date_range_mixin_db,
):
    """start and end dates are rounded to the Studio timing_resolution."""
    data = setup_date_range_mixin_db
    log.set_level(logging.DEBUG)
    studio = Studio.query.first()
    if not studio:
        logger.debug("No studio found! Creating one!")
        studio = Studio(
            name="Test Studio", timing_resolution=datetime.timedelta(minutes=5)
        )
        DBSession.add(studio)
        DBSession.commit()
    else:
        logger.debug("A studio found! Updating timing resolution!")
        studio.timing_resolution = datetime.timedelta(minutes=5)
        studio.update_defaults()

    data["kwargs"]["start"] = datetime.datetime(
        2013, 3, 22, 2, 38, 55, 531, tzinfo=pytz.utc
    )
    data["kwargs"]["end"] = datetime.datetime(
        2013, 3, 24, 16, 46, 32, 102, tzinfo=pytz.utc
    )

    new_foo_obj = DateRangeMixFooMixedInClass(**data["kwargs"])
    # check the start
    expected_start = datetime.datetime(2013, 3, 22, 2, 40, tzinfo=pytz.utc)
    assert new_foo_obj.start == expected_start
    # check the end
    expected_end = datetime.datetime(2013, 3, 24, 16, 45, tzinfo=pytz.utc)
    assert new_foo_obj.end == expected_end
    # check the duration
    assert new_foo_obj.duration == expected_end - expected_start
