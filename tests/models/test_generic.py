# -*- coding: utf-8 -*-
"""Tests utility functions."""

import datetime

import pytest

import pytz

from stalker.utils import make_plural, utc_to_local, local_to_utc


@pytest.mark.parametrize(
    "test_value,expected",
    [
        ("asset", "assets"),
        ("client", "clients"),
        ("department", "departments"),
        ("entity", "entities"),
        ("template", "templates"),
        ("group", "groups"),
        ("format", "formats"),
        ("link", "links"),
        ("session", "sessions"),
        ("note", "notes"),
        ("permission", "permissions"),
        ("project", "projects"),
        ("repository", "repositories"),
        ("review", "reviews"),
        ("scene", "scenes"),
        ("sequence", "sequences"),
        ("shot", "shots"),
        ("status", "statuses"),
        ("list", "lists"),
        ("structure", "structures"),
        ("studio", "studios"),
        ("tag", "tags"),
        ("task", "tasks"),
        ("dependency", "dependencies"),
        ("type", "types"),
        ("bench", "benches"),
        ("thief", "thieves"),
    ],
)
def test_make_plural_is_working_properly(test_value, expected):
    """make_plural() is working properly."""
    assert expected == make_plural(test_value)


def test_utc_to_local_is_working_properly():
    """utc_to_local() is working properly."""
    local_now = datetime.datetime.now()
    utc_now = datetime.datetime.now(pytz.utc)

    utc_without_tz = datetime.datetime(
        utc_now.year,
        utc_now.month,
        utc_now.day,
        utc_now.hour,
        utc_now.minute,
    )
    local_from_utc = utc_to_local(utc_without_tz)

    assert local_from_utc.year == local_now.year
    assert local_from_utc.month == local_now.month
    assert local_from_utc.day == local_now.day
    assert local_from_utc.hour == local_now.hour
    assert local_from_utc.minute == local_now.minute


def test_local_to_utc_is_working_properly():
    """local_to_utc() is working properly."""
    local_now = datetime.datetime.now()
    utc_now = datetime.datetime.now(pytz.utc)

    utc_without_tz = datetime.datetime(
        utc_now.year,
        utc_now.month,
        utc_now.day,
        utc_now.hour,
        utc_now.minute,
    )
    utc_from_local = local_to_utc(local_now)

    assert utc_from_local.year == utc_without_tz.year
    assert utc_from_local.month == utc_without_tz.month
    assert utc_from_local.day == utc_without_tz.day
    assert utc_from_local.hour == utc_without_tz.hour
    assert utc_from_local.minute == utc_without_tz.minute
