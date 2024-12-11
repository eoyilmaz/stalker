# -*- coding: utf-8 -*-
"""ScheduleModel related tests are here."""
from enum import Enum
import sys

import pytest

from stalker.models.enum import ScheduleModel


@pytest.mark.parametrize(
    "model",
    [
        ScheduleModel.Effort,
        ScheduleModel.Duration,
        ScheduleModel.Length,
    ],
)
def test_it_is_an_enum(model):
    """ScheduleModel is an Enum."""
    assert isinstance(model, Enum)


@pytest.mark.parametrize(
    "model,expected_value",
    [
        [ScheduleModel.Effort, "effort"],
        [ScheduleModel.Duration, "duration"],
        [ScheduleModel.Length, "length"],
    ],
)
def test_enum_values(model, expected_value):
    """Test enum values."""
    assert model.value == expected_value


@pytest.mark.parametrize(
    "model,expected_name",
    [
        [ScheduleModel.Effort, "Effort"],
        [ScheduleModel.Duration, "Duration"],
        [ScheduleModel.Length, "Length"],
    ],
)
def test_enum_names(model, expected_name):
    """Test enum names."""
    assert model.name == expected_name


@pytest.mark.parametrize(
    "model,expected_value",
    [
        [ScheduleModel.Effort, "effort"],
        [ScheduleModel.Duration, "duration"],
        [ScheduleModel.Length, "length"],
    ],
)
def test_enum_as_str(model, expected_value):
    """Test enum names."""
    assert str(model) == expected_value


def test_to_model_model_is_skipped():
    """ScheduleModel.to_model() model is skipped."""
    with pytest.raises(TypeError) as cm:
        _ = ScheduleModel.to_model()

    py_error_message = {
        8: "to_model() missing 1 required positional argument: 'model'",
        9: "to_model() missing 1 required positional argument: 'model'",
        10: "ScheduleModel.to_model() missing 1 required positional argument: 'model'",
        11: "ScheduleModel.to_model() missing 1 required positional argument: 'model'",
        12: "ScheduleModel.to_model() missing 1 required positional argument: 'model'",
        13: "ScheduleModel.to_model() missing 1 required positional argument: 'model'",
    }[sys.version_info.minor]
    assert str(cm.value) == py_error_message


def test_to_model_model_is_none():
    """ScheduleModel.to_model() model is None."""
    with pytest.raises(TypeError) as cm:
        _ = ScheduleModel.to_model(None)
    assert str(cm.value) == (
        "model should be a ScheduleModel enum value or one of ['Effort', "
        "'Duration', 'Length', 'effort', 'duration', 'length'], "
        "not NoneType: 'None'"
    )


def test_to_model_model_is_not_a_str():
    """ScheduleModel.to_model() model is not a str."""
    with pytest.raises(TypeError) as cm:
        _ = ScheduleModel.to_model(12334.123)

    assert str(cm.value) == (
        "model should be a ScheduleModel enum value or one of ['Effort', "
        "'Duration', 'Length', 'effort', 'duration', 'length'], "
        "not float: '12334.123'"
    )


def test_to_model_model_is_not_a_valid_str():
    """ScheduleModel.to_model() model is not a valid str."""
    with pytest.raises(ValueError) as cm:
        _ = ScheduleModel.to_model("not a valid value")

    assert str(cm.value) == (
        "model should be a ScheduleModel enum value or one of ['Effort', "
        "'Duration', 'Length', 'effort', 'duration', 'length'], "
        "not 'not a valid value'"
    )


@pytest.mark.parametrize(
    "model_name,model",
    [
        # Effort
        ["Effort", ScheduleModel.Effort],
        ["effort", ScheduleModel.Effort],
        ["EFFORT", ScheduleModel.Effort],
        ["EfFoRt", ScheduleModel.Effort],
        # Duration
        ["Duration", ScheduleModel.Duration],
        ["duration", ScheduleModel.Duration],
        ["DURATION", ScheduleModel.Duration],
        ["DuRaTiOn", ScheduleModel.Duration],
        ["dUrAtIoN", ScheduleModel.Duration],
        # Length
        ["Length", ScheduleModel.Length],
        ["length", ScheduleModel.Length],
        ["LENGTH", ScheduleModel.Length],
        ["LeNgTh", ScheduleModel.Length],
        ["lEnGtH", ScheduleModel.Length],
    ],
)
def test_to_model_is_working_properly(model_name, model):
    """ScheduleModel can parse schedule model names."""
    assert ScheduleModel.to_model(model_name) == model
