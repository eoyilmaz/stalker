# -*- coding: utf-8 -*-
"""DateRangeMixin related tests."""

import datetime
import logging

import pytest

import pytz

from sqlalchemy import Column, ForeignKey, Integer

from stalker import log
from stalker.models.entity import SimpleEntity
from stalker.models.mixins import DateRangeMixin


logger = log.get_logger(__name__)
log.set_level(logging.DEBUG)


class DeclSchedMixA(SimpleEntity, DateRangeMixin):
    """A class for testing DateRangeMixin."""

    __tablename__ = "DeclSchedMixAs"
    __mapper_args__ = {"polymorphic_identity": "DeclSchedMixA"}
    a_id = Column("id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True)

    def __init__(self, **kwargs):
        super(DeclSchedMixA, self).__init__(**kwargs)
        DateRangeMixin.__init__(self, **kwargs)


class DeclSchedMixB(SimpleEntity, DateRangeMixin):
    """A class for testing DateRangeMixin."""

    __tablename__ = "DeclSchedMixBs"
    __mapper_args__ = {"polymorphic_identity": "DeclSchedMixB"}
    b_id = Column("id", Integer, ForeignKey("SimpleEntities.id"), primary_key=True)

    def __init__(self, **kwargs):
        super(DeclSchedMixB, self).__init__(**kwargs)
        DateRangeMixin.__init__(self, **kwargs)


@pytest.fixture(scope="function")
def setup_schedule_mixin_tester():
    """Set up the tests for DateRangeMixin setup.

    Returns:
        dict: Test data.
    """
    data = dict()
    data["kwargs"] = {
        "name": "ozgur",
        "start": datetime.datetime(2013, 3, 20, 4, 0, tzinfo=pytz.utc),
        "end": datetime.datetime(2013, 3, 30, 4, 0, tzinfo=pytz.utc),
        "duration": datetime.timedelta(10),
    }
    return data


def test_mixin_setup_is_working_as_expected(setup_schedule_mixin_tester):
    """Mixin setup is working as expected."""
    data = setup_schedule_mixin_tester
    new_a = DeclSchedMixA(**data["kwargs"])  # should not create any problem
    assert new_a.start == data["kwargs"]["start"]
    assert new_a.end == data["kwargs"]["end"]
    assert new_a.duration == data["kwargs"]["duration"]

    logger.debug("----------------------------")
    logger.debug(new_a.start)
    logger.debug(new_a.end)
    logger.debug(new_a.duration)

    # try to change the start and check if the duration is also updated
    new_a.start = datetime.datetime(2013, 3, 30, 10, 0, tzinfo=pytz.utc)

    assert new_a.start == datetime.datetime(2013, 3, 30, 10, 0, tzinfo=pytz.utc)

    assert new_a.end == datetime.datetime(2013, 4, 9, 10, 0, tzinfo=pytz.utc)

    assert new_a.duration == datetime.timedelta(10)

    a_start = new_a.start
    a_end = new_a.end
    a_duration = new_a.duration

    # now check the start, end and duration
    logger.debug("----------------------------")
    logger.debug(new_a.start)
    logger.debug(new_a.end)
    logger.debug(new_a.duration)

    # create a new class
    new_b = DeclSchedMixB(**data["kwargs"])
    # now check the start, end and duration
    assert new_b.start == data["kwargs"]["start"]
    assert new_b.end == data["kwargs"]["end"]
    assert new_b.duration == data["kwargs"]["duration"]

    logger.debug("----------------------------")
    logger.debug(new_b.start)
    logger.debug(new_b.end)
    logger.debug(new_b.duration)

    # now check the start, end and duration of A
    logger.debug("----------------------------")
    logger.debug(new_a.start)
    logger.debug(new_a.end)
    logger.debug(new_a.duration)
    assert new_a.start == a_start
    assert new_a.end == a_end
    assert new_a.duration == a_duration
