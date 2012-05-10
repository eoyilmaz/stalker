# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, validates
from stalker.models.entity import Entity

class Review(Entity):
    """User reviews and comments about other entities.
    
    :param body: the body of the review, it is a string or unicode variable,
      it can be empty but it is then meaningless to have an empty review.
      Anything other than a string or unicode will raise a TypeError.
    
    :param to: The relation variable, that holds the connection that this
      review is related to. Any object which has a list-like attribute called
      "reviews" is accepted. Anything other will raise AttributeError.
    """

    __tablename__ = "Reviews"
    __mapper_args__ = {"polymorphic_identity": "Review"}
    review_id = Column("id", Integer, ForeignKey("SimpleEntities.id"),
                       primary_key=True)
    body = Column(
        String,
        doc="""The body (content) of this Review.
        """
    )

    to_id = Column(ForeignKey("Entities.id"))
    to = relationship(
        "Entity",
        primaryjoin="Reviews.c.to_id==Entities.c.id",
        back_populates="reviews",
        uselist=False,
        doc="""The owner object of this Review.
        """
    )

    def __init__(self, body="", to=None, **kwargs):
        super(Review, self).__init__(**kwargs)

        self.body = body
        self.to = to

    @validates("body")
    def _validate_body(self, key, body):
        """validates the given body variable
        """

        # the body could be empty
        # but it should be an instance of string or unicode

        if not isinstance(body, (str, unicode)):
            raise TypeError("%s.body should be an instance of string or "
                            "unicode not %s" %
                            (self.__class__.__name__,
                             body.__class__.__name__))

        return body

    @validates("to")
    def _validate_to(self, key, to):
        """validates the given to variable
        """

        if to is None:
            if self.to is not None:
                # TODO: think about adding an OrphanError
                raise RuntimeError(
                    "this Review instance can not be removed from the "
                    "%s.reviews attribute. If you want to remove it, either "
                    "delete it or assign it to a new Review accepting "
                    "object" % self.to.__class__.__name__
                )
        
        if not isinstance(to, Entity):
            raise TypeError(
                "%s.to should be inherited from stalker.models.entity.Entity "
                "class not %s" % (self.__class__.__name__,
                                  to.__class__.__name__)
            )

        return to
