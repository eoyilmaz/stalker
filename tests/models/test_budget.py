# -*- coding: utf-8 -*-
"""Budget class tests."""

import pytest

from stalker import (
    Budget,
    BudgetEntry,
    Good,
    Project,
    Repository,
    Status,
    StatusList,
    Type,
    User,
)


@pytest.fixture(scope="function")
def setup_budget_test_base():
    """Set up the tests for the Budget class.

    Returns:
        dict: Test data.
    """
    data = dict()
    data["status_wfd"] = Status(name="Waiting For Dependency", code="WFD")
    data["status_rts"] = Status(name="Ready To Start", code="RTS")
    data["status_wip"] = Status(name="Work In Progress", code="WIP")
    data["status_prev"] = Status(name="Pending Review", code="PREV")
    data["status_hrev"] = Status(name="Has Revision", code="HREV")
    data["status_drev"] = Status(name="Dependency Has Revision", code="DREV")
    data["status_oh"] = Status(name="On Hold", code="OH")
    data["status_stop"] = Status(name="Stopped", code="STOP")
    data["status_cmpl"] = Status(name="Completed", code="CMPL")
    data["status_new"] = Status(name="New", code="NEW")
    data["status_app"] = Status(name="Approved", code="APP")
    data["budget_status_list"] = StatusList(
        name="Budget Statuses",
        target_entity_type="Budget",
        statuses=[data["status_new"], data["status_prev"], data["status_app"]],
    )
    data["task_status_list"] = StatusList(
        statuses=[
            data["status_wfd"],
            data["status_rts"],
            data["status_wip"],
            data["status_prev"],
            data["status_hrev"],
            data["status_drev"],
            data["status_cmpl"],
        ],
        target_entity_type="Task",
    )
    data["test_project_status_list"] = StatusList(
        name="Project Statuses",
        statuses=[data["status_wip"], data["status_prev"], data["status_cmpl"]],
        target_entity_type="Project",
    )
    data["test_movie_project_type"] = Type(
        name="Movie Project",
        code="movie",
        target_entity_type="Project",
    )
    data["test_repository_type"] = Type(
        name="Test Repository Type",
        code="test",
        target_entity_type="Repository",
    )
    data["test_repository"] = Repository(
        name="Test Repository",
        code="TR",
        type=data["test_repository_type"],
        linux_path="/mnt/T/",
        windows_path="T:/",
        osx_path="/Volumes/T/",
    )
    data["test_user1"] = User(
        name="User1", login="user1", email="user1@user1.com", password="1234"
    )
    data["test_user2"] = User(
        name="User2", login="user2", email="user2@user2.com", password="1234"
    )
    data["test_user3"] = User(
        name="User3", login="user3", email="user3@user3.com", password="1234"
    )
    data["test_user4"] = User(
        name="User4", login="user4", email="user4@user4.com", password="1234"
    )
    data["test_user5"] = User(
        name="User5", login="user5", email="user5@user5.com", password="1234"
    )
    data["test_project"] = Project(
        name="Test Project1",
        code="tp1",
        type=data["test_movie_project_type"],
        status_list=data["test_project_status_list"],
        repository=data["test_repository"],
    )
    data["kwargs"] = {
        "project": data["test_project"],
        "name": "Test Budget 1",
        "status_list": data["budget_status_list"],
    }
    data["test_budget"] = Budget(**data["kwargs"])
    data["test_good"] = Good(name="Some Good", cost=100, msrp=120, unit="$")
    return data


def test_entries_attribute_is_set_to_a_list_of_other_instances_than_a_budget_entry(
    setup_budget_test_base,
):
    """TypeError is raised if the entries attribute is not a list of BudgetEntries."""
    data = setup_budget_test_base
    with pytest.raises(TypeError) as cm:
        data["test_budget"].entries = ["some", "string", 1, 2]

    assert (
        str(cm.value)
        == "Budget.entries should be a list of BudgetEntry instances, not str"
    )


def test_entries_attribute_is_working_properly(setup_budget_test_base):
    """Entries attribute is working properly."""
    data = setup_budget_test_base
    some_other_budget = Budget(
        name="Test Budget",
        project=data["test_project"],
        status_list=data["budget_status_list"],
    )
    entry1 = BudgetEntry(
        budget=some_other_budget,
        good=data["test_good"],
    )
    entry2 = BudgetEntry(
        budget=some_other_budget,
        good=data["test_good"],
    )
    data["test_budget"].entries = [entry1, entry2]
    assert data["test_budget"].entries == [entry1, entry2]


def test_statuses_is_working_properly(setup_budget_test_base):
    """Budget accepts statuses."""
    data = setup_budget_test_base
    data["test_budget"].status = data["status_new"]
    assert data["test_budget"].status == data["status_new"]
    data["test_budget"].status = data["status_prev"]
    assert data["test_budget"].status == data["status_prev"]
    data["test_budget"].status = data["status_app"]
    assert data["test_budget"].status == data["status_app"]


def test_budget_argument_is_skipped(setup_budget_test_base):
    """TypeError is raised if the budget argument is skipped."""
    with pytest.raises(TypeError) as cm:
        BudgetEntry(amount=10.0)
    assert (
        str(cm.value) == "BudgetEntry.budget should be a Budget instance, not NoneType"
    )


def test_budget_argument_is_none(setup_budget_test_base):
    """TypeError is raised if the budget argument is None."""
    with pytest.raises(TypeError) as cm:
        BudgetEntry(budget=None, amount=10.0)
    assert (
        str(cm.value) == "BudgetEntry.budget should be a Budget instance, not NoneType"
    )


def test_budget_attribute_is_set_to_none(setup_budget_test_base):
    """TypeError is raised if the budget attribute is set to None."""
    data = setup_budget_test_base
    entry = BudgetEntry(
        budget=data["test_budget"],
        good=data["test_good"],
    )
    with pytest.raises(TypeError) as cm:
        entry.budget = None
    assert (
        str(cm.value) == "BudgetEntry.budget should be a Budget instance, not NoneType"
    )


def test_budget_argument_is_not_a_budget_instance(setup_budget_test_base):
    """TypeError is raised if the budget argument is not a Budget instance."""
    with pytest.raises(TypeError) as cm:
        BudgetEntry(budget="not a budget", amount=10.0)
    assert str(cm.value) == "BudgetEntry.budget should be a Budget instance, not str"


def test_budget_attribute_is_not_a_budget_instance(setup_budget_test_base):
    """TypeError is raised if the budget attribute is not a Budget instance."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"], amount=10.0)
    with pytest.raises(TypeError) as cm:
        entry.budget = "not a budget instance"
    assert str(cm.value) == "BudgetEntry.budget should be a Budget instance, not str"


def test_budget_argument_is_working_properly(setup_budget_test_base):
    """If the budget argument value is correctly passed to the budget attribute."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"], amount=10.0)
    assert entry.budget == data["test_budget"]


def test_budget_attribute_is_working_properly(setup_budget_test_base):
    """If the budget attribute value can correctly be changed."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"], amount=10.0)
    new_budget = Budget(
        name="Test Budget",
        project=data["test_project"],
        status_list=data["budget_status_list"],
    )
    assert entry.budget != new_budget
    entry.budget = new_budget
    assert entry.budget == new_budget


def test_cost_attribute_value_will_be_copied_from_the_supplied_good_argument(
    setup_budget_test_base,
):
    """Cost attribute is copied from the good argument."""
    data = setup_budget_test_base
    good = Good(name="Some Good", cost=10, msrp=20, unit="$/hour")
    entry = BudgetEntry(budget=data["test_budget"], good=good)
    assert entry.cost == good.cost


def test_cost_attribute_is_set_to_none(setup_budget_test_base):
    """If the cost attribute is set to 0 if it is set to None."""
    data = setup_budget_test_base
    entry = BudgetEntry(
        budget=data["test_budget"],
        good=data["test_good"],
    )
    assert entry.cost == data["test_good"].cost
    entry.cost = None
    assert entry.cost == 0.0


def test_cost_attribute_is_not_a_number(setup_budget_test_base):
    """TypeError is raised if cost attribute is not a number."""
    data = setup_budget_test_base
    entry = BudgetEntry(
        budget=data["test_budget"],
        good=data["test_good"],
    )
    with pytest.raises(TypeError) as cm:
        entry.cost = "some string"
    assert str(cm.value) == "BudgetEntry.cost should be a number, not str"


def test_cost_attribute_is_working_properly(setup_budget_test_base):
    """If the cost attribute is working properly."""
    data = setup_budget_test_base
    entry = BudgetEntry(
        budget=data["test_budget"],
        good=data["test_good"],
    )
    test_value = 5.0
    assert entry.cost != test_value
    entry.cost = test_value
    assert entry.cost == test_value


def test_msrp_attribute_is_set_to_none(setup_budget_test_base):
    """Msrp attribute is 0 if it is set to None."""
    data = setup_budget_test_base
    entry = BudgetEntry(
        budget=data["test_budget"],
        good=data["test_good"],
    )
    assert entry.msrp == data["test_good"].msrp
    entry.msrp = None
    assert entry.msrp == 0.0


def test_msrp_attribute_is_not_a_number(setup_budget_test_base):
    """TypeError is raised if msrp attribute is not a number."""
    data = setup_budget_test_base
    entry = BudgetEntry(
        budget=data["test_budget"],
        good=data["test_good"],
    )
    with pytest.raises(TypeError) as cm:
        entry.msrp = "some string"
    assert str(cm.value) == "BudgetEntry.msrp should be a number, not str"


def test_msrp_attribute_is_working_properly(setup_budget_test_base):
    """Msrp attribute is working properly."""
    data = setup_budget_test_base
    entry = BudgetEntry(
        budget=data["test_budget"],
        good=data["test_good"],
    )
    test_value = 5.0
    assert entry.msrp != test_value
    entry.msrp = test_value
    assert entry.msrp == test_value


def test_msrp_attribute_value_will_be_copied_from_the_supplied_good_argument(
    setup_budget_test_base,
):
    """Msrp attribute value is copied from the supplied good argument value."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"])
    assert entry.msrp == data["test_good"].msrp


def test_price_argument_is_skipped(setup_budget_test_base):
    """Price attribute is 0 if the price argument is skipped."""
    data = setup_budget_test_base
    entry = BudgetEntry(
        budget=data["test_budget"],
        good=data["test_good"],
    )
    assert entry.price == 0.0


def test_price_argument_is_set_to_none(setup_budget_test_base):
    """Price attribute is set to 0 if the price argument is set to None."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"], price=None)
    assert entry.price == 0.0


def test_price_attribute_is_set_to_none(setup_budget_test_base):
    """Price attribute is set to 0 if price attribute is set to None."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"], price=10.0)
    assert entry.price == 10.0
    entry.price = None
    assert entry.price == 0.0


def test_price_argument_is_not_a_number(setup_budget_test_base):
    """TypeError is raised if the price arg is not a number."""
    data = setup_budget_test_base
    with pytest.raises(TypeError) as cm:
        BudgetEntry(
            budget=data["test_budget"], good=data["test_good"], price="some string"
        )

    assert str(cm.value) == "BudgetEntry.price should be a number, not str"


def test_price_attribute_is_not_a_number(setup_budget_test_base):
    """TypeError is raised if price attribute is not a number."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"], price=10)
    with pytest.raises(TypeError) as cm:
        entry.price = "some string"
    assert str(cm.value) == "BudgetEntry.price should be a number, not str"


def test_price_argument_is_working_properly(setup_budget_test_base):
    """Price arg value is passed to the price attribute."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"], price=10)
    assert entry.price == 10.0


def test_price_attribute_is_working_properly(setup_budget_test_base):
    """Price attribute is working properly."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"], price=10)
    test_value = 5.0
    assert entry.price != test_value
    entry.price = test_value
    assert entry.price == test_value


def test_realized_total_argument_is_skipped(setup_budget_test_base):
    """Realized_total attribute is 0 if the realized_total arg is skipped."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"])
    assert entry.realized_total == 0.0


def test_realized_total_argument_is_set_to_none(setup_budget_test_base):
    """Realized_total attribute is set to 0 if realized_total arg is None."""
    data = setup_budget_test_base
    entry = BudgetEntry(
        budget=data["test_budget"], good=data["test_good"], realized_total=None
    )
    assert entry.realized_total == 0.0


def test_realized_total_attribute_is_set_to_none(setup_budget_test_base):
    """Realized_total attribute is set to 0 if it is set to None."""
    data = setup_budget_test_base
    entry = BudgetEntry(
        budget=data["test_budget"], good=data["test_good"], realized_total=10.0
    )
    assert entry.realized_total == 10.0
    entry.realized_total = None
    assert entry.realized_total == 0.0


def test_realized_total_argument_is_not_a_number(setup_budget_test_base):
    """TypeError is raised if the realized_total arg not a number."""
    data = setup_budget_test_base
    with pytest.raises(TypeError) as cm:
        BudgetEntry(
            budget=data["test_budget"],
            good=data["test_good"],
            realized_total="some string",
        )

    assert str(cm.value) == "BudgetEntry.realized_total should be a number, not str"


def test_realized_total_attribute_is_not_a_number(setup_budget_test_base):
    """TypeError is raised if realized_total attribute is not a number."""
    data = setup_budget_test_base
    entry = BudgetEntry(
        budget=data["test_budget"], good=data["test_good"], realized_total=10
    )
    with pytest.raises(TypeError) as cm:
        entry.realized_total = "some string"
    assert str(cm.value) == "BudgetEntry.realized_total should be a number, not str"


def test_realized_total_argument_is_working_properly(setup_budget_test_base):
    """Realized_total arg value is passed to the realized_total attribute."""
    data = setup_budget_test_base
    entry = BudgetEntry(
        budget=data["test_budget"], good=data["test_good"], realized_total=10
    )
    assert entry.realized_total == 10.0


def test_realized_total_attribute_is_working_properly(setup_budget_test_base):
    """Realized_total attribute is working properly."""
    data = setup_budget_test_base
    entry = BudgetEntry(
        budget=data["test_budget"], good=data["test_good"], realized_total=10
    )
    test_value = 5.0
    assert entry.realized_total != test_value
    entry.realized_total = test_value
    assert entry.realized_total == test_value


def test_unit_attribute_is_set_to_none(setup_budget_test_base):
    """Unit attribute is set to an empty value if it is set to None."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"])
    assert entry.unit == data["test_good"].unit
    entry.unit = None
    assert entry.unit == ""


def test_unit_attribute_is_not_a_string(setup_budget_test_base):
    """TypeError is raised if the unit attribute is not a str."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"])
    with pytest.raises(TypeError) as cm:
        entry.unit = 100.212
    assert str(cm.value) == "BudgetEntry.unit should be a string, not float"


def test_unit_attribute_is_working_properly(setup_budget_test_base):
    """Unit attribute is working properly."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"])
    test_value = "TL/hour"
    assert entry.unit != test_value
    entry.unit = test_value
    assert entry.unit == test_value


def test_unit_attribute_value_will_be_copied_from_the_supplied_good(
    setup_budget_test_base,
):
    """Unit attribute value is copied from the good argument value."""
    data = setup_budget_test_base
    entry = BudgetEntry(
        budget=data["test_budget"],
        good=data["test_good"],
    )
    assert entry.unit == data["test_good"].unit


def test_amount_argument_is_skipped(setup_budget_test_base):
    """Amount attribute is 0 if the amount argument is skipped."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"])
    assert entry.amount == 0.0


def test_amount_argument_is_set_to_none(setup_budget_test_base):
    """Amount attribute is 0 if the amount argument is set to None."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"], amount=None)
    assert entry.amount == 0.0


def test_amount_attribute_is_set_to_none(setup_budget_test_base):
    """Amount attribute is set to 0 if it is set to None."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"], amount=10.0)
    assert entry.amount == 10.0
    entry.amount = None
    assert entry.amount == 0.0


def test_amount_argument_is_not_a_number(setup_budget_test_base):
    """TypeError is raised if the amount arg not a number."""
    data = setup_budget_test_base
    with pytest.raises(TypeError) as cm:
        BudgetEntry(
            budget=data["test_budget"], good=data["test_good"], amount="some string"
        )
    assert str(cm.value) == "BudgetEntry.amount should be a number, not str"


def test_amount_attribute_is_not_a_number(setup_budget_test_base):
    """TypeError is raised if amount attribute is not a number."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"], amount=10)
    with pytest.raises(TypeError) as cm:
        entry.amount = "some string"
    assert str(cm.value) == "BudgetEntry.amount should be a number, not str"


def test_amount_argument_is_working_properly(setup_budget_test_base):
    """Amount argument value is correctly passed to the amount attribute."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"], amount=10)
    assert entry.amount == 10.0


def test_amount_attribute_is_working_properly(setup_budget_test_base):
    """Amount attribute is working properly."""
    data = setup_budget_test_base
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"], amount=10)
    test_value = 5.0
    assert entry.amount != test_value
    entry.amount = test_value
    assert entry.amount == test_value


def test_good_argument_is_skipped(setup_budget_test_base):
    """TypeError is raised when the good argument is skipped."""
    data = setup_budget_test_base
    with pytest.raises(TypeError) as cm:
        BudgetEntry(budget=data["test_budget"])
    assert (
        str(cm.value) == "BudgetEntry.good should be a stalker.models.budget.Good "
        "instance, not NoneType"
    )


def test_good_argument_is_none(setup_budget_test_base):
    """TypeError is raised when the good argument is None."""
    data = setup_budget_test_base
    with pytest.raises(TypeError) as cm:
        BudgetEntry(
            budget=data["test_budget"],
            good=None,
            amount=53,
        )
    assert (
        str(cm.value) == "BudgetEntry.good should be a stalker.models.budget.Good "
        "instance, not NoneType"
    )


def test_good_attribute_is_set_to_none(setup_budget_test_base):
    """TypeError is raised if the good attribute is set to None."""
    data = setup_budget_test_base
    entry = BudgetEntry(
        budget=data["test_budget"], good=Good(name="Some Good"), amount=53
    )
    with pytest.raises(TypeError) as cm:
        entry.good = None
    assert (
        str(cm.value) == "BudgetEntry.good should be a stalker.models.budget.Good "
        "instance, not NoneType"
    )


def test_good_argument_is_not_a_good_instance(setup_budget_test_base):
    """TypeError is raised when the good argument is not a Good instance."""
    data = setup_budget_test_base
    with pytest.raises(TypeError) as cm:
        _ = BudgetEntry(
            budget=data["test_budget"],
            good="this is not a Good instance",
            amount=53,
        )
    assert (
        str(cm.value) == "BudgetEntry.good should be a stalker.models.budget.Good "
        "instance, not str"
    )


def test_good_attribute_is_not_a_good_instance(setup_budget_test_base):
    """TypeError is raised if the good attribute is not a Good instance."""
    data = setup_budget_test_base
    entry = BudgetEntry(
        budget=data["test_budget"],
        good=data["test_good"],
        amount=53,
    )
    with pytest.raises(TypeError) as cm:
        entry.good = "this is not a Good instance"
    assert (
        str(cm.value) == "BudgetEntry.good should be a stalker.models.budget.Good "
        "instance, not str"
    )


def test_good_argument_is_working_properly(setup_budget_test_base):
    """Good argument value is correctly passed to the good attribute."""
    data = setup_budget_test_base
    test_value = Good(name="Some Good")
    entry = BudgetEntry(
        budget=data["test_budget"],
        good=test_value,
        amount=53,
    )
    assert entry.good == test_value


def test_good_attribute_is_working_properly(setup_budget_test_base):
    """Good attribute can be correctly set."""
    data = setup_budget_test_base
    test_value = Good(name="Some Other Good")
    entry = BudgetEntry(budget=data["test_budget"], good=data["test_good"], amount=53)
    assert entry.good != test_value
    entry.good = test_value
    assert entry.good == test_value


def test_parent_child_relation(setup_budget_test_base):
    """Parent/child relation of Budgets."""
    data = setup_budget_test_base
    b1 = Budget(**data["kwargs"])
    b2 = Budget(**data["kwargs"])
    b2.parent = b1
    assert b1.children == [b2]
