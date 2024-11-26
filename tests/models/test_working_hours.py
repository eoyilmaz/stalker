# -*- coding: utf-8 -*-
"""Tests related to the WorkingHours class."""
import copy
import datetime
import sys

import pytest

import pytz

from stalker import defaults
from stalker.models.studio import WorkingHours


def test___auto_name___is_true():
    """WorkingHours.__auto_name__ is True"""
    assert WorkingHours.__auto_name__ is True


def test_working_hours_argument_is_skipped():
    """WorkingHours is created with the default settings by default."""
    wh = WorkingHours()
    assert wh.working_hours == defaults.working_hours


def test_working_hours_argument_is_none():
    """WorkingHours created with default settings if the working_hours arg is None."""
    wh = WorkingHours(working_hours=None)
    assert wh.working_hours == defaults.working_hours


def test_working_hours_argument_is_not_a_dictionary():
    """TypeError is raised if the working_hours argument value is not a dictionary."""
    with pytest.raises(TypeError) as cm:
        WorkingHours(working_hours="not a dictionary of proper values")

    assert str(cm.value) == (
        "WorkingHours.working_hours should be a dictionary, "
        "not str: 'not a dictionary of proper values'"
    )


def test_working_hours_attribute_is_not_a_dictionary():
    """TypeError raised if the working_hours attr is not a dictionary."""
    wh = WorkingHours()
    with pytest.raises(TypeError) as cm:
        wh.working_hours = "not a dictionary of proper values"

    assert str(cm.value) == (
        "WorkingHours.working_hours should be a dictionary, "
        "not str: 'not a dictionary of proper values'"
    )


def test_working_hours_argument_value_is_dictionary_of_other_formatted_data():
    """TypeError raised if the working_hours arg is not a dict of list of two int."""
    with pytest.raises(TypeError) as cm:
        WorkingHours(working_hours={"not": "properly valued"})

    assert str(cm.value) == (
        "WorkingHours.working_hours should be a dictionary with keys "
        '"mon, tue, wed, thu, fri, sat, sun" and the values should a list '
        "of lists of two integers like [[540, 720], [800, 1080]], "
        "not str: 'properly valued'"
    )


def test_working_hours_attribute_is_set_to_a_dictionary_of_other_formatted_data():
    """TypeError raised if the working hours attr is a dict of some other value."""
    wh = WorkingHours()
    with pytest.raises(TypeError) as cm:
        wh.working_hours = {"not": "properly valued"}

    assert (
        str(cm.value) == "WorkingHours.working_hours should be a dictionary with keys "
        '"mon, tue, wed, thu, fri, sat, sun" and the values should a '
        "list of lists of two integers like [[540, 720], [800, 1080]], "
        "not str: 'properly valued'"
    )


@pytest.mark.parametrize(
    "test_key, test_value",
    [
        ["sun", [[-10, 1000]]],
        ["sat", [[900, 1080], [1090, 1500]]],
    ],
)
def test_working_hours_argument_data_is_not_in_correct_range1(test_key, test_value):
    """ValueError raised if the time values are not correct in the working_hours arg."""
    wh = copy.copy(defaults.working_hours)
    wh[test_key] = test_value
    with pytest.raises(ValueError) as cm:
        WorkingHours(working_hours=wh)

    assert str(cm.value) == (
        "WorkingHours.working_hours value should be a list of lists of "
        "two integers and the range of integers should be between 0-1440, "
        f"not list: '{test_value}'"
    )


@pytest.mark.parametrize(
    "test_key, test_value",
    [
        ["sun", [[-10, 1000]]],
        ["sat", [[900, 1080], [1090, 1500]]],
    ],
)
def test_working_hours_attribute_data_is_not_in_correct_range1(test_key, test_value):
    """ValueError raised if the times are not correct in the working_hours attr."""
    wh = copy.copy(defaults.working_hours)
    wh[test_key] = test_value

    wh_ins = WorkingHours()
    with pytest.raises(ValueError) as cm:
        wh_ins.working_hours = wh

    assert str(cm.value) == (
        "WorkingHours.working_hours value should be a list of lists of "
        "two integers and the range of integers should be between 0-1440, "
        f"not list: '{test_value}'"
    )


def test_working_hours_argument_value_is_not_complete():
    """default values are used for missing days in the given working_hours arg."""
    working_hours = {"sat": [[900, 1080]], "sun": [[900, 1080]]}
    wh = WorkingHours(working_hours=working_hours)
    assert wh["mon"] == defaults.working_hours["mon"]
    assert wh["tue"] == defaults.working_hours["tue"]
    assert wh["wed"] == defaults.working_hours["wed"]
    assert wh["thu"] == defaults.working_hours["thu"]
    assert wh["fri"] == defaults.working_hours["fri"]


def test_working_hours_attribute_value_is_not_complete():
    """default values are used for missing days in the given working_hours attr."""
    working_hours = {"sat": [[900, 1080]], "sun": [[900, 1080]]}
    wh = WorkingHours()
    wh.working_hours = working_hours
    assert wh["mon"] == defaults.working_hours["mon"]
    assert wh["tue"] == defaults.working_hours["tue"]
    assert wh["wed"] == defaults.working_hours["wed"]
    assert wh["thu"] == defaults.working_hours["thu"]
    assert wh["fri"] == defaults.working_hours["fri"]


def test_working_hours_can_be_indexed_with_day_number():
    """working hours for a day can be reached by an index."""
    wh = WorkingHours()
    assert wh[6] == defaults.working_hours["sun"]
    # this should not raise any errors
    wh[6] = [[540, 1080]]


def test_working_hours_day_0_is_monday():
    """day zero is monday."""
    wh = WorkingHours()
    wh[0] = [[270, 980]]
    assert wh["mon"] == wh[0]


def test_working_hours_can_be_string_indexed_with_the_date_short_name():
    """working hours info can be reached by using the short date name as the index."""
    wh = WorkingHours()
    assert wh["sun"] == defaults.working_hours["sun"]
    # this should not raise any errors
    wh["sun"] = [[540, 1080]]


@pytest.mark.parametrize(
    "test_key, test_value, error_type",
    [
        [0, "not a proper data", TypeError],
        ["sun", "not a proper data", TypeError],
        [0, ["no proper data"], TypeError],
        ["sun", ["no proper data"], TypeError],
        [0, [["no proper data"]], ValueError],
        ["sun", [["no proper data"]], ValueError],
        [0, [[3]], ValueError],
        [2, [[2, "a"]], TypeError],
        [1, [[20, 10], ["a", 300]], TypeError],
        [5, [[323, 1344], [2, "d"]], TypeError],
        [0, [[4, 100, 3]], ValueError],
        ["mon", [[3]], ValueError],
        ["mon", [[2, "a"]], TypeError],
        ["tue", [[20, 10], ["a", 300]], TypeError],
        ["fri", [[323, 1344], [2, "d"]], TypeError],
        ["sat", [[4, 100, 3]], ValueError],
        ["sun", [[-10, 100]], ValueError],
        ["sat", [[0, 1800]], ValueError],
        [7, [[32, 23], [233, 324]], IndexError],
        [7, [[32, 23], [233, 324]], IndexError],
        ["zon", [[32, 23], [233, 324]], KeyError],
    ],
)
def test___setitem__checks_the_given_data(test_key, test_value, error_type):
    """__setitem__ checks the given data format."""
    wh = WorkingHours()
    with pytest.raises(error_type) as cm:
        wh[test_key] = test_value

    error_message = {
        TypeError: (
            "WorkingHours.working_hours value should be a list of lists of "
            "two integers and the range of integers should be between 0-1440, "
            f"not {test_value.__class__.__name__}: '{test_value}'"
        ),
        ValueError: (
            "WorkingHours.working_hours value should be a list of lists of "
            "two integers and the range of integers should be between 0-1440, "
            f"not {test_value.__class__.__name__}: '{test_value}'"
        ),
        IndexError: "list index out of range",
        KeyError: (
            "\"WorkingHours accepts only ['mon', 'tue', 'wed', 'thu', "
            "'fri', 'sat', 'sun'] as key, not 'zon'\""
        ),
    }[error_type]

    assert str(cm.value) == error_message


def test_working_hours_argument_is_working_as_expected():
    """working_hours argument is working as expected,"""
    working_hours = copy.copy(defaults.working_hours)
    working_hours["sun"] = [[540, 1000]]
    working_hours["sat"] = [[500, 800], [900, 1440]]
    wh = WorkingHours(working_hours=working_hours)
    assert wh.working_hours == working_hours
    assert wh.working_hours["sun"] == working_hours["sun"]
    assert wh.working_hours["sat"] == working_hours["sat"]


def test_working_hours_attribute_is_working_as_expected():
    """working_hours attribute is working as expected."""
    working_hours = copy.copy(defaults.working_hours)
    working_hours["sun"] = [[540, 1000]]
    working_hours["sat"] = [[500, 800], [900, 1440]]
    wh = WorkingHours()
    wh.working_hours = working_hours
    assert wh.working_hours == working_hours
    assert wh.working_hours["sun"] == working_hours["sun"]
    assert wh.working_hours["sat"] == working_hours["sat"]


def test_to_tjp_attribute_is_read_only():
    """to_tjp attribute is read only."""
    wh = WorkingHours()
    with pytest.raises(AttributeError) as cm:
        wh.to_tjp = "some value"

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'to_tjp'",
    }.get(
        sys.version_info.minor,
        "property 'to_tjp' of 'WorkingHours' object has no setter",
    )

    assert str(cm.value) == error_message


def test_to_tjp_attribute_is_working_as_expected():
    """to_tjp property is working as expected."""
    wh = WorkingHours()
    wh["mon"] = [[570, 1110]]
    wh["tue"] = [[570, 1110]]
    wh["wed"] = [[570, 1110]]
    wh["thu"] = [[570, 1110]]
    wh["fri"] = [[570, 1110]]
    wh["sat"] = []
    wh["sun"] = []

    expected_tjp = """workinghours mon 09:30 - 18:30
workinghours tue 09:30 - 18:30
workinghours wed 09:30 - 18:30
workinghours thu 09:30 - 18:30
workinghours fri 09:30 - 18:30
workinghours sat off
workinghours sun off"""

    # print("Expected:")
    # print("---------")
    # print(expected_tjp)
    # print("--------------------")
    # print("Result:")
    # print("-------")
    # print(wh.to_tjp)

    assert wh.to_tjp == expected_tjp


def test_to_tjp_attribute_is_working_as_expected_for_multiple_work_hour_ranges():
    """to_tjp property is working as expected."""
    wh = WorkingHours()
    wh["mon"] = [[570, 720], [780, 1110]]
    wh["tue"] = [[570, 720], [780, 1110]]
    wh["wed"] = [[570, 720], [780, 1110]]
    wh["thu"] = [[570, 720], [780, 1110]]
    wh["fri"] = [[570, 720], [780, 1110]]
    wh["sat"] = [[570, 720]]
    wh["sun"] = []

    expected_tjp = """workinghours mon 09:30 - 12:00, 13:00 - 18:30
workinghours tue 09:30 - 12:00, 13:00 - 18:30
workinghours wed 09:30 - 12:00, 13:00 - 18:30
workinghours thu 09:30 - 12:00, 13:00 - 18:30
workinghours fri 09:30 - 12:00, 13:00 - 18:30
workinghours sat 09:30 - 12:00
workinghours sun off"""

    # print("Expected:")
    # print("---------")
    # print(expected_tjp)
    # print("--------------------")
    # print("Result:")
    # print("-------")
    # print(wh.to_tjp)

    assert wh.to_tjp == expected_tjp


def test_weekly_working_hours_attribute_is_read_only():
    """weekly_working_hours is a read-only attribute."""
    wh = WorkingHours()
    with pytest.raises(AttributeError) as cm:
        wh.weekly_working_hours = 232

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'weekly_working_hours'",
    }.get(
        sys.version_info.minor,
        "property 'weekly_working_hours' of 'WorkingHours' object has no setter",
    )

    assert str(cm.value) == error_message


def test_weekly_working_hours_attribute_is_working_as_expected():
    """weekly_working_hours attribute is working as expected."""
    wh = WorkingHours()
    wh["mon"] = [[570, 720], [780, 1110]]  # 480
    wh["tue"] = [[570, 720], [780, 1110]]  # 480
    wh["wed"] = [[570, 720], [780, 1110]]  # 480
    wh["thu"] = [[570, 720], [780, 1110]]  # 480
    wh["fri"] = [[570, 720], [780, 1110]]  # 480
    wh["sat"] = [[570, 720]]  # 150
    wh["sun"] = []  # 0

    expected_value = 42.5
    assert wh.weekly_working_hours == expected_value


def test_is_working_hour_is_working_as_expected():
    """is_working_hour method is working as expected."""
    wh = WorkingHours()

    wh["mon"] = [[570, 720], [780, 1110]]
    wh["tue"] = [[570, 720], [780, 1110]]
    wh["wed"] = [[570, 720], [780, 1110]]
    wh["thu"] = [[570, 720], [780, 1110]]
    wh["fri"] = [[570, 720], [780, 1110]]
    wh["sat"] = [[570, 720]]
    wh["sun"] = []

    # monday
    check_date = datetime.datetime(2013, 4, 8, 13, 55, tzinfo=pytz.utc)
    assert wh.is_working_hour(check_date) is True

    # sunday
    check_date = datetime.datetime(2013, 4, 14, 13, 55, tzinfo=pytz.utc)
    assert wh.is_working_hour(check_date) is False


def test_day_numbers_are_correct():
    """day numbers are correct."""
    wh = WorkingHours()
    wh["mon"] = [[1, 2]]
    wh["tue"] = [[3, 4]]
    wh["wed"] = [[5, 6]]
    wh["thu"] = [[7, 8]]
    wh["fri"] = [[9, 10]]
    wh["sat"] = [[11, 12]]
    wh["sun"] = [[13, 14]]

    assert defaults.day_order[0] == "mon"
    assert defaults.day_order[1] == "tue"
    assert defaults.day_order[2] == "wed"
    assert defaults.day_order[3] == "thu"
    assert defaults.day_order[4] == "fri"
    assert defaults.day_order[5] == "sat"
    assert defaults.day_order[6] == "sun"

    assert wh["mon"] == wh[0]
    assert wh["tue"] == wh[1]
    assert wh["wed"] == wh[2]
    assert wh["thu"] == wh[3]
    assert wh["fri"] == wh[4]
    assert wh["sat"] == wh[5]
    assert wh["sun"] == wh[6]


def test_weekly_working_days_is_a_read_only_attribute():
    """weekly working days is a read-only attribute."""
    wh = WorkingHours()
    with pytest.raises(AttributeError) as cm:
        wh.weekly_working_days = 6

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'weekly_working_days'",
    }.get(
        sys.version_info.minor,
        "property 'weekly_working_days' of 'WorkingHours' object has no setter",
    )

    assert str(cm.value) == error_message


@pytest.mark.parametrize(
    "test_data, expected_result",
    [
        [
            {
                "mon": [[1, 2]],
                "tue": [[3, 4]],
                "wed": [[5, 6]],
                "thu": [[7, 8]],
                "fri": [[9, 10]],
                "sat": [],
                "sun": [],
            },
            5,
        ],
        [
            {
                "mon": [[1, 2]],
                "tue": [[3, 4]],
                "wed": [[5, 6]],
                "thu": [[7, 8]],
                "fri": [[9, 10]],
                "sat": [[11, 12]],
                "sun": [],
            },
            6,
        ],
        [
            {
                "mon": [[1, 2]],
                "tue": [[3, 4]],
                "wed": [[5, 6]],
                "thu": [[7, 8]],
                "fri": [[9, 10]],
                "sat": [[11, 12]],
                "sun": [[13, 14]],
            },
            7,
        ],
    ],
)
def test_weekly_working_days_is_calculated_correctly(test_data, expected_result):
    """weekly working days are calculated correctly."""
    wh = WorkingHours()
    for day in test_data:
        wh[day] = test_data[day]
    assert wh.weekly_working_days == expected_result


def test_yearly_working_days_is_a_read_only_attribute():
    """yearly_working_days attribute is a read only attribute."""
    wh = WorkingHours()
    with pytest.raises(AttributeError) as cm:
        wh.yearly_working_days = 260.1

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute 'yearly_working_days'",
    }.get(
        sys.version_info.minor,
        "property 'yearly_working_days' of 'WorkingHours' object has no setter",
    )

    assert str(cm.value) == error_message


@pytest.mark.parametrize(
    "test_data, expected_result",
    [
        [
            {
                "mon": [[1, 2]],
                "tue": [[3, 4]],
                "wed": [[5, 6]],
                "thu": [[7, 8]],
                "fri": [[9, 10]],
                "sat": [],
                "sun": [],
            },
            261,
        ],
        [
            {
                "mon": [[1, 2]],
                "tue": [[3, 4]],
                "wed": [[5, 6]],
                "thu": [[7, 8]],
                "fri": [[9, 10]],
                "sat": [[11, 12]],
                "sun": [],
            },
            313,
        ],
        [
            {
                "mon": [[1, 2]],
                "tue": [[3, 4]],
                "wed": [[5, 6]],
                "thu": [[7, 8]],
                "fri": [[9, 10]],
                "sat": [[11, 12]],
                "sun": [[13, 14]],
            },
            365,
        ],
    ],
)
def test_yearly_working_days_is_calculated_correctly(test_data, expected_result):
    """yearly_working_days is calculated correctly."""
    wh = WorkingHours()
    for day in test_data:
        wh[day] = test_data[day]
    assert wh.yearly_working_days == pytest.approx(expected_result)


def test_daily_working_hours_argument_is_skipped():
    """daily_working_hours arg is skipped, daily_working_hours attr is equal to the
    default settings."""
    wh = WorkingHours()
    assert wh.daily_working_hours == defaults.daily_working_hours


def test_daily_working_hours_argument_is_none():
    """daily_working_hours attr is equal to the default settings value if the
    daily_working_hours argument is None."""
    kwargs = dict()
    kwargs["daily_working_hours"] = None
    wh = WorkingHours(**kwargs)
    assert wh.daily_working_hours == defaults.daily_working_hours


def test_daily_working_hours_attribute_is_none():
    """daily_working_hours attr is set to default if it is set to None."""
    wh = WorkingHours()
    wh.daily_working_hours = None
    assert wh.daily_working_hours == defaults.daily_working_hours


def test_daily_working_hours_argument_is_not_integer():
    """TypeError raised if the daily_working_hours argument is not an integer."""
    kwargs = dict()
    kwargs["daily_working_hours"] = "not an integer"
    with pytest.raises(TypeError) as cm:
        WorkingHours(**kwargs)
    assert str(cm.value) == (
        "WorkingHours.daily_working_hours should be an integer, "
        "not str: 'not an integer'"
    )


def test_daily_working_hours_attribute_is_not_an_integer():
    """TypeError raised if the daily_working hours attr is not an integer."""
    wh = WorkingHours()
    with pytest.raises(TypeError) as cm:
        wh.daily_working_hours = "not an integer"

    assert str(cm.value) == (
        "WorkingHours.daily_working_hours should be an integer, "
        "not str: 'not an integer'"
    )


def test_daily_working_hours_argument_is_working_fine():
    """daily working hours arg is correctly passed to daily_working_hours attr."""
    kwargs = dict()
    kwargs["daily_working_hours"] = 12
    wh = WorkingHours(**kwargs)
    assert wh.daily_working_hours == 12


def test_daily_working_hours_attribute_is_working_as_expected():
    """daily_working_hours attribute is working as expected."""
    wh = WorkingHours()
    wh.daily_working_hours = 23
    assert wh.daily_working_hours == 23


def test_daily_working_hours_argument_is_zero():
    """ValueError is raised if the daily_working_hours argument value is zero."""
    kwargs = dict()
    kwargs["daily_working_hours"] = 0
    with pytest.raises(ValueError) as cm:
        WorkingHours(**kwargs)

    assert (
        str(cm.value)
        == "WorkingHours.daily_working_hours should be a positive integer "
        "value greater than 0 and smaller than or equal to 24"
    )


def test_daily_working_hours_attribute_is_zero():
    """ValueError is raised if the daily_working_hours attribute is set to zero."""
    wh = WorkingHours()
    with pytest.raises(ValueError) as cm:
        wh.daily_working_hours = 0

    assert (
        str(cm.value)
        == "WorkingHours.daily_working_hours should be a positive integer "
        "value greater than 0 and smaller than or equal to 24"
    )


def test_daily_working_hours_argument_is_a_negative_number():
    """ValueError is raised if the daily_working_hours argument value is negative."""
    kwargs = dict()
    kwargs["daily_working_hours"] = -10
    with pytest.raises(ValueError) as cm:
        WorkingHours(**kwargs)

    assert (
        str(cm.value)
        == "WorkingHours.daily_working_hours should be a positive integer "
        "value greater than 0 and smaller than or equal to 24"
    )


def test_daily_working_hours_attribute_is_a_negative_number():
    """ValueError raised if the daily_working_hours attr is set to a negative value."""
    wh = WorkingHours()
    with pytest.raises(ValueError) as cm:
        wh.daily_working_hours = -10

    assert (
        str(cm.value)
        == "WorkingHours.daily_working_hours should be a positive integer "
        "value greater than 0 and smaller than or equal to 24"
    )


def test_daily_working_hours_argument_is_set_to_a_number_bigger_than_24():
    """ValueError is raised if the daily working hours argument is bigger than 24."""
    kwargs = dict()
    kwargs["daily_working_hours"] = 25
    with pytest.raises(ValueError) as cm:
        WorkingHours(**kwargs)

    assert (
        str(cm.value)
        == "WorkingHours.daily_working_hours should be a positive integer "
        "value greater than 0 and smaller than or equal to 24"
    )


def test_daily_working_hours_attribute_is_set_to_a_number_bigger_than_24():
    """ValueError is raised if the daily working hours attr is bigger than 24."""
    wh = WorkingHours()
    with pytest.raises(ValueError) as cm:
        wh.daily_working_hours = 25

    assert (
        str(cm.value)
        == "WorkingHours.daily_working_hours should be a positive integer "
        "value greater than 0 and smaller than or equal to 24"
    )


def test_split_in_to_working_hours_is_not_implemented_yet():
    """NotimplementedError is raised if the split_in_to_working_hours() is called."""
    with pytest.raises(NotImplementedError):
        wh = WorkingHours()
        start = datetime.datetime.now(pytz.utc)
        end = start + datetime.timedelta(days=10)
        wh.split_in_to_working_hours(start, end)
