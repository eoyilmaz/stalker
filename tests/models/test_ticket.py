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

from stalker.db.session import DBSession
from stalker import (db, TicketLog, Asset, User, Note, Project, Repository,
                     Status, StatusList, Task, Ticket, Type, Version, defaults)

from stalker import log
import logging

logger = logging.getLogger("stalker.models.ticket")
logger.setLevel(log.logging_level)


class TicketTester(unittest.TestCase):
    """Tests the :class:`~stalker.models.ticket.Ticket` class
    """

    def setUp(self):
        """set up the test
        """
        # create the db
        DBSession.remove()
        db.setup()
        # db.init()
        # we just need statuses so create them instead of initializing the db
        db.create_ticket_statuses()
        db.create_entity_statuses(entity_type='Task',
                                  status_names=defaults.task_status_names,
                                  status_codes=defaults.task_status_codes)
        db.create_entity_statuses(entity_type='Asset',
                                  status_names=defaults.task_status_names,
                                  status_codes=defaults.task_status_codes)
        db.create_entity_statuses(entity_type='Shot',
                                  status_names=defaults.task_status_names,
                                  status_codes=defaults.task_status_codes)
        db.create_entity_statuses(entity_type='Sequence',
                                  status_names=defaults.task_status_names,
                                  status_codes=defaults.task_status_codes)
        db.create_entity_statuses(entity_type='Review',
                                  status_names=defaults.review_status_names,
                                  status_codes=defaults.review_status_codes)


        # create statuses
        self.test_status1 = Status(name='N', code='N')
        self.test_status2 = Status(name='R', code='R')

        # get the ticket types
        ticket_types = Type.query \
            .filter(Type.target_entity_type == 'Ticket').all()
        self.ticket_type_1 = ticket_types[0]
        self.ticket_type_2 = ticket_types[1]

        # create a User
        self.test_user = User(
            name='Test User',
            login='testuser1',
            email='test1@user.com',
            password='secret'
        )

        # create a Repository
        self.test_repo = Repository(name="Test Repo")

        # create a Project Type
        self.test_project_type = Type(
            name='Commercial Project',
            code='comm',
            target_entity_type=Project,
        )

        # create a Project StatusList
        self.test_project_status1 = Status(name='PrjStat1', code='PrjStat1')
        self.test_project_status2 = Status(name='PrjStat2', code='PrjStat2')

        self.test_project_status_list = StatusList(
            name="Project Status List",
            target_entity_type=Project,
            statuses=[
                self.test_project_status1,
                self.test_project_status2,
            ]
        )

        self.test_task_status_list = StatusList.query\
            .filter_by(target_entity_type='Task').first()

        # create a Project
        self.test_project = Project(
            name="Test Project 1",
            code="TEST_PROJECT_1",
            type=self.test_project_type,
            repository=self.test_repo,
            status_list=self.test_project_status_list
        )

        # create an Asset
        self.test_asset_status_list = StatusList.query\
            .filter_by(target_entity_type='Asset').first()

        self.test_asset_type = Type(
            name='Character Asset',
            code='char',
            target_entity_type=Asset
        )

        self.test_asset = Asset(
            name="Test Asset",
            code='ta',
            project=self.test_project,
            status_list=self.test_asset_status_list,
            type=self.test_asset_type
        )

        # create a Task
        self.test_task = Task(
            name="Modeling of Asset 1",
            resources=[self.test_user],
            status_list=self.test_task_status_list,
            parent=self.test_asset
        )

        # create a Version
        self.test_version_status_list = StatusList(
            name='Version Statuses',
            target_entity_type=Version,
            statuses=[self.test_status1, self.test_status2]
        )

        self.test_version = Version(
            name='Test Version',
            task=self.test_task,
            status_list=self.test_version_status_list,
            version=1,
            full_path='some/path'
        )

        # create the Ticket
        self.kwargs = {
            'project': self.test_project,
            'links': [self.test_version],
            'summary': 'This is a test ticket',
            'description': 'This is the long description',
            'priority': 'TRIVIAL',
            'reported_by': self.test_user,
        }

        self.test_ticket = Ticket(**self.kwargs)
        DBSession.add(self.test_ticket)
        DBSession.commit()

        # get the Ticket Statuses
        self.status_new = Status.query.filter_by(name='New').first()
        self.status_accepted = Status.query.filter_by(name='Accepted').first()
        self.status_assigned = Status.query.filter_by(name='Assigned').first()
        self.status_reopened = Status.query.filter_by(name='Reopened').first()
        self.status_closed = Status.query.filter_by(name='Closed').first()

    def tearDown(self):
        """clean up the test
        """
        DBSession.remove()

    @classmethod
    def tearDownClass(cls):
        """clean up the test
        """
        DBSession.remove()

    def test___auto_name__class_attribute_is_set_to_True(self):
        """testing if the __auto_name__ class attribute is set to True for
        Ticket class
        """
        self.assertTrue(Ticket.__auto_name__)

    def test_name_argument_is_not_used(self):
        """testing if the given name argument is not used
        """
        test_value = 'Test Name'
        self.kwargs['name'] = test_value
        new_ticket = Ticket(**self.kwargs)
        self.assertNotEqual(new_ticket.name, test_value)

    def test_name_argument_is_skipped_will_not_raise_error(self):
        """testing if skipping the name argument is not important and an
        automatically generated name will be used in that case
        """
        if 'name' in self.kwargs:
            self.kwargs.pop('name')
            # expect no errors
        Ticket(**self.kwargs)

    def test_number_attribute_is_not_created_per_project(self):
        """testing if the number attribute is not created per project and
        continues to increase for every created ticket
        """
        proj1 = Project(
            name='Test Project 1',
            code='TP1',
            repository=self.test_repo,
            status_list=self.test_project_status_list
        )

        proj2 = Project(
            name='Test Project 2',
            code='TP2',
            repository=self.test_repo,
            status_list=self.test_project_status_list
        )

        proj3 = Project(
            name='Test Project 3',
            code='TP3',
            repository=self.test_repo,
            status_list=self.test_project_status_list
        )

        p1_t1 = Ticket(project=proj1)
        DBSession.add(p1_t1)
        DBSession.commit()
        self.assertEqual(p1_t1.number, 2)

        p1_t2 = Ticket(project=proj1)
        DBSession.add(p1_t2)
        DBSession.commit()
        self.assertEqual(p1_t2.number, 3)

        p2_t1 = Ticket(project=proj2)
        DBSession.add(p2_t1)
        DBSession.commit()
        self.assertEqual(p2_t1.number, 4)

        p1_t3 = Ticket(project=proj1)
        DBSession.add(p1_t3)
        DBSession.commit()
        self.assertEqual(p1_t3.number, 5)

        p3_t1 = Ticket(project=proj3)
        DBSession.add(p3_t1)
        DBSession.commit()
        self.assertEqual(p3_t1.number, 6)

        p2_t2 = Ticket(project=proj2)
        DBSession.add(p2_t2)
        DBSession.commit()
        self.assertEqual(p2_t2.number, 7)

        p3_t2 = Ticket(project=proj3)
        DBSession.add(p3_t2)
        DBSession.commit()
        self.assertEqual(p3_t2.number, 8)

        p2_t3 = Ticket(project=proj2)
        DBSession.add(p2_t3)
        DBSession.commit()
        self.assertEqual(p2_t3.number, 9)

    def test_number_attribute_is_read_only(self):
        """testing if the number attribute is read-only
        """
        self.assertRaises(AttributeError, setattr, self.test_ticket, 'number',
                          234)

    def test_number_attribute_is_automatically_increased(self):
        """testing if the number attribute is automatically increased
        """
        # create two new tickets
        ticket1 = Ticket(**self.kwargs)
        DBSession.add(ticket1)
        DBSession.commit()

        ticket2 = Ticket(**self.kwargs)
        DBSession.add(ticket2)
        DBSession.commit()

        self.assertEqual(ticket1.number + 1, ticket2.number)
        self.assertEqual(ticket1.number, 2)
        self.assertEqual(ticket2.number, 3)

    def test_links_argument_accepts_anything_derived_from_SimpleEntity(self):
        """testing if links accepting anything derived from SimpleEntity
        """
        self.kwargs['links'] = [
            self.test_project,
            self.test_project_status1,
            self.test_project_status2,
            self.test_repo,
            self.test_version
        ]

        new_ticket = Ticket(**self.kwargs)
        self.assertEqual(
            sorted(self.kwargs['links'], key=lambda x: x.name),
            sorted(new_ticket.links, key=lambda x: x.name)
        )

    def test_links_attribute_accepts_anything_derived_from_SimpleEntity(self):
        """testing if links attribute is accepting anything derived from
        SimpleEntity
        """
        links = [
            self.test_project,
            self.test_project_status1,
            self.test_project_status2,
            self.test_repo,
            self.test_version
        ]
        self.test_ticket.links = links
        self.assertEqual(
            sorted(links, key=lambda x: x.name),
            sorted(self.test_ticket.links, key=lambda x: x.name)
        )

    def test_related_tickets_attribute_is_an_empty_list_on_init(self):
        """testing if the related_tickets attribute is an empty list on init
        """
        self.assertEqual(self.test_ticket.related_tickets, [])

    def test_related_tickets_attribute_is_set_to_something_other_then_a_list_of_Tickets(self):
        """testing if a TypeError will be raised when the related_tickets
        attribute is set to something other than a list of Tickets
        """
        self.assertRaises(TypeError, setattr, self.test_ticket,
                          'related_tickets', ['a ticket'])

    def test_related_tickets_attribute_accepts_list_of_Ticket_instances(self):
        """testing if the related tickets attribute accepts only list of
        stalker.models.ticket.Ticket instances
        """
        new_ticket1 = Ticket(**self.kwargs)
        new_ticket2 = Ticket(**self.kwargs)

        self.test_ticket.related_tickets = [new_ticket1, new_ticket2]

    def test_related_ticket_attribute_will_not_accept_self(self):
        """testing if the related_tickets attribute will not accept the Ticket
        itself and will raise ValueError
        """
        self.assertRaises(ValueError, setattr, self.test_ticket,
                          'related_tickets', [self.test_ticket])

    def test_priority_argument_is_skipped_will_set_it_to_zero(self):
        """testing if the priority argument is skipped will set the priority
        of the Ticket to 0 or TRIVIAL
        """
        self.kwargs.pop('priority')
        new_ticket = Ticket(**self.kwargs)
        self.assertEqual(new_ticket.priority, 'TRIVIAL')

    def test_comments_attribute_is_synonym_for_notes_attribute(self):
        """testing if the comments attribute is the synonym for the notes
        attribute, so setting one will also set the other
        """
        note1 = Note(name='Test Note 1', content='Test note 1')
        note2 = Note(name='Test Note 2', content='Test note 2')

        self.test_ticket.comments.append(note1)
        self.test_ticket.comments.append(note2)

        self.assertTrue(note1 in self.test_ticket.notes)
        self.assertTrue(note2 in self.test_ticket.notes)

        self.test_ticket.notes.remove(note1)
        self.assertFalse(note1 in self.test_ticket.comments)

        self.test_ticket.notes.remove(note2)
        self.assertFalse(note2 in self.test_ticket.comments)

    def test_reported_by_attribute_is_synonym_of_created_by(self):
        """testing if the reported_by attribute is a synonym for the created_by
        attribute
        """
        user1 = User(
            name='user1',
            login='user1',
            password='secret',
            email='user1@test.com'
        )

        self.test_ticket.reported_by = user1
        self.assertEqual(user1, self.test_ticket.created_by)

    def test_status_for_newly_created_tickets_will_be_NEW_when_skipped(self):
        """testing if the status of newly created tickets will be New
        """
        # get the status NEW from the session
        new_ticket = Ticket(**self.kwargs)
        self.assertEqual(new_ticket.status, self.status_new)

    def test_project_argument_is_skipped(self):
        """testing if a TypeError will be raised when the project argument is
        skipped
        """
        self.kwargs.pop('project')
        self.assertRaises(TypeError, Ticket, **self.kwargs)

    def test_project_argument_is_None(self):
        """testing if a TypeError will be raised when the project argument is
        None
        """
        self.kwargs['project'] = None
        self.assertRaises(TypeError, Ticket, **self.kwargs)

    def test_project_argument_accepts_Project_instances_only(self):
        """testing if the project argument accepts Project instances only
        """
        self.kwargs['project'] = 'Not a Project instance'
        self.assertRaises(TypeError, Ticket, **self.kwargs)

    def test_project_argument_is_working_properly(self):
        """testing if the project argument is working properly
        """
        self.kwargs['project'] = self.test_project
        new_ticket = Ticket(**self.kwargs)
        self.assertEqual(new_ticket.project, self.test_project)

    def test_project_attribute_is_read_only(self):
        """testing if the project attribute is read only
        """
        self.assertRaises(AttributeError, setattr, self.test_ticket, 'project',
                          self.test_project)

    ## STATUSES ##

    ## resolve ##
    def test_resolve_method_will_change_the_status_from_New_to_Closed_and_creates_a_log(self):
        """testing if invoking the resolve method will change the status of the
        Ticket from New to Closed
        """
        self.assertEqual(self.test_ticket.status, self.status_new)
        ticket_log = self.test_ticket.resolve()
        self.assertEqual(self.test_ticket.status, self.status_closed)
        self.assertEqual(ticket_log.from_status, self.status_new)
        self.assertEqual(ticket_log.to_status, self.status_closed)
        self.assertEqual(ticket_log.action, 'resolve')

    def test_resolve_method_will_change_the_status_from_Accepted_to_Closed(self):
        """testing if invoking the resolve method will change the status of the
        Ticket from Accepted to Closed
        """
        self.test_ticket.status = self.status_accepted
        self.assertEqual(self.test_ticket.status, self.status_accepted)
        ticket_log = self.test_ticket.resolve()
        self.assertEqual(self.test_ticket.status, self.status_closed)
        self.assertEqual(ticket_log.from_status, self.status_accepted)
        self.assertEqual(ticket_log.to_status, self.status_closed)
        self.assertEqual(ticket_log.action, 'resolve')

    def test_resolve_method_will_change_the_status_from_Assigned_to_Closed(self):
        """testing if invoking the resolve method will change the status of the
        Ticket from Assigned to Closed
        """
        self.test_ticket.status = self.status_assigned
        self.assertEqual(self.test_ticket.status, self.status_assigned)
        ticket_log = self.test_ticket.resolve()
        self.assertEqual(self.test_ticket.status, self.status_closed)
        self.assertEqual(ticket_log.from_status, self.status_assigned)
        self.assertEqual(ticket_log.to_status, self.status_closed)
        self.assertEqual(ticket_log.action, 'resolve')

    def test_resolve_method_will_change_the_status_from_Reopened_to_Closed(self):
        """testing if invoking the accept method will change the status of the
        Ticket from Reopened to closed
        """
        self.test_ticket.status = self.status_reopened
        self.assertEqual(self.test_ticket.status, self.status_reopened)
        ticket_log = self.test_ticket.resolve()
        self.assertEqual(self.test_ticket.status, self.status_closed)
        self.assertEqual(ticket_log.from_status, self.status_reopened)
        self.assertEqual(ticket_log.to_status, self.status_closed)
        self.assertEqual(ticket_log.action, 'resolve')

    def test_resolve_method_will_not_change_the_status_from_Closed_to_anything(self):
        """testing if invoking the resolve method will not change the status of
        the Ticket from Closed to anything
        """
        self.test_ticket.status = self.status_closed
        self.assertEqual(self.test_ticket.status, self.status_closed)
        ticket_log = self.test_ticket.resolve()
        self.assertTrue(ticket_log is None)
        self.assertEqual(self.test_ticket.status, self.status_closed)

    ## reopen ##
    def test_reopen_method_will_not_change_the_status_from_New_to_anything(self):
        """testing if invoking the reopen method will not change the status of
        the Ticket from New to anything
        """
        self.test_ticket.status = self.status_new
        self.assertEqual(self.test_ticket.status, self.status_new)
        ticket_log = self.test_ticket.reopen()
        self.assertTrue(ticket_log is None)
        self.assertEqual(self.test_ticket.status, self.status_new)

    def test_reopen_method_will_not_change_the_status_from_Accepted_to_anything(self):
        """testing if invoking the reopen method will not change the status of
        the Ticket from Accepted to anything
        """
        self.test_ticket.status = self.status_accepted
        self.assertEqual(self.test_ticket.status, self.status_accepted)
        ticket_log = self.test_ticket.reopen()
        self.assertTrue(ticket_log is None)
        self.assertEqual(self.test_ticket.status, self.status_accepted)

    def test_reopen_method_will_not_change_the_status_from_Assigned_to_anything(self):
        """testing if invoking the reopen method will not change the status of
        the Ticket from Assigned to anything
        """
        self.test_ticket.status = self.status_assigned
        self.assertEqual(self.test_ticket.status, self.status_assigned)
        ticket_log = self.test_ticket.reopen()
        self.assertTrue(ticket_log is None)
        self.assertEqual(self.test_ticket.status, self.status_assigned)

    def test_reopen_method_will_not_change_the_status_from_Reopened_to_anything(self):
        """testing if invoking the reopen method will not change the status of
        the Ticket from Reopened to anything
        """
        self.test_ticket.status = self.status_reopened
        self.assertEqual(self.test_ticket.status, self.status_reopened)
        ticket_log = self.test_ticket.reopen()
        self.assertTrue(ticket_log is None)
        self.assertEqual(self.test_ticket.status, self.status_reopened)

    def test_reopen_method_will_change_the_status_from_Closed_to_Reopened(self):
        """testing if invoking the reopen method will change the status of the
        Ticket from Closed to Reopened
        """
        self.test_ticket.status = self.status_closed
        self.assertEqual(self.test_ticket.status, self.status_closed)
        ticket_log = self.test_ticket.reopen()
        self.assertEqual(self.test_ticket.status, self.status_reopened)
        self.assertEqual(ticket_log.from_status, self.status_closed)
        self.assertEqual(ticket_log.to_status, self.status_reopened)
        self.assertEqual(ticket_log.action, 'reopen')

    ## accept ##

    def test_accept_method_will_change_the_status_from_New_to_Accepted(self):
        """testing if invoking the accept method will change the status of the
        Ticket from New to Accepted
        """
        self.test_ticket.status = self.status_new
        self.assertEqual(self.test_ticket.status, self.status_new)
        ticket_log = self.test_ticket.accept()
        self.assertEqual(self.test_ticket.status, self.status_accepted)
        self.assertEqual(ticket_log.from_status, self.status_new)
        self.assertEqual(ticket_log.to_status, self.status_accepted)
        self.assertEqual(ticket_log.action, 'accept')

    def test_accept_method_will_change_the_status_from_Accepted_to_Accepted(self):
        """testing if invoking the accept method will change the status of the
        Ticket from Accepted to Accepted
        """
        self.test_ticket.status = self.status_accepted
        self.assertEqual(self.test_ticket.status, self.status_accepted)
        ticket_log = self.test_ticket.accept()
        self.assertEqual(self.test_ticket.status, self.status_accepted)
        self.assertEqual(ticket_log.from_status, self.status_accepted)
        self.assertEqual(ticket_log.to_status, self.status_accepted)
        self.assertEqual(ticket_log.action, 'accept')

    def test_accept_method_will_change_the_status_from_Assigned_to_Accepted(self):
        """testing if invoking the accept method will change the status of the
        Ticket from Assigned to Accepted
        """
        self.test_ticket.status = self.status_assigned
        self.assertEqual(self.test_ticket.status, self.status_assigned)
        ticket_log = self.test_ticket.accept()
        self.assertEqual(self.test_ticket.status, self.status_accepted)
        self.assertEqual(ticket_log.from_status, self.status_assigned)
        self.assertEqual(ticket_log.to_status, self.status_accepted)
        self.assertEqual(ticket_log.action, 'accept')

    def test_accept_method_will_change_the_status_from_Reopened_to_Accepted(self):
        """testing if invoking the accept method will change the status of the
        Ticket from Reopened to Accepted
        """
        self.test_ticket.status = self.status_reopened
        self.assertEqual(self.test_ticket.status, self.status_reopened)
        ticket_log = self.test_ticket.accept()
        self.assertEqual(self.test_ticket.status, self.status_accepted)
        self.assertEqual(ticket_log.from_status, self.status_reopened)
        self.assertEqual(ticket_log.to_status, self.status_accepted)
        self.assertEqual(ticket_log.action, 'accept')

    def test_accept_method_will_not_change_the_status_of_Closed_to_Anything(self):
        """testing if invoking the accept method will not change the status of
        the Ticket from Closed to Anything
        """
        self.test_ticket.status = self.status_closed
        self.assertEqual(self.test_ticket.status, self.status_closed)
        ticket_log = self.test_ticket.accept()
        self.assertTrue(ticket_log is None)
        self.assertEqual(self.test_ticket.status, self.status_closed)

    ## reassign ##

    def test_reassign_method_will_change_the_status_from_New_to_Assigned(self):
        """testing if invoking the reassign method will change the status of
        the Ticket from New to Assigned
        """
        self.test_ticket.status = self.status_new
        self.assertEqual(self.test_ticket.status, self.status_new)
        ticket_log = self.test_ticket.reassign()
        self.assertEqual(self.test_ticket.status, self.status_assigned)
        self.assertEqual(ticket_log.from_status, self.status_new)
        self.assertEqual(ticket_log.to_status, self.status_assigned)
        self.assertEqual(ticket_log.action, 'reassign')

    def test_reassign_method_will_change_the_status_from_Accepted_to_Assigned(self):
        """testing if invoking the reassign method will change the status of
        the Ticket from Accepted to Accepted
        """
        self.test_ticket.status = self.status_accepted
        self.assertEqual(self.test_ticket.status, self.status_accepted)
        ticket_log = self.test_ticket.reassign()
        self.assertEqual(self.test_ticket.status, self.status_assigned)
        self.assertEqual(ticket_log.from_status, self.status_accepted)
        self.assertEqual(ticket_log.to_status, self.status_assigned)
        self.assertEqual(ticket_log.action, 'reassign')

    def test_reassign_method_will_change_the_status_from_Assigned_to_Assigned(self):
        """testing if invoking the reassign method will change the status of
        the Ticket from Assigned to Accepted
        """
        self.test_ticket.status = self.status_assigned
        self.assertEqual(self.test_ticket.status, self.status_assigned)
        ticket_log = self.test_ticket.reassign()
        self.assertEqual(self.test_ticket.status, self.status_assigned)
        self.assertEqual(ticket_log.from_status, self.status_assigned)
        self.assertEqual(ticket_log.to_status, self.status_assigned)
        self.assertEqual(ticket_log.action, 'reassign')

    def test_reassign_method_will_change_the_status_from_Reopened_to_Assigned(self):
        """testing if invoking the accept method will change the status of the
        Ticket from Reopened to Assigned
        """
        self.test_ticket.status = self.status_reopened
        self.assertEqual(self.test_ticket.status, self.status_reopened)
        ticket_log = self.test_ticket.reassign()
        self.assertEqual(self.test_ticket.status, self.status_assigned)
        self.assertEqual(ticket_log.from_status, self.status_reopened)
        self.assertEqual(ticket_log.to_status, self.status_assigned)
        self.assertEqual(ticket_log.action, 'reassign')

    def test_reassign_method_will_not_change_the_status_of_Closed_to_Anything(self):
        """testing if invoking the reassign method will not change the status
        of the Ticket from Closed to Anything
        """
        self.test_ticket.status = self.status_closed
        self.assertEqual(self.test_ticket.status, self.status_closed)
        ticket_log = self.test_ticket.reassign()
        self.assertTrue(ticket_log is None)
        self.assertEqual(self.test_ticket.status, self.status_closed)

    def test_resolve_method_will_set_the_resolution(self):
        """testing if invoking the resolve method will change the status of the
        Ticket from New to Closed
        """
        self.assertEqual(self.test_ticket.status, self.status_new)
        ticket_log = self.test_ticket.resolve(resolution='fixed')
        self.assertEqual(self.test_ticket.status, self.status_closed)
        self.assertEqual(ticket_log.from_status, self.status_new)
        self.assertEqual(ticket_log.to_status, self.status_closed)
        self.assertEqual(ticket_log.action, 'resolve')
        self.assertEqual(self.test_ticket.resolution, 'fixed')

    def test_reopen_will_clear_resolution(self):
        """testing if invoking the reopen method will clear the
        timing_resolution
        """
        self.assertEqual(self.test_ticket.status, self.status_new)
        self.test_ticket.resolve(resolution='fixed')
        self.assertEqual(self.test_ticket.resolution, 'fixed')
        ticket_log = self.test_ticket.reopen()
        self.assertTrue(isinstance(ticket_log, TicketLog))
        self.assertEqual(self.test_ticket.resolution, '')

    def test_reassign_will_set_the_owner(self):
        """testing if invoking the reassign method will set the owner
        """
        self.assertEqual(self.test_ticket.status, self.status_new)
        self.assertNotEqual(self.test_ticket.owner, self.test_user)
        ticket_log = self.test_ticket.reassign(assign_to=self.test_user)
        self.assertTrue(isinstance(ticket_log, TicketLog))
        self.assertEqual(self.test_ticket.owner, self.test_user)

    def test_accept_will_set_the_owner(self):
        """testing if invoking the accept method will set the owner
        """
        self.assertEqual(self.test_ticket.status, self.status_new)
        self.assertNotEqual(self.test_ticket.owner, self.test_user)
        ticket_log = self.test_ticket.accept(created_by=self.test_user)
        self.assertTrue(isinstance(ticket_log, TicketLog))
        self.assertEqual(self.test_ticket.owner, self.test_user)

    def test_summary_argument_skipped(self):
        """testing if the summary argument can be skipped
        """
        try:
            self.kwargs.pop('summary')
        except KeyError:
            pass
        new_ticket = Ticket(**self.kwargs)
        self.assertEqual(new_ticket.summary, '')

    def test_summary_argument_can_be_None(self):
        """testing if the summary argument can be None
        """
        self.kwargs['summary'] = None
        new_ticket = Ticket(**self.kwargs)
        self.assertEqual(new_ticket.summary, '')

    def test_summary_attribute_can_be_set_to_None(self):
        """testing if the summary attribute can be set to None
        """
        self.test_ticket.summary = None
        self.assertEqual(self.test_ticket.summary, '')

    def test_summary_argument_is_not_a_string(self):
        """testing if a TypeError will be raised when the summary argument
        value is not a string
        """
        self.kwargs['summary'] = ['not a string instance']
        self.assertRaises(TypeError, Ticket, self.kwargs)

    def test_summary_attribute_is_set_to_a_value_other_than_a_string(self):
        """testing if the summary attribute is set to a value other than a
        string
        """
        self.assertRaises(TypeError, setattr, self.test_ticket, 'summary',
                          ['not a string'])

    def test_summary_argument_is_working_properly(self):
        """testing if the summary argument value is passed to summary attribute
        correctly
        """
        test_value = 'test summary'
        self.kwargs['summary'] = test_value
        new_ticket = Ticket(**self.kwargs)
        self.assertEqual(new_ticket.summary, test_value)

    def test_summary_attribute_is_working_properly(self):
        """testing if the summary attribute is working properly
        """
        test_value = 'test_summary'
        self.assertNotEqual(self.test_ticket.summary, test_value)
        self.test_ticket.summary = test_value
        self.assertEqual(self.test_ticket.summary, test_value)
