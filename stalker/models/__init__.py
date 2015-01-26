# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
import calendar
import datetime
from stalker.exceptions import CircularDependencyError


def make_plural(name):
    """Returns the plural version of the given name argument.
    """
    plural_name = name + "s"

    if name[-1] == "y":
        plural_name = name[:-1] + "ies"
    elif name[-2:] == "ch":
        plural_name = name + "es"
    elif name[-1] == "f":
        plural_name = name[:-1] + "ves"
    elif name[-1] == "s":
        plural_name = name + "es"

    return plural_name


def walk_hierarchy(entity, attr, method=0):
    """Walks the entity hierarchy over the given attribute and yields the
    entity.

    It doesn't check for cycle, so if the attribute is not acyclic then this
    function will not find an exit point.

    The default mode is Depth First Search (DFS), to walk with Breadth First
    Search (BFS) set the direction to 1.

    :param entity: Starting Entity
    :param attr: The attribute name to walk over
    :param method: 0:Depth first or 1:Breadth First
    :return:
    """
    entity_to_visit = [entity]
    if not method:  # DFS
        while len(entity_to_visit):
            current_entity = entity_to_visit.pop(0)
            for child in reversed(getattr(current_entity, attr)):
                entity_to_visit.insert(0, child)
            yield current_entity
    else:  # BFS
        while len(entity_to_visit):
            current_entity = entity_to_visit.pop(0)
            entity_to_visit.extend(getattr(current_entity, attr))
            yield current_entity


def check_circular_dependency(entity, other_entity, attr_name):
    """Checks the circular dependency in entity if it has other_entity in its
    dependency attr which is specified with attr_name
    """
    for e in walk_hierarchy(entity, attr_name):
        if e is other_entity:
            raise CircularDependencyError(
                '%(entity_name)s (%(entity_class)s) and '
                '%(other_entity_name)s (%(other_entity_class)s) creates a '
                'circular dependency in their "%(attr_name)s" attribute' %
                {
                    'entity_name': entity,
                    'entity_class': entity.__class__.__name__,
                    'other_entity_name': other_entity,
                    'other_entity_class': other_entity.__class__.__name__,
                    'attr_name': attr_name
                }
            )


def utc_to_local(utc_dt):
    """converts utc time to local time

    based on the answer of J.F. Sebastian on
    http://stackoverflow.com/questions/4563272/how-to-convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-stand/13287083#13287083
    """
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.datetime.fromtimestamp(timestamp)
    return local_dt.replace(microsecond=utc_dt.microsecond)


def local_to_utc(local_dt):
    """converts local datetime to utc datetime

    based on the answer of J.F. Sebastian on
    http://stackoverflow.com/questions/4563272/how-to-convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-stand/13287083#13287083
    """
    # get the utc_dt as if the local_dt is utc and calculate the timezone
    # difference and add it to the local dt object
    return local_dt - (utc_to_local(local_dt) - local_dt)
