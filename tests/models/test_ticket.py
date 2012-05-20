# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause
import tempfile

import unittest
from stalker import db
#import os
from stalker.db.session import DBSession
from zope.sqlalchemy import ZopeTransactionExtension
from stalker.models.asset import Asset
from stalker.models.auth import User
from stalker.models.note import Note
from stalker.models.project import Project
from stalker.models.repository import Repository
from stalker.models.status import Status, StatusList
from stalker.models.task import Task
from stalker.models.ticket import Ticket
from stalker.models.type import Type
from stalker.models.version import Version

import logging
logger = logging.getLogger("stalker.models.ticket")
logger.setLevel(logging.DEBUG)

class TicketTester(unittest.TestCase):
    """Tests the :class:`~stalker.models.ticket.Ticket` class
    """
    
    def setUp(self):
        """set up the test
        """
        # create the db
        DBSession.remove()
        DBSession.configure(extension=None)
        db.setup()
        
        # create statuses
        self.test_status1 = Status(name='N', code='N')
        self.test_status2 = Status(name='R', code='R')
       
        # get the ticket types
        ticket_types = Type.query()\
            .filter(Type.target_entity_type=='Ticket').all()
        self.ticket_type_1 = ticket_types[0]
        self.ticket_type_2 = ticket_types[1]
        
        # create a User
        self.test_user = User(
            email='test1@user.com',
            first_name='Test',
            last_name='User',
            password='secret',
            login_name='testuser1'
        )
        
        # create a Repository
        self.test_repo = Repository(name="Test Repo")
        
        # create a Project Type
        self.test_project_type = Type(
            name='Commercial Project',
            target_entity_type=Project,
        )
        
        # create a Project StatusList
        self.test_project_status1 = Status(name='PrjStat1', code='PrjStat1')
        self.test_project_status2 = Status(name='PrjStat2', code='PrjStat2')
        
        self.test_project_statusList = StatusList(
            name="Project Status List",
            target_entity_type=Project,
            statuses=[
                self.test_project_status1,
                self.test_project_status2,
            ]
        )
        
        self.test_task_status_list = StatusList(
            name="Task Status List",
            target_entity_type=Task,
            statuses=[
                self.test_project_status1,
                self.test_project_status2
            ]
        )
        
        # create a Project
        self.test_project = Project(
            name="Test Project 1",
            code="TEST_PROJECT_1",
            type=self.test_project_type,
            repository=self.test_repo,
            status_list=self.test_project_statusList
        )
        
        # create an Asset
        self.test_asset_status_list = StatusList(
            name="Asset Status List",
            target_entity_type=Asset,
            statuses=[self.test_status1, self.test_status2]
        )
        
        self.test_asset_type = Type(
            name='Character Asset',
            target_entity_type=Asset
        )
        
        self.test_asset = Asset(
            name="Test Asset",
            project=self.test_project,
            status_list=self.test_asset_status_list,
            type=self.test_asset_type
        )
        
        # create a Task
        self.test_task = Task(
            name="Modeling of Asset 1",
            resources=[self.test_user],
            status_list=self.test_task_status_list,
            task_of=self.test_asset
        )
        
        # create a Version
        self.test_version_status_list = StatusList(
            name='Version Statuses',
            target_entity_type=Version,
            statuses=[self.test_status1, self.test_status2]
        )
        
        self.test_version = Version(
            name='Test Version',
            version_of=self.test_task,
            status_list=self.test_version_status_list,
            version=1
        )
        
        # create the Ticket
        self.kwargs = {
            'ticket_for': self.test_version,
            'summary': 'This is a test ticket',
            'description': 'This is the long description',
            'priority': 'TRIVIAL',
            'reported_by': self.test_user,
        }
        
        self.test_ticket = Ticket(**self.kwargs)
        DBSession.add(self.test_ticket)
        DBSession.commit()
        
        # get the Ticket Statuses
        self.status_NEW = DBSession.query(Status)\
            .filter(Status.name=='New').first()
        
        self.status_REOPENED = DBSession.query(Status)\
            .filter(Status.name=='Reopened').first()
        
        self.status_CLOSED = DBSession.query(Status)\
            .filter(Status.name=='Closed').first()
    
    def tearDown(self):
        """clean up the test
        """
        DBSession.remove()
    
    @classmethod
    def tearDownClass(cls):
        """clean up the test
        """
        # revert the session back to the normal state
        DBSession.remove()
        DBSession.configure(extension=ZopeTransactionExtension())
    
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
        if self.kwargs.has_key('name'):
            self.kwargs.pop('name')
        # expect no errors
        new_ticket = Ticket(**self.kwargs)
    
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
    
    def test_ticket_for_argument_is_skipped_will_raise_TypeError(self):
        """testing if a TypeError will be raised when the ticket_for argument
        is skipped
        """
        self.kwargs.pop('ticket_for')
        self.assertRaises(TypeError, Ticket, **self.kwargs)
    
    def test_ticket_for_argument_is_None_will_raise_a_TypeError(self):
        """testing if a TypeError will be raised when the ticket_for argument
        is None
        """
        self.kwargs['ticket_for'] = None
        self.assertRaises(TypeError, Ticket, **self.kwargs)
    
    def test_ticket_for_attribute_is_None_will_raise_a_TypeError(self):
        """testing if a TypeError will be raised when setting the ticket_for
        attribute to None
        """
        self.assertRaises(TypeError, setattr, self.test_ticket, 'ticket_for',
                          None)
    
    def test_ticket_for_argument_is_not_a_Version_instance(self):
        """testing if a TypeError will be raised when the object given by the
        ticket_for argument is not a stalker.models.version.Version instance
        """
        self.kwargs['ticket_for'] = 'a version'
        self.assertRaises(TypeError, Ticket, **self.kwargs)
    
    def test_ticket_for_attribute_is_not_a_Version_instance(self):
        """testing if a TypeError will be raised when the ticket_for attribute
        is set to something other then a stalker.models.version.Version
        instance
        """
        self.assertRaises(TypeError, setattr, self.test_ticket, 'ticket_for',
                          'a ticket')
    
    def test_ticket_for_argument_accepts_Version_instances(self):
        """testing if ticket_for argument accepts
        stalker.models.version.Version instances
        """
        self.kwargs['ticket_for'] = self.test_version
        new_ticket = Ticket(**self.kwargs)
        self.assertIsInstance(new_ticket.ticket_for, Version)
    
    def test_ticket_for_attribute_accepts_Version_instances(self):
        """testing if ticket_for attribute accepts
        stalker.models.version.Version instances
        """
        # there should be no problem assigning a new Version
        self.test_ticket.ticket_for = Version(
            name='Test Version 2',
            version_of=self.test_task,
            status_list=self.test_version_status_list,
            version=2
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
        
        self.assertIn(note1, self.test_ticket.notes)
        self.assertIn(note2, self.test_ticket.notes)
        
        self.test_ticket.notes.remove(note1)
        self.assertNotIn(note1, self.test_ticket.comments)
        
        self.test_ticket.notes.remove(note2)
        self.assertNotIn(note2, self.test_ticket.comments)
        
    
    def test_reported_by_attribute_is_synonym_of_created_by(self):
        """testing if the reported_by attribute is a synonym for the created_by
        attribute
        """
        user1 = User(
            login_name='user1',
            first_name='user1',
            password='secret',
            email='uesr1@test.com'
        )
        
        self.test_ticket.reported_by = user1
        self.assertEqual(user1, self.test_ticket.created_by)
    
    def test_status_for_newly_created_tickets_will_be_NEW_when_skipped(self):
        """testing if the status of newly created tickets will be New
        """
        # get the status NEW from the DBSession
        new_ticket = Ticket(**self.kwargs)
        self.assertEqual(new_ticket.status, self.status_NEW)
    
    def test_resolve_method_will_change_the_status_from_New_to_Closed(self):
        """testing if invoking the resolve method will change the status of the
        Ticket from New to Closed
        """
        self.assertEqual(self.test_ticket.status, self.status_NEW)
        self.test_ticket.resolve()
        self.assertEqual(self.test_ticket.status, self.status_CLOSED)
    
    def test_resolve_method_will_change_the_status_from_Reopened_to_Closed(self):
        """testing if invoking the accept method will change the status of the
        Ticket from Reopened to closed
        """
        self.test_ticket.status = self.status_REOPENED
        self.assertEqual(self.test_ticket.status, self.status_REOPENED)
        self.test_ticket.resolve()
        self.assertEqual(self.test_ticket.status, self.status_CLOSED)
    
    def test_resolve_method_will_not_change_the_status_from_Closed_to_anything(self):
        """testing if invoking the resolve method will not change the status of
        the Ticket from Closed to anything
        """
        self.test_ticket.status = self.status_CLOSED
        self.assertEqual(self.test_ticket.status, self.status_CLOSED)
        self.test_ticket.resolve()
        self.assertEqual(self.test_ticket.status, self.status_CLOSED)
    
    def test_reopen_method_will_not_change_the_status_from_New_to_anything(self):
        """testing if invoking the reopen method will not change the status of
        the Ticket from New to anything
        """
        self.test_ticket.status = self.status_NEW
        self.assertEqual(self.test_ticket.status, self.status_NEW)
        self.test_ticket.reopen()
        self.assertEqual(self.test_ticket.status, self.status_NEW)
    
    def test_reopen_method_will_not_change_the_status_from_Reopened_to_anything(self):
        """testing if invoking the reopen method will not change the status of
        the Ticket from Reopened to anything
        """
        self.test_ticket.status = self.status_REOPENED
        self.assertEqual(self.test_ticket.status, self.status_REOPENED)
        self.test_ticket.reopen()
        self.assertEqual(self.test_ticket.status, self.status_REOPENED)
 
    def test_reopen_method_will_change_the_status_from_Closed_to_Reopened(self):
        """testing if invoking the reopen method will change the status of the
        Ticket from Closed to Reopened
        """
        self.test_ticket.status = self.status_CLOSED
        self.assertEqual(self.test_ticket.status, self.status_CLOSED)
        self.test_ticket.reopen()
        self.assertEqual(self.test_ticket.status, self.status_REOPENED)
    
    
    
    def test_resolve_method_will_create_a_new_log_telling_status_is_changed_from_New_to_Closed(self):
        """testing if invoking the resolve method will create a new log entry
        telling the status changed from New to Closed
        """
        self.assertEqual(self.test_ticket.status, self.status_NEW)
        self.test_ticket.resolve()
        self.assertEqual(self.test_ticket.status, self.status_CLOSED)
        log = self.test_ticket.logs[-1]
        self.assertEqual(log.from_status, self.status_NEW)
        self.assertEqual(log.to_status, self.status_CLOSED)
        self.assertEqual(log.action, 'RESOLVE')
    
    def test_resolve_method_will_create_a_new_log_telling_status_is_changed_from_Reopened_to_Closed(self):
        """testing if invoking the accept method will create a new log entry
        telling the status is changed from Reopened to closed
        """
        self.test_ticket.status = self.status_REOPENED
        self.assertEqual(self.test_ticket.status, self.status_REOPENED)
        self.test_ticket.resolve()
        self.assertEqual(self.test_ticket.status, self.status_CLOSED)
        log = self.test_ticket.logs[-1]
        self.assertEqual(log.from_status, self.status_REOPENED)
        self.assertEqual(log.to_status, self.status_CLOSED)
        self.assertEqual(log.action, 'RESOLVE')
    
    def test_resolve_method_will_not_create_a_new_log_when_the_status_is_Closed(self):
        """testing if invoking the resolve method will not create a new log
        entry when the status is Closed
        """
        self.test_ticket.status = self.status_CLOSED
        logs_pre = self.test_ticket.logs
        self.assertEqual(self.test_ticket.status, self.status_CLOSED)
        self.test_ticket.resolve()
        self.assertEqual(self.test_ticket.status, self.status_CLOSED)
        logs_post = self.test_ticket.logs
        self.assertEqual(logs_pre, logs_post)
    
    def test_reopen_method_will_not_create_a_new_log_when_the_status_is_New(self):
        """testing if invoking the reopen method will not create a new log
        entry when the status is New
        """
        self.test_ticket.status = self.status_NEW
        logs_pre = self.test_ticket.logs
        self.assertEqual(self.test_ticket.status, self.status_NEW)
        self.test_ticket.reopen()
        self.assertEqual(self.test_ticket.status, self.status_NEW)
        logs_post = self.test_ticket.logs
        self.assertEqual(logs_pre, logs_post)
    
    def test_reopen_method_will_not_create_a_new_log_when_the_status_is_Reopened(self):
        """testing if invoking the reopen method will not create a new log
        entry when the status is Reopened
        """
        self.test_ticket.status = self.status_REOPENED
        logs_pre = self.test_ticket.logs
        self.assertEqual(self.test_ticket.status, self.status_REOPENED)
        self.test_ticket.reopen()
        self.assertEqual(self.test_ticket.status, self.status_REOPENED)
        logs_post = self.test_ticket.logs
        self.assertEqual(logs_pre, logs_post)
 
    def test_reopen_method_will_create_a_new_log_telling_the_status_is_changed_from_Closed_to_Reopened(self):
        """testing if invoking the reopen method will create a new log entry
        telling the status is changed from Closed to Reopened
        """
        self.test_ticket.status = self.status_CLOSED
        self.assertEqual(self.test_ticket.status, self.status_CLOSED)
        self.test_ticket.reopen()
        self.assertEqual(self.test_ticket.status, self.status_REOPENED)
        log = self.test_ticket.logs[-1]
        self.assertEqual(log.from_status, self.status_CLOSED)
        self.assertEqual(log.to_status, self.status_REOPENED)
        self.assertEqual(log.action, 'REOPENED')
    
    def test___eq___operator(self):
        """testing the equality of two tickets
        """
        
        ticket1 = Ticket(**self.kwargs)
        ticket2 = Ticket(**self.kwargs)
        
        # no two tickets are equal
        self.assertNotEqual(ticket1, ticket2)
