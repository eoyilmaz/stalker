# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
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

import unittest

from stalker import Studio, SchedulerBase


class SchedulerBaseTester(unittest.TestCase):
    """tests the stalker.models.scheduler.SchedulerBase
    """

    def setUp(self):
        """set up the test
        """
        self.test_studio = Studio(name='Test Studio')
        self.kwargs = {
            'studio': self.test_studio
        }
        self.test_scheduler_base = SchedulerBase(**self.kwargs)

    def test_studio_argument_is_skipped(self):
        """testing if the studio attribute will be None if the studio argument
        is skipped
        """
        self.kwargs.pop('studio')
        new_scheduler_base = SchedulerBase(**self.kwargs)
        self.assertTrue(new_scheduler_base.studio is None)

    def test_studio_argument_is_None(self):
        """testing if the studio attribute will be None if the studio argument
        is None
        """
        self.kwargs['studio'] = None
        new_scheduler_base = SchedulerBase(**self.kwargs)
        self.assertTrue(new_scheduler_base.studio is None)

    def test_studio_attribute_is_None(self):
        """testing if the studio argument can be set to None
        """
        self.test_scheduler_base.studio = None
        self.assertTrue(self.test_scheduler_base.studio is None)

    def test_studio_argument_is_not_a_Studio_instance(self):
        """testing if a TypeError will be raised when the studio argument is
        not stalker.models.studio.Studio instance
        """
        self.kwargs['studio'] = 'not a studio instance'
        self.assertRaises(TypeError, SchedulerBase, **self.kwargs)

    def test_studio_attribute_is_not_a_Studio_instance(self):
        """testing if a TypeError will be raised when the studio attribute is
        set to a value which is not a stalker.models.studio.Studio instance
        """
        self.assertRaises(TypeError, setattr, self.test_scheduler_base,
                          'studio', 'not a studio instance')

    def test_studio_argument_is_working_properly(self):
        """testing if the studio argument value is correctly passed to the
        studio attribute
        """
        self.assertEqual(self.test_scheduler_base.studio,
                         self.kwargs['studio'])

    def test_studio_attribute_is_working_properly(self):
        """testing if the studio attribute is working properly
        """
        new_studio = Studio(name='Test Studio 2')
        self.test_scheduler_base.studio = new_studio
        self.assertEqual(self.test_scheduler_base.studio, new_studio)
