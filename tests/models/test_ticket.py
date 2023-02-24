# -*- coding: utf-8 -*-
"""Tests for the Ticket class."""

import logging

import pytest

from stalker import log
from stalker import Asset
from stalker import Note
from stalker import Project
from stalker import Repository
from stalker import Status
from stalker import Task
from stalker import Ticket
from stalker import TicketLog
from stalker import Type
from stalker import User
from stalker import Version
from stalker.db.session import DBSession

logger = logging.getLogger("stalker.models.ticket")
logger.setLevel(log.logging_level)


@pytest.fixture(scope="function")
def setup_ticket_tests(setup_postgresql_db):
    """Set up the tests for the Ticket class."""
    data = dict()
    # create statuses
    data["test_status1"] = Status(name="N", code="N")
    data["test_status2"] = Status(name="R", code="R")

    # get the ticket types
    ticket_types = Type.query.filter(Type.target_entity_type == "Ticket").all()
    data["ticket_type_1"] = ticket_types[0]
    data["ticket_type_2"] = ticket_types[1]

    # create a User
    data["test_user"] = User(
        name="Test User", login="test_user1", email="test1@user.com", password="secret"
    )

    # create a Repository
    data["test_repo"] = Repository(name="Test Repo", code="TR")

    # create a Project Type
    data["test_project_type"] = Type(
        name="Commercial Project",
        code="comm",
        target_entity_type="Project",
    )

    # create a Project StatusList
    data["test_project_status1"] = Status(name="PrjStat1", code="PrjStat1")
    data["test_project_status2"] = Status(name="PrjStat2", code="PrjStat2")

    # create a Project
    data["test_project"] = Project(
        name="Test Project 1",
        code="TEST_PROJECT_1",
        type=data["test_project_type"],
        repository=data["test_repo"],
    )
    DBSession.add(data["test_project"])
    DBSession.commit()

    data["test_asset_type"] = Type(
        name="Character Asset", code="char", target_entity_type="Asset"
    )

    data["test_asset"] = Asset(
        name="Test Asset",
        code="ta",
        project=data["test_project"],
        type=data["test_asset_type"],
    )
    DBSession.add(data["test_asset"])
    DBSession.commit()

    # create a Task
    data["test_task"] = Task(
        name="Modeling of Asset 1",
        resources=[data["test_user"]],
        parent=data["test_asset"],
    )
    DBSession.add(data["test_task"])
    DBSession.commit()

    data["test_version"] = Version(
        name="Test Version", task=data["test_task"], version=1, full_path="some/path"
    )

    # create the Ticket
    data["kwargs"] = {
        "project": data["test_project"],
        "links": [data["test_version"]],
        "summary": "This is a test ticket",
        "description": "This is the long description",
        "priority": "TRIVIAL",
        "reported_by": data["test_user"],
    }

    data["test_ticket"] = Ticket(**data["kwargs"])
    DBSession.add(data["test_ticket"])
    DBSession.commit()

    # get the Ticket Statuses
    data["status_new"] = Status.query.filter_by(name="New").first()
    data["status_accepted"] = Status.query.filter_by(name="Accepted").first()
    data["status_assigned"] = Status.query.filter_by(name="Assigned").first()
    data["status_reopened"] = Status.query.filter_by(name="Reopened").first()
    data["status_closed"] = Status.query.filter_by(name="Closed").first()

    return data


def test___auto_name__class_attribute_is_set_to_true():
    """__auto_name__ class attribute is set to True for Ticket class."""
    assert Ticket.__auto_name__ is True


def test_name_argument_is_not_used(setup_ticket_tests):
    """name argument is not used."""
    data = setup_ticket_tests
    test_value = "Test Name"
    data["kwargs"]["name"] = test_value
    new_ticket = Ticket(**data["kwargs"])
    assert new_ticket.name != test_value


def test_name_argument_is_skipped_will_not_raise_error(setup_ticket_tests):
    """name arg skipped an automatically generated name is used."""
    data = setup_ticket_tests
    if "name" in data["kwargs"]:
        data["kwargs"].pop("name")
        # expect no errors
    Ticket(**data["kwargs"])


def test_number_attribute_is_not_created_per_project(setup_ticket_tests):
    """number attr is not per project and uniquely increment for every new ticket."""
    data = setup_ticket_tests
    proj1 = Project(
        name="Test Project 1",
        code="TP1",
        repository=data["test_repo"],
    )

    proj2 = Project(
        name="Test Project 2",
        code="TP2",
        repository=data["test_repo"],
    )

    proj3 = Project(
        name="Test Project 3",
        code="TP3",
        repository=data["test_repo"],
    )

    p1_t1 = Ticket(project=proj1)
    DBSession.add(p1_t1)
    DBSession.commit()
    assert p1_t1.number == 2

    p1_t2 = Ticket(project=proj1)
    DBSession.add(p1_t2)
    DBSession.commit()
    assert p1_t2.number == 3

    p2_t1 = Ticket(project=proj2)
    DBSession.add(p2_t1)
    DBSession.commit()
    assert p2_t1.number == 4

    p1_t3 = Ticket(project=proj1)
    DBSession.add(p1_t3)
    DBSession.commit()
    assert p1_t3.number == 5

    p3_t1 = Ticket(project=proj3)
    DBSession.add(p3_t1)
    DBSession.commit()
    assert p3_t1.number == 6

    p2_t2 = Ticket(project=proj2)
    DBSession.add(p2_t2)
    DBSession.commit()
    assert p2_t2.number == 7

    p3_t2 = Ticket(project=proj3)
    DBSession.add(p3_t2)
    DBSession.commit()
    assert p3_t2.number == 8

    p2_t3 = Ticket(project=proj2)
    DBSession.add(p2_t3)
    DBSession.commit()
    assert p2_t3.number == 9


def test_number_attribute_is_read_only(setup_ticket_tests):
    """number attribute is read-only."""
    data = setup_ticket_tests
    with pytest.raises(AttributeError) as cm:
        data["test_ticket"].number = 234

    assert str(cm.value) == "can't set attribute"


def test_number_attribute_is_automatically_increased(setup_ticket_tests):
    """number attribute is automatically increased."""
    data = setup_ticket_tests
    # create two new tickets
    ticket1 = Ticket(**data["kwargs"])
    DBSession.add(ticket1)
    DBSession.commit()

    ticket2 = Ticket(**data["kwargs"])
    DBSession.add(ticket2)
    DBSession.commit()

    assert ticket1.number + 1 == ticket2.number
    assert ticket1.number == 2
    assert ticket2.number == 3


def test_links_argument_accepts_anything_derived_from_simple_entity(setup_ticket_tests):
    """links accepting anything derived from SimpleEntity."""
    data = setup_ticket_tests
    data["kwargs"]["links"] = [
        data["test_project"],
        data["test_project_status1"],
        data["test_project_status2"],
        data["test_repo"],
        data["test_version"],
    ]

    new_ticket = Ticket(**data["kwargs"])
    assert sorted(data["kwargs"]["links"], key=lambda x: x.name) == sorted(
        new_ticket.links, key=lambda x: x.name
    )


def test_links_attribute_accepts_anything_derived_from_simple_entity(
    setup_ticket_tests,
):
    """links attribute is accepting anything derived from SimpleEntity."""
    data = setup_ticket_tests
    links = [
        data["test_project"],
        data["test_project_status1"],
        data["test_project_status2"],
        data["test_repo"],
        data["test_version"],
    ]
    data["test_ticket"].links = links
    assert sorted(links, key=lambda x: x.name) == sorted(
        data["test_ticket"].links, key=lambda x: x.name
    )


def test_related_tickets_attribute_is_an_empty_list_on_init(setup_ticket_tests):
    """related_tickets attribute is an empty list on init."""
    data = setup_ticket_tests
    assert data["test_ticket"].related_tickets == []


def test_related_tickets_attribute_is_set_to_something_other_then_a_list_of_tickets(
    setup_ticket_tests,
):
    """TypeError raised if the related_tickets attr is not a list of Tickets."""
    data = setup_ticket_tests
    with pytest.raises(TypeError) as cm:
        data["test_ticket"].related_tickets = ["a ticket"]

    assert (
        str(cm.value) == "Ticket.related_ticket attribute should be a list of other "
        "stalker.models.ticket.Ticket instances not str"
    )


def test_related_tickets_attribute_accepts_list_of_ticket_instances(setup_ticket_tests):
    """related tickets attr accepts only list of Ticket instances."""
    data = setup_ticket_tests
    new_ticket1 = Ticket(**data["kwargs"])
    DBSession.add(new_ticket1)
    DBSession.commit()

    new_ticket2 = Ticket(**data["kwargs"])
    DBSession.add(new_ticket2)
    DBSession.commit()

    data["test_ticket"].related_tickets = [new_ticket1, new_ticket2]


def test_related_ticket_attribute_will_not_accept_self(setup_ticket_tests):
    """related_tickets attr don't accept the Ticket itself and raises ValueError."""
    data = setup_ticket_tests
    with pytest.raises(ValueError) as cm:
        data["test_ticket"].related_tickets = [data["test_ticket"]]

    assert (
        str(cm.value) == "Ticket.related_ticket attribute can not "
        "have itself in the list"
    )


def test_priority_argument_is_skipped_will_set_it_to_zero(setup_ticket_tests):
    """priority arg is skipped will set the priority of the Ticket to 0 or TRIVIAL."""
    data = setup_ticket_tests
    data["kwargs"].pop("priority")
    new_ticket = Ticket(**data["kwargs"])
    assert new_ticket.priority == "TRIVIAL"


def test_comments_attribute_is_synonym_for_notes_attribute(setup_ticket_tests):
    """comments attr is the synonym for the notes attr."""
    data = setup_ticket_tests
    note1 = Note(name="Test Note 1", content="Test note 1")
    note2 = Note(name="Test Note 2", content="Test note 2")

    data["test_ticket"].comments.append(note1)
    data["test_ticket"].comments.append(note2)

    assert note1 in data["test_ticket"].notes
    assert note2 in data["test_ticket"].notes

    data["test_ticket"].notes.remove(note1)
    assert note1 not in data["test_ticket"].comments

    data["test_ticket"].notes.remove(note2)
    assert note2 not in data["test_ticket"].comments


def test_reported_by_attribute_is_synonym_of_created_by(setup_ticket_tests):
    """reported_by attribute is a synonym for the created_by attribute."""
    data = setup_ticket_tests
    user1 = User(name="user1", login="user1", password="secret", email="user1@test.com")
    data["test_ticket"].reported_by = user1
    assert user1 == data["test_ticket"].created_by


def test_status_for_newly_created_tickets_will_be_new_if_skipped(setup_ticket_tests):
    """status of newly created tickets New."""
    data = setup_ticket_tests
    # get the status NEW from the session
    new_ticket = Ticket(**data["kwargs"])
    assert new_ticket.status == data["status_new"]


def test_project_argument_is_skipped(setup_ticket_tests):
    """TypeError raised if the project argument is skipped."""
    data = setup_ticket_tests
    data["kwargs"].pop("project")
    with pytest.raises(TypeError) as cm:
        Ticket(**data["kwargs"])

    assert (
        str(cm.value) == "Ticket.project should be an instance of "
        "stalker.models.project.Project, not NoneType"
    )


def test_project_argument_is_none(setup_ticket_tests):
    """TypeError raised if the project argument is None."""
    data = setup_ticket_tests
    data["kwargs"]["project"] = None
    with pytest.raises(TypeError) as cm:
        Ticket(**data["kwargs"])

    assert (
        str(cm.value) == "Ticket.project should be an instance of "
        "stalker.models.project.Project, not NoneType"
    )


def test_project_argument_accepts_project_instances_only(setup_ticket_tests):
    """project argument accepts Project instances only."""
    data = setup_ticket_tests
    data["kwargs"]["project"] = "Not a Project instance"
    with pytest.raises(TypeError) as cm:
        Ticket(**data["kwargs"])

    assert (
        str(cm.value) == "Ticket.project should be an instance of "
        "stalker.models.project.Project, not str"
    )


def test_project_argument_is_working_properly(setup_ticket_tests):
    """project argument is working properly."""
    data = setup_ticket_tests
    data["kwargs"]["project"] = data["test_project"]
    new_ticket = Ticket(**data["kwargs"])
    assert new_ticket.project == data["test_project"]


def test_project_attribute_is_read_only(setup_ticket_tests):
    """project attribute is read only."""
    data = setup_ticket_tests
    with pytest.raises(AttributeError) as cm:
        data["test_ticket"].project = data["test_project"]

    assert str(cm.value) == "can't set attribute"


# STATUSES

# resolve
def test_resolve_method_will_change_the_status_from_new_to_closed_and_creates_a_log(
    setup_ticket_tests,
):
    """resolve action changes Ticket status from New to Closed."""
    data = setup_ticket_tests
    assert data["test_ticket"].status == data["status_new"]
    ticket_log = data["test_ticket"].resolve()
    assert data["test_ticket"].status == data["status_closed"]
    assert ticket_log.from_status == data["status_new"]
    assert ticket_log.to_status == data["status_closed"]
    assert ticket_log.action == "resolve"


def test_resolve_method_will_change_the_status_from_accepted_to_closed(
    setup_ticket_tests,
):
    """resolve action changes Ticket status from Accepted to Closed."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_accepted"]
    assert data["test_ticket"].status == data["status_accepted"]
    ticket_log = data["test_ticket"].resolve()
    assert data["test_ticket"].status == data["status_closed"]
    assert ticket_log.from_status == data["status_accepted"]
    assert ticket_log.to_status == data["status_closed"]
    assert ticket_log.action == "resolve"


def test_resolve_method_will_change_the_status_from_assigned_to_closed(
    setup_ticket_tests,
):
    """resolve action changes Ticket status from Assigned to Closed."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_assigned"]
    assert data["test_ticket"].status == data["status_assigned"]
    ticket_log = data["test_ticket"].resolve()
    assert data["test_ticket"].status == data["status_closed"]
    assert ticket_log.from_status == data["status_assigned"]
    assert ticket_log.to_status == data["status_closed"]
    assert ticket_log.action == "resolve"


def test_resolve_method_will_change_the_status_from_reopened_to_closed(
    setup_ticket_tests,
):
    """accept action changes Ticket status from Reopened to closed."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_reopened"]
    assert data["test_ticket"].status == data["status_reopened"]
    ticket_log = data["test_ticket"].resolve()
    assert data["test_ticket"].status == data["status_closed"]
    assert ticket_log.from_status == data["status_reopened"]
    assert ticket_log.to_status == data["status_closed"]
    assert ticket_log.action == "resolve"


def test_resolve_method_will_not_change_the_status_from_closed_to_anything(
    setup_ticket_tests,
):
    """resolve action don't change Ticket status from Closed to anything."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_closed"]
    assert data["test_ticket"].status == data["status_closed"]
    ticket_log = data["test_ticket"].resolve()
    assert ticket_log is None
    assert data["test_ticket"].status == data["status_closed"]


# reopen
def test_reopen_method_will_not_change_the_status_from_new_to_anything(
    setup_ticket_tests,
):
    """reopen action will not change Ticket status from New to anything."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_new"]
    assert data["test_ticket"].status == data["status_new"]
    ticket_log = data["test_ticket"].reopen()
    assert ticket_log is None
    assert data["test_ticket"].status == data["status_new"]


def test_reopen_method_will_not_change_the_status_from_accepted_to_anything(
    setup_ticket_tests,
):
    """reopen action will not change Ticket status from Accepted to anything."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_accepted"]
    assert data["test_ticket"].status == data["status_accepted"]
    ticket_log = data["test_ticket"].reopen()
    assert ticket_log is None
    assert data["test_ticket"].status == data["status_accepted"]


def test_reopen_method_will_not_change_the_status_from_assigned_to_anything(
    setup_ticket_tests,
):
    """reopen action will not change Ticket status from Assigned to anything."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_assigned"]
    assert data["test_ticket"].status == data["status_assigned"]
    ticket_log = data["test_ticket"].reopen()
    assert ticket_log is None
    assert data["test_ticket"].status == data["status_assigned"]


def test_reopen_method_will_not_change_the_status_from_reopened_to_anything(
    setup_ticket_tests,
):
    """reopen action will not change Ticket status from Reopened to anything."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_reopened"]
    assert data["test_ticket"].status == data["status_reopened"]
    ticket_log = data["test_ticket"].reopen()
    assert ticket_log is None
    assert data["test_ticket"].status == data["status_reopened"]


def test_reopen_method_will_change_the_status_from_closed_to_reopened(
    setup_ticket_tests,
):
    """reopen action changes Ticket status from Closed to "Reopened"."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_closed"]
    assert data["test_ticket"].status == data["status_closed"]
    ticket_log = data["test_ticket"].reopen()
    assert data["test_ticket"].status == data["status_reopened"]
    assert ticket_log.from_status == data["status_closed"]
    assert ticket_log.to_status == data["status_reopened"]
    assert ticket_log.action == "reopen"


# accept
def test_accept_method_will_change_the_status_from_new_to_accepted(setup_ticket_tests):
    """accept action changes Ticket status from New to Accepted."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_new"]
    assert data["test_ticket"].status == data["status_new"]
    ticket_log = data["test_ticket"].accept()
    assert data["test_ticket"].status == data["status_accepted"]
    assert ticket_log.from_status == data["status_new"]
    assert ticket_log.to_status == data["status_accepted"]
    assert ticket_log.action == "accept"


def test_accept_method_will_change_the_status_from_accepted_to_accepted(
    setup_ticket_tests,
):
    """accept action changes Ticket status from Accepted to Accepted."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_accepted"]
    assert data["test_ticket"].status == data["status_accepted"]
    ticket_log = data["test_ticket"].accept()
    assert data["test_ticket"].status == data["status_accepted"]
    assert ticket_log.from_status == data["status_accepted"]
    assert ticket_log.to_status == data["status_accepted"]
    assert ticket_log.action == "accept"


def test_accept_method_will_change_the_status_from_assigned_to_accepted(
    setup_ticket_tests,
):
    """accept action changes Ticket status from Assigned to Accepted."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_assigned"]
    assert data["test_ticket"].status == data["status_assigned"]
    ticket_log = data["test_ticket"].accept()
    assert data["test_ticket"].status == data["status_accepted"]
    assert ticket_log.from_status == data["status_assigned"]
    assert ticket_log.to_status == data["status_accepted"]
    assert ticket_log.action == "accept"


def test_accept_method_will_change_the_status_from_reopened_to_accepted(
    setup_ticket_tests,
):
    """accept action changes Ticket status from Reopened to Accepted."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_reopened"]
    assert data["test_ticket"].status == data["status_reopened"]
    ticket_log = data["test_ticket"].accept()
    assert data["test_ticket"].status == data["status_accepted"]
    assert ticket_log.from_status == data["status_reopened"]
    assert ticket_log.to_status == data["status_accepted"]
    assert ticket_log.action == "accept"


def test_accept_method_will_not_change_the_status_of_closed_to_anything(
    setup_ticket_tests,
):
    """accept action will not change Ticket status from Closed to Anything."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_closed"]
    assert data["test_ticket"].status == data["status_closed"]
    ticket_log = data["test_ticket"].accept()
    assert ticket_log is None
    assert data["test_ticket"].status == data["status_closed"]


# reassign
def test_reassign_method_will_change_the_status_from_new_to_assigned(
    setup_ticket_tests,
):
    """reassign action changes Ticket status from New to Assigned."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_new"]
    assert data["test_ticket"].status == data["status_new"]
    ticket_log = data["test_ticket"].reassign()
    assert data["test_ticket"].status == data["status_assigned"]
    assert ticket_log.from_status == data["status_new"]
    assert ticket_log.to_status == data["status_assigned"]
    assert ticket_log.action == "reassign"


def test_reassign_method_will_change_the_status_from_accepted_to_assigned(
    setup_ticket_tests,
):
    """reassign action changes Ticket status from Accepted to Accepted."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_accepted"]
    assert data["test_ticket"].status == data["status_accepted"]
    ticket_log = data["test_ticket"].reassign()
    assert data["test_ticket"].status == data["status_assigned"]
    assert ticket_log.from_status == data["status_accepted"]
    assert ticket_log.to_status == data["status_assigned"]
    assert ticket_log.action == "reassign"


def test_reassign_method_will_change_the_status_from_assigned_to_assigned(
    setup_ticket_tests,
):
    """reassign action changes Ticket status from Assigned to Accepted."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_assigned"]
    assert data["test_ticket"].status == data["status_assigned"]
    ticket_log = data["test_ticket"].reassign()
    assert data["test_ticket"].status == data["status_assigned"]
    assert ticket_log.from_status == data["status_assigned"]
    assert ticket_log.to_status == data["status_assigned"]
    assert ticket_log.action == "reassign"


def test_reassign_method_will_change_the_status_from_reopened_to_assigned(
    setup_ticket_tests,
):
    """accept action changes Ticket status from Reopened to Assigned."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_reopened"]
    assert data["test_ticket"].status == data["status_reopened"]
    ticket_log = data["test_ticket"].reassign()
    assert data["test_ticket"].status == data["status_assigned"]
    assert ticket_log.from_status == data["status_reopened"]
    assert ticket_log.to_status == data["status_assigned"]
    assert ticket_log.action == "reassign"


def test_reassign_method_will_not_change_the_status_of_closed_to_anything(
    setup_ticket_tests,
):
    """reassign action will not change Ticket status from Closed to Anything."""
    data = setup_ticket_tests
    data["test_ticket"].status = data["status_closed"]
    assert data["test_ticket"].status == data["status_closed"]
    ticket_log = data["test_ticket"].reassign()
    assert ticket_log is None
    assert data["test_ticket"].status == data["status_closed"]


def test_resolve_method_will_set_the_resolution(setup_ticket_tests):
    """resolve action changes Ticket status from New to Closed."""
    data = setup_ticket_tests
    assert data["test_ticket"].status == data["status_new"]
    ticket_log = data["test_ticket"].resolve(resolution="fixed")
    assert data["test_ticket"].status == data["status_closed"]
    assert ticket_log.from_status == data["status_new"]
    assert ticket_log.to_status == data["status_closed"]
    assert ticket_log.action == "resolve"
    assert data["test_ticket"].resolution == "fixed"


def test_reopen_will_clear_resolution(setup_ticket_tests):
    """reopen method will clear the timing_resolution."""
    data = setup_ticket_tests
    assert data["test_ticket"].status == data["status_new"]
    data["test_ticket"].resolve(resolution="fixed")
    assert data["test_ticket"].resolution == "fixed"
    ticket_log = data["test_ticket"].reopen()
    assert isinstance(ticket_log, TicketLog)
    assert data["test_ticket"].resolution == ""


def test_reassign_will_set_the_owner(setup_ticket_tests):
    """reassign method will set the owner."""
    data = setup_ticket_tests
    assert data["test_ticket"].status == data["status_new"]
    assert data["test_ticket"].owner != data["test_user"]
    ticket_log = data["test_ticket"].reassign(assign_to=data["test_user"])
    assert isinstance(ticket_log, TicketLog)
    assert data["test_ticket"].owner == data["test_user"]


def test_accept_will_set_the_owner(setup_ticket_tests):
    """accept method will set the owner."""
    data = setup_ticket_tests
    assert data["test_ticket"].status == data["status_new"]
    assert data["test_ticket"].owner != data["test_user"]
    ticket_log = data["test_ticket"].accept(created_by=data["test_user"])
    assert isinstance(ticket_log, TicketLog)
    assert data["test_ticket"].owner == data["test_user"]


def test_summary_argument_skipped(setup_ticket_tests):
    """summary argument can be skipped."""
    data = setup_ticket_tests
    try:
        data["kwargs"].pop("summary")
    except KeyError:
        pass
    new_ticket = Ticket(**data["kwargs"])
    assert new_ticket.summary == ""


def test_summary_argument_can_be_none(setup_ticket_tests):
    """summary argument can be None."""
    data = setup_ticket_tests
    data["kwargs"]["summary"] = None
    new_ticket = Ticket(**data["kwargs"])
    assert new_ticket.summary == ""


def test_summary_attribute_can_be_set_to_none(setup_ticket_tests):
    """summary attribute can be set to None."""
    data = setup_ticket_tests
    data["test_ticket"].summary = None
    assert data["test_ticket"].summary == ""


def test_summary_argument_is_not_a_string(setup_ticket_tests):
    """TypeError raised if the summary argument value is not a str."""
    data = setup_ticket_tests
    data["kwargs"]["summary"] = ["not a string instance"]
    with pytest.raises(TypeError) as cm:
        Ticket(data["kwargs"])

    assert (
        str(cm.value) == "Ticket.project should be an instance of "
        "stalker.models.project.Project, not dict"
    )


def test_summary_attribute_is_set_to_a_value_other_than_a_string(setup_ticket_tests):
    """summary attribute is set to a value other than a str."""
    data = setup_ticket_tests
    with pytest.raises(TypeError) as cm:
        data["test_ticket"].summary = ["not a string"]

    assert str(cm.value) == "Ticket.summary should be an instance of str, not list"


def test_summary_argument_is_working_properly(setup_ticket_tests):
    """summary argument value is passed to summary attribute correctly."""
    data = setup_ticket_tests
    test_value = "test summary"
    data["kwargs"]["summary"] = test_value
    new_ticket = Ticket(**data["kwargs"])
    assert new_ticket.summary == test_value


def test_summary_attribute_is_working_properly(setup_ticket_tests):
    """summary attribute is working properly."""
    data = setup_ticket_tests
    test_value = "test_summary"
    assert data["test_ticket"].summary != test_value
    data["test_ticket"].summary = test_value
    assert data["test_ticket"].summary == test_value
