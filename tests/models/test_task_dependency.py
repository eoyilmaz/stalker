# -*- coding: utf-8 -*-
"""Tests related to the TaskDependency class."""

import pytest

from sqlalchemy.exc import IntegrityError, SAWarning

from stalker import defaults
from stalker import Project
from stalker import Repository
from stalker import Structure
from stalker import Task
from stalker import TaskDependency
from stalker import User
from stalker.db.session import DBSession


@pytest.fixture(scope="function")
def setup_task_dependency_db_test(setup_postgresql_db):
    """set up the test TaskDependency class."""
    data = dict()
    data["test_user1"] = User(
        name="Test User 1", login="testuser1", email="user1@test.com", password="secret"
    )
    DBSession.add(data["test_user1"])

    data["test_user2"] = User(
        name="Test User 2", login="testuser2", email="user2@test.com", password="secret"
    )
    DBSession.add(data["test_user2"])

    data["test_user3"] = User(
        name="Test User 3", login="testuser3", email="user3@test.com", password="secret"
    )
    DBSession.add(data["test_user3"])

    data["test_repo"] = Repository(
        name="Test Repository",
        code="TR",
    )
    DBSession.add(data["test_repo"])

    data["test_structure"] = Structure(name="test structure")
    DBSession.add(data["test_structure"])

    data["test_project1"] = Project(
        name="Test Project 1",
        code="TP1",
        repository=data["test_repo"],
        structure=data["test_structure"],
    )
    DBSession.add(data["test_project1"])
    DBSession.commit()

    # create three Tasks
    data["test_task1"] = Task(name="Test Task 1", project=data["test_project1"])
    DBSession.add(data["test_task1"])

    data["test_task2"] = Task(name="Test Task 2", project=data["test_project1"])
    DBSession.add(data["test_task2"])

    data["test_task3"] = Task(name="Test Task 3", project=data["test_project1"])
    DBSession.add(data["test_task3"])
    DBSession.commit()

    data["kwargs"] = {
        "task": data["test_task1"],
        "depends_on": data["test_task2"],
        "dependency_target": "onend",
        "gap_timing": 0,
        "gap_unit": "h",
        "gap_model": "length",
    }
    return data


def test_task_argument_is_skipped(setup_task_dependency_db_test):
    """no error raised if the task argument is skipped."""
    data = setup_task_dependency_db_test
    data["kwargs"].pop("task")
    TaskDependency(**data["kwargs"])


def test_task_argument_is_skipped_raises_error_on_commit(setup_task_dependency_db_test):
    """IntegrityError raised if the task arg is skipped and the session is committed."""
    data = setup_task_dependency_db_test
    data["kwargs"].pop("task")
    new_dependency = TaskDependency(**data["kwargs"])
    DBSession.add(new_dependency)
    with pytest.raises(IntegrityError) as cm:
        with pytest.warns(SAWarning) as _:
            DBSession.commit()

    assert (
        '(psycopg2.errors.NotNullViolation) null value in column "task_id" of '
        'relation "Task_Dependencies" violates not-null constraint' in str(cm.value)
    )


def test_task_argument_is_not_a_task_instance(setup_task_dependency_db_test):
    """TypeError raised if the task arg is not a stalker.models.task.Task instance."""
    data = setup_task_dependency_db_test
    data["kwargs"]["task"] = "Not a Task instance"
    with pytest.raises(TypeError) as cm:
        TaskDependency(**data["kwargs"])

    assert (
        str(cm.value) == "TaskDependency.task should be and instance of "
        "stalker.models.task.Task, not str: 'Not a Task instance'"
    )


def test_task_attribute_is_not_a_task_instance(setup_task_dependency_db_test):
    """TypeError raised if the task attr is not a stalker.models.task.Task instance."""
    data = setup_task_dependency_db_test
    new_dep = TaskDependency(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_dep.task = "not a task"

    assert (
        str(cm.value) == "TaskDependency.task should be and instance of "
        "stalker.models.task.Task, not str: 'not a task'"
    )


def test_task_argument_is_working_as_expected(setup_task_dependency_db_test):
    """task argument value is correctly passed to task attribute."""
    data = setup_task_dependency_db_test
    data["test_task1"].depends_on = []
    new_dep = TaskDependency(**data["kwargs"])
    assert new_dep.task == data["test_task1"]


def test_depends_on_argument_is_skipped(setup_task_dependency_db_test):
    """no error raised if the depends_on argument is skipped."""
    data = setup_task_dependency_db_test
    data["kwargs"].pop("depends_on")
    TaskDependency(**data["kwargs"])


def test_depends_on_argument_is_skipped_raises_error_on_commit(
    setup_task_dependency_db_test,
):
    """IntegrityError raised if depends_on arg is skipped and session is committed."""
    data = setup_task_dependency_db_test
    data["kwargs"].pop("depends_on")
    new_dependency = TaskDependency(**data["kwargs"])
    DBSession.add(new_dependency)
    with pytest.raises(IntegrityError) as cm:
        with pytest.warns(SAWarning) as _:
            DBSession.commit()

    assert (
        '(psycopg2.errors.NotNullViolation) null value in column "depends_on_id" of '
        'relation "Task_Dependencies" violates not-null constraint' in str(cm.value)
    )


def test_depends_on_argument_is_not_a_task_instance(setup_task_dependency_db_test):
    """TypeError raised if the depends_on arg is not a Task instance."""
    data = setup_task_dependency_db_test
    data["kwargs"]["depends_on"] = "Not a Task instance"
    with pytest.raises(TypeError) as cm:
        TaskDependency(**data["kwargs"])

    assert (
        str(cm.value) == "TaskDependency.depends_on can should be and instance of "
        "stalker.models.task.Task, not str: 'Not a Task instance'"
    )


def test_depends_on_attribute_is_not_a_task_instance(setup_task_dependency_db_test):
    """TypeError raised if depends_on attr is not a Task instance."""
    data = setup_task_dependency_db_test
    new_dep = TaskDependency(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_dep.depends_on = "not a task"

    assert (
        str(cm.value) == "TaskDependency.depends_on can should be and instance of "
        "stalker.models.task.Task, not str: 'not a task'"
    )


def test_depends_on_argument_is_working_as_expected(setup_task_dependency_db_test):
    """depends_on argument value is correctly passed to depends_on attribute."""
    data = setup_task_dependency_db_test
    data["test_task1"].depends_on = []
    new_dep = TaskDependency(**data["kwargs"])
    assert new_dep.depends_on == data["test_task2"]


def test_gap_timing_argument_is_skipped(setup_task_dependency_db_test):
    """gap_timing attribute value 0 if the gap_timing argument is skipped."""
    data = setup_task_dependency_db_test
    data["kwargs"].pop("gap_timing")
    tdep = TaskDependency(**data["kwargs"])
    assert tdep.gap_timing == 0


def test_gap_timing_argument_is_none(setup_task_dependency_db_test):
    """gap_timing attribute value 0 if the gap_timing argument value is None."""
    data = setup_task_dependency_db_test
    data["kwargs"]["gap_timing"] = None
    tdep = TaskDependency(**data["kwargs"])
    assert tdep.gap_timing == 0


def test_gap_timing_attribute_is_set_to_none(setup_task_dependency_db_test):
    """gap_timing attribute value 0 if it is set to None."""
    data = setup_task_dependency_db_test
    tdep = TaskDependency(**data["kwargs"])
    tdep.gap_timing = None
    assert tdep.gap_timing == 0


def test_gap_timing_argument_is_not_a_float(setup_task_dependency_db_test):
    """TypeError raised if the gap_timing argument value is not a float value."""
    data = setup_task_dependency_db_test
    data["kwargs"]["gap_timing"] = "not a time delta"
    with pytest.raises(TypeError) as cm:
        TaskDependency(**data["kwargs"])

    assert str(cm.value) == (
        "TaskDependency.gap_timing should be an integer or float number showing the "
        "value of the gap timing of this TaskDependency, "
        "not str: 'not a time delta'"
    )


def test_gap_timing_attribute_is_not_a_float(setup_task_dependency_db_test):
    """TypeError raised if the gap_timing attribute value is not float."""
    data = setup_task_dependency_db_test
    tdep = TaskDependency(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        tdep.gap_timing = "not float"

    assert str(cm.value) == (
        "TaskDependency.gap_timing should be an integer or float number showing the "
        "value of the gap timing of this TaskDependency, not str: 'not float'"
    )


def test_gap_timing_argument_is_working_as_expected(setup_task_dependency_db_test):
    """gap_timing argument value is correctly passed to the gap_timing attribute."""
    data = setup_task_dependency_db_test
    test_value = 11
    data["kwargs"]["gap_timing"] = test_value
    tdep = TaskDependency(**data["kwargs"])
    assert tdep.gap_timing == test_value


def test_gap_timing_attribute_is_working_as_expected(setup_task_dependency_db_test):
    """gap_timing attribute is working as expected."""
    data = setup_task_dependency_db_test
    tdep = TaskDependency(**data["kwargs"])
    test_value = 11
    tdep.gap_timing = test_value
    assert tdep.gap_timing == test_value


def test_gap_unit_argument_is_skipped(setup_task_dependency_db_test):
    """default value used if the gap_unit argument is skipped."""
    data = setup_task_dependency_db_test
    data["kwargs"].pop("gap_unit")
    tdep = TaskDependency(**data["kwargs"])
    assert tdep.gap_unit == TaskDependency.__default_schedule_unit__


def test_gap_unit_argument_is_none(setup_task_dependency_db_test):
    """default value used if the gap_unit argument is None."""
    data = setup_task_dependency_db_test
    data["kwargs"]["gap_unit"] = None
    tdep = TaskDependency(**data["kwargs"])
    assert tdep.gap_unit == TaskDependency.__default_schedule_unit__


def test_gap_unit_attribute_is_none(setup_task_dependency_db_test):
    """default value used if the gap_unit attribute is set to None."""
    data = setup_task_dependency_db_test
    tdep = TaskDependency(**data["kwargs"])
    tdep.gap_unit = None
    assert tdep.gap_unit == TaskDependency.__default_schedule_unit__


def test_gap_unit_argument_is_not_a_str_instance(setup_task_dependency_db_test):
    """TypeError raised if the gap_unit argument is not a str."""
    data = setup_task_dependency_db_test
    data["kwargs"]["gap_unit"] = 231
    with pytest.raises(TypeError) as cm:
        TaskDependency(**data["kwargs"])

    assert (
        str(cm.value) == "TaskDependency.gap_unit should be a string value one of "
        "['min', 'h', 'd', 'w', 'm', 'y'] showing the unit of the gap "
        "timing of this TaskDependency, not int: '231'"
    )


def test_gap_unit_attribute_is_not_a_str_instance(setup_task_dependency_db_test):
    """TypeError raised if the gap_unit attribute is not a str."""
    data = setup_task_dependency_db_test
    tdep = TaskDependency(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        tdep.gap_unit = 2342

    assert str(cm.value) == (
        "TaskDependency.gap_unit should be a string value one of "
        "['min', 'h', 'd', 'w', 'm', 'y'] showing the unit of the gap "
        "timing of this TaskDependency, not int: '2342'"
    )


def test_gap_unit_argument_value_is_not_in_the_enum_list(setup_task_dependency_db_test):
    """ValueError raised if the gap_unit arg value is not valid."""
    data = setup_task_dependency_db_test
    data["kwargs"]["gap_unit"] = "not in the list"
    with pytest.raises(ValueError) as cm:
        TaskDependency(**data["kwargs"])

    assert (
        str(cm.value) == "TaskDependency.gap_unit should be a string value one of "
        "['min', 'h', 'd', 'w', 'm', 'y'] showing the unit of the gap "
        "timing of this TaskDependency, not str"
    )


def test_gap_unit_attribute_value_is_not_in_the_enum_list(
    setup_task_dependency_db_test,
):
    """ValueError raised if the gap_unit attr is not valid."""
    data = setup_task_dependency_db_test
    tdep = TaskDependency(**data["kwargs"])
    with pytest.raises(ValueError) as cm:
        tdep.gap_unit = "not in the list"

    assert (
        str(cm.value) == "TaskDependency.gap_unit should be a string value one of "
        "['min', 'h', 'd', 'w', 'm', 'y'] showing the unit of the gap "
        "timing of this TaskDependency, not str"
    )


def test_gap_unit_argument_is_working_as_expected(setup_task_dependency_db_test):
    """gap_unit argument value is correctly passed to the gap_unit attribute on init."""
    data = setup_task_dependency_db_test
    test_value = "y"
    data["kwargs"]["gap_unit"] = test_value
    tdep = TaskDependency(**data["kwargs"])
    assert tdep.gap_unit == test_value


def test_gap_unit_attribute_is_working_as_expected(setup_task_dependency_db_test):
    """gap_unit attribute is working as expected."""
    data = setup_task_dependency_db_test
    tdep = TaskDependency(**data["kwargs"])
    test_value = "w"
    assert tdep.gap_unit != test_value
    tdep.gap_unit = test_value
    assert tdep.gap_unit == test_value


def test_gap_model_argument_is_skipped(setup_task_dependency_db_test):
    """default value used if the gap_model argument is skipped."""
    data = setup_task_dependency_db_test
    data["kwargs"].pop("gap_model")
    tdep = TaskDependency(**data["kwargs"])
    assert tdep.gap_model == defaults.task_dependency_gap_models[0]


def test_gap_model_argument_is_none(setup_task_dependency_db_test):
    """default value used if the gap_model argument is None."""
    data = setup_task_dependency_db_test
    data["kwargs"]["gap_model"] = None
    tdep = TaskDependency(**data["kwargs"])
    assert tdep.gap_model == defaults.task_dependency_gap_models[0]


def test_gap_model_attribute_is_none(setup_task_dependency_db_test):
    """default value used if the gap_model attribute is set to None."""
    data = setup_task_dependency_db_test
    tdep = TaskDependency(**data["kwargs"])
    tdep.gap_model = None
    assert tdep.gap_model == defaults.task_dependency_gap_models[0]


def test_gap_model_argument_is_not_a_str_instance(setup_task_dependency_db_test):
    """TypeError raised if the gap_model argument is not a str."""
    data = setup_task_dependency_db_test
    data["kwargs"]["gap_model"] = 231
    with pytest.raises(TypeError) as cm:
        TaskDependency(**data["kwargs"])

    assert (
        str(cm.value) == "TaskDependency.gap_model should be one of ['length', "
        "'duration'], not int: '231'"
    )


def test_gap_model_attribute_is_not_a_str_instance(setup_task_dependency_db_test):
    """TypeError raised if the gap_model attribute is not a str."""
    data = setup_task_dependency_db_test
    tdep = TaskDependency(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        tdep.gap_model = 2342

    assert (
        str(cm.value) == "TaskDependency.gap_model should be one of ['length', "
        "'duration'], not int: '2342'"
    )


def test_gap_model_argument_value_is_not_in_the_enum_list(
    setup_task_dependency_db_test,
):
    """ValueError raised if the gap_model arg is not valid."""
    data = setup_task_dependency_db_test
    data["kwargs"]["gap_model"] = "not in the list"
    with pytest.raises(ValueError) as cm:
        TaskDependency(**data["kwargs"])

    assert (
        str(cm.value) == "TaskDependency.gap_model should be one of ['length', "
        "'duration'], not str: 'not in the list'"
    )


def test_gap_model_attribute_value_is_not_in_the_enum_list(
    setup_task_dependency_db_test,
):
    """ValueError raised if the gap_model attr is not valid."""
    data = setup_task_dependency_db_test
    tdep = TaskDependency(**data["kwargs"])
    with pytest.raises(ValueError) as cm:
        tdep.gap_model = "not in the list"

    assert (
        str(cm.value) == "TaskDependency.gap_model should be one of ['length', "
        "'duration'], not str: 'not in the list'"
    )


def test_gap_model_argument_is_working_as_expected(setup_task_dependency_db_test):
    """gap_model arg is passed okay to the gap_model attr on init."""
    data = setup_task_dependency_db_test
    test_value = "duration"
    data["kwargs"]["gap_model"] = test_value
    tdep = TaskDependency(**data["kwargs"])
    assert tdep.gap_model == test_value


def test_gap_model_attribute_is_working_as_expected(setup_task_dependency_db_test):
    """gap_model attribute is working as expected."""
    data = setup_task_dependency_db_test
    tdep = TaskDependency(**data["kwargs"])
    test_value = "duration"
    assert tdep.gap_model != test_value
    tdep.gap_model = test_value
    assert tdep.gap_model == test_value


def test_dependency_target_argument_is_skipped(setup_task_dependency_db_test):
    """default value used if the dependency_target argument is skipped."""
    data = setup_task_dependency_db_test
    data["kwargs"].pop("dependency_target")
    tdep = TaskDependency(**data["kwargs"])
    assert tdep.dependency_target == defaults.task_dependency_targets[0]


def test_dependency_target_argument_is_none(setup_task_dependency_db_test):
    """default value used if the dependency_target argument is None."""
    data = setup_task_dependency_db_test
    data["kwargs"]["dependency_target"] = None
    tdep = TaskDependency(**data["kwargs"])
    assert tdep.dependency_target == defaults.task_dependency_targets[0]


def test_dependency_target_attribute_is_none(setup_task_dependency_db_test):
    """default value used if the dependency_target attribute is set to None."""
    data = setup_task_dependency_db_test
    tdep = TaskDependency(**data["kwargs"])
    tdep.dependency_target = None
    assert tdep.dependency_target == defaults.task_dependency_targets[0]


def test_dependency_target_argument_is_not_a_str_instance(
    setup_task_dependency_db_test,
):
    """TypeError raised if the dependency_target argument is not a str."""
    data = setup_task_dependency_db_test
    data["kwargs"]["dependency_target"] = 0
    with pytest.raises(TypeError) as cm:
        TaskDependency(**data["kwargs"])

    assert str(cm.value) == (
        "TaskDependency.dependency_target should be a string with a value one of "
        "['onend', 'onstart'], not int: '0'"
    )


def test_dependency_target_attribute_is_not_a_str_instance(
    setup_task_dependency_db_test,
):
    """TypeError raised if the dependency_target attribute is not a str."""
    data = setup_task_dependency_db_test
    tdep = TaskDependency(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        tdep.dependency_target = 0

    assert str(cm.value) == (
        "TaskDependency.dependency_target should be a string with a value one of "
        "['onend', 'onstart'], not int: '0'"
    )


def test_dependency_target_argument_value_is_not_in_the_enum_list(
    setup_task_dependency_db_test,
):
    """ValueError raised if dependency_target arg is not valid."""
    data = setup_task_dependency_db_test
    data["kwargs"]["dependency_target"] = "not in the list"
    with pytest.raises(ValueError) as cm:
        TaskDependency(**data["kwargs"])

    assert (
        str(cm.value) == "TaskDependency.dependency_target should be one of ['onend', "
        "'onstart'], not 'not in the list'"
    )


def test_dependency_target_attribute_value_is_not_in_the_enum_list(
    setup_task_dependency_db_test,
):
    """ValueError raised if the dependency_target attr is not valid."""
    data = setup_task_dependency_db_test
    tdep = TaskDependency(**data["kwargs"])
    with pytest.raises(ValueError) as cm:
        tdep.dependency_target = "not in the list"

    assert (
        str(cm.value) == "TaskDependency.dependency_target should be one of ['onend', "
        "'onstart'], not 'not in the list'"
    )


def test_dependency_target_argument_is_working_as_expected(setup_task_dependency_db_test):
    """dependency_target arg is passed okay to the dependency_target attr on init."""
    data = setup_task_dependency_db_test
    tdep = TaskDependency(**data["kwargs"])
    assert tdep.dependency_target == "onend"


def test_dependency_target_attribute_is_working_as_expected(setup_task_dependency_db_test):
    """dependency_target attribute is working as expected."""
    data = setup_task_dependency_db_test
    tdep = TaskDependency(**data["kwargs"])
    onstart = "onstart"
    tdep.dependency_target = onstart
    assert tdep.dependency_target == onstart
