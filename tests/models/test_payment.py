# -*- coding: utf-8 -*-
"""Tests for the Payment class."""

import pytest

from stalker import (
    Budget,
    Client,
    Invoice,
    Payment,
    Project,
    Repository,
    Status,
    StatusList,
    Type,
    User,
)


@pytest.fixture(scope="function")
def setup_payment_tests():
    """Payment class related tests."""
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
        target_entity_type=Project,
    )

    data["test_repository_type"] = Type(
        name="Test Repository Type",
        code="test",
        target_entity_type=Repository,
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

    data["test_invoice"] = Invoice(
        budget=data["test_budget"], client=data["test_client"], amount=1500, unit="TRY"
    )
    return data


def test_creating_a_payment_instance(setup_payment_tests):
    """Payment instance creation."""
    data = setup_payment_tests
    payment = Payment(invoice=data["test_invoice"], amount=1000, unit="TRY")
    assert isinstance(payment, Payment)


def test_invoice_argument_is_skipped(setup_payment_tests):
    """TypeError is raised if the invoice argument is skipped."""
    data = setup_payment_tests
    with pytest.raises(TypeError) as cm:
        _ = Payment(amount=1499, unit="TRY")

    assert str(cm.value) == (
        "Payment.invoice should be an Invoice instance, not NoneType: 'None'"
    )


def test_invoice_argument_is_none(setup_payment_tests):
    """TypeError is raised if the invoice argument is None."""
    with pytest.raises(TypeError) as cm:
        _ = Payment(invoice=None, amount=1499, unit="TRY")

    assert str(cm.value) == (
        "Payment.invoice should be an Invoice instance, not NoneType: 'None'"
    )


def test_invoice_attribute_is_none(setup_payment_tests):
    """TypeError is raised if the invoice attribute is set to None."""
    data = setup_payment_tests
    p = Payment(invoice=data["test_invoice"], amount=1499, unit="TRY")

    with pytest.raises(TypeError) as cm:
        p.invoice = None

    assert str(cm.value) == (
        "Payment.invoice should be an Invoice instance, not NoneType: 'None'"
    )


def test_invoice_argument_is_not_an_invoice_instance():
    """TypeError is raised if the invoice argument is not an Invoice instance."""
    with pytest.raises(TypeError) as cm:
        _ = Payment(invoice="not an invoice instance", amount=1499, unit="TRY")

    assert str(cm.value) == (
        "Payment.invoice should be an Invoice instance, "
        "not str: 'not an invoice instance'"
    )


def test_invoice_attribute_is_set_to_a_value_other_than_an_invoice_instance(
    setup_payment_tests,
):
    """TypeError is raised if the invoice attr is not an Invoice instance."""
    data = setup_payment_tests
    p = Payment(invoice=data["test_invoice"], amount=1499, unit="TRY")

    with pytest.raises(TypeError) as cm:
        p.invoice = "not an invoice instance"

    assert str(cm.value) == (
        "Payment.invoice should be an Invoice instance, "
        "not str: 'not an invoice instance'"
    )


def test_invoice_argument_is_working_properly(setup_payment_tests):
    """invoice argument value is correctly passed to the invoice attribute."""
    data = setup_payment_tests
    p = Payment(invoice=data["test_invoice"], amount=1499, unit="TRY")
    assert p.invoice == data["test_invoice"]


def test_invoice_attribute_is_working_properly(setup_payment_tests):
    """invoice attribute value can be correctly changed."""
    data = setup_payment_tests
    p = Payment(invoice=data["test_invoice"], amount=1499, unit="TRY")
    new_invoice = Invoice(
        budget=data["test_budget"], client=data["test_client"], amount=2500, unit="TRY"
    )
    assert p.invoice != new_invoice
    p.invoice = new_invoice
    assert p.invoice == new_invoice
