# -*- coding: utf-8 -*-
"""The venerable DBSession is situated here.

This is a runtime storage for the DB session. Greatly simplifying the usage of a
scoped session.
"""
from typing import Any, List, TYPE_CHECKING, Union

from sqlalchemy.orm import scoped_session, sessionmaker

if TYPE_CHECKING:  # pragma: no cover
    from stalker.models.entity import SimpleEntity


class ExtendedScopedSession(scoped_session):
    """A customized scoped_session which adds new functionality."""

    def save(self, data: Union[None, List[Any], "SimpleEntity"] = None) -> None:
        """Add and commits data at once.

        Args:
            data (Union[list, stalker.models.entity.SimpleEntity]): Either a single or
                a list of :class:`stalker.models.entity.SimpleEntity` or derivatives.
        """
        if data is not None:
            if isinstance(data, list):
                self.add_all(data)
            else:
                self.add(data)
        self.commit()


DBSession = ExtendedScopedSession(sessionmaker(future=True))
