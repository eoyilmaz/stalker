# -*- coding: utf-8 -*-
"""Tests for the stalker.models.scheduler.TaskJugglerScheduler class."""

import datetime
import os
import tempfile
import sys

import jinja2

import pytest

import pytz

import stalker
from stalker import TaskJugglerScheduler
from stalker import Department
from stalker import User
from stalker import Repository
from stalker import Status
from stalker import Studio
from stalker import Project
from stalker import Task
from stalker import TimeLog
from stalker.db.session import DBSession


@pytest.fixture(scope="function")
def monkeypatch_tj3():
    """patch tj3 command with a python script that returns an error message."""
    default_tj3_command_path = stalker.defaults.tj_command
    patched_tj3_command_path = tempfile.mktemp("patched_tj3_command")
    # create the script
    with open(patched_tj3_command_path, "w") as f:
        f.write(
            f"#!{sys.executable}\n"
            "# -*- coding: utf-8 -*-\n"
            "import sys\n"
            'sys.exit("some random exit message")\n'
        )
    # make it executable
    os.chmod(patched_tj3_command_path, 0o777)
    stalker.defaults["tj_command"] = patched_tj3_command_path
    yield
    stalker.defaults["tj_command"] = default_tj3_command_path
    # and clean the temp file
    os.remove(patched_tj3_command_path)


@pytest.fixture(scope="function")
def setup_tsk_juggler_scheduler_db_tests(setup_postgresql_db):
    """Set up tests for the  TaskJugglerScheduler class."""
    data = dict()

    # create departments
    data["test_dep1"] = Department(name="Dep1")
    data["test_dep2"] = Department(name="Dep2")

    # create resources
    data["test_user1"] = User(
        login="user1",
        name="User1",
        email="user1@users.com",
        password="1234",
        departments=[data["test_dep1"]],
    )
    DBSession.add(data["test_user1"])

    data["test_user2"] = User(
        login="user2",
        name="User2",
        email="user2@users.com",
        password="1234",
        departments=[data["test_dep1"]],
    )
    DBSession.add(data["test_user2"])

    data["test_user3"] = User(
        login="user3",
        name="User3",
        email="user3@users.com",
        password="1234",
        departments=[data["test_dep2"]],
    )
    DBSession.add(data["test_user3"])

    data["test_user4"] = User(
        login="user4",
        name="User4",
        email="user4@users.com",
        password="1234",
        departments=[data["test_dep2"]],
    )
    DBSession.add(data["test_user4"])

    # user with two departments
    data["test_user5"] = User(
        login="user5",
        name="User5",
        email="user5@users.com",
        password="1234",
        departments=[data["test_dep1"], data["test_dep2"]],
    )
    DBSession.add(data["test_user5"])

    # user with no departments
    data["test_user6"] = User(
        login="user6", name="User6", email="user6@users.com", password="1234"
    )
    DBSession.add(data["test_user6"])

    # repository
    data["test_repo"] = Repository(
        name="Test Repository",
        code="TR",
        linux_path="/mnt/T/",
        windows_path="T:/",
        macos_path="/Volumes/T/",
    )
    DBSession.add(data["test_repo"])

    # statuses
    data["test_status1"] = Status(name="Status 1", code="STS1")
    data["test_status2"] = Status(name="Status 2", code="STS2")
    data["test_status3"] = Status(name="Status 3", code="STS3")
    data["test_status4"] = Status(name="Status 4", code="STS4")
    data["test_status5"] = Status(name="Status 5", code="STS5")
    DBSession.add_all(
        [
            data["test_status1"],
            data["test_status2"],
            data["test_status3"],
            data["test_status4"],
            data["test_status5"],
        ]
    )

    # create one project
    data["test_proj1"] = Project(
        name="Test Project 1",
        code="TP1",
        repository=data["test_repo"],
        start=datetime.datetime(2013, 4, 4, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 5, 4, tzinfo=pytz.utc),
    )
    DBSession.add(data["test_proj1"])
    data["test_proj1"].now = datetime.datetime(2013, 4, 4, tzinfo=pytz.utc)

    # create two tasks with the same resources
    data["test_task1"] = Task(
        name="Task1",
        project=data["test_proj1"],
        resources=[data["test_user1"], data["test_user2"]],
        alternative_resources=[
            data["test_user3"],
            data["test_user4"],
            data["test_user5"],
        ],
        schedule_model=0,
        schedule_timing=50,
        schedule_unit="h",
    )
    DBSession.add(data["test_task1"])

    data["test_task2"] = Task(
        name="Task2",
        project=data["test_proj1"],
        resources=[data["test_user1"], data["test_user2"]],
        alternative_resources=[
            data["test_user3"],
            data["test_user4"],
            data["test_user5"],
        ],
        depends_on=[data["test_task1"]],
        schedule_model=0,
        schedule_timing=60,
        schedule_unit="h",
        priority=800,
    )
    DBSession.save(data["test_task2"])
    return data


def test_tjp_file_is_created(setup_tsk_juggler_scheduler_db_tests):
    """tjp file is correctly created."""
    data = setup_tsk_juggler_scheduler_db_tests
    # create the scheduler
    tjp_sched = TaskJugglerScheduler()
    tjp_sched.projects = [data["test_proj1"]]

    tjp_sched._create_tjp_file()
    tjp_sched._create_tjp_file_content()
    tjp_sched._fill_tjp_file()

    # check
    assert os.path.exists(tjp_sched.tjp_file_full_path)

    # clean up the test
    tjp_sched._clean_up()


def test_tjp_file_content_is_correct(setup_tsk_juggler_scheduler_db_tests):
    """tjp file content is correct."""
    data = setup_tsk_juggler_scheduler_db_tests
    # enter a couple of time_logs
    tlog1 = TimeLog(
        resource=data["test_user1"],
        task=data["test_task1"],
        start=datetime.datetime(2013, 4, 16, 6, 0, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc),
    )
    DBSession.add(tlog1)
    DBSession.commit()

    tjp_sched = TaskJugglerScheduler()
    test_studio = Studio(
        name="Test Studio", timing_resolution=datetime.timedelta(minutes=30)
    )
    test_studio.daily_working_hours = 9

    test_studio.id = 564
    test_studio.start = datetime.datetime(2013, 4, 16, 0, 7, tzinfo=pytz.utc)
    test_studio.end = datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc)
    test_studio.now = datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
    tjp_sched.studio = test_studio

    tjp_sched._create_tjp_file()
    tjp_sched._create_tjp_file_content()

    assert TimeLog.query.all() != []

    expected_tjp_template = jinja2.Template(
        """# Generated By Stalker v{{stalker.__version__}}
        
project Studio_564 "Studio_564" 2013-04-16 - 2013-06-30 {
    timingresolution 30min
    now 2013-04-16-00:00
    dailyworkinghours 9
    weekstartsmonday
    workinghours mon 09:00 - 18:00
    workinghours tue 09:00 - 18:00
    workinghours wed 09:00 - 18:00
    workinghours thu 09:00 - 18:00
    workinghours fri 09:00 - 18:00
    workinghours sat off
    workinghours sun off
    timeformat "%Y-%m-%d"
    scenario plan "Plan"
    trackingscenario plan
}

        # resources
        resource resources "Resources" {
            resource User_3 "User_3" {
    efficiency 1.0
}
            resource User_{{user1.id}} "User_{{user1.id}}" {
    efficiency 1.0
}
            resource User_{{user2.id}} "User_{{user2.id}}" {
    efficiency 1.0
}
            resource User_{{user3.id}} "User_{{user3.id}}" {
    efficiency 1.0
}
            resource User_{{user4.id}} "User_{{user4.id}}" {
    efficiency 1.0
}
            resource User_{{user5.id}} "User_{{user5.id}}" {
    efficiency 1.0
}
            resource User_{{user6.id}} "User_{{user6.id}}" {
    efficiency 1.0
}
        }

# tasks
task Project_{{proj.id}} "Project_{{proj.id}}" {
  task Task_{{task1.id}} "Task_{{task1.id}}" {
    effort 50.0h
    allocate User_{{user1.id}} { alternative User_{{user3.id}}, User_{{user4.id}}, User_{{user5.id}} select minallocated persistent }, User_{{user2.id}} { alternative User_{{user3.id}}, User_{{user4.id}}, User_{{user5.id}} select minallocated persistent }
    booking User_{{user1.id}} 2013-04-16-06:00:00 - 2013-04-16-09:00:00 { overtime 2 }
  }
  task Task_{{task2.id}} "Task_{{task2.id}}" {
    priority 800
    depends Project_{{proj.id}}.Task_{{task1.id}} {onend}
    effort 60.0h
    allocate User_{{user1.id}} { alternative User_{{user3.id}}, User_{{user4.id}}, User_{{user5.id}} select minallocated persistent }, User_{{user2.id}} { alternative User_{{user3.id}}, User_{{user4.id}}, User_{{user5.id}} select minallocated persistent }
  }
}

# reports
taskreport breakdown "{{csv_path}}"{
    formats csv
    timeformat "%Y-%m-%d-%H:%M"
    columns id, start, end
}
"""
    )
    expected_tjp_content = expected_tjp_template.render(
        {
            "stalker": stalker,
            "studio": test_studio,
            "csv_path": tjp_sched.temp_file_name,
            "user1": data["test_user1"],
            "user2": data["test_user2"],
            "user3": data["test_user3"],
            "user4": data["test_user4"],
            "user5": data["test_user5"],
            "user6": data["test_user6"],
            "proj": data["test_proj1"],
            "task1": data["test_task1"],
            "task2": data["test_task2"],
        }
    )

    data["maxDiff"] = None
    tjp_content = tjp_sched.tjp_content
    # print tjp_content
    tjp_sched._clean_up()
    # print(expected_tjp_content)
    # print('----------------')
    # print(tjp_content)
    assert tjp_content == expected_tjp_content


def test_schedule_will_not_work_if_the_studio_attribute_is_None(
    setup_tsk_juggler_scheduler_db_tests,
):
    """TypeError raised if the studio attribute is None."""
    tjp_sched = TaskJugglerScheduler()
    tjp_sched.studio = None
    with pytest.raises(TypeError) as cm:
        tjp_sched.schedule()

    assert (
        str(cm.value) == "TaskJugglerScheduler.studio should be an instance of "
        "stalker.models.studio.Studio, not NoneType: 'None'"
    )


pytest.mark.skipif(sys.platform == "win32", "Runs in Linux/macOS for now!")
def test_schedule_will_raise_tj3_command_errors_as_a_runtime_error(
    setup_tsk_juggler_scheduler_db_tests, monkeypatch_tj3
):
    data = setup_tsk_juggler_scheduler_db_tests
    # create a dummy Project to schedule
    dummy_project = Project(
        name="Dummy Project", code="DP", repository=data["test_repo"]
    )

    dt1 = Task(
        name="Dummy Task 1",
        project=dummy_project,
        schedule_timing=4,
        schedule_unit="h",
        resources=[data["test_user1"]],
    )

    dt2 = Task(
        name="Dummy Task 2",
        project=dummy_project,
        schedule_timing=4,
        schedule_unit="h",
        resources=[data["test_user2"]],
    )
    DBSession.add_all([dummy_project, dt1, dt2])
    DBSession.commit()

    tjp_sched = TaskJugglerScheduler(compute_resources=True, projects=[dummy_project])
    test_studio = Studio(
        name="Test Studio", now=datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
    )
    test_studio.start = datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
    test_studio.end = datetime.datetime(2013, 4, 30, 0, 0, tzinfo=pytz.utc)
    test_studio.daily_working_hours = 9
    DBSession.add(test_studio)
    DBSession.commit()

    tjp_sched.studio = test_studio

    # update the defaults.tj_command to false so that it returns an error

    with pytest.raises(RuntimeError) as cm:
        tjp_sched.schedule()

    assert str(cm.value) == "some random exit message"


def test_tasks_are_correctly_scheduled(setup_tsk_juggler_scheduler_db_tests):
    """tasks are correctly scheduled."""
    data = setup_tsk_juggler_scheduler_db_tests
    tjp_sched = TaskJugglerScheduler(compute_resources=True)
    test_studio = Studio(
        name="Test Studio", now=datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
    )
    test_studio.start = datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
    test_studio.end = datetime.datetime(2013, 4, 30, 0, 0, tzinfo=pytz.utc)
    test_studio.daily_working_hours = 9
    DBSession.add(test_studio)

    tjp_sched.studio = test_studio
    tjp_sched.schedule()
    DBSession.commit()

    # check if the task and project timings are all adjusted
    assert (
        datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)
        == data["test_proj1"].computed_start
    )
    assert (
        datetime.datetime(2013, 4, 24, 10, 0, tzinfo=pytz.utc)
        == data["test_proj1"].computed_end
    )

    possible_resources = [
        data["test_user1"],
        data["test_user2"],
        data["test_user3"],
        data["test_user4"],
        data["test_user5"],
    ]
    assert (
        datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)
        == data["test_task1"].computed_start
    )
    assert (
        datetime.datetime(2013, 4, 18, 16, 0, tzinfo=pytz.utc)
        == data["test_task1"].computed_end
    )

    assert len(data["test_task1"].computed_resources) == 2
    assert data["test_task1"].computed_resources[0] in possible_resources
    assert data["test_task1"].computed_resources[1] in possible_resources

    assert (
        datetime.datetime(2013, 4, 18, 16, 0, tzinfo=pytz.utc)
        == data["test_task2"].computed_start
    )
    assert (
        datetime.datetime(2013, 4, 24, 10, 0, tzinfo=pytz.utc)
        == data["test_task2"].computed_end
    )

    assert len(data["test_task2"].computed_resources) == 2
    assert data["test_task2"].computed_resources[0] in possible_resources
    assert data["test_task2"].computed_resources[1] in possible_resources


def test_tasks_are_correctly_scheduled_if_compute_resources_is_False(
    setup_tsk_juggler_scheduler_db_tests,
):
    """tasks are correctly scheduled if the compute_resources is False."""
    data = setup_tsk_juggler_scheduler_db_tests
    tjp_sched = TaskJugglerScheduler(compute_resources=False)
    test_studio = Studio(
        name="Test Studio", now=datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
    )
    test_studio.start = datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
    test_studio.end = datetime.datetime(2013, 4, 30, 0, 0, tzinfo=pytz.utc)
    test_studio.daily_working_hours = 9
    DBSession.add(test_studio)

    tjp_sched.studio = test_studio
    tjp_sched.schedule()
    DBSession.commit()

    # check if the task and project timings are all adjusted
    assert (
        datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)
        == data["test_proj1"].computed_start
    )
    assert (
        datetime.datetime(2013, 4, 24, 10, 0, tzinfo=pytz.utc)
        == data["test_proj1"].computed_end
    )

    assert (
        datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)
        == data["test_task1"].computed_start
    )
    assert (
        datetime.datetime(2013, 4, 18, 16, 0, tzinfo=pytz.utc)
        == data["test_task1"].computed_end
    )
    assert len(data["test_task1"].computed_resources) == 2
    assert data["test_task1"].computed_resources[0] in [
        data["test_user1"],
        data["test_user2"],
        data["test_user3"],
        data["test_user4"],
        data["test_user5"],
    ]
    assert data["test_task1"].computed_resources[1] in [
        data["test_user1"],
        data["test_user2"],
        data["test_user3"],
        data["test_user4"],
        data["test_user5"],
    ]

    assert (
        datetime.datetime(2013, 4, 18, 16, 0, tzinfo=pytz.utc)
        == data["test_task2"].computed_start
    )
    assert (
        datetime.datetime(2013, 4, 24, 10, 0, tzinfo=pytz.utc)
        == data["test_task2"].computed_end
    )
    assert len(data["test_task2"].computed_resources) == 2
    assert data["test_task2"].computed_resources[0] in [
        data["test_user1"],
        data["test_user2"],
        data["test_user3"],
        data["test_user4"],
        data["test_user5"],
    ]
    assert data["test_task2"].computed_resources[1] in [
        data["test_user1"],
        data["test_user2"],
        data["test_user3"],
        data["test_user4"],
        data["test_user5"],
    ]


def test_tasks_are_correctly_scheduled_if_compute_resources_is_True(
    setup_tsk_juggler_scheduler_db_tests,
):
    """tasks are correctly scheduled if the compute_resources is True."""
    data = setup_tsk_juggler_scheduler_db_tests
    tjp_sched = TaskJugglerScheduler(compute_resources=True)
    test_studio = Studio(
        name="Test Studio", now=datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
    )
    test_studio.start = datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
    test_studio.end = datetime.datetime(2013, 4, 30, 0, 0, tzinfo=pytz.utc)
    test_studio.daily_working_hours = 9
    DBSession.add(test_studio)

    tjp_sched.studio = test_studio
    tjp_sched.schedule()
    DBSession.commit()

    possible_resources = [
        data["test_user1"],
        data["test_user2"],
        data["test_user3"],
        data["test_user4"],
        data["test_user5"],
    ]

    # check if the task and project timings are all adjusted
    assert (
        datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)
        == data["test_proj1"].computed_start
    )
    assert (
        datetime.datetime(2013, 4, 24, 10, 0, tzinfo=pytz.utc)
        == data["test_proj1"].computed_end
    )

    assert (
        datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)
        == data["test_task1"].computed_start
    )
    assert (
        datetime.datetime(2013, 4, 18, 16, 0, tzinfo=pytz.utc)
        == data["test_task1"].computed_end
    )
    assert len(data["test_task1"].computed_resources) == 2
    assert data["test_task1"].computed_resources[0] in possible_resources
    assert data["test_task1"].computed_resources[1] in possible_resources

    assert (
        datetime.datetime(2013, 4, 18, 16, 0, tzinfo=pytz.utc)
        == data["test_task2"].computed_start
    )
    assert (
        datetime.datetime(2013, 4, 24, 10, 0, tzinfo=pytz.utc)
        == data["test_task2"].computed_end
    )
    assert data["test_task2"].computed_resources[0] in possible_resources
    assert data["test_task2"].computed_resources[1] in possible_resources


def test_tasks_of_given_projects_are_correctly_scheduled(
    setup_tsk_juggler_scheduler_db_tests,
):
    """tasks of given projects are correctly scheduled."""
    data = setup_tsk_juggler_scheduler_db_tests
    # create a dummy Project to schedule
    dummy_project = Project(
        name="Dummy Project", code="DP", repository=data["test_repo"]
    )

    dt1 = Task(
        name="Dummy Task 1",
        project=dummy_project,
        schedule_timing=4,
        schedule_unit="h",
        resources=[data["test_user1"]],
    )

    dt2 = Task(
        name="Dummy Task 2",
        project=dummy_project,
        schedule_timing=4,
        schedule_unit="h",
        resources=[data["test_user2"]],
    )
    DBSession.add_all([dummy_project, dt1, dt2])
    DBSession.commit()

    tjp_sched = TaskJugglerScheduler(compute_resources=True, projects=[dummy_project])
    test_studio = Studio(
        name="Test Studio", now=datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
    )
    test_studio.start = datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
    test_studio.end = datetime.datetime(2013, 4, 30, 0, 0, tzinfo=pytz.utc)
    test_studio.daily_working_hours = 9
    DBSession.add(test_studio)
    DBSession.commit()

    tjp_sched.studio = test_studio
    tjp_sched.schedule()
    DBSession.commit()

    # check if the task and project timings are all adjusted
    assert data["test_proj1"].computed_start is None
    assert data["test_proj1"].computed_end is None

    assert data["test_task1"].computed_start is None
    assert data["test_task1"].computed_end is None
    assert data["test_task1"].computed_resources == [
        data["test_user1"],
        data["test_user2"],
    ]

    assert data["test_task2"].computed_start is None
    assert data["test_task2"].computed_end is None
    assert data["test_task2"].computed_resources == [
        data["test_user1"],
        data["test_user2"],
    ]

    assert dt1.computed_start == datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)
    assert dt1.computed_end == datetime.datetime(2013, 4, 16, 13, 0, tzinfo=pytz.utc)

    assert dt2.computed_start == datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)
    assert dt2.computed_end == datetime.datetime(2013, 4, 16, 13, 0, tzinfo=pytz.utc)


def test_csv_file_does_not_exist_returns_without_scheduling(
    setup_tsk_juggler_scheduler_db_tests, monkeypatch
):
    """csv_file_full_path doesn't exist will return without schedule data parsed."""
    data = setup_tsk_juggler_scheduler_db_tests
    # create a dummy Project to schedule
    dummy_project = Project(
        name="Dummy Project", code="DP", repository=data["test_repo"]
    )

    dt1 = Task(
        name="Dummy Task 1",
        project=dummy_project,
        schedule_timing=4,
        schedule_unit="h",
        resources=[data["test_user1"]],
    )

    dt2 = Task(
        name="Dummy Task 2",
        project=dummy_project,
        schedule_timing=4,
        schedule_unit="h",
        resources=[data["test_user2"]],
    )
    DBSession.add_all([dummy_project, dt1, dt2])
    DBSession.commit()

    tjp_sched = TaskJugglerScheduler(compute_resources=True, projects=[dummy_project])
    test_studio = Studio(
        name="Test Studio", now=datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
    )
    test_studio.start = datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
    test_studio.end = datetime.datetime(2013, 4, 30, 0, 0, tzinfo=pytz.utc)
    test_studio.daily_working_hours = 9
    DBSession.add(test_studio)
    DBSession.commit()

    tjp_sched.studio = test_studio

    # trick _arse_csv_file() to think that the csv file doesn't exist
    import os

    called = []
    def patched_exists(path):
        if path == tjp_sched.csv_file_full_path:
            called.append(path)
            return False
        return os.path.exists(path)

    monkeypatch.setattr("stalker.models.schedulers.os.path.exists", patched_exists)
    assert len(called) == 0
    # should run without any errors
    tjp_sched.schedule()
    assert len(called) > 0
    assert tjp_sched.csv_file_full_path in called


def test_projects_argument_is_skipped(setup_tsk_juggler_scheduler_db_tests):
    """projects attribute an empty list if the projects argument is skipped."""
    tjp_sched = TaskJugglerScheduler(compute_resources=True)
    assert tjp_sched.projects == []


def test_projects_argument_is_None(setup_tsk_juggler_scheduler_db_tests):
    """projects attribute an empty list if the projects argument is None."""
    tjp_sched = TaskJugglerScheduler(compute_resources=True, projects=None)
    assert tjp_sched.projects == []


def test_projects_attribute_is_set_to_None(setup_tsk_juggler_scheduler_db_tests):
    """projects attribute an empty list if it is set to None."""
    tjp_sched = TaskJugglerScheduler(compute_resources=True)
    tjp_sched.projects = None
    assert tjp_sched.projects == []


def test_projects_argument_is_not_a_list(setup_tsk_juggler_scheduler_db_tests):
    """TypeError raised if the projects argument value is not a list."""
    with pytest.raises(TypeError) as cm:
        TaskJugglerScheduler(compute_resources=True, projects="not a list of projects")

    assert str(cm.value) == (
        "TaskJugglerScheduler.projects should be a list of "
        "stalker.models.project.Project instances, not str: 'not a list of projects'"
    )


def test_projects_attribute_is_not_a_list(setup_tsk_juggler_scheduler_db_tests):
    """TypeError raised if the projects attribute not a list."""
    tjp = TaskJugglerScheduler(compute_resources=True)
    with pytest.raises(TypeError) as cm:
        tjp.projects = "not a list of projects"

    assert str(cm.value) == (
        "TaskJugglerScheduler.projects should be a list of "
        "stalker.models.project.Project instances, not str: 'not a list of projects'"
    )


def test_projects_argument_is_not_a_list_of_all_projects():
    """TypeError raised if the items in the projects arg are not all Projects."""
    with pytest.raises(TypeError) as cm:
        TaskJugglerScheduler(
            compute_resources=True, projects=["not", 1, [], "of", "projects"]
        )

    assert str(cm.value) == (
        "TaskJugglerScheduler.projects should be a list of "
        "stalker.models.project.Project instances, not str: 'not'"
    )


def test_projects_attribute_is_not_list_of_all_projects():
    """TypeError raised if the items in the projects attr is not all Projects."""
    tjp = TaskJugglerScheduler(compute_resources=True)
    with pytest.raises(TypeError) as cm:
        tjp.projects = ["not", 1, [], "of", "projects"]

    assert (
        str(cm.value) == "TaskJugglerScheduler.projects should be a list of "
        "stalker.models.project.Project instances, not str: 'not'"
    )


def test_projects_argument_is_working_as_expected(setup_tsk_juggler_scheduler_db_tests):
    """projects argument value is correctly passed to the projects attribute."""
    data = setup_tsk_juggler_scheduler_db_tests
    dp1 = Project(name="Dummy Project", code="DP", repository=data["test_repo"])
    dp2 = Project(name="Dummy Project", code="DP", repository=data["test_repo"])
    tjp = TaskJugglerScheduler(compute_resources=True, projects=[dp1, dp2])
    assert tjp.projects == [dp1, dp2]


def test_projects_attribute_is_working_as_expected(
    setup_tsk_juggler_scheduler_db_tests,
):
    """projects attribute is working as expected."""
    data = setup_tsk_juggler_scheduler_db_tests
    dp1 = Project(name="Dummy Project", code="DP", repository=data["test_repo"])
    dp2 = Project(name="Dummy Project", code="DP", repository=data["test_repo"])
    tjp = TaskJugglerScheduler(compute_resources=True)
    tjp.projects = [dp1, dp2]
    assert tjp.projects == [dp1, dp2]


def test_tjp_file_content_is_correct_2(setup_tsk_juggler_scheduler_db_tests):
    """tjp file content is correct."""
    data = setup_tsk_juggler_scheduler_db_tests
    tjp_sched = TaskJugglerScheduler()
    test_studio = Studio(
        name="Test Studio", timing_resolution=datetime.timedelta(minutes=30)
    )
    test_studio.daily_working_hours = 9
    test_studio.id = 564
    test_studio.start = datetime.datetime(2013, 4, 16, 0, 7, tzinfo=pytz.utc)
    test_studio.end = datetime.datetime(2013, 6, 30, 0, 0, tzinfo=pytz.utc)
    test_studio.now = datetime.datetime(2013, 4, 16, 0, 0, tzinfo=pytz.utc)
    tjp_sched.studio = test_studio

    tjp_sched._create_tjp_file()
    tjp_sched._create_tjp_file_content()

    expected_tjp_template = jinja2.Template(
        """# Generated By Stalker v{{stalker.__version__}}
        
project Studio_564 "Studio_564" 2013-04-16 - 2013-06-30 {
    timingresolution 30min
    now 2013-04-16-00:00
    dailyworkinghours 9
    weekstartsmonday
    workinghours mon 09:00 - 18:00
    workinghours tue 09:00 - 18:00
    workinghours wed 09:00 - 18:00
    workinghours thu 09:00 - 18:00
    workinghours fri 09:00 - 18:00
    workinghours sat off
    workinghours sun off
    timeformat "%Y-%m-%d"
    scenario plan "Plan"
    trackingscenario plan
}

        # resources
        resource resources "Resources" {
            resource User_3 "User_3" {
    efficiency 1.0
}
            resource User_{{user1.id}} "User_{{user1.id}}" {
    efficiency 1.0
}
            resource User_{{user2.id}} "User_{{user2.id}}" {
    efficiency 1.0
}
            resource User_{{user3.id}} "User_{{user3.id}}" {
    efficiency 1.0
}
            resource User_{{user4.id}} "User_{{user4.id}}" {
    efficiency 1.0
}
            resource User_{{user5.id}} "User_{{user5.id}}" {
    efficiency 1.0
}
            resource User_{{user6.id}} "User_{{user6.id}}" {
    efficiency 1.0
}
        }

# tasks
task Project_{{proj1.id}} "Project_{{proj1.id}}" {
  task Task_{{task1.id}} "Task_{{task1.id}}" {
    effort 50.0h
    allocate User_{{user1.id}} { alternative User_{{user3.id}}, User_{{user4.id}}, User_{{user5.id}} select minallocated persistent }, User_{{user2.id}} { alternative User_{{user3.id}}, User_{{user4.id}}, User_{{user5.id}} select minallocated persistent }
  }
  task Task_{{task2.id}} "Task_{{task2.id}}" {
    priority 800
    depends Project_{{proj1.id}}.Task_{{task1.id}} {onend}
    effort 60.0h
    allocate User_{{user1.id}} { alternative User_{{user3.id}}, User_{{user4.id}}, User_{{user5.id}} select minallocated persistent }, User_{{user2.id}} { alternative User_{{user3.id}}, User_{{user4.id}}, User_{{user5.id}} select minallocated persistent }
  }
}

# reports
taskreport breakdown "{{csv_path}}"{
    formats csv
    timeformat "%Y-%m-%d-%H:%M"
    columns id, start, end
}"""
    )
    expected_tjp_content = expected_tjp_template.render(
        {
            "stalker": stalker,
            "studio": test_studio,
            "csv_path": tjp_sched.temp_file_name,
            "user1": data["test_user1"],
            "user2": data["test_user2"],
            "user3": data["test_user3"],
            "user4": data["test_user4"],
            "user5": data["test_user5"],
            "user6": data["test_user6"],
            "proj1": data["test_proj1"],
            "task1": data["test_task1"],
            "task2": data["test_task2"],
        }
    )

    data["maxDiff"] = None
    tjp_content = tjp_sched.tjp_content
    # print tjp_content
    tjp_sched._clean_up()
    assert tjp_content == expected_tjp_content
