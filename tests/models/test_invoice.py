# -*- coding: utf-8 -*-
"""Tests for the Invoice class."""

import datetime

import pytest

import pytz

from stalker import (
    Budget,
    Client,
    Invoice,
    Project,
    Repository,
    Status,
    StatusList,
    Type,
    User,
)


@pytest.fixture(scope="function")
def setup_invoice_tests():
    """Set up invoice class related tests."""
    data = dict()
    data["status_new"] = Status(name="Mew", code="NEW")
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
        name="Task Statuses",
        statuses=[
            data["status_wfd"],
            data["status_rts"],
            data["status_wip"],
            data["status_prev"],
            data["status_hrev"],
            data["status_drev"],
            data["status_oh"],
            data["status_stop"],
            data["status_cmpl"],
        ],
        target_entity_type="Task",
    )

    data["test_project_status_list"] = StatusList(
        name="Project Statuses",
        statuses=[data["status_wip"], data["status_prev"], data["status_cmpl"]],
        target_entity_type=Project,
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

    data["test_client"] = Client(
        name="Test Client",
    )

    data["test_project"] = Project(
        name="Test Project1",
        code="tp1",
        type=data["test_movie_project_type"],
        status_list=data["test_project_status_list"],
        repository=data["test_repository"],
        clients=[data["test_client"]],
    )

    data["test_budget"] = Budget(
        project=data["test_project"],
        name="Test Budget 1",
        status_list=data["budget_status_list"],
    )
    return data


def test_creating_an_invoice_instance(setup_invoice_tests):
    """Creation of an Invoice instance."""
    data = setup_invoice_tests
    invoice = Invoice(
        budget=data["test_budget"],
        amount=1500,
        unit="TL",
        client=data["test_client"],
        date_created=datetime.datetime(2016, 11, 7, tzinfo=pytz.utc),
    )
    assert isinstance(invoice, Invoice)


def test_budget_argument_is_skipped(setup_invoice_tests):
    """TypeError is raised if the budget argument is skipped."""
    data = setup_invoice_tests
    with pytest.raises(TypeError) as cm:
        Invoice(client=data["test_client"], amount=1500, unit="TRY")

    assert str(cm.value) == "Invoice.budget should be a Budget instance, not NoneType"


def test_budget_argument_is_none(setup_invoice_tests):
    """TypeError is raised if the budget argument is None."""
    data = setup_invoice_tests
    with pytest.raises(TypeError) as cm:
        Invoice(budget=None, client=data["test_client"], amount=1500, unit="TRY")
    assert str(cm.value) == "Invoice.budget should be a Budget instance, not NoneType"


def test_budget_attribute_is_set_to_none(setup_invoice_tests):
    """TypeError is raised if the budget attribute is set to None."""
    data = setup_invoice_tests
    test_invoice = Invoice(
        budget=data["test_budget"], client=data["test_client"], amount=1500, unit="TRY"
    )
    with pytest.raises(TypeError) as cm:
        test_invoice.budget = None

    assert str(cm.value) == "Invoice.budget should be a Budget instance, not NoneType"


def test_budget_argument_is_not_a_budget_instance(setup_invoice_tests):
    """TypeError is raised if the Budget argument is not a Budget instance."""
    data = setup_invoice_tests
    with pytest.raises(TypeError) as cm:
        Invoice(
            budget="Not a budget instance",
            client=data["test_client"],
            amount=1500,
            unit="TRY",
        )
    assert str(cm.value) == "Invoice.budget should be a Budget instance, not str"


def test_budget_attribute_is_set_to_a_value_other_than_a_budget_instance(
    setup_invoice_tests,
):
    """TypeError is raised if the Budget attr is not a Budget instance."""
    data = setup_invoice_tests
    test_invoice = Invoice(
        budget=data["test_budget"], client=data["test_client"], amount=1500, unit="TRY"
    )
    with pytest.raises(TypeError) as cm:
        test_invoice.budget = "Not a budget instance"

    assert str(cm.value) == "Invoice.budget should be a Budget instance, not str"


def test_budget_argument_is_working_properly(setup_invoice_tests):
    """budget argument value is properly passed to the budget attribute."""
    data = setup_invoice_tests
    test_invoice = Invoice(
        budget=data["test_budget"], client=data["test_client"], amount=1500, unit="TRY"
    )
    assert test_invoice.budget == data["test_budget"]


def test_client_argument_is_skipped(setup_invoice_tests):
    """TypeError is raised if the client argument is skipped."""
    data = setup_invoice_tests
    with pytest.raises(TypeError) as cm:
        Invoice(budget=data["test_budget"], amount=100, unit="TRY")
    assert str(cm.value) == "Invoice.client should be a Client instance, not NoneType"


def test_client_argument_is_none(setup_invoice_tests):
    """TypeError is raised if the client argument is None."""
    data = setup_invoice_tests
    with pytest.raises(TypeError) as cm:
        Invoice(budget=data["test_budget"], client=None, amount=100, unit="TRY")
    assert str(cm.value) == "Invoice.client should be a Client instance, not NoneType"


def test_client_attribute_is_set_to_none(setup_invoice_tests):
    """TypeError is raised if the client attribute is set to None."""
    data = setup_invoice_tests
    test_invoice = Invoice(
        budget=data["test_budget"], client=data["test_client"], amount=100, unit="TRY"
    )
    with pytest.raises(TypeError) as cm:
        test_invoice.client = None
    assert str(cm.value) == "Invoice.client should be a Client instance, not NoneType"


def test_client_argument_is_not_a_client_instance(setup_invoice_tests):
    """TypeError is raised if the client argument is not a Client instance."""
    data = setup_invoice_tests
    with pytest.raises(TypeError) as cm:
        Invoice(
            budget=data["test_budget"],
            client="not a client instance",
            amount=100,
            unit="TRY",
        )
    assert str(cm.value) == "Invoice.client should be a Client instance, not str"


def test_client_attribute_is_set_to_a_value_other_than_a_client_instance(
    setup_invoice_tests,
):
    """TypeError is raised if the client attr is set to a non Client instance."""
    data = setup_invoice_tests
    test_invoice = Invoice(
        budget=data["test_budget"], client=data["test_client"], amount=100, unit="TRY"
    )
    with pytest.raises(TypeError) as cm:
        test_invoice.client = "not a client instance"
    assert str(cm.value) == "Invoice.client should be a Client instance, not str"


def test_client_argument_is_working_properly(setup_invoice_tests):
    """client argument value is correctly passed to the client attribute."""
    data = setup_invoice_tests
    test_invoice = Invoice(
        budget=data["test_budget"], client=data["test_client"], amount=100, unit="TRY"
    )
    assert test_invoice.client == data["test_client"]


def test_client_attribute_is_working_properly(setup_invoice_tests):
    """client attribute value an be changed properly."""
    data = setup_invoice_tests
    test_invoice = Invoice(
        budget=data["test_budget"], client=data["test_client"], amount=100, unit="TRY"
    )
    test_client = Client(name="Test Client 2")
    assert test_invoice.client != test_client
    test_invoice.client = test_client
    assert test_invoice.client == test_client
