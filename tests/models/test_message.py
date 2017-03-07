# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2016 Erkan Ozgur Yilmaz
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


from stalker.testing import UnitTestBase
from stalker import Message


class MessageTestCase(UnitTestBase):
    """tests for Message class
    """

    def test_message_instance_creation(self):
        """testing message instance creation
        """
        from stalker import Status, StatusList
        status_unread = Status(name='Unread', code='UR')
        status_read = Status(name='Read', code='READ')
        status_replied = Status(name='Replied', code='REP')

        message_status_list = StatusList(
            name='Message Statuses',
            statuses=[status_unread, status_read, status_replied],
            target_entity_type='Message'
        )

        new_message = Message(
            description='This is a test message',
            status_list=message_status_list
        )
        self.assertEqual(new_message.description, 'This is a test message')
