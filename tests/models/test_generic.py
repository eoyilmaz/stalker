# -*- coding: utf-8 -*-


def test_make_plural_is_working_properly():
    """testing if stalker.models.make_plural() function is working properly
    """
    from stalker.models import make_plural
    test_words = [
        ('asset', 'assets'),
        ('client', 'clients'),
        ('department', 'departments'),
        ('entity', 'entities'),
        ('template', 'templates'),
        ('group', 'groups'),
        ('format', 'formats'),
        ('link', 'links'),
        ('session', 'sessions'),
        ('note', 'notes'),
        ('permission', 'permissions'),
        ('project', 'projects'),
        ('repository', 'repositories'),
        ('review', 'reviews'),
        ('scene', 'scenes'),
        ('sequence', 'sequences'),
        ('shot', 'shots'),
        ('status', 'statuses'),
        ('list', 'lists'),
        ('structure', 'structures'),
        ('studio', 'studios'),
        ('tag', 'tags'),
        ('task', 'tasks'),
        ('dependency', 'dependencies'),
        ('type', 'types'),
        ('bench', 'benches'),
        ('thief', 'thieves')
    ]
    for t, e in test_words:
        r = make_plural(t)
        assert r == e


def test_utc_to_local_is_working_properly():
    """testing if utc_to_local() function is working properly
    """
    from stalker.models import utc_to_local
    import datetime
    import pytz
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
    """testing if local_to_utc() function is working properly
    """
    from stalker.models import local_to_utc
    import datetime
    import pytz
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
