# -*- coding: utf-8 -*-
"""The venerable DBSession is situated here.

This is a runtime storage for the DB session. Greatly simplifying the usage of a
scoped session.
"""
from sqlalchemy.orm import scoped_session, sessionmaker


class ExtendedScopedSession(scoped_session):
    """A customized scoped_session which adds new functionality."""

    def save(self, data=None):
        """Add and commits data at once.

        Args:
            data (Union[list, stalker.models.entity.SimpleEntity]): Either a single or
                a list of :class:`stalker.models.entity.SimpleEntity` or derivatives.
        """
        if data:
            if hasattr(data, "__getitem__"):
                self.add_all(data)
            else:
                self.add(data)
        self.commit()


# try:
#     DBSession = ExtendedScopedSession(sessionmaker(extension=None))
# except TypeError:
DBSession = ExtendedScopedSession(sessionmaker())
