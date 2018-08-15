# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2018 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# Stalker is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# Stalker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with Stalker.  If not, see <http://www.gnu.org/licenses/>

from sqlalchemy.orm import scoped_session, sessionmaker


class ExtendedScopedSession(scoped_session):
    """An customized scoped_session which adds new functionality
    """

    def save(self, data=None):
        """adds and commits data at once
        """
        if data:
            if hasattr(data, '__getitem__'):
                self.add_all(data)
            else:
                self.add(data)
        self.commit()


DBSession = ExtendedScopedSession(
    sessionmaker(extension=None)
)
