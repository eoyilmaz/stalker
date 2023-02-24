# -*- coding: utf-8 -*-
"""Tests for the SchedulerBase class."""

import pytest

from stalker import SchedulerBase, Studio


@pytest.fixture(scope="function")
def setup_scheduler_base_tests():
    """Set up the tests for stalker.models.scheduler.SchedulerBase class."""
    data = dict()
    data["test_studio"] = Studio(name="Test Studio")
    data["kwargs"] = {"studio": data["test_studio"]}
    data["test_scheduler_base"] = SchedulerBase(**data["kwargs"])
    return data


def test_studio_argument_is_skipped(setup_scheduler_base_tests):
    """studio attribute None if the studio argument is skipped."""
    data = setup_scheduler_base_tests
    data["kwargs"].pop("studio")
    new_scheduler_base = SchedulerBase(**data["kwargs"])
    assert new_scheduler_base.studio is None


def test_studio_argument_is_none(setup_scheduler_base_tests):
    """studio attribute None if the studio argument is None."""
    data = setup_scheduler_base_tests
    data["kwargs"]["studio"] = None
    new_scheduler_base = SchedulerBase(**data["kwargs"])
    assert new_scheduler_base.studio is None


def test_studio_attribute_is_none(setup_scheduler_base_tests):
    """studio argument can be set to None."""
    data = setup_scheduler_base_tests
    data["test_scheduler_base"].studio = None
    assert data["test_scheduler_base"].studio is None


def test_studio_argument_is_not_a_studio_instance(setup_scheduler_base_tests):
    """TypeError raised if the studio argument is not Studio instance."""
    data = setup_scheduler_base_tests
    data["kwargs"]["studio"] = "not a studio instance"
    with pytest.raises(TypeError) as cm:
        SchedulerBase(**data["kwargs"])

    assert (
        str(cm.value) == "SchedulerBase.studio should be an instance of "
        "stalker.models.studio.Studio, not str"
    )


def test_studio_attribute_is_not_a_studio_instance(setup_scheduler_base_tests):
    """TypeError raised if the studio attr is not a Studio instance."""
    data = setup_scheduler_base_tests
    with pytest.raises(TypeError) as cm:
        data["test_scheduler_base"].studio = "not a studio instance"

    assert (
        str(cm.value) == "SchedulerBase.studio should be an instance of "
        "stalker.models.studio.Studio, not str"
    )


def test_studio_argument_is_working_properly(setup_scheduler_base_tests):
    """studio argument value is correctly passed to the studio attribute."""
    data = setup_scheduler_base_tests
    assert data["test_scheduler_base"].studio == data["kwargs"]["studio"]


def test_studio_attribute_is_working_properly(setup_scheduler_base_tests):
    """studio attribute is working properly."""
    data = setup_scheduler_base_tests
    new_studio = Studio(name="Test Studio 2")
    data["test_scheduler_base"].studio = new_studio
    assert data["test_scheduler_base"].studio == new_studio


def test_schedule_method_will_raise_not_implemented_error():
    """schedule() method will raise a NotImplementedError."""
    base = SchedulerBase()
    with pytest.raises(NotImplementedError) as cm:
        base.schedule()

    assert str(cm.value) == ""
