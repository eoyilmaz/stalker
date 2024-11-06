# -*- coding: utf-8 -*-
"""Tests related to Review class."""

import datetime
import sys

import pytest

import pytz

from stalker import Project, Repository, Review, Status, Structure, Task, User
from stalker.db.session import DBSession


@pytest.fixture(scope="function")
def setup_review_db_test(setup_postgresql_db):
    """Set up the tests for stalker.models.review.Review class with a DB."""
    data = dict()
    data["user1"] = User(
        name="Test User 1",
        login="test_user1",
        email="test1@user.com",
        password="secret",
    )
    DBSession.add(data["user1"])

    data["user2"] = User(
        name="Test User 2",
        login="test_user2",
        email="test2@user.com",
        password="secret",
    )
    DBSession.add(data["user2"])

    data["user3"] = User(
        name="Test User 2",
        login="test_user3",
        email="test3@user.com",
        password="secret",
    )
    DBSession.add(data["user3"])

    # Review Statuses
    with DBSession.no_autoflush:
        data["status_new"] = Status.query.filter_by(code="NEW").first()
        data["status_rrev"] = Status.query.filter_by(code="RREV").first()
        data["status_app"] = Status.query.filter_by(code="APP").first()

        # Task Statuses
        data["status_wfd"] = Status.query.filter_by(code="WFD").first()
        data["status_rts"] = Status.query.filter_by(code="RTS").first()
        data["status_wip"] = Status.query.filter_by(code="WIP").first()
        data["status_prev"] = Status.query.filter_by(code="PREV").first()
        data["status_hrev"] = Status.query.filter_by(code="HREV").first()
        data["status_drev"] = Status.query.filter_by(code="DREV").first()
        data["status_cmpl"] = Status.query.filter_by(code="CMPL").first()

    data["repo"] = Repository(
        name="Test Repository",
        code="TR",
        linux_path="/mnt/T/",
        windows_path="T:/",
        macos_path="/Volumes/T/",
    )
    DBSession.add(data["repo"])

    data["structure"] = Structure(name="Test Project Structure")
    DBSession.add(data["structure"])

    data["project"] = Project(name="Test Project", code="TP", repository=data["repo"])
    DBSession.add(data["project"])

    data["task1"] = Task(
        name="Test Task 1",
        project=data["project"],
        resources=[data["user1"]],
        responsible=[data["user2"]],
    )
    DBSession.add(data["task1"])

    data["task2"] = Task(
        name="Test Task 2", project=data["project"], responsible=[data["user1"]]
    )
    DBSession.add(data["task2"])

    data["task3"] = Task(
        name="Test Task 3", parent=data["task2"], resources=[data["user1"]]
    )
    DBSession.add(data["task3"])

    data["task4"] = Task(
        name="Test Task 4",
        project=data["project"],
        resources=[data["user1"]],
        depends_on=[data["task3"]],
        responsible=[data["user2"]],
        schedule_timing=2,
        schedule_unit="h",
    )
    DBSession.add(data["task4"])

    data["task5"] = Task(
        name="Test Task 5",
        project=data["project"],
        resources=[data["user2"]],
        depends_on=[data["task3"]],
        responsible=[data["user2"]],
        schedule_timing=2,
        schedule_unit="h",
    )
    DBSession.add(data["task5"])

    data["task6"] = Task(
        name="Test Task 6",
        project=data["project"],
        resources=[data["user3"]],
        depends_on=[data["task3"]],
        responsible=[data["user2"]],
        schedule_timing=2,
        schedule_unit="h",
    )
    DBSession.add(data["task6"])
    data["kwargs"] = {"task": data["task1"], "reviewer": data["user1"]}
    # add everything to the db
    DBSession.commit()
    return data


def test_task_argument_is_not_a_task_instance(setup_review_db_test):
    """TypeError is raised if the task argument value is not a Task instance."""
    data = setup_review_db_test
    data["kwargs"]["task"] = "not a Task instance"
    with pytest.raises(TypeError) as cm:
        Review(**data["kwargs"])

    assert (
        str(cm.value)
        == "Review.task should be an instance of stalker.models.task.Task, "
        "not str: 'not a Task instance'"
    )


def test_task_argument_is_not_a_leaf_task(setup_review_db_test):
    """ValueError is raised if the task given in task argument is not a leaf task."""
    data = setup_review_db_test
    task1 = Task(name="Task1", project=data["project"])
    task2 = Task(name="Task2", parent=task1)
    data["kwargs"]["task"] = task1
    with pytest.raises(ValueError) as cm:
        Review(**data["kwargs"])

    assert (
        str(cm.value) == "It is only possible to create a review for a leaf tasks, and "
        "<Task1 (Task)> is not a leaf task."
    )


def test_task_argument_is_working_as_expected(setup_review_db_test):
    """task argument value is passed to the task argument."""
    data = setup_review_db_test
    now = datetime.datetime.now(pytz.utc)
    data["task1"].create_time_log(
        resource=data["task1"].resources[0],
        start=now,
        end=now + datetime.timedelta(hours=1),
    )
    reviews = data["task1"].request_review()
    assert reviews[0].task == data["task1"]


def test_auto_name_is_true():
    """review instances are named automatically."""
    assert Review.__auto_name__ is True


def test_status_is_new_for_a_newly_created_review_instance(setup_review_db_test):
    """status is NEW for a newly created review instance."""
    data = setup_review_db_test
    review = Review(**data["kwargs"])
    assert review.status == data["status_new"]


def test_review_number_attribute_is_a_read_only_attribute(setup_review_db_test):
    """review_number attribute is a read only attribute."""
    data = setup_review_db_test
    review = Review(**data["kwargs"])
    with pytest.raises(AttributeError) as cm:
        review.review_number = 2

    error_message = {
        8: "can't set attribute",
        9: "can't set attribute",
        10: "can't set attribute",
        11: "property of 'Review' object has no setter",
        12: "property of 'Review' object has no setter",
    }.get(
        sys.version_info.minor,
        "property '_review_number_getter' of 'Review' object has no setter",
    )

    assert str(cm.value) == error_message


def test_review_number_attribute_is_initialized_to_the_task_review_number_plus_1(
    setup_review_db_test,
):
    """review_number attribute is initialized with task.review_number + 1."""
    data = setup_review_db_test
    review = Review(**data["kwargs"])
    assert review.review_number == 1


def test_review_number_for_multiple_responsible_task_is_equal_to_each_other(
    setup_review_db_test,
):
    """Review.review_number for a task with multiple responsible equal to each other."""
    data = setup_review_db_test
    data["task1"].responsible = [data["user1"], data["user2"], data["user3"]]

    now = datetime.datetime.now(pytz.utc)
    data["task1"].create_time_log(
        resource=data["task1"].resources[0],
        start=now,
        end=now + datetime.timedelta(hours=1),
    )
    reviews = data["task1"].request_review()
    expected_review_number = data["task1"].review_number + 1

    assert len(reviews) == 3
    assert reviews[0].review_number == expected_review_number
    assert reviews[1].review_number == expected_review_number
    assert reviews[2].review_number == expected_review_number


def test_reviewer_argument_is_skipped(setup_review_db_test):
    """TypeError is raised if the reviewer argument is skipped."""
    data = setup_review_db_test
    data["kwargs"].pop("reviewer")
    with pytest.raises(TypeError) as cm:
        Review(**data["kwargs"])
    assert (
        str(cm.value) == "Review.reviewer should be set to a stalker.models.auth.User "
        "instance, not NoneType: 'None'"
    )


def test_reviewer_argument_is_none(setup_review_db_test):
    """TypeError is raised if the reviewer argument is None."""
    data = setup_review_db_test
    data["kwargs"]["reviewer"] = None
    with pytest.raises(TypeError) as cm:
        Review(**data["kwargs"])
    assert (
        str(cm.value) == "Review.reviewer should be set to a stalker.models.auth.User "
        "instance, not NoneType: 'None'"
    )


def test_reviewer_attribute_is_set_to_none(setup_review_db_test):
    """TypeError is raised if the reviewer attribute is set to None."""
    data = setup_review_db_test
    review = Review(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        review.reviewer = None
    assert (
        str(cm.value) == "Review.reviewer should be set to a stalker.models.auth.User "
        "instance, not NoneType: 'None'"
    )


def test_reviewer_argument_is_not_a_user_instance(setup_review_db_test):
    """TypeError is raised if the reviewer argument is not a User instance."""
    data = setup_review_db_test
    data["kwargs"]["reviewer"] = "not a user instance"
    with pytest.raises(TypeError) as cm:
        Review(**data["kwargs"])
    assert (
        str(cm.value) == "Review.reviewer should be set to a stalker.models.auth.User "
        "instance, not str: 'not a user instance'"
    )


def test_reviewer_attribute_is_not_a_user_instance(setup_review_db_test):
    """TypeError is raised if the reviewer attr is not a User instance."""
    data = setup_review_db_test
    review = Review(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        review.reviewer = "not a user"
    assert (
        str(cm.value) == "Review.reviewer should be set to a stalker.models.auth.User "
        "instance, not str: 'not a user'"
    )


def test_reviewer_argument_is_not_in_task_responsible_list(setup_review_db_test):
    """A user not listed in Task.responsible can be reviewer."""
    data = setup_review_db_test
    data["task1"].responsible = [data["user1"]]
    data["kwargs"]["reviewer"] = data["user2"]
    review = Review(**data["kwargs"])
    assert review.reviewer == data["user2"]


def test_reviewer_attribute_is_not_in_task_responsible_list(setup_review_db_test):
    """A user not listed in Task.responsible can be reviewer."""
    data = setup_review_db_test
    data["task1"].responsible = [data["user1"]]
    data["kwargs"]["reviewer"] = data["user1"]
    review = Review(**data["kwargs"])
    review.reviewer = data["user2"]
    assert review.reviewer == data["user2"]


def test_reviewer_argument_is_working_as_expected(setup_review_db_test):
    """reviewer argument value is correctly passed to reviewer attribute."""
    data = setup_review_db_test
    data["task1"].responsible = [data["user1"]]
    data["kwargs"]["reviewer"] = data["user1"]
    review = Review(**data["kwargs"])
    assert review.reviewer == data["user1"]


def test_reviewer_attribute_is_working_as_expected(setup_review_db_test):
    """reviewer attribute is working as expected."""
    data = setup_review_db_test
    data["task1"].responsible = [data["user1"], data["user2"]]
    data["kwargs"]["reviewer"] = data["user1"]
    review = Review(**data["kwargs"])
    review.reviewer = data["user2"]
    assert review.reviewer == data["user2"]


# TODO: Add tests for the same user is being the reviewer for all reviews at the same
#       level with same task.


def test_approve_method_updates_task_status_correctly_for_a_single_responsible_task(
    setup_review_db_test,
):
    """approve() updates status correctly for a task with only one responsible."""
    data = setup_review_db_test
    data["task1"].responsible = [data["user1"]]
    data["kwargs"]["reviewer"] = data["user1"]
    assert data["task1"].status != data["status_cmpl"]
    review = Review(**data["kwargs"])
    review.approve()
    assert data["task1"].status == data["status_cmpl"]


def test_approve_method_updates_task_status_correctly_for_a_multi_responsible_task_if_all_approve(
    setup_review_db_test,
):
    """approve() updates status correctly for a task with multiple responsible."""
    data = setup_review_db_test
    data["task1"].responsible = [data["user1"], data["user2"]]
    now = datetime.datetime.now(pytz.utc)
    data["task1"].create_time_log(
        resource=data["user1"], start=now, end=now + datetime.timedelta(hours=1)
    )

    reviews = data["task1"].request_review()
    review1 = reviews[0]
    review2 = reviews[1]

    review1.approve()
    # still pending review
    assert data["task1"].status == data["status_prev"]

    # first reviewer
    review2.approve()
    assert data["task1"].status == data["status_cmpl"]


def test_approve_method_updates_task_parent_status(setup_review_db_test):
    """approve() updates the task parent status."""
    data = setup_review_db_test
    data["task3"].status = data["status_rts"]
    now = datetime.datetime.now(pytz.utc)
    td = datetime.timedelta
    data["task3"].create_time_log(
        resource=data["task3"].resources[0], start=now, end=now + td(hours=1)
    )

    reviews = data["task3"].request_review()
    assert data["task3"].status == data["status_prev"]

    review1 = reviews[0]
    review1.approve()

    assert data["task3"].status == data["status_cmpl"]
    assert data["task2"].status == data["status_cmpl"]


def test_approve_method_updates_task_dependent_statuses(setup_review_db_test):
    """approve() updates the task dependent statuses."""
    data = setup_review_db_test
    data["task3"].status = data["status_rts"]
    now = datetime.datetime.now(pytz.utc)
    td = datetime.timedelta
    data["task3"].create_time_log(
        resource=data["task3"].resources[0], start=now, end=now + td(hours=1)
    )

    reviews = data["task3"].request_review()
    assert data["task3"].status == data["status_prev"]
    review1 = reviews[0]
    review1.approve()

    assert data["task3"].status == data["status_cmpl"]
    assert data["task4"].status == data["status_rts"]
    assert data["task5"].status == data["status_rts"]
    assert data["task6"].status == data["status_rts"]

    # create time logs for task4 to make it wip
    data["task4"].create_time_log(
        resource=data["task4"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    assert data["task4"].status == data["status_wip"]

    # now request revision to task3
    data["task3"].request_revision(reviewer=data["task3"].responsible[0])

    # check statuses of task4 and task4
    assert data["task4"].status == data["status_drev"]
    assert data["task5"].status == data["status_wfd"]
    assert data["task6"].status == data["status_wfd"]

    # now approve task3
    reviews = data["task3"].review_set()
    for rev in reviews:
        rev.approve()

    # check the task statuses again
    assert data["task4"].status == data["status_hrev"]
    assert data["task5"].status == data["status_rts"]
    assert data["task5"].status == data["status_rts"]


def test_approve_method_updates_task_dependent_timings(setup_review_db_test):
    """approve updates the task dependent timings for DREV tasks with no effort left."""
    data = setup_review_db_test
    data["task3"].status = data["status_rts"]
    now = datetime.datetime.now(pytz.utc)
    td = datetime.timedelta
    data["task3"].create_time_log(
        resource=data["task3"].resources[0], start=now, end=now + td(hours=1)
    )
    reviews = data["task3"].request_review()
    assert data["task3"].status == data["status_prev"]

    review1 = reviews[0]
    review1.approve()

    assert data["task3"].status == data["status_cmpl"]
    assert data["task4"].status == data["status_rts"]
    assert data["task5"].status == data["status_rts"]
    assert data["task6"].status == data["status_rts"]

    # create time logs for task4 and task5 to make them wip
    data["task4"].create_time_log(
        resource=data["task4"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    data["task5"].create_time_log(
        resource=data["task5"].resources[0],
        start=now + td(hours=1),
        end=now + td(hours=2),
    )

    # no time log for task6

    assert data["task4"].status == data["status_wip"]
    assert data["task5"].status == data["status_wip"]
    assert data["task6"].status == data["status_rts"]

    # now request revision to task3
    data["task3"].request_revision(reviewer=data["task3"].responsible[0])

    # check statuses of task4 and task4
    assert data["task4"].status == data["status_drev"]
    assert data["task5"].status == data["status_drev"]
    assert data["task6"].status == data["status_wfd"]

    # TODO: add a new dependent task with schedule_model is not 'effort'
    # enter a new time log for task4 to complete its allowed time
    data["task4"].create_time_log(
        resource=data["task4"].resources[0],
        start=now + td(hours=2),
        end=now + td(hours=3),
    )
    DBSession.commit()

    # the task should have not effort left
    assert data["task4"].schedule_seconds == data["task4"].total_logged_seconds

    # task5 should have an extra time
    assert data["task5"].schedule_seconds == data["task5"].total_logged_seconds + 3600

    # task6 should be intact
    assert data["task6"].total_logged_seconds == 0

    # now approve task3
    reviews = data["task3"].review_set()
    for rev in reviews:
        rev.approve()
    DBSession.commit()

    # check the task statuses again
    assert data["task4"].status == data["status_hrev"]
    assert data["task5"].status == data["status_hrev"]
    assert data["task6"].status == data["status_rts"]

    # and check if task4 is expanded by the timing resolution
    assert data["task4"].schedule_seconds == data["task4"].total_logged_seconds + 3600

    # and task5 still has 1 hours
    assert data["task4"].schedule_seconds == data["task4"].total_logged_seconds + 3600

    # and task6 intact
    assert data["task6"].total_logged_seconds == 0


def test_approve_method_updates_task_timings(setup_review_db_test):
    """approve method will also update the task timings."""
    data = setup_review_db_test
    data["task3"].status = data["status_rts"]
    now = datetime.datetime.now(pytz.utc)
    td = datetime.timedelta

    data["task3"].schedule_timing = 2
    data["task3"].schedule_unit = "h"
    data["task3"].create_time_log(
        resource=data["task3"].resources[0], start=now, end=now + td(hours=1)
    )

    reviews = data["task3"].request_review()
    assert data["task3"].status == data["status_prev"]
    assert data["task3"].total_logged_seconds != data["task3"].schedule_seconds

    review1 = reviews[0]
    review1.approve()

    assert data["task3"].status == data["status_cmpl"]
    assert data["task3"].total_logged_seconds == data["task3"].schedule_seconds


def test_approve_method_updates_task_status_correctly_for_a_multi_responsible_task_if_one_approve(
    setup_review_db_test,
):
    """Review.approve() updates the task status for a task with multiple responsible."""
    data = setup_review_db_test
    data["task1"].responsible = [data["user1"], data["user2"]]
    now = datetime.datetime.now(pytz.utc)
    td = datetime.timedelta
    data["task1"].create_time_log(
        resource=data["task1"].resources[0], start=now, end=now + td(hours=1)
    )

    reviews = data["task1"].request_review()
    review1 = reviews[0]
    review2 = reviews[1]

    review1.request_revision()
    # one request review should be enough to set the status to hrev,
    # note that this is another tests duty to check
    assert data["task1"].status == data["status_prev"]

    # first reviewer
    review2.approve()
    assert data["task1"].status == data["status_hrev"]


def test_request_revision_method_updates_task_status_correctly_for_a_single_responsible_task(
    setup_review_db_test,
):
    """request_revision updates status to HREV for a Task with only one responsible."""
    data = setup_review_db_test
    data["task1"].responsible = [data["user1"]]
    now = datetime.datetime.now(pytz.utc)
    data["task1"].create_time_log(
        resource=data["task1"].resources[0],
        start=now,
        end=now + datetime.timedelta(hours=1),
    )

    reviews = data["task1"].request_review()
    review = reviews[0]
    review.request_revision()
    assert data["task1"].status == data["status_hrev"]


def test_request_revision_method_updates_task_status_correctly_for_a_multi_responsible_task_if_one_request_revision(
    setup_review_db_test,
):
    """request_revision updates status for a Task with multiple responsible."""
    data = setup_review_db_test
    data["task1"].responsible = [data["user1"], data["user2"]]
    now = datetime.datetime.now(pytz.utc)
    data["task1"].create_time_log(
        resource=data["task1"].resources[0],
        start=now,
        end=now + datetime.timedelta(hours=1),
    )

    # first reviewer requests a revision
    reviews = data["task1"].request_review()

    review1 = reviews[0]
    review2 = reviews[1]

    review1.approve()
    assert data["task1"].status == data["status_prev"]

    review2.request_revision()
    assert data["task1"].status == data["status_hrev"]


def test_request_revision_method_updates_task_status_correctly_for_a_multi_responsible_task_if_all_request_revision(
    setup_review_db_test,
):
    """request_revision updates status for a Task with multiple responsible."""
    data = setup_review_db_test
    data["task1"].responsible = [data["user1"], data["user2"]]
    now = datetime.datetime.now(pytz.utc)
    data["task1"].create_time_log(
        resource=data["task1"].resources[0],
        start=now,
        end=now + datetime.timedelta(hours=1),
    )

    # first reviewer requests a revision
    reviews = data["task1"].request_review()

    review1 = reviews[0]
    review2 = reviews[1]

    review1.request_revision()
    assert data["task1"].status == data["status_prev"]

    # first reviewer
    review2.request_revision()
    assert data["task1"].status == data["status_hrev"]


def test_request_revision_method_updates_task_timing_correctly_for_a_multi_responsible_task_if_all_request_revision(
    setup_review_db_test,
):
    """request_revision updates task timing for a Task with multiple responsible."""
    data = setup_review_db_test
    data["task1"].responsible = [data["user1"], data["user2"]]
    data["task1"].schedule_timing = 3
    data["task1"].schedule_unit = "h"

    assert data["task1"].status == data["status_rts"]

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)
    # create 1 hour time log
    data["task1"].create_time_log(
        resource=data["user1"], start=now, end=now + td(hours=1)
    )
    DBSession.commit()

    # first reviewer requests a revision
    reviews = data["task1"].request_review()

    assert len(reviews) == 2

    review1 = reviews[0]
    review2 = reviews[1]

    review1.request_revision(
        schedule_timing=2, schedule_unit="h", description="do some 2 hours extra work"
    )
    assert data["task1"].status == data["status_prev"]

    # first reviewer
    review2.request_revision(
        schedule_timing=5, schedule_unit="h", description="do some 5 hours extra work"
    )

    assert data["task1"].status == data["status_hrev"]

    # check the timing values
    assert data["task1"].schedule_timing == 8
    assert data["task1"].schedule_unit == "h"


def test_request_revision_method_updates_task_timing_correctly_for_a_multi_responsible_task_with_exactly_the_same_amount_of_schedule_timing_as_the_given_revision_timing(
    setup_review_db_test,
):
    """request_revision updates the task timing for a Task with multiple responsible.

    And has the same amount of schedule timing left with the given revision without
    expanding the task more then the total amount of revision requested.
    """
    data = setup_review_db_test
    data["task1"].responsible = [data["user1"], data["user2"]]
    data["task1"].schedule_timing = 8
    data["task1"].schedule_unit = "h"

    assert data["task1"].status == data["status_rts"]

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)
    # create 1 hour time log
    data["task1"].create_time_log(
        resource=data["user1"], start=now, end=now + td(hours=1)
    )

    # we should have 7 hours left

    # first reviewer requests a revision
    reviews = data["task1"].request_review()

    assert len(reviews) == 2

    review1 = reviews[0]
    review2 = reviews[1]

    review1.request_revision(
        schedule_timing=2, schedule_unit="h", description="do some 2 hours extra work"
    )
    assert data["task1"].status == data["status_prev"]

    # first reviewer
    review2.request_revision(
        schedule_timing=5, schedule_unit="h", description="do some 5 hours extra work"
    )

    assert data["task1"].status == data["status_hrev"]

    # check the timing values
    assert data["task1"].schedule_timing == 8
    assert data["task1"].schedule_unit == "h"


def test_request_revision_method_updates_task_timing_correctly_for_a_multi_responsible_task_with_more_schedule_timing_then_given_revision_timing(
    setup_review_db_test,
):
    """request_revision updates the task timing for a Task with multiple responsible.

    And still has more schedule timing then the given revision without expanding the
    task more then the total amount of revision requested.
    """
    data = setup_review_db_test
    data["task1"].responsible = [data["user1"], data["user2"]]
    data["task1"].schedule_timing = 100
    data["task1"].schedule_unit = "h"

    assert data["task1"].status == data["status_rts"]

    dt = datetime.datetime
    td = datetime.timedelta
    now = dt.now(pytz.utc)
    # create 1 hour time log
    data["task1"].create_time_log(
        resource=data["user1"], start=now, end=now + td(hours=1)
    )

    # we should have 8 hours left

    # first reviewer requests a revision
    reviews = data["task1"].request_review()

    assert len(reviews) == 2

    review1 = reviews[0]
    review2 = reviews[1]

    review1.request_revision(
        schedule_timing=2, schedule_unit="h", description="do some 2 hours extra work"
    )
    assert data["task1"].status == data["status_prev"]

    # first reviewer
    review2.request_revision(
        schedule_timing=5, schedule_unit="h", description="do some 5 hours extra work"
    )

    assert data["task1"].status == data["status_hrev"]

    # check the timing values
    assert data["task1"].schedule_timing == 100
    assert data["task1"].schedule_unit == "h"


def test_review_set_property_return_all_the_revision_instances_with_same_review_number(
    setup_review_db_test,
):
    """review_set returns all the Reviews of the task with the same review_number."""
    data = setup_review_db_test
    data["task1"].responsible = [data["user1"], data["user2"], data["user3"]]
    now = datetime.datetime.now(pytz.utc)
    data["task1"].create_time_log(
        resource=data["user1"], start=now, end=now + datetime.timedelta(hours=1)
    )
    data["task1"].status = data["status_wip"]
    reviews = data["task1"].request_review()
    review1 = reviews[0]
    review2 = reviews[1]
    review3 = reviews[2]

    assert review1.review_number == 1
    assert review2.review_number == 1
    assert review3.review_number == 1

    review1.approve()
    review2.approve()
    review3.approve()

    review4 = data["task1"].request_revision(reviewer=data["user1"])

    data["task1"].status = data["status_wip"]
    assert review4.review_number == 2

    # enter new time log to turn it into WIP
    data["task1"].create_time_log(
        resource=data["user1"],
        start=now + datetime.timedelta(hours=1),
        end=now + datetime.timedelta(hours=2),
    )

    review_set2 = data["task1"].request_review()
    review5 = review_set2[0]
    review6 = review_set2[1]
    review7 = review_set2[2]

    assert review5.review_number == 3
    assert review6.review_number == 3
    assert review7.review_number == 3
