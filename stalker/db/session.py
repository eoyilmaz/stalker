# -*- coding: utf-8 -*-

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


# try:
#     DBSession = ExtendedScopedSession(sessionmaker(extension=None))
# except TypeError:
DBSession = ExtendedScopedSession(sessionmaker())
