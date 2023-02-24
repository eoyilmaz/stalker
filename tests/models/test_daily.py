# -*- coding: utf-8 -*-
"""Tests for the stalker.models.review.Daily class."""

import pytest

from stalker import (
    Daily,
    DailyLink,
    Link,
    Project,
    Repository,
    Status,
    StatusList,
    Task,
    Version,
)
from stalker.db.session import DBSession


@pytest.fixture(scope="function")
def setup_daily_tests():
    """Set up Daily test data."""
    data = dict()
    data["status_new"] = Status(name="Mew", code="NEW")
    data["status_wfd"] = Status(name="Waiting For Dependency", code="WFD")
    data["status_rts"] = Status(name="Ready To Start", code="RTS")
    data["status_wip"] = Status(name="Work In Progress", code="WIP")
    data["status_prev"] = Status(name="Pending Review", code="PREV")
    data["status_hrev"] = Status(name="Has Revision", code="HREV")
    data["status_drev"] = Status(name="Dependency Has Revision", code="DREV")
    data["status_cmpl"] = Status(name="Completed", code="CMPL")
    data["status_open"] = Status(name="Open", code="OPEN")
    data["status_cls"] = Status(name="Closed", code="CLS")

    data["daily_status_list"] = StatusList(
        name="Daily Statuses",
        statuses=[data["status_open"], data["status_cls"]],
        target_entity_type="Daily",
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
            data["status_cmpl"],
        ],
        target_entity_type="Task",
    )

    data["test_project_status_list"] = StatusList(
        name="Project Statuses",
        target_entity_type="Project",
        statuses=[data["status_new"], data["status_wip"], data["status_cmpl"]],
    )

    data["test_repo"] = Repository(name="Test Repository", code="TR")

    data["test_project"] = Project(
        name="Test Project",
        code="TP",
        repository=data["test_repo"],
        status_list=data["test_project_status_list"],
    )

    data["test_task1"] = Task(
        name="Test Task 1",
        project=data["test_project"],
        status_list=data["task_status_list"],
    )
    data["test_task2"] = Task(
        name="Test Task 2",
        project=data["test_project"],
        status_list=data["task_status_list"],
    )
    data["test_task3"] = Task(
        name="Test Task 3",
        project=data["test_project"],
        status_list=data["task_status_list"],
    )

    data["test_version1"] = Version(task=data["test_task1"])
    data["test_version2"] = Version(task=data["test_task1"])
    data["test_version3"] = Version(task=data["test_task1"])
    data["test_version4"] = Version(task=data["test_task2"])

    data["test_link1"] = Link(original_filename="test_render1.jpg")
    data["test_link2"] = Link(original_filename="test_render2.jpg")
    data["test_link3"] = Link(original_filename="test_render3.jpg")
    data["test_link4"] = Link(original_filename="test_render4.jpg")

    data["test_version1"].outputs = [
        data["test_link1"],
        data["test_link2"],
        data["test_link3"],
    ]
    data["test_version4"].outputs = [data["test_link4"]]
    return data


def test_daily_instance_creation(setup_daily_tests):
    """It is possible to create a Daily without a problem."""
    data = setup_daily_tests
    daily = Daily(
        name="Test Daily",
        project=data["test_project"],
        status_list=data["daily_status_list"],
    )
    assert isinstance(daily, Daily)


def test_links_argument_is_skipped(setup_daily_tests):
    """links attribute is an empty list if the links argument is skipped."""
    data = setup_daily_tests
    daily = Daily(
        name="Test Daily",
        project=data["test_project"],
        status_list=data["daily_status_list"],
    )
    assert daily.links == []


def test_links_argument_is_none(setup_daily_tests):
    """links attribute is an empty list if the links argument is None."""
    data = setup_daily_tests
    daily = Daily(
        name="Test Daily",
        links=None,
        project=data["test_project"],
        status_list=data["daily_status_list"],
    )
    assert daily.links == []


def test_links_attribute_is_set_to_none(setup_daily_tests):
    """TypeError is raised if the links attribute is set to None."""
    data = setup_daily_tests
    daily = Daily(
        name="Test Daily",
        project=data["test_project"],
        status_list=data["daily_status_list"],
    )
    with pytest.raises(TypeError):
        daily.links = None


def test_links_argument_is_not_a_list_instance(setup_daily_tests):
    """TypeError is raised if the links argument is not a list."""
    data = setup_daily_tests
    with pytest.raises(TypeError) as cm:
        Daily(
            name="Test Daily",
            links="not a list of Daily instances",
            project=data["test_project"],
            status_list=data["daily_status_list"],
        )

    assert (
        str(cm.value) == "DailyLink.link should be an instance of "
        "stalker.models.link.Link instance, not str"
    )


def test_links_argument_is_not_a_list_of_link_instances(setup_daily_tests):
    """TypeError is raised if the links argument is not a list of Link instances."""
    data = setup_daily_tests
    with pytest.raises(TypeError) as cm:
        Daily(
            name="Test Daily",
            links=["not", 1, "list", "of", Daily, "instances"],
            project=data["test_project"],
            status_list=data["daily_status_list"],
        )

    assert (
        str(cm.value) == "DailyLink.link should be an instance of "
        "stalker.models.link.Link instance, not str"
    )


def test_links_argument_is_working_properly(setup_daily_tests):
    """links argument value is correctly passed to the links attribute."""
    data = setup_daily_tests
    test_value = [data["test_link1"], data["test_link2"]]
    daily = Daily(
        name="Test Daily",
        links=test_value,
        project=data["test_project"],
        status_list=data["daily_status_list"],
    )
    assert daily.links == test_value


def test_links_attribute_is_working_properly(setup_daily_tests):
    """links attribute is working properly."""
    data = setup_daily_tests
    daily = Daily(
        name="Test Daily",
        project=data["test_project"],
        status_list=data["daily_status_list"],
    )
    daily.links.append(data["test_link1"])

    assert daily.links == [data["test_link1"]]


def test_versions_attribute_is_read_only(setup_daily_tests):
    """versions attribute is a read only attribute."""
    data = setup_daily_tests
    daily = Daily(
        name="Test Daily",
        project=data["test_project"],
        status_list=data["daily_status_list"],
    )
    with pytest.raises(AttributeError):
        setattr(daily, "versions", 10)


@pytest.fixture(scope="function")
def setup_daily_db_tests(setup_postgresql_db):
    """Set up Daily test with a Postgres DB."""
    data = dict()

    data["status_new"] = Status.query.filter_by(code="NEW").first()
    data["status_wfd"] = Status.query.filter_by(code="WFD").first()
    data["status_rts"] = Status.query.filter_by(code="RTS").first()
    data["status_wip"] = Status.query.filter_by(code="WIP").first()
    data["status_prev"] = Status.query.filter_by(code="PREV").first()
    data["status_hrev"] = Status.query.filter_by(code="HREV").first()
    data["status_drev"] = Status.query.filter_by(code="DREV").first()
    data["status_cmpl"] = Status.query.filter_by(code="CMPL").first()

    data["status_open"] = Status.query.filter_by(code="OPEN").first()
    data["status_cls"] = Status.query.filter_by(code="CLS").first()

    data["daily_status_list"] = StatusList.query.filter_by(
        target_entity_type="Daily"
    ).first()

    data["task_status_list"] = StatusList.query.filter_by(
        target_entity_type="Task"
    ).first()

    data["test_repo"] = Repository(name="Test Repository", code="TR")
    DBSession.add(data["test_repo"])

    data["test_project"] = Project(
        name="Test Project",
        code="TP",
        repository=data["test_repo"],
    )
    DBSession.add(data["test_project"])

    data["test_task1"] = Task(
        name="Test Task 1",
        project=data["test_project"],
        status_list=data["task_status_list"],
    )
    DBSession.add(data["test_task1"])
    data["test_task2"] = Task(
        name="Test Task 2",
        project=data["test_project"],
        status_list=data["task_status_list"],
    )
    DBSession.add(data["test_task2"])
    data["test_task3"] = Task(
        name="Test Task 3",
        project=data["test_project"],
        status_list=data["task_status_list"],
    )
    DBSession.add(data["test_task3"])
    DBSession.commit()

    data["test_version1"] = Version(task=data["test_task1"])
    DBSession.add(data["test_version1"])
    DBSession.commit()
    data["test_version2"] = Version(task=data["test_task1"])
    DBSession.add(data["test_version2"])
    DBSession.commit()
    data["test_version3"] = Version(task=data["test_task1"])
    DBSession.add(data["test_version3"])
    DBSession.commit()
    data["test_version4"] = Version(task=data["test_task2"])
    DBSession.add(data["test_version4"])
    DBSession.commit()

    data["test_link1"] = Link(original_filename="test_render1.jpg")
    data["test_link2"] = Link(original_filename="test_render2.jpg")
    data["test_link3"] = Link(original_filename="test_render3.jpg")
    data["test_link4"] = Link(original_filename="test_render4.jpg")
    DBSession.add_all(
        [
            data["test_link1"],
            data["test_link2"],
            data["test_link3"],
            data["test_link4"],
        ]
    )

    data["test_version1"].outputs = [
        data["test_link1"],
        data["test_link2"],
        data["test_link3"],
    ]
    data["test_version4"].outputs = [data["test_link4"]]
    DBSession.commit()
    yield data


def test_tasks_attribute_will_return_a_list_of_tasks(setup_daily_db_tests):
    """tasks attribute is a list of Task instances related to the given links."""
    data = setup_daily_db_tests
    daily = Daily(
        name="Test Daily",
        project=data["test_project"],
        status_list=data["daily_status_list"],
    )
    daily.links = [data["test_link1"], data["test_link2"]]
    DBSession.add(daily)
    DBSession.commit()
    assert daily.tasks == [data["test_task1"]]


def test_versions_attribute_will_return_a_list_of_versions(setup_daily_db_tests):
    """versions attribute is a list of Version instances related to the given links."""
    data = setup_daily_db_tests
    daily = Daily(
        name="Test Daily",
        project=data["test_project"],
        status_list=data["daily_status_list"],
    )
    daily.links = [data["test_link1"], data["test_link2"]]
    DBSession.add(daily)
    DBSession.commit()
    assert daily.versions == [data["test_version1"]]


def test_rank_argument_is_skipped():
    """rank attribute will use the default value is if skipped."""
    dl = DailyLink()
    assert dl.rank == 0


def test_daily_argument_is_not_a_daily_instance(setup_daily_tests):
    """TypeError is raised if the daily argument is not a Daily and not None."""
    with pytest.raises(TypeError) as cm:
        DailyLink(daily="not a daily")

    assert (
        str(cm.value) == "DailyLink.daily should be an instance of "
        "stalker.models.review.Daily instance, not str"
    )
