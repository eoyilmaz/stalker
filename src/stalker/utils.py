# -*- coding: utf-8 -*-
"""Utilities are situated here."""
import calendar
from datetime import datetime
from typing import Any, Generator

from stalker.exceptions import CircularDependencyError


def make_plural(name: str) -> str:
    """Return the plural version of the given name argument.

    Args:
        name (str): The name to make plural.

    Returns:
        str: The plural version of the given name.
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


def walk_hierarchy(entity: Any, attr: str, method: int = 0) -> Generator[Any, Any, Any]:
    """Walk the entity hierarchy over the given attribute and yield the entities found.

    It doesn't check for cycle, so if the attribute is not acyclic then this
    function will not find an exit point.

    The default mode is Depth First Search (DFS), to walk with Breadth First
    Search (BFS) set the direction to 1.

    Args:
        entity (Any): Starting Entity.
        attr (str): The attribute name to walk over.
        method (int): 0:Depth first or 1:Breadth First

    Yields:
        Any: List any entities found while traversing the hierarchy.
    """
    entity_to_visit = [entity]
    if not method:  # Depth First Search (DFS)
        while len(entity_to_visit):
            current_entity = entity_to_visit.pop(0)
            for child in reversed(getattr(current_entity, attr)):
                entity_to_visit.insert(0, child)
            yield current_entity
    else:  # Breadth First Search (BFS)
        while len(entity_to_visit):
            current_entity = entity_to_visit.pop(0)
            entity_to_visit.extend(getattr(current_entity, attr))
            yield current_entity


def check_circular_dependency(entity: Any, other_entity: Any, attr_name: str) -> None:
    """Check circular dependency.

    Check if entity and other_entity are in circular dependency over the attr with the
    name attr_name.

    Args:
        entity (Any): Any Python object.
        other_entity (Any): Any Python object.
        attr_name (str): The name of the attribute to check the circular dependency of.

    Raises:
        CircularDependencyError: If the entities are in circular dependency over the
            attr with the name attr_name.
    """
    for e in walk_hierarchy(entity, attr_name):
        if e is other_entity:
            raise CircularDependencyError(
                "{entity_name} ({entity_class}) and "
                "{other_entity_name} ({other_entity_class}) creates a "
                'circular dependency in their "{attr_name}" attribute'.format(
                    entity_name=entity,
                    entity_class=entity.__class__.__name__,
                    other_entity_name=other_entity,
                    other_entity_class=other_entity.__class__.__name__,
                    attr_name=attr_name,
                )
            )


def utc_to_local(utc_datetime) -> datetime:
    """Convert utc time to local time.

    Based on the answer of J.F. Sebastian on
    http://stackoverflow.com/questions/4563272/how-to-convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-stand/13287083#13287083

    Args:
        utc_datetime (datetime): The UTC datetime instance.

    Returns:
        datetime: The local datetime instance.
    """
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_datetime.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    return local_dt.replace(microsecond=utc_datetime.microsecond)


def local_to_utc(local_datetime) -> datetime:
    """Convert local datetime to utc datetime.

    Based on the answer of J.F. Sebastian on
    http://stackoverflow.com/questions/4563272/how-to-convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-stand/13287083#13287083

    Args:
        local_datetime (datetime): The local `datetime` instance.

    Returns:
        datetime: The UTC datetime instace.
    """
    # get the utc_datetime as if the local_datetime is utc and calculate the timezone
    # difference and add it to the local datetime object
    return local_datetime - (utc_to_local(local_datetime) - local_datetime)


