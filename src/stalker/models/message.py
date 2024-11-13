# -*- coding: utf-8 -*-
"""The Message related classes and functions are situated here."""
from typing import Any, Dict

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from stalker.log import get_logger
from stalker.models.entity import Entity
from stalker.models.mixins import StatusMixin

logger = get_logger(__name__)


class Message(Entity, StatusMixin):
    """The base of the messaging system in Stalker.

    Messages are one of the ways to collaborate in Stalker. The model of the
    messages is taken from the e-mail system. So it is pretty similar to an
    e-mail message.

    Args:
        from (User): The :class:`.User` object sending the message.
        to (User): The list of :class:`.User` s to receive this message.
        subject (str): The subject of the message.
        body (str): tThe body of the message.
        in_reply_to (Message): The :class:`.Message` object which this message is a
            reply to.
        replies (Message): The list of :class:`.Message` objects which are the direct
            replies of this message.
        attachments (SimpleEntity): A list of :class:`.SimpleEntity` objects attached to
            this message (so anything can be attached to a message).
    """

    __auto_name__ = True
    __tablename__ = "Messages"
    __mapper_args__ = {"polymorphic_identity": "Message"}
    message_id: Mapped[int] = mapped_column(
        "id", ForeignKey("Entities.id"), primary_key=True
    )

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        super(Message, self).__init__(**kwargs)
        StatusMixin.__init__(self, **kwargs)
