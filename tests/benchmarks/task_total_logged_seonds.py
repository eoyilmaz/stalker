# -*- coding: utf-8 -*-
"""Benchmark total logged session computation."""
import datetime
import logging
import os
import time

import pytz
from sqlalchemy.orm import close_all_sessions

from sqlalchemy.pool import NullPool

import stalker
import stalker.db.setup
from stalker import (
    Project,
    Repository,
    Status,
    StatusList,
    Task,
    TimeLog,
    Type,
    User,
    db,
    log,
)
from stalker.config import Config
from stalker.db.declarative import Base
from stalker.db.session import DBSession

from stalker.models.enum import TimeUnit
from stalker.models.enum import ScheduleModel
from tests.utils import create_random_db, drop_db, get_server_details_from_url

log.logging_level = logging.INFO
logging.getLogger("stalker.models.task").setLevel(logging.INFO)


# create a new database for this test only
database_url = create_random_db()

# update the config
config = {"sqlalchemy.url": database_url, "sqlalchemy.poolclass": NullPool}


try:
    os.environ.pop(Config.env_key)
except KeyError:
    # already removed
    pass

# regenerate the defaults
# stalker.defaults = Config()
stalker.defaults.config_values = stalker.defaults.default_config_values.copy()
stalker.defaults["timing_resolution"] = datetime.timedelta(minutes=10)

# init database
stalker.db.setup.setup(config)
stalker.db.setup.init()

status_wfd = Status.query.filter_by(code="WFD").first()
status_rts = Status.query.filter_by(code="RTS").first()
status_wip = Status.query.filter_by(code="WIP").first()
status_prev = Status.query.filter_by(code="PREV").first()
status_hrev = Status.query.filter_by(code="HREV").first()
status_drev = Status.query.filter_by(code="DREV").first()
status_oh = Status.query.filter_by(code="OH").first()
status_stop = Status.query.filter_by(code="STOP").first()
status_cmpl = Status.query.filter_by(code="CMPL").first()

task_status_list = StatusList.query.filter_by(target_entity_type="Task").first()

test_movie_project_type = Type(
    name="Movie Project",
    code="movie",
    target_entity_type="Project",
)

test_repository_type = Type(
    name="Test Repository Type",
    code="test",
    target_entity_type="Repository",
)

test_repository = Repository(
    name="Test Repository",
    code="TR",
    type=test_repository_type,
    linux_path="/mnt/T/",
    windows_path="T:/",
    macos_path="/Volumes/T/",
)


test_user1 = User(name="User1", login="user1", email="user1@user1.com", password="1234")

test_user2 = User(name="User2", login="user2", email="user2@user2.com", password="1234")

test_user3 = User(name="User3", login="user3", email="user3@user3.com", password="1234")

test_user4 = User(name="User4", login="user4", email="user4@user4.com", password="1234")

test_user5 = User(name="User5", login="user5", email="user5@user5.com", password="1234")


test_project1 = Project(
    name="Test Project1",
    code="tp1",
    type=test_movie_project_type,
    repositories=[test_repository],
)

test_dependent_task1 = Task(
    name="Dependent Task1",
    project=test_project1,
    status_list=task_status_list,
    responsible=[test_user1],
)

test_dependent_task2 = Task(
    name="Dependent Task2",
    project=test_project1,
    status_list=task_status_list,
    responsible=[test_user1],
)

kwargs = {
    "name": "Modeling",
    "description": "A Modeling Task",
    "project": test_project1,
    "priority": 500,
    "responsible": [test_user1],
    "resources": [test_user1, test_user2],
    "alternative_resources": [test_user3, test_user4, test_user5],
    "allocation_strategy": "minloaded",
    "persistent_allocation": True,
    "watchers": [test_user3],
    "bid_timing": 4,
    "bid_unit": TimeUnit.Day,
    "schedule_timing": 1,
    "schedule_unit": TimeUnit.Day,
    "start": datetime.datetime(2013, 4, 8, 13, 0, tzinfo=pytz.utc),
    "end": datetime.datetime(2013, 4, 8, 18, 0, tzinfo=pytz.utc),
    "depends_on": [test_dependent_task1, test_dependent_task2],
    "time_logs": [],
    "versions": [],
    "is_milestone": False,
    "status": 0,
    "status_list": task_status_list,
}


DBSession.add_all(
    [
        test_movie_project_type,
        test_repository_type,
        test_repository,
        test_user1,
        test_user2,
        test_user3,
        test_user4,
        test_user5,
        test_project1,
        test_dependent_task1,
        test_dependent_task2,
    ]
)
DBSession.commit()


kwargs["depends_on"] = []

dt = datetime.datetime
td = datetime.timedelta
now = dt(2017, 3, 15, 0, 30, tzinfo=pytz.utc)

kwargs["schedule_model"] = ScheduleModel.Effort

# -------------- HOURS --------------
kwargs["schedule_timing"] = 10
kwargs["schedule_unit"] = TimeUnit.Hour
new_task = Task(**kwargs)
DBSession.add(new_task)

# create 100000 of 10 minutes of TimeLogs
benchmark_start = time.time()

tl_count = 100000

start = now
ten_minutes = datetime.timedelta(minutes=10)
resource = kwargs["resources"][0]
print(f"creating {tl_count} TimeLogs")
for i in range(tl_count):
    end = start + ten_minutes
    tl = TimeLog(
        resource=resource,
        task=new_task,
        start=start,
        end=end,
    )
    DBSession.add(tl)
    start = end
    if i % 1000 == 0:
        print(f"i: {i}")
        DBSession.flush()
        DBSession.commit()
DBSession.flush()
DBSession.commit()

benchmark_end = time.time()
print("data created in: {:0.3f} secs".format(benchmark_end - benchmark_start))

task_id = new_task.id
# del all the TimeLogs
del new_task.time_logs
del new_task


# now get back the task from db
task_from_db = DBSession.get(Task, task_id)

# now query the total_logged_seconds
benchmark_start = time.time()
total_logged_seconds = task_from_db.total_logged_seconds
benchmark_end = time.time()
print("total_logged_seconds: {:0.3f} sec".format(total_logged_seconds))
print("old way worked in: {:0.3f} sec".format(benchmark_end - benchmark_start))

# now use the new way of doing it
benchmark_start = time.time()
quick_total_logged_seconds = task_from_db.total_logged_seconds
benchmark_end = time.time()
print("quick_total_logged_seconds: {:0.3f} sec".format(quick_total_logged_seconds))
print("new way worked in: {:0.3f} sec".format(benchmark_end - benchmark_start))
assert total_logged_seconds == quick_total_logged_seconds

# clean up test database
DBSession.rollback()
connection = DBSession.connection()
engine = connection.engine
connection.close()

Base.metadata.drop_all(engine, checkfirst=True)
DBSession.remove()

stalker.defaults["timing_resolution"] = datetime.timedelta(hours=1)

close_all_sessions()
drop_db(**get_server_details_from_url(database_url))
