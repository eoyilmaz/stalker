# -*- coding: utf-8 -*-
"""Tests for the Studio class."""

import datetime
import sys

from jinja2 import Template

import pytest

import pytz

from stalker import (
    Asset,
    Department,
    Project,
    Repository,
    SchedulerBase,
    Shot,
    Studio,
    Task,
    TaskJugglerScheduler,
    Type,
    User,
    Vacation,
    WorkingHours,
    defaults,
)
from stalker.db.session import DBSession


class DummyScheduler(SchedulerBase):
    """This is a dummy scheduler to be used in tests."""

    def __init__(self, studio=None, callback=None):
        SchedulerBase.__init__(self, studio)
        self.callback = callback

    def schedule(self):
        """Call the callback function before finishing."""
        if self.callback:
            self.callback()


@pytest.fixture(scope="function")
def setup_studio_db_tests(setup_postgresql_db):
    """Set up the test for stalker.models.studio.Studio class."""
    data = dict()
    data["test_user1"] = User(
        name="User 1", login="user1", email="user1@users.com", password="password"
    )
    DBSession.add(data["test_user1"])

    data["test_user2"] = User(
        name="User 2", login="user2", email="user2@users.com", password="password"
    )
    DBSession.add(data["test_user2"])

    data["test_user3"] = User(
        name="User 3", login="user3", email="user3@users.com", password="password"
    )
    DBSession.add(data["test_user3"])

    data["test_department1"] = Department(name="Test Department 1")
    DBSession.add(data["test_department1"])

    data["test_department2"] = Department(name="Test Department 2")
    DBSession.add(data["test_department2"])

    data["test_repo"] = Repository(
        name="Test Repository",
        code="TR",
        windows_path="T:/",
        linux_path="/mnt/T/",
        osx_path="/Volumes/T/",
    )
    DBSession.add(data["test_repo"])

    # create a couple of projects
    data["test_project1"] = Project(
        name="Test Project 1", code="TP1", repository=data["test_repo"]
    )
    DBSession.add(data["test_project1"])

    data["test_project2"] = Project(
        name="Test Project 2", code="TP2", repository=data["test_repo"]
    )
    DBSession.add(data["test_project2"])

    # an inactive project
    data["test_project3"] = Project(
        name="Test Project 3", code="TP3", repository=data["test_repo"]
    )
    data["test_project3"].active = False
    DBSession.save(data["test_project3"])

    # create assets and shots
    data["test_asset_type"] = Type(
        name="Character", code="Char", target_entity_type="Asset"
    )
    DBSession.add(data["test_asset_type"])

    data["test_asset1"] = Asset(
        name="Test Asset 1",
        code="TA1",
        project=data["test_project1"],
        type=data["test_asset_type"],
    )
    DBSession.add(data["test_asset1"])

    data["test_asset2"] = Asset(
        name="Test Asset 2",
        code="TA2",
        project=data["test_project2"],
        type=data["test_asset_type"],
    )
    DBSession.add(data["test_asset2"])

    # shots
    # for project 1
    data["test_shot1"] = Shot(
        code="shot1",
        project=data["test_project1"],
    )
    DBSession.add(data["test_shot1"])

    data["test_shot2"] = Shot(
        code="shot2",
        project=data["test_project1"],
    )
    DBSession.add(data["test_shot2"])

    # for project 2
    data["test_shot3"] = Shot(
        code="shot3",
        project=data["test_project2"],
    )
    DBSession.add(data["test_shot3"])

    data["test_shot4"] = Shot(
        code="shot4",
        project=data["test_project2"],
    )
    DBSession.add(data["test_shot4"])

    # for project 3
    data["test_shot5"] = Shot(
        code="shot5",
        project=data["test_project3"],
    )
    DBSession.add(data["test_shot5"])

    #########################################################
    # tasks for projects
    data["test_task1"] = Task(
        name="Project Planing",
        project=data["test_project1"],
        resources=[data["test_user1"]],
        alternative_resources=[data["test_user2"], data["test_user3"]],
        schedule_timing=10,
        schedule_unit="d",
    )
    DBSession.add(data["test_task1"])

    data["test_task2"] = Task(
        name="Project Planing",
        project=data["test_project2"],
        resources=[data["test_user1"]],
        alternative_resources=[data["test_user2"], data["test_user3"]],
        schedule_timing=10,
        schedule_unit="d",
    )
    DBSession.add(data["test_task2"])

    data["test_task3"] = Task(
        name="Project Planing",
        project=data["test_project3"],
        resources=[data["test_user1"]],
        alternative_resources=[data["test_user2"], data["test_user3"]],
        schedule_timing=5,
        schedule_unit="d",
    )
    DBSession.add(data["test_task3"])

    # for shots

    # Shot 1
    data["test_task4"] = Task(
        name="Match Move",
        parent=data["test_shot1"],
        resources=[data["test_user1"]],
        alternative_resources=[data["test_user2"], data["test_user3"]],
        schedule_timing=2,
        schedule_unit="d",
    )
    DBSession.add(data["test_task4"])

    data["test_task5"] = Task(
        name="FX",
        parent=data["test_shot1"],
        resources=[data["test_user2"]],
        alternative_resources=[data["test_user1"], data["test_user3"]],
        depends=[data["test_task4"]],
        schedule_timing=2,
        schedule_unit="d",
    )
    DBSession.add(data["test_task5"])

    data["test_task6"] = Task(
        name="Lighting",
        parent=data["test_shot1"],
        resources=[data["test_user2"]],
        alternative_resources=[data["test_user1"], data["test_user3"]],
        depends=[data["test_task4"], data["test_task5"]],
        schedule_timing=3,
        schedule_unit="d",
    )
    DBSession.add(data["test_task6"])

    data["test_task7"] = Task(
        name="Comp",
        parent=data["test_shot1"],
        resources=[data["test_user2"]],
        alternative_resources=[data["test_user1"], data["test_user3"]],
        depends=[data["test_task6"]],
        schedule_timing=3,
        schedule_unit="d",
    )
    DBSession.add(data["test_task7"])

    # Shot 2
    data["test_task8"] = Task(
        name="Match Move",
        parent=data["test_shot2"],
        resources=[data["test_user3"]],
        alternative_resources=[data["test_user1"], data["test_user2"]],
        schedule_timing=2,
        schedule_unit="d",
    )
    DBSession.add(data["test_task8"])

    data["test_task9"] = Task(
        name="FX",
        parent=data["test_shot2"],
        resources=[data["test_user3"]],
        alternative_resources=[data["test_user1"], data["test_user2"]],
        depends=[data["test_task8"]],
        schedule_timing=2,
        schedule_unit="d",
    )
    DBSession.add(data["test_task9"])

    data["test_task10"] = Task(
        name="Lighting",
        parent=data["test_shot2"],
        resources=[data["test_user2"]],
        alternative_resources=[data["test_user1"], data["test_user3"]],
        depends=[data["test_task8"], data["test_task9"]],
        schedule_timing=3,
        schedule_unit="d",
    )
    DBSession.add(data["test_task10"])

    data["test_task11"] = Task(
        name="Comp",
        parent=data["test_shot2"],
        resources=[data["test_user2"]],
        alternative_resources=[data["test_user1"], data["test_user3"]],
        depends=[data["test_task10"]],
        schedule_timing=4,
        schedule_unit="d",
    )
    DBSession.add(data["test_task11"])

    # Shot 3
    data["test_task12"] = Task(
        name="Match Move",
        parent=data["test_shot3"],
        resources=[data["test_user1"]],
        alternative_resources=[data["test_user2"], data["test_user3"]],
        schedule_timing=2,
        schedule_unit="d",
    )
    DBSession.add(data["test_task12"])

    data["test_task13"] = Task(
        name="FX",
        parent=data["test_shot3"],
        resources=[data["test_user1"]],
        alternative_resources=[data["test_user2"], data["test_user3"]],
        depends=[data["test_task12"]],
        schedule_timing=2,
        schedule_unit="d",
    )
    DBSession.add(data["test_task13"])

    data["test_task14"] = Task(
        name="Lighting",
        parent=data["test_shot3"],
        resources=[data["test_user1"]],
        alternative_resources=[data["test_user2"], data["test_user3"]],
        depends=[data["test_task12"], data["test_task13"]],
        schedule_timing=3,
        schedule_unit="d",
    )
    DBSession.add(data["test_task14"])

    data["test_task15"] = Task(
        name="Comp",
        parent=data["test_shot3"],
        resources=[data["test_user1"]],
        alternative_resources=[data["test_user2"], data["test_user3"]],
        depends=[data["test_task14"]],
        schedule_timing=4,
        schedule_unit="d",
    )
    DBSession.add(data["test_task15"])

    # Shot 4
    data["test_task16"] = Task(
        name="Match Move",
        parent=data["test_shot4"],
        resources=[data["test_user2"]],
        alternative_resources=[data["test_user1"], data["test_user3"]],
        schedule_timing=2,
        schedule_unit="d",
    )
    DBSession.add(data["test_task16"])

    data["test_task17"] = Task(
        name="FX",
        parent=data["test_shot4"],
        resources=[data["test_user2"]],
        alternative_resources=[data["test_user1"], data["test_user3"]],
        depends=[data["test_task16"]],
        schedule_timing=2,
        schedule_unit="d",
    )
    DBSession.add(data["test_task17"])

    data["test_task18"] = Task(
        name="Lighting",
        parent=data["test_shot4"],
        resources=[data["test_user2"]],
        alternative_resources=[data["test_user1"], data["test_user3"]],
        depends=[data["test_task16"], data["test_task17"]],
        schedule_timing=3,
        schedule_unit="d",
    )
    DBSession.add(data["test_task18"])

    data["test_task19"] = Task(
        name="Comp",
        parent=data["test_shot4"],
        resources=[data["test_user2"]],
        alternative_resources=[data["test_user1"], data["test_user3"]],
        depends=[data["test_task18"]],
        schedule_timing=4,
        schedule_unit="d",
    )
    DBSession.add(data["test_task19"])

    # Shot 5
    data["test_task20"] = Task(
        name="Match Move",
        parent=data["test_shot5"],
        resources=[data["test_user3"]],
        alternative_resources=[data["test_user1"], data["test_user2"]],
        schedule_timing=2,
        schedule_unit="d",
    )
    DBSession.add(data["test_task20"])

    data["test_task21"] = Task(
        name="FX",
        parent=data["test_shot5"],
        resources=[data["test_user3"]],
        alternative_resources=[data["test_user1"], data["test_user2"]],
        depends=[data["test_task20"]],
        schedule_timing=2,
        schedule_unit="d",
    )
    DBSession.add(data["test_task21"])

    data["test_task22"] = Task(
        name="Lighting",
        parent=data["test_shot5"],
        resources=[data["test_user3"]],
        alternative_resources=[data["test_user1"], data["test_user2"]],
        depends=[data["test_task20"], data["test_task21"]],
        schedule_timing=3,
        schedule_unit="d",
    )
    DBSession.add(data["test_task22"])

    data["test_task23"] = Task(
        name="Comp",
        parent=data["test_shot5"],
        resources=[data["test_user3"]],
        alternative_resources=[data["test_user1"], data["test_user2"]],
        depends=[data["test_task22"]],
        schedule_timing=4,
        schedule_unit="d",
    )
    DBSession.add(data["test_task23"])

    ####################################################
    # For Assets

    # Asset 1
    data["test_task24"] = Task(
        name="Design",
        parent=data["test_asset1"],
        resources=[data["test_user1"]],
        alternative_resources=[data["test_user2"], data["test_user3"]],
        schedule_timing=10,
        schedule_unit="d",
    )
    DBSession.add(data["test_task24"])

    data["test_task25"] = Task(
        name="Model",
        parent=data["test_asset1"],
        depends=[data["test_task24"]],
        resources=[data["test_user1"]],
        alternative_resources=[data["test_user2"], data["test_user3"]],
        schedule_timing=15,
        schedule_unit="d",
    )
    DBSession.add(data["test_task25"])

    data["test_task26"] = Task(
        name="LookDev",
        parent=data["test_asset1"],
        depends=[data["test_task25"]],
        resources=[data["test_user1"]],
        alternative_resources=[data["test_user2"], data["test_user3"]],
        schedule_timing=10,
        schedule_unit="d",
    )
    DBSession.add(data["test_task26"])

    data["test_task27"] = Task(
        name="Rig",
        parent=data["test_asset1"],
        depends=[data["test_task25"]],
        resources=[data["test_user1"]],
        alternative_resources=[data["test_user2"], data["test_user3"]],
        schedule_timing=10,
        schedule_unit="d",
    )
    DBSession.add(data["test_task27"])

    # Asset 2
    data["test_task28"] = Task(
        name="Design",
        parent=data["test_asset2"],
        resources=[data["test_user2"]],
        alternative_resources=[data["test_user1"], data["test_user3"]],
        schedule_timing=10,
        schedule_unit="d",
    )
    DBSession.add(data["test_task28"])

    data["test_task29"] = Task(
        name="Model",
        parent=data["test_asset2"],
        depends=[data["test_task28"]],
        resources=[data["test_user2"]],
        alternative_resources=[data["test_user1"], data["test_user3"]],
        schedule_timing=15,
        schedule_unit="d",
    )
    DBSession.add(data["test_task29"])

    data["test_task30"] = Task(
        name="LookDev",
        parent=data["test_asset2"],
        depends=[data["test_task29"]],
        resources=[data["test_user2"]],
        alternative_resources=[data["test_user1"], data["test_user3"]],
        schedule_timing=10,
        schedule_unit="d",
    )
    DBSession.add(data["test_task30"])

    data["test_task31"] = Task(
        name="Rig",
        parent=data["test_asset2"],
        depends=[data["test_task29"]],
        resources=[data["test_user2"]],
        alternative_resources=[data["test_user1"], data["test_user3"]],
        schedule_timing=10,
        schedule_unit="d",
    )
    DBSession.add(data["test_task31"])

    # TODO: Add Milestones
    data["kwargs"] = dict(
        name="Studio",
        daily_working_hours=8,
        timing_resolution=datetime.timedelta(hours=1),
    )

    data["test_studio"] = Studio(**data["kwargs"])
    DBSession.add(data["test_studio"])
    DBSession.commit()
    return data


def test_working_hours_arg_is_skipped(setup_studio_db_tests):
    """default working hours is used if the working_hours arg is skipped."""
    data = setup_studio_db_tests
    data["kwargs"]["name"] = "New Studio"
    try:
        data["kwargs"].pop("working_hours")  # pop if there are any
    except KeyError:
        pass

    new_studio = Studio(**data["kwargs"])
    assert new_studio.working_hours == WorkingHours()


def test_working_hours_arg_is_none(setup_studio_db_tests):
    """WorkingHour with default settings is used if working_hours arg is skipped."""
    data = setup_studio_db_tests
    data["kwargs"]["name"] = "New Studio"
    data["kwargs"]["working_hours"] = None
    new_studio = Studio(**data["kwargs"])
    assert new_studio.working_hours == WorkingHours()


def test_working_hours_attribute_is_none(setup_studio_db_tests):
    """WorkingHour with default values is used if working_hours attr is set to None."""
    data = setup_studio_db_tests
    data["test_studio"].working_horus = None
    assert data["test_studio"].working_hours == WorkingHours()


def test_working_hours_arg_is_not_a_working_hours_instance(setup_studio_db_tests):
    """TypeError is raised if the working_hours arg is not a WorkingHours instance."""
    data = setup_studio_db_tests
    data["kwargs"]["working_hours"] = "not a working hours instance"
    data["kwargs"]["name"] = "New Studio"
    with pytest.raises(TypeError) as cm:
        Studio(**data["kwargs"])

    assert (
        str(cm.value) == "Studio.working_hours should be a "
        "stalker.models.studio.WorkingHours instance, not str"
    )


def test_working_hours_attribute_is_not_a_working_hours_instance(setup_studio_db_tests):
    """TypeError is raised if working_hours attr is not a WorkingHours instance."""
    data = setup_studio_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_studio"].working_hours = "not a working hours instance"

    assert (
        str(cm.value) == "Studio.working_hours should be a "
        "stalker.models.studio.WorkingHours instance, not str"
    )


def test_working_hours_arg_is_working_properly(setup_studio_db_tests):
    """working_hours arg is passed to the working_hours attr without any problem."""
    data = setup_studio_db_tests
    data["kwargs"]["name"] = "New Studio"
    wh = WorkingHours(working_hours={"mon": [[60, 900]]})

    data["kwargs"]["working_hours"] = wh
    new_studio = Studio(**data["kwargs"])
    assert new_studio.working_hours == wh


def test_working_hours_attribute_is_working_properly(setup_studio_db_tests):
    """working_hours attribute is working properly."""
    data = setup_studio_db_tests
    new_working_hours = WorkingHours(
        working_hours={
            "mon": [[60, 1200]]  # they were doing all the jobs in
            # Monday :))
        }
    )
    assert data["test_studio"].working_hours != new_working_hours
    data["test_studio"].working_hours = new_working_hours
    assert data["test_studio"].working_hours == new_working_hours


def test_tjp_id_attribute_returns_a_plausible_id(setup_studio_db_tests):
    """tjp_id is returning something meaningful."""
    data = setup_studio_db_tests
    data["test_studio"].id = 432
    assert data["test_studio"].tjp_id == "Studio_432"


def test_projects_attribute_is_read_only(setup_studio_db_tests):
    """project attribute is a read only attribute."""
    data = setup_studio_db_tests
    with pytest.raises(AttributeError) as cm:
        data["test_studio"].projects = [data["test_project1"]]

    error_message = (
        "can't set attribute 'projects'"
        if sys.version_info.minor < 11
        else "property 'projects' of 'Studio' object has no setter"
    )

    assert str(cm.value) == error_message


def test_projects_attribute_is_working_properly(setup_studio_db_tests):
    """projects attribute is working properly."""
    data = setup_studio_db_tests
    assert sorted(data["test_studio"].projects, key=lambda x: x.name) == sorted(
        [data["test_project1"], data["test_project2"], data["test_project3"]],
        key=lambda x: x.name,
    )


def test_active_projects_attribute_is_read_only(setup_studio_db_tests):
    """active_projects attribute is a read only attribute."""
    data = setup_studio_db_tests
    with pytest.raises(AttributeError) as cm:
        data["test_studio"].active_projects = [data["test_project1"]]

    error_message = (
       "can't set attribute 'active_projects'"
        if sys.version_info.minor < 11
        else "property 'active_projects' of 'Studio' object has no setter"
    )

    assert str(cm.value) == error_message


def test_active_projects_attribute_is_working_properly(setup_studio_db_tests):
    """active_projects attribute is working properly."""
    data = setup_studio_db_tests
    assert sorted(data["test_studio"].active_projects, key=lambda x: x.name) == sorted(
        [data["test_project1"], data["test_project2"]], key=lambda x: x.name
    )


def test_inactive_projects_attribute_is_read_only(setup_studio_db_tests):
    """inactive_projects attribute is a read only attribute."""
    data = setup_studio_db_tests
    with pytest.raises(AttributeError) as cm:
        data["test_studio"].inactive_projects = [data["test_project1"]]

    error_message = (
        "can't set attribute 'inactive_projects'"
        if sys.version_info.minor < 11
        else "property 'inactive_projects' of 'Studio' object has no setter"
    )

    assert str(cm.value) == error_message


def test_inactive_projects_attribute_is_working_properly(setup_studio_db_tests):
    """inactive_projects attribute is working properly."""
    data = setup_studio_db_tests
    assert sorted(
        data["test_studio"].inactive_projects, key=lambda x: x.name
    ) == sorted([data["test_project3"]], key=lambda x: x.name)


def test_departments_attribute_is_read_only(setup_studio_db_tests):
    """departments attribute is a read only attribute."""
    data = setup_studio_db_tests
    with pytest.raises(AttributeError) as cm:
        data["test_studio"].departments = [data["test_project1"]]

    error_message = (
        "can't set attribute 'departments'"
        if sys.version_info.minor < 11
        else "property 'departments' of 'Studio' object has no setter"
    )

    assert str(cm.value) == error_message


def test_departments_attribute_is_working_properly(setup_studio_db_tests):
    """departments attribute is working properly."""
    data = setup_studio_db_tests
    admins_dep = Department.query.filter(Department.name == "admins").first()
    assert admins_dep is not None
    assert sorted(data["test_studio"].departments, key=lambda x: x.name) == sorted(
        [data["test_department1"], data["test_department2"], admins_dep],
        key=lambda x: x.name,
    )


def test_users_attribute_is_read_only(setup_studio_db_tests):
    """users attribute is a read only attribute."""
    data = setup_studio_db_tests
    with pytest.raises(AttributeError) as cm:
        data["test_studio"].users = [data["test_project1"]]

    error_message = (
        "can't set attribute 'users'"
        if sys.version_info.minor < 11
        else "property 'users' of 'Studio' object has no setter"
    )

    assert str(cm.value) == error_message


def test_users_attribute_is_working_properly(setup_studio_db_tests):
    """users attribute is working properly."""
    data = setup_studio_db_tests
    # don't forget the admin
    admin = User.query.filter_by(name="admin").first()
    assert admin is not None
    assert sorted(data["test_studio"].users, key=lambda x: x.name) == sorted(
        [admin, data["test_user1"], data["test_user2"], data["test_user3"]],
        key=lambda x: x.name,
    )


def test_to_tjp_attribute_is_read_only(setup_studio_db_tests):
    """to_tjp attribute is a read only attribute."""
    data = setup_studio_db_tests
    with pytest.raises(AttributeError) as cm:
        data["test_studio"].to_tjp = "some text"

    error_message = (
        "can't set attribute 'to_tjp'"
        if sys.version_info.minor < 11
        else "property 'to_tjp' of 'Studio' object has no setter"
    )

    assert str(cm.value) == error_message


def test_now_arg_is_skipped(setup_studio_db_tests):
    """now attr uses rounded datetime.now(pytz.utc) value if the now arg is skipped."""
    data = setup_studio_db_tests
    try:
        data["kwargs"].pop("now")
    except KeyError:
        pass

    new_studio = Studio(**data["kwargs"])
    assert new_studio.now == new_studio.round_time(datetime.datetime.now(pytz.utc))


def test_now_arg_is_None(setup_studio_db_tests):
    """now attr uses rounded datetime.now(pytz.utc) value if the now arg is None."""
    data = setup_studio_db_tests
    data["kwargs"]["now"] = None
    new_studio = Studio(**data["kwargs"])
    assert new_studio.now == new_studio.round_time(datetime.datetime.now(pytz.utc))


def test_now_attribute_is_none(setup_studio_db_tests):
    """now attr equals rounded value of datetime.now(pytz.utc) if it is set to None."""
    data = setup_studio_db_tests
    data["test_studio"].now = None
    assert data["test_studio"].now == data["test_studio"].round_time(
        datetime.datetime.now(pytz.utc)
    )


def test_now_arg_is_not_a_datetime_instance(setup_studio_db_tests):
    """TypeError is raised if the now arg is not a datetime.datetime instance."""
    data = setup_studio_db_tests
    data["kwargs"]["now"] = "not a datetime instance"
    with pytest.raises(TypeError) as cm:
        Studio(**data["kwargs"])

    assert str(cm.value) == (
        "Studio.now attribute should be an instance of datetime.datetime, "
        "not str: 'not a datetime instance'"
    )


def test_now_attribute_is_set_to_a_value_other_than_datetime_instance(
    setup_studio_db_tests,
):
    """TypeError is raised if the now attribute is set
    to a value other than a datetime.datetime instance
    """
    data = setup_studio_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_studio"].now = "not a datetime instance"

    assert (
        str(cm.value) == "Studio.now attribute should be an instance of "
        "datetime.datetime, not str: 'not a datetime instance'"
    )


def test_now_arg_is_working_properly(setup_studio_db_tests):
    """now arg value is passed to the now attribute properly."""
    data = setup_studio_db_tests
    data["kwargs"]["now"] = datetime.datetime(2013, 4, 15, 21, 9, tzinfo=pytz.utc)
    expected_now = datetime.datetime(2013, 4, 15, 21, 0, tzinfo=pytz.utc)
    new_studio = Studio(**data["kwargs"])
    assert new_studio.now == expected_now


def test_now_attribute_is_working_properly(setup_studio_db_tests):
    """now attribute is working properly."""
    data = setup_studio_db_tests
    data["test_studio"].now = datetime.datetime(2013, 4, 15, 21, 11, tzinfo=pytz.utc)
    expected_now = datetime.datetime(2013, 4, 15, 21, 0, tzinfo=pytz.utc)
    assert data["test_studio"].now == expected_now


def test_now_attribute_is_working_properly_case2(setup_studio_db_tests):
    """now attribute is working properly."""
    data = setup_studio_db_tests
    data["test_studio"]._now = None
    expected_now = Studio.round_time(datetime.datetime.now(pytz.utc))
    assert data["test_studio"].now == expected_now


def test_to_tjp_attribute_is_working_properly(setup_studio_db_tests):
    """to_tjp attribute is working properly."""
    data = setup_studio_db_tests
    data["test_studio"].start = datetime.datetime(2013, 4, 15, 17, 40, tzinfo=pytz.utc)
    data["test_studio"].end = datetime.datetime(2013, 6, 30, 17, 40, tzinfo=pytz.utc)
    data["test_studio"].working_hours[0] = [[540, 1080]]
    data["test_studio"].working_hours[1] = [[540, 1080]]
    data["test_studio"].working_hours[2] = [[540, 1080]]
    data["test_studio"].working_hours[3] = [[540, 1080]]
    data["test_studio"].working_hours[4] = [[540, 1080]]
    data["test_studio"].working_hours[5] = [[540, 720]]
    data["test_studio"].working_hours[6] = []

    expected_tjp_template = Template(
        """
project Studio_{{studio.id}} "Studio_{{studio.id}}" 2013-04-15 - 2013-06-30 {
    timingresolution 60min
    now {{ studio.now.strftime('%Y-%m-%d-%H:%M') }}
    dailyworkinghours 8
    weekstartsmonday
    workinghours mon 09:00 - 18:00
    workinghours tue 09:00 - 18:00
    workinghours wed 09:00 - 18:00
    workinghours thu 09:00 - 18:00
    workinghours fri 09:00 - 18:00
    workinghours sat 09:00 - 12:00
    workinghours sun off
    timeformat "%Y-%m-%d"
    scenario plan "Plan"
    trackingscenario plan
}
"""
    )

    expected_tjp = expected_tjp_template.render({"studio": data["test_studio"]})
    # print('-----------------------------------')
    # print(expected_tjp)
    # print('-----------------------------------')
    # print(data["test_studio"].to_tjp)
    # print('-----------------------------------')
    assert data["test_studio"].to_tjp == expected_tjp


def test_scheduler_attribute_can_be_set_to_none(setup_studio_db_tests):
    """scheduler attribute can be set to None."""
    data = setup_studio_db_tests
    data["test_studio"].scheduler = None


def test_scheduler_attribute_accepts_scheduler_instances_only(setup_studio_db_tests):
    """TypeError raised if scheduler attr is set to a value which is not a Scheduler."""
    data = setup_studio_db_tests
    with pytest.raises(TypeError) as cm:
        data["test_studio"].scheduler = "not a Scheduler instance"

    assert (
        str(cm.value) == "Studio.scheduler should be an instance of "
        "stalker.models.scheduler.SchedulerBase, not str: 'not a Scheduler instance'"
    )


def test_scheduler_attribute_is_working_properly(setup_studio_db_tests):
    """scheduler attribute is working properly."""
    data = setup_studio_db_tests
    tj_s = TaskJugglerScheduler()
    data["test_studio"].scheduler = tj_s
    assert data["test_studio"].scheduler == tj_s


def test_schedule_will_not_work_without_a_scheduler(setup_studio_db_tests):
    """RuntimeError is raised if the scheduler
    attribute is not set to a Scheduler instance and schedule is called
    """
    data = setup_studio_db_tests
    data["test_studio"].scheduler = None
    with pytest.raises(RuntimeError) as cm:
        data["test_studio"].schedule()

    assert (
        str(cm.value) == "There is no scheduler for this Studio, please assign a "
        "scheduler to the Studio.scheduler attribute, before calling "
        "Studio.schedule()"
    )


def test_schedule_will_schedule_the_tasks_with_the_given_scheduler(
    setup_studio_db_tests,
):
    """schedule method will schedule the tasks with the given scheduler."""
    data = setup_studio_db_tests
    tj_scheduler = TaskJugglerScheduler(compute_resources=True)
    data["test_studio"].now = datetime.datetime(2013, 4, 15, 22, 56, tzinfo=pytz.utc)
    data["test_studio"].start = datetime.datetime(2013, 4, 15, 22, 56, tzinfo=pytz.utc)
    data["test_studio"].end = datetime.datetime(2013, 7, 30, 0, 0, tzinfo=pytz.utc)

    # just to be sure that it is not creating any issue on schedule
    data["test_task25"].task_depends_to[0].dependency_target = "onstart"
    data["test_task25"].resources = [data["test_user2"]]

    data["test_studio"].scheduler = tj_scheduler
    data["test_studio"].schedule()
    DBSession.commit()

    # now check the timings of the tasks are all adjusted
    # Projects
    # data["test_project"]
    assert data["test_project1"].computed_start == datetime.datetime(
        2013, 4, 16, 9, 0, tzinfo=pytz.utc
    )

    assert data["test_project1"].computed_end == datetime.datetime(
        2013, 6, 24, 16, 0, tzinfo=pytz.utc
    )

    # data["test_asset1"]
    assert data["test_asset1"].computed_start == datetime.datetime(
        2013, 4, 16, 9, 0, tzinfo=pytz.utc
    )

    assert data["test_asset1"].computed_end == datetime.datetime(
        2013, 5, 17, 18, 0, tzinfo=pytz.utc
    )

    assert data["test_asset1"].computed_resources == []

    # data["test_task24"]
    assert data["test_task24"].computed_start == datetime.datetime(
        2013, 4, 16, 9, 0, tzinfo=pytz.utc
    )

    assert data["test_task24"].computed_end == datetime.datetime(
        2013, 4, 26, 17, 0, tzinfo=pytz.utc
    )

    possible_resources = [data["test_user1"], data["test_user2"], data["test_user3"]]
    assert len(data["test_task24"].computed_resources) == 1
    assert data["test_task24"].computed_resources[0] in possible_resources

    # data["test_task25"]
    assert data["test_task25"].computed_start == datetime.datetime(
        2013, 4, 16, 9, 0, tzinfo=pytz.utc
    )

    assert data["test_task25"].computed_end == datetime.datetime(
        2013, 5, 3, 12, 0, tzinfo=pytz.utc
    )

    assert len(data["test_task25"].computed_resources) == 1
    assert data["test_task25"].computed_resources[0] in possible_resources

    # data["test_task26"]
    assert data["test_task26"].computed_start == datetime.datetime(
        2013, 5, 6, 11, 0, tzinfo=pytz.utc
    )

    assert data["test_task26"].computed_end == datetime.datetime(
        2013, 5, 17, 10, 0, tzinfo=pytz.utc
    )

    assert len(data["test_task26"].computed_resources) == 1
    assert data["test_task26"].computed_resources[0] in possible_resources

    # data["test_task27"]
    assert data["test_task27"].computed_start == datetime.datetime(
        2013, 5, 7, 10, 0, tzinfo=pytz.utc
    )

    assert data["test_task27"].computed_end == datetime.datetime(
        2013, 5, 17, 18, 0, tzinfo=pytz.utc
    )

    assert len(data["test_task27"].computed_resources) == 1
    assert data["test_task27"].computed_resources[0] in possible_resources

    # data["test_shot2"]
    assert data["test_shot2"].computed_start == datetime.datetime(
        2013, 4, 26, 17, 0, tzinfo=pytz.utc
    )

    assert data["test_shot2"].computed_end == datetime.datetime(
        2013, 6, 20, 10, 0, tzinfo=pytz.utc
    )

    assert data["test_shot2"].computed_resources == []

    # data["test_task8"]
    assert data["test_task8"].computed_start == datetime.datetime(
        2013, 4, 26, 17, 0, tzinfo=pytz.utc
    )

    assert data["test_task8"].computed_end == datetime.datetime(
        2013, 4, 30, 15, 0, tzinfo=pytz.utc
    )

    assert len(data["test_task8"].computed_resources) == 1
    assert data["test_task8"].computed_resources[0] in possible_resources

    # data["test_task9"]
    assert data["test_task9"].computed_start == datetime.datetime(
        2013, 5, 30, 17, 0, tzinfo=pytz.utc
    )

    assert data["test_task9"].computed_end == datetime.datetime(
        2013, 6, 3, 15, 0, tzinfo=pytz.utc
    )

    assert len(data["test_task9"].computed_resources) == 1
    assert data["test_task9"].computed_resources[0] in possible_resources

    # data["test_task10"]
    assert data["test_task10"].computed_start == datetime.datetime(
        2013, 6, 5, 13, 0, tzinfo=pytz.utc
    )

    assert data["test_task10"].computed_end == datetime.datetime(
        2013, 6, 10, 10, 0, tzinfo=pytz.utc
    )

    assert len(data["test_task10"].computed_resources) == 1
    assert data["test_task10"].computed_resources[0] in possible_resources

    # data["test_task11"]
    assert data["test_task11"].computed_start == datetime.datetime(
        2013, 6, 14, 14, 0, tzinfo=pytz.utc
    )

    assert data["test_task11"].computed_end == datetime.datetime(
        2013, 6, 20, 10, 0, tzinfo=pytz.utc
    )

    assert len(data["test_task11"].computed_resources) == 1
    assert data["test_task11"].computed_resources[0] in possible_resources

    # data["test_shot1"]
    assert data["test_shot1"].computed_start == datetime.datetime(
        2013, 5, 16, 11, 0, tzinfo=pytz.utc
    )

    assert data["test_shot1"].computed_end == datetime.datetime(
        2013, 6, 24, 16, 0, tzinfo=pytz.utc
    )

    assert data["test_shot1"].computed_resources == []

    # data["test_task4"]
    assert data["test_task4"].computed_start == datetime.datetime(
        2013, 5, 16, 11, 0, tzinfo=pytz.utc
    )

    assert data["test_task4"].computed_end == datetime.datetime(
        2013, 5, 17, 18, 0, tzinfo=pytz.utc
    )

    assert len(data["test_task4"].computed_resources) == 1
    assert data["test_task4"].computed_resources[0] in possible_resources

    # data["test_task5"]
    assert data["test_task5"].computed_start == datetime.datetime(
        2013, 6, 5, 13, 0, tzinfo=pytz.utc
    )

    assert data["test_task5"].computed_end == datetime.datetime(
        2013, 6, 7, 11, 0, tzinfo=pytz.utc
    )

    assert len(data["test_task5"].computed_resources) == 1
    assert data["test_task5"].computed_resources[0] in possible_resources

    # data["test_task6"]
    assert data["test_task6"].computed_start == datetime.datetime(
        2013, 6, 11, 17, 0, tzinfo=pytz.utc
    )

    assert data["test_task6"].computed_end == datetime.datetime(
        2013, 6, 14, 14, 0, tzinfo=pytz.utc
    )

    assert len(data["test_task6"].computed_resources) == 1
    assert data["test_task6"].computed_resources[0] in possible_resources

    # data["test_task7"]
    assert data["test_task7"].computed_start == datetime.datetime(
        2013, 6, 20, 10, 0, tzinfo=pytz.utc
    )

    assert data["test_task7"].computed_end == datetime.datetime(
        2013, 6, 24, 16, 0, tzinfo=pytz.utc
    )

    assert len(data["test_task7"].computed_resources) == 1
    assert data["test_task7"].computed_resources[0] in possible_resources

    # data["test_task1"]
    assert data["test_task1"].computed_start == datetime.datetime(
        2013, 5, 17, 10, 0, tzinfo=pytz.utc
    )

    assert data["test_task1"].computed_end == datetime.datetime(
        2013, 5, 29, 18, 0, tzinfo=pytz.utc
    )

    assert len(data["test_task1"].computed_resources) == 1
    assert data["test_task1"].computed_resources[0] in possible_resources

    # data["test_project2"]
    # assert data["test_project2"].computed_start == \
    #     datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)
    #
    # assert data["test_project2"].computed_end == \
    #     datetime.datetime(2013, 6, 18, 12, 0, tzinfo=pytz.utc)
    #
    # assert data["test_project2"].computed_resources == []

    # data["test_asset2"]
    assert data["test_asset2"].computed_start == datetime.datetime(
        2013, 4, 16, 9, 0, tzinfo=pytz.utc
    )

    assert data["test_asset2"].computed_end == datetime.datetime(
        2013, 5, 30, 17, 0, tzinfo=pytz.utc
    )

    assert data["test_asset2"].computed_resources == []

    # data["test_task28"]
    assert data["test_task28"].computed_start == datetime.datetime(
        2013, 4, 16, 9, 0, tzinfo=pytz.utc
    )

    assert data["test_task28"].computed_end == datetime.datetime(
        2013, 4, 26, 17, 0, tzinfo=pytz.utc
    )

    assert len(data["test_task28"].computed_resources) == 1
    assert data["test_task28"].computed_resources[0] in possible_resources

    # data["test_task29"]
    assert data["test_task29"].computed_start == datetime.datetime(
        2013, 4, 26, 17, 0, tzinfo=pytz.utc
    )

    assert data["test_task29"].computed_end == datetime.datetime(
        2013, 5, 16, 11, 0, tzinfo=pytz.utc
    )

    assert len(data["test_task29"].computed_resources) == 1
    assert data["test_task29"].computed_resources[0] in possible_resources

    # data["test_task30"]
    assert data["test_task30"].computed_start == datetime.datetime(
        2013, 5, 20, 9, 0, tzinfo=pytz.utc
    )

    assert data["test_task30"].computed_end == datetime.datetime(
        2013, 5, 30, 17, 0, tzinfo=pytz.utc
    )

    assert len(data["test_task30"].computed_resources) == 1
    assert data["test_task30"].computed_resources[0] in possible_resources

    # data["test_task31"]
    assert data["test_task31"].computed_start == datetime.datetime(
        2013, 5, 20, 9, 0, tzinfo=pytz.utc
    )

    assert data["test_task31"].computed_end == datetime.datetime(
        2013, 5, 30, 17, 0, tzinfo=pytz.utc
    )

    assert len(data["test_task31"].computed_resources) == 1
    assert data["test_task31"].computed_resources[0] in possible_resources

    # data["test_shot3"]
    assert data["test_shot3"].computed_start == datetime.datetime(
        2013, 4, 30, 15, 0, tzinfo=pytz.utc
    )
    assert data["test_shot3"].computed_end == datetime.datetime(
        2013, 6, 20, 10, 0, tzinfo=pytz.utc
    )
    assert data["test_shot3"].computed_resources == []

    # data["test_task12"]
    assert data["test_task12"].computed_start == datetime.datetime(
        2013, 4, 30, 15, 0, tzinfo=pytz.utc
    )
    assert data["test_task12"].computed_end == datetime.datetime(
        2013, 5, 2, 13, 0, tzinfo=pytz.utc
    )
    assert len(data["test_task12"].computed_resources) == 1
    assert data["test_task12"].computed_resources[0] in possible_resources

    # data["test_task13"]
    assert data["test_task13"].computed_start == datetime.datetime(
        2013, 5, 30, 17, 0, tzinfo=pytz.utc
    )
    assert data["test_task13"].computed_end == datetime.datetime(
        2013, 6, 3, 15, 0, tzinfo=pytz.utc
    )
    assert len(data["test_task13"].computed_resources) == 1
    assert data["test_task13"].computed_resources[0] in possible_resources

    # data["test_task14"]
    assert data["test_task14"].computed_start == datetime.datetime(
        2013, 6, 7, 11, 0, tzinfo=pytz.utc
    )
    assert data["test_task14"].computed_end == datetime.datetime(
        2013, 6, 11, 17, 0, tzinfo=pytz.utc
    )
    assert len(data["test_task14"].computed_resources) == 1
    assert data["test_task14"].computed_resources[0] in possible_resources

    # data["test_task15"]
    assert data["test_task15"].computed_start == datetime.datetime(
        2013, 6, 14, 14, 0, tzinfo=pytz.utc
    )
    assert data["test_task15"].computed_end == datetime.datetime(
        2013, 6, 20, 10, 0, tzinfo=pytz.utc
    )
    assert len(data["test_task15"].computed_resources) == 1
    assert data["test_task15"].computed_resources[0] in possible_resources

    # data["test_shot4"]
    assert data["test_shot4"].computed_start == datetime.datetime(
        2013, 5, 2, 13, 0, tzinfo=pytz.utc
    )
    assert data["test_shot4"].computed_end == datetime.datetime(
        2013, 6, 24, 16, 0, tzinfo=pytz.utc
    )
    assert data["test_shot4"].computed_resources == []

    # data["test_task16"]
    assert data["test_task16"].computed_start == datetime.datetime(
        2013, 5, 2, 13, 0, tzinfo=pytz.utc
    )
    assert data["test_task16"].computed_end == datetime.datetime(
        2013, 5, 6, 11, 0, tzinfo=pytz.utc
    )
    assert len(data["test_task16"].computed_resources) == 1
    assert data["test_task16"].computed_resources[0] in possible_resources

    # data["test_task17"]
    assert data["test_task17"].computed_start == datetime.datetime(
        2013, 6, 3, 15, 0, tzinfo=pytz.utc
    )
    assert data["test_task17"].computed_end == datetime.datetime(
        2013, 6, 5, 13, 0, tzinfo=pytz.utc
    )
    assert len(data["test_task17"].computed_resources) == 1
    assert data["test_task17"].computed_resources[0] in possible_resources

    # data["test_task18"]
    assert data["test_task18"].computed_start == datetime.datetime(
        2013, 6, 10, 10, 0, tzinfo=pytz.utc
    )
    assert data["test_task18"].computed_end == datetime.datetime(
        2013, 6, 12, 16, 0, tzinfo=pytz.utc
    )
    assert len(data["test_task18"].computed_resources) == 1
    assert data["test_task18"].computed_resources[0] in possible_resources

    # data["test_task19"]
    assert data["test_task19"].computed_start == datetime.datetime(
        2013, 6, 19, 11, 0, tzinfo=pytz.utc
    )
    assert data["test_task19"].computed_end == datetime.datetime(
        2013, 6, 24, 16, 0, tzinfo=pytz.utc
    )
    assert len(data["test_task19"].computed_resources) == 1
    assert data["test_task19"].computed_resources[0] in possible_resources

    # data["test_task2"]
    assert data["test_task2"].computed_start == datetime.datetime(
        2013, 5, 30, 9, 0, tzinfo=pytz.utc
    )
    assert data["test_task2"].computed_end == datetime.datetime(
        2013, 6, 11, 17, 0, tzinfo=pytz.utc
    )
    assert len(data["test_task2"].computed_resources) == 1
    assert data["test_task2"].computed_resources[0] in possible_resources


def test_schedule_schedules_only_tasks_of_the_given_projects_with_the_given_scheduler(
    setup_studio_db_tests,
):
    """schedule method schedules the tasks of the projects with the Scheduler."""
    data = setup_studio_db_tests
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

    tj_scheduler = TaskJugglerScheduler(
        compute_resources=True, projects=[dummy_project]
    )

    data["test_studio"].now = datetime.datetime(2013, 4, 15, 22, 56, tzinfo=pytz.utc)
    data["test_studio"].start = datetime.datetime(2013, 4, 15, 22, 56, tzinfo=pytz.utc)
    data["test_studio"].end = datetime.datetime(2013, 7, 30, 0, 0, tzinfo=pytz.utc)

    data["test_studio"].scheduler = tj_scheduler
    data["test_studio"].schedule()
    DBSession.commit()

    # now check the timings of the tasks are all adjusted
    assert dt1.computed_start == datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)
    assert dt1.computed_end == datetime.datetime(2013, 4, 16, 13, 0, tzinfo=pytz.utc)
    assert dt2.computed_start == datetime.datetime(2013, 4, 16, 9, 0, tzinfo=pytz.utc)
    assert dt2.computed_end == datetime.datetime(2013, 4, 16, 13, 0, tzinfo=pytz.utc)

    # data["test_project"]
    assert data["test_project1"].computed_start is None
    assert data["test_project1"].computed_end is None

    # data["test_asset1"]
    assert data["test_asset1"].computed_start is None
    assert data["test_asset1"].computed_end is None
    assert data["test_asset1"].computed_resources == data["test_asset1"].resources

    # data["test_task24"]
    assert data["test_task24"].computed_start is None
    assert data["test_task24"].computed_end is None
    assert data["test_task24"].computed_resources == data["test_task24"].resources

    # data["test_task25"]
    assert data["test_task25"].computed_start is None
    assert data["test_task25"].computed_end is None
    assert data["test_task25"].computed_resources == data["test_task25"].resources

    # data["test_task26"]
    assert data["test_task26"].computed_start is None
    assert data["test_task26"].computed_end is None
    assert data["test_task26"].computed_resources == data["test_task26"].resources

    # data["test_task27"]
    assert data["test_task27"].computed_start is None
    assert data["test_task27"].computed_end is None
    assert data["test_task27"].computed_resources == data["test_task27"].resources

    # data["test_shot2"]
    assert data["test_shot2"].computed_start is None
    assert data["test_shot2"].computed_end is None
    assert data["test_shot2"].computed_resources == data["test_shot2"].resources

    # data["test_task8"]
    assert data["test_task8"].computed_start is None
    assert data["test_task8"].computed_end is None
    assert data["test_task8"].computed_resources == data["test_task8"].resources

    # data["test_task9"]
    assert data["test_task9"].computed_start is None
    assert data["test_task9"].computed_end is None
    assert data["test_task9"].computed_resources == data["test_task9"].resources

    # data["test_task10"]
    assert data["test_task10"].computed_start is None
    assert data["test_task10"].computed_end is None
    assert data["test_task10"].computed_resources == data["test_task10"].resources

    # data["test_task11"]
    assert data["test_task11"].computed_start is None
    assert data["test_task11"].computed_end is None
    assert data["test_task11"].computed_resources == data["test_task11"].resources

    # data["test_shot1"]
    assert data["test_shot1"].computed_start is None
    assert data["test_shot1"].computed_end is None
    assert data["test_shot1"].computed_resources == data["test_shot1"].resources

    # data["test_task4"]
    assert data["test_task4"].computed_start is None
    assert data["test_task4"].computed_end is None
    assert data["test_task4"].computed_resources == data["test_task4"].resources

    # data["test_task5"]
    assert data["test_task5"].computed_start is None
    assert data["test_task5"].computed_end is None
    assert data["test_task5"].computed_resources == data["test_task5"].resources

    # data["test_task6"]
    assert data["test_task6"].computed_start is None
    assert data["test_task6"].computed_end is None
    assert data["test_task6"].computed_resources == data["test_task6"].resources

    # data["test_task7"]
    assert data["test_task7"].computed_start is None
    assert data["test_task7"].computed_end is None
    assert data["test_task7"].computed_resources == data["test_task7"].resources

    # data["test_task1"]
    assert data["test_task1"].computed_start is None
    assert data["test_task1"].computed_end is None
    assert data["test_task1"].computed_resources == data["test_task1"].resources

    # data["test_asset2"]
    assert data["test_asset2"].computed_start is None
    assert data["test_asset2"].computed_end is None
    assert data["test_asset2"].computed_resources == data["test_asset2"].resources

    # data["test_task28"]
    assert data["test_task28"].computed_start is None
    assert data["test_task28"].computed_end is None
    assert data["test_task28"].computed_resources == data["test_task28"].resources

    # data["test_task29"]
    assert data["test_task29"].computed_start is None
    assert data["test_task29"].computed_end is None
    assert data["test_task29"].computed_resources == data["test_task29"].resources

    # data["test_task30"]
    assert data["test_task30"].computed_start is None
    assert data["test_task30"].computed_end is None
    assert data["test_task30"].computed_resources == data["test_task30"].resources

    # data["test_task31"]
    assert data["test_task31"].computed_start is None
    assert data["test_task31"].computed_end is None
    assert data["test_task31"].computed_resources == data["test_task31"].resources

    # data["test_shot3"]
    assert data["test_shot3"].computed_start is None
    assert data["test_shot3"].computed_end is None
    assert data["test_shot3"].computed_resources == data["test_shot3"].resources

    # data["test_task12"]
    assert data["test_task12"].computed_start is None
    assert data["test_task12"].computed_end is None
    assert data["test_task12"].computed_resources == data["test_task12"].resources

    # data["test_task13"]
    assert data["test_task13"].computed_start is None
    assert data["test_task13"].computed_end is None
    assert data["test_task13"].computed_resources == data["test_task13"].resources

    # data["test_task14"]
    assert data["test_task14"].computed_start is None
    assert data["test_task14"].computed_end is None
    assert data["test_task14"].computed_resources == data["test_task14"].resources

    # data["test_task15"]
    assert data["test_task15"].computed_start is None
    assert data["test_task15"].computed_end is None
    assert data["test_task15"].computed_resources == data["test_task15"].resources

    # data["test_shot4"]
    assert data["test_shot4"].computed_start is None
    assert data["test_shot4"].computed_end is None
    assert data["test_shot4"].computed_resources == data["test_shot4"].resources

    # data["test_task16"]
    assert data["test_task16"].computed_start is None
    assert data["test_task16"].computed_end is None
    assert data["test_task16"].computed_resources == data["test_task16"].resources

    # data["test_task17"]
    assert data["test_task17"].computed_start is None
    assert data["test_task17"].computed_end is None
    assert data["test_task17"].computed_resources == data["test_task17"].resources

    # data["test_task18"]
    assert data["test_task18"].computed_start is None
    assert data["test_task18"].computed_end is None
    assert data["test_task18"].computed_resources == data["test_task18"].resources

    # data["test_task19"]
    assert data["test_task19"].computed_start is None
    assert data["test_task19"].computed_end is None
    assert data["test_task19"].computed_resources == data["test_task19"].resources

    # data["test_task2"]
    assert data["test_task2"].computed_start is None
    assert data["test_task2"].computed_end is None
    assert data["test_task2"].computed_resources == data["test_task2"].resources


def test_is_scheduling_will_be_false_after_scheduling_is_done(setup_studio_db_tests):
    """is_scheduling attribute is back to False if the scheduling is finished."""
    data = setup_studio_db_tests
    # use a dummy scheduler
    data["test_studio"].now = datetime.datetime(2013, 4, 15, 22, 56, tzinfo=pytz.utc)
    data["test_studio"].start = datetime.datetime(2013, 4, 15, 22, 56, tzinfo=pytz.utc)
    data["test_studio"].end = datetime.datetime(2013, 7, 30, 0, 0, tzinfo=pytz.utc)

    def callback():
        assert data["test_studio"].is_scheduling is True

    dummy_scheduler = DummyScheduler(callback=callback)

    data["test_studio"].scheduler = dummy_scheduler
    assert data["test_studio"].is_scheduling is False

    # with v0.2.6.9 it is now the users duty to set is_scheduling to True
    data["test_studio"].is_scheduling = True

    data["test_studio"].schedule()
    assert data["test_studio"].is_scheduling is False


def test_schedule_will_store_schedule_info_in_database(setup_studio_db_tests):
    """schedule method will store the schedule info in database."""
    data = setup_studio_db_tests
    tj_scheduler = TaskJugglerScheduler()
    data["test_studio"].now = datetime.datetime(2013, 4, 15, 22, 56, tzinfo=pytz.utc)
    data["test_studio"].start = datetime.datetime(2013, 4, 15, 22, 56, tzinfo=pytz.utc)
    data["test_studio"].end = datetime.datetime(2013, 7, 30, 0, 0, tzinfo=pytz.utc)

    data["test_studio"].scheduler = tj_scheduler
    data["test_studio"].schedule(scheduled_by=data["test_user1"])

    assert data["test_studio"].last_scheduled_by == data["test_user1"]

    last_schedule_message = data["test_studio"].last_schedule_message
    last_scheduled_at = data["test_studio"].last_scheduled_at
    last_scheduled_by = data["test_studio"].last_scheduled_by

    assert last_schedule_message is not None
    assert last_scheduled_at is not None
    assert last_scheduled_by is not None

    DBSession.add(data["test_studio"])
    DBSession.commit()

    # delete the studio instance and retrieve it back and check if it has
    # the info
    del data["test_studio"]

    studio = Studio.query.first()

    assert studio.is_scheduling is False
    assert datetime.datetime.now(
        pytz.utc
    ) - studio.scheduling_started_at < datetime.timedelta(minutes=1)
    assert studio.last_schedule_message == last_schedule_message
    assert studio.last_scheduled_at == last_scheduled_at
    assert studio.last_scheduled_by == last_scheduled_by

    assert studio.last_scheduled_by_id == data["test_user1"].id
    assert studio.last_scheduled_by == data["test_user1"]


def test_vacation_attribute_is_read_only(setup_studio_db_tests):
    """vacation attribute is a read-only attribute."""
    data = setup_studio_db_tests
    with pytest.raises(AttributeError) as cm:
        data["test_studio"].vacations = "some random value"

    error_message = (
        "can't set attribute 'vacations'"
        if sys.version_info.minor < 11
        else "property 'vacations' of 'Studio' object has no setter"
    )

    assert str(cm.value) == error_message


def test_vacation_attribute_returns_studio_vacation_instances(setup_studio_db_tests):
    """vacation attribute is returning the Vacation instances with no user set."""
    data = setup_studio_db_tests
    vacation1 = Vacation(
        start=datetime.datetime(2013, 8, 2, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 8, 10, tzinfo=pytz.utc),
    )
    vacation2 = Vacation(
        start=datetime.datetime(2013, 8, 11, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 8, 20, tzinfo=pytz.utc),
    )
    vacation3 = Vacation(
        user=data["test_user1"],
        start=datetime.datetime(2013, 8, 11, tzinfo=pytz.utc),
        end=datetime.datetime(2013, 8, 20, tzinfo=pytz.utc),
    )
    DBSession.add_all([vacation1, vacation2, vacation3])
    DBSession.commit()

    assert sorted(data["test_studio"].vacations, key=lambda x: x.name) == sorted(
        [vacation1, vacation2], key=lambda x: x.name
    )


def test_timing_resolution_arg_skipped(setup_studio_db_tests):
    """timing_resolution attr is set to default if timing_resolution arg is skipped."""
    data = setup_studio_db_tests
    try:
        data["kwargs"].pop("timing_resolution")
    except KeyError:
        pass

    studio = Studio(**data["kwargs"])
    assert studio.timing_resolution == defaults.timing_resolution


def test_timing_resolution_arg_is_none(setup_studio_db_tests):
    """timing_resolution attr is set to default if timing_resolution arg is None."""
    data = setup_studio_db_tests
    data["kwargs"]["timing_resolution"] = None
    studio = Studio(**data["kwargs"])
    assert studio.timing_resolution == defaults.timing_resolution


def test_timing_resolution_attribute_is_set_to_none(setup_studio_db_tests):
    """timing_resolution attr is set to the default if it is set to None."""
    data = setup_studio_db_tests
    data["kwargs"]["timing_resolution"] = datetime.timedelta(minutes=5)
    studio = Studio(**data["kwargs"])
    # check start conditions
    assert studio.timing_resolution == data["kwargs"]["timing_resolution"]
    studio.timing_resolution = None
    assert studio.timing_resolution == defaults.timing_resolution


def test_timing_resolution_arg_is_not_a_timedelta_instance(setup_studio_db_tests):
    """TypeError is raised if timing_resolution arg is not datetime.timedelta."""
    data = setup_studio_db_tests
    data["kwargs"]["timing_resolution"] = "not a timedelta instance"
    with pytest.raises(TypeError) as cm:
        Studio(**data["kwargs"])

    assert str(cm.value) == (
        "Studio.timing_resolution should be an instance of datetime.timedelta, "
        "not str: 'not a timedelta instance'"
    )


def test_timing_resolution_attribute_is_not_a_timedelta_instance(setup_studio_db_tests):
    """TypeError raised if timing_resolution attr is not a datetime.timedelta."""
    data = setup_studio_db_tests
    new_foo_obj = Studio(**data["kwargs"])
    with pytest.raises(TypeError) as cm:
        new_foo_obj.timing_resolution = "not a timedelta instance"

    assert str(cm.value) == (
        "Studio.timing_resolution should be an instance of datetime.timedelta, "
        "not str: 'not a timedelta instance'"
    )


def test_timing_resolution_arg_is_working_properly(setup_studio_db_tests):
    """timing_resolution arg value is passed to timing_resolution attr correctly."""
    data = setup_studio_db_tests
    data["kwargs"]["timing_resolution"] = datetime.timedelta(minutes=5)
    studio = Studio(**data["kwargs"])
    assert studio.timing_resolution == data["kwargs"]["timing_resolution"]


def test_timing_resolution_attribute_is_working_properly(setup_studio_db_tests):
    """timing_resolution attribute is working properly."""
    data = setup_studio_db_tests
    studio = Studio(**data["kwargs"])
    res = studio
    new_res = datetime.timedelta(hours=1, minutes=30)
    assert res != new_res
    studio.timing_resolution = new_res
    assert studio.timing_resolution == new_res
