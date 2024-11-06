# -*- coding: utf-8 -*-
"""Tests for the PriceList class."""

import pytest

from stalker import Good, PriceList


@pytest.fixture(scope="function")
def setup_price_list_tests():
    """Set up tests for the PriceList class."""
    data = dict()
    data["kwargs"] = {
        "name": "Test Price List",
    }
    return data


def test_goods_argument_is_skipped(setup_price_list_tests):
    """goods attribute is an empty list if the goods argument is skipped."""
    data = setup_price_list_tests
    p = PriceList(**data["kwargs"])
    assert p.goods == []


def test_goods_argument_is_none(setup_price_list_tests):
    """goods attribute is an empty list if the goods argument is None."""
    data = setup_price_list_tests
    data["kwargs"]["goods"] = None
    p = PriceList(**data["kwargs"])
    assert p.goods == []


def test_goods_attribute_is_none(setup_price_list_tests):
    """TypeError is raised if the goods attribute is set to None."""
    data = setup_price_list_tests
    g1 = Good(name="Test Good")
    data["kwargs"]["goods"] = [g1]
    p = PriceList(**data["kwargs"])
    assert p.goods == [g1]

    with pytest.raises(TypeError) as cm:
        p.goods = None

    assert str(cm.value) == "Incompatible collection type: None is not list-like"


def test_goods_argument_is_not_a_list(setup_price_list_tests):
    """TypeError is raised if the goods argument value is not a list."""
    data = setup_price_list_tests
    data["kwargs"]["goods"] = "this is not a list"
    with pytest.raises(TypeError) as cm:
        PriceList(**data["kwargs"])

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_goods_attribute_is_not_a_list(setup_price_list_tests):
    """TypeError is raised if the goods attribute is not a list."""
    data = setup_price_list_tests
    g1 = Good(name="Test Good")
    data["kwargs"]["goods"] = [g1]
    p = PriceList(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        p.goods = "this is not a list"

    assert str(cm.value) == "Incompatible collection type: str is not list-like"


def test_goods_argument_is_a_list_of_objects_which_are_not_goods(
    setup_price_list_tests,
):
    """TypeError is raised if the goods argument is not a list of Good instances."""
    data = setup_price_list_tests
    data["kwargs"]["goods"] = ["not", 1, "good", "instances"]
    with pytest.raises(TypeError) as cm:
        PriceList(**data["kwargs"])

    assert str(cm.value) == (
        "PriceList.goods should be a list of stalker.model.budget.Good instances, "
        "not str: 'not'"
    )


def test_good_attribute_is_a_list_of_objects_which_are_not_goods(
    setup_price_list_tests,
):
    """TypeError is raised if the goods attribute is not a list of Good instances."""
    data = setup_price_list_tests
    p = PriceList(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        p.goods = ["not", 1, "good", "instances"]

    assert str(cm.value) == (
        "PriceList.goods should be a list of "
        "stalker.model.budget.Good instances, not str: 'not'"
    )


def test_good_argument_is_working_as_expected(setup_price_list_tests):
    """good argument value is passed to the good attribute."""
    data = setup_price_list_tests
    g1 = Good(name="Good1")
    g2 = Good(name="Good2")
    g3 = Good(name="Good3")
    test_value = [g1, g2, g3]
    data["kwargs"]["goods"] = test_value
    p = PriceList(**data["kwargs"])
    assert p.goods == test_value


def test_good_attribute_is_working_as_expected(setup_price_list_tests):
    """good attribute value can be set."""
    data = setup_price_list_tests
    g1 = Good(name="Good1")
    g2 = Good(name="Good2")
    g3 = Good(name="Good3")
    test_value = [g1, g2, g3]
    p = PriceList(**data["kwargs"])
    assert p.goods != test_value
    p.goods = test_value
    assert p.goods == test_value
