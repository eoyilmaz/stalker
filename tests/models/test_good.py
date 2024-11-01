# -*- coding: utf-8 -*-
"""Tests for the Good class."""

import pytest

from stalker import Client, Good


@pytest.fixture(scope="function")
def setup_good_tests():
    """Set up the test for the stalker.models.budget.Good class."""
    data = dict()
    data["kwargs"] = {"name": "Comp", "cost": 10, "msrp": 12, "unit": "TL/hour"}
    return data


def test_cost_argument_is_skipped(setup_good_tests):
    """cost attribute value is 0.0 if the cost argument is skipped."""
    data = setup_good_tests
    data["kwargs"].pop("cost")
    g = Good(**data["kwargs"])
    assert g.cost == 0


def test_cost_argument_is_none(setup_good_tests):
    """cost attribute value is 0.0 if the cost argument is None."""
    data = setup_good_tests
    data["kwargs"]["cost"] = None
    g = Good(**data["kwargs"])
    assert g.cost == 0


def test_cost_attribute_is_none(setup_good_tests):
    """cost attribute is 0.0 if it is set to None."""
    data = setup_good_tests
    g = Good(**data["kwargs"])
    assert g.cost != 0
    g.cost = None
    assert g.cost == 0


def test_cost_argument_is_not_a_number(setup_good_tests):
    """TypeError is raised if cost argument is not a number."""
    data = setup_good_tests
    data["kwargs"]["cost"] = "not a number"
    with pytest.raises(TypeError) as cm:
        _ = Good(**data["kwargs"])

    assert str(cm.value) == (
        "Good.cost should be a non-negative number, not str: 'not a number'"
    )


def test_cost_attribute_is_not_a_number(setup_good_tests):
    """TypeError is raised if the cost attr is not a number."""
    data = setup_good_tests
    g = Good(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        g.cost = "not a number"

    assert str(cm.value) == (
        "Good.cost should be a non-negative number, not str: 'not a number'"
    )


def test_cost_argument_is_zero(setup_good_tests):
    """It is totally ok to set the cost to 0."""
    data = setup_good_tests
    data["kwargs"]["cost"] = 0
    g = Good(**data["kwargs"])
    assert g.cost == 0.0


def test_cost_attribute_is_zero(setup_good_tests):
    """It is totally ok to test the cost attribute to 0."""
    data = setup_good_tests
    g = Good(**data["kwargs"])
    assert g.cost != 0.0
    g.cost = 0.0
    assert g.cost == 0.0


def test_cost_argument_is_negative(setup_good_tests):
    """ValueError is raised if the cost argument is a negative number."""
    data = setup_good_tests
    data["kwargs"]["cost"] = -10
    with pytest.raises(ValueError) as cm:
        _ = Good(**data["kwargs"])

    assert str(cm.value) == "Good.cost should be a non-negative number"


def test_cost_attribute_is_negative(setup_good_tests):
    """ValueError is raised if the cost attribute is set to a negative number."""
    data = setup_good_tests
    g = Good(**data["kwargs"])
    with pytest.raises(ValueError) as cm:
        g.cost = -10

    assert str(cm.value) == "Good.cost should be a non-negative number"


def test_cost_argument_is_working_properly(setup_good_tests):
    """cost argument value is properly passed to the cost attribute."""
    data = setup_good_tests
    test_value = 113
    data["kwargs"]["cost"] = test_value
    g = Good(**data["kwargs"])
    assert g.cost == test_value


def test_cost_attribute_is_working_properly(setup_good_tests):
    """cost attribute value can be properly changed."""
    data = setup_good_tests
    test_value = 145
    g = Good(**data["kwargs"])
    assert g.cost != test_value

    g.cost = test_value
    assert g.cost == test_value


def test_msrp_argument_is_skipped(setup_good_tests):
    """msrp attribute value is 0.0 if the msrp argument is skipped."""
    data = setup_good_tests
    data["kwargs"].pop("msrp")
    g = Good(**data["kwargs"])
    assert g.msrp == 0


def test_msrp_argument_is_none(setup_good_tests):
    """msrp attribute value is 0.0 if the msrp argument is None."""
    data = setup_good_tests
    data["kwargs"]["msrp"] = None
    g = Good(**data["kwargs"])
    assert g.msrp == 0


def test_msrp_attribute_is_none(setup_good_tests):
    """msrp attribute is 0.0 if it is set to None."""
    data = setup_good_tests
    g = Good(**data["kwargs"])
    assert g.msrp != 0
    g.msrp = None
    assert g.msrp == 0


def test_msrp_argument_is_not_a_number(setup_good_tests):
    """TypeError is raised if msrp argument is not a number."""
    data = setup_good_tests
    data["kwargs"]["msrp"] = "not a number"
    with pytest.raises(TypeError) as cm:
        _ = Good(**data["kwargs"])

    assert str(cm.value) == (
        "Good.msrp should be a non-negative number, not str: 'not a number'"
    )


def test_msrp_attribute_is_not_a_number(setup_good_tests):
    """TypeError is raised if the msrp attr is not a number."""
    data = setup_good_tests
    g = Good(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        g.msrp = "not a number"

    assert str(cm.value) == (
        "Good.msrp should be a non-negative number, not str: 'not a number'"
    )


def test_msrp_argument_is_zero(setup_good_tests):
    """It is totally ok to set the msrp to 0."""
    data = setup_good_tests
    data["kwargs"]["msrp"] = 0
    g = Good(**data["kwargs"])
    assert g.msrp == 0.0


def test_msrp_attribute_is_zero(setup_good_tests):
    """It is totally ok to test the msrp attribute to 0."""
    data = setup_good_tests
    g = Good(**data["kwargs"])
    assert g.msrp != 0.0
    g.msrp = 0.0
    assert g.msrp == 0.0


def test_msrp_argument_is_negative(setup_good_tests):
    """ValueError is raised if the msrp argument is a negative number."""
    data = setup_good_tests
    data["kwargs"]["msrp"] = -10
    with pytest.raises(ValueError) as cm:
        _ = Good(**data["kwargs"])

    assert str(cm.value) == "Good.msrp should be a non-negative number"


def test_msrp_attribute_is_negative(setup_good_tests):
    """ValueError is raised if the msrp attribute is set to a negative number."""
    data = setup_good_tests
    g = Good(**data["kwargs"])
    with pytest.raises(ValueError) as cm:
        g.msrp = -10

    assert str(cm.value) == "Good.msrp should be a non-negative number"


def test_msrp_argument_is_working_properly(setup_good_tests):
    """msrp argument value is properly passed to the msrp attribute."""
    data = setup_good_tests
    test_value = 113
    data["kwargs"]["msrp"] = test_value
    g = Good(**data["kwargs"])
    assert g.msrp == test_value


def test_msrp_attribute_is_working_properly(setup_good_tests):
    """msrp attribute value can be properly changed."""
    data = setup_good_tests
    test_value = 145
    g = Good(**data["kwargs"])
    assert g.msrp != test_value

    g.msrp = test_value
    assert g.msrp == test_value


def test_unit_argument_is_skipped(setup_good_tests):
    """unit attribute is an empty string if the unit argument is skipped."""
    data = setup_good_tests
    data["kwargs"].pop("unit")
    g = Good(**data["kwargs"])
    assert g.unit == ""


def test_unit_argument_is_none(setup_good_tests):
    """unit attribute is an empty string if the unit argument is None."""
    data = setup_good_tests
    data["kwargs"]["unit"] = None
    g = Good(**data["kwargs"])
    assert g.unit == ""


def test_unit_attribute_is_set_to_none(setup_good_tests):
    """unit attribute is an empty string if it is set to None."""
    data = setup_good_tests
    g = Good(**data["kwargs"])
    assert g.unit != ""
    g.unit = None
    assert g.unit == ""


def test_unit_argument_is_not_a_string(setup_good_tests):
    """TypeError is raised if the unit argument is not a string."""
    data = setup_good_tests
    data["kwargs"]["unit"] = 12312
    with pytest.raises(TypeError) as cm:
        g = Good(**data["kwargs"])

    assert str(cm.value) == "Good.unit should be a string, not int: '12312'"


def test_unit_attribute_is_not_a_string(setup_good_tests):
    """TypeError is raised if the unit attr is set to a value which is not a string."""
    data = setup_good_tests
    g = Good(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        g.unit = 2342

    assert str(cm.value) == "Good.unit should be a string, not int: '2342'"


def test_unit_argument_is_working_properly(setup_good_tests):
    """unit argument value is properly passed to the unit attribute."""
    data = setup_good_tests
    test_value = "this is my unit"
    data["kwargs"]["unit"] = test_value
    g = Good(**data["kwargs"])
    assert g.unit == test_value


def test_unit_attribute_is_working_properly(setup_good_tests):
    """unit attribute value can be changed properly."""
    data = setup_good_tests
    test_value = "this is my unit"
    g = Good(**data["kwargs"])
    assert g.unit != test_value
    g.unit = test_value
    assert g.unit == test_value


def test_client_argument_is_skipped(setup_good_tests):
    """Good can be created without a Client."""
    data = setup_good_tests
    data["kwargs"].pop("client", None)
    g = Good(**data["kwargs"])
    assert g is not None
    assert isinstance(g, Good)


def test_client_argument_is_none(setup_good_tests):
    """Good can be created without a Client."""
    data = setup_good_tests
    data["kwargs"]["client"] = None
    g = Good(**data["kwargs"])
    assert g is not None
    assert isinstance(g, Good)


def test_client_argument_is_not_a_client_instance(setup_good_tests):
    """TypeError is raised if the client argument is not a Client instance."""
    data = setup_good_tests
    data["kwargs"]["client"] = "not a client"
    with pytest.raises(TypeError) as cm:
        Good(**data["kwargs"])

    assert str(cm.value) == (
        "Good.client attribute should be a stalker.models.client.Client instance, "
        "not str: 'not a client'"
    )


def test_client_attribute_is_set_to_a_value_other_than_a_client(setup_good_tests):
    """TypeError is raised if the client attr is not a Client instance."""
    data = setup_good_tests
    g = Good(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        g.client = "not a client"

    assert str(cm.value) == (
        "Good.client attribute should be a stalker.models.client.Client instance, "
        "not str: 'not a client'"
    )


def test_client_argument_is_working_properly(setup_good_tests):
    """client argument is working properly."""
    data = setup_good_tests
    client = Client(name="Test Client")
    data["kwargs"]["client"] = client
    g = Good(**data["kwargs"])
    assert g.client == client


def test_client_attribute_is_working_properly(setup_good_tests):
    """client attribute is working properly."""
    data = setup_good_tests
    client = Client(name="Test Client")
    g = Good(**data["kwargs"])
    assert g.client != client
    g.client = client
    assert g.client == client
