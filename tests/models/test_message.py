# -*- coding: utf-8 -*-
"""Tests related to the Message class."""

from stalker import Message, Status, StatusList


def test_message_instance_creation():
    """message instance creation."""
    status_unread = Status(name="Unread", code="UR")
    status_read = Status(name="Read", code="READ")
    status_replied = Status(name="Replied", code="REP")

    message_status_list = StatusList(
        name="Message Statuses",
        statuses=[status_unread, status_read, status_replied],
        target_entity_type="Message",
    )

    new_message = Message(
        description="This is a test message", status_list=message_status_list
    )
    assert new_message.description == "This is a test message"
