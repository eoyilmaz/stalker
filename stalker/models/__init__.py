# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
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


def check_circular_dependency(entity, other_entity, attr_name):
    """Checks the circular dependency in entity if it has other_entity in its
    dependency attr which is specified with attr_name
    """
    # check itself
    if entity is other_entity:
        raise CircularDependencyError(
            '%s %s and %s creates a circular dependency' %
            (entity.__class__.__name__, entity, other_entity)
        )

    for dependent_entity in getattr(entity, attr_name):
        if dependent_entity is other_entity:
            raise CircularDependencyError(
                '%s %s and %s creates a circular dependency' %
                (entity.__class__.__name__, entity, other_entity)
            )
        else:
            check_circular_dependency(
                dependent_entity, other_entity, attr_name
            )


