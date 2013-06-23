# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2013 Erkan Ozgur Yilmaz
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

import unittest2
import datetime

from stalker import (Entity, Link, Project, Repository, Sequence, Status,
                     StatusList, Task, Type, User)


class SequenceTester(unittest2.TestCase):
    """Tests stalker.models.sequence.Sequence class
    """

    def setUp(self):
        """setup the test
        """
        # create statuses
        self.test_status1 = Status(name="Status1", code="STS1")
        self.test_status2 = Status(name="Status2", code="STS2")
        self.test_status3 = Status(name="Status3", code="STS3")
        self.test_status4 = Status(name="Status4", code="STS4")
        self.test_status5 = Status(name="Status5", code="STS5")

        # create a test project, user and a couple of shots
        self.project_type = Type(
            name="Test Project Type",
            code='test',
            target_entity_type=Project,
        )

        # create a status list for project
        self.project_status_list = StatusList(
            name="Project Statuses",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type=Project,
        )

        # create a repository
        self.repository_type = Type(
            name="Test Type",
            code='test',
            target_entity_type=Repository
        )

        self.test_repository = Repository(
            name="Test Repository",
            type=self.repository_type,
        )

        # create projects
        self.test_project = Project(
            name="Test Project 1",
            code='tp1',
            type=self.project_type,
            status_list=self.project_status_list,
            repository=self.test_repository,
        )

        self.test_project2 = Project(
            name="Test Project 2",
            code='tp2',
            type=self.project_type,
            status_list=self.project_status_list,
            repository=self.test_repository,
        )

        self.sequence_status_list = StatusList(
            name="Sequence Statuses",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
            ],
            target_entity_type=Sequence,
        )

        # the parameters
        self.kwargs = {
            "name": "Test Sequence",
            'code': 'tseq',
            "description": "A test sequence",
            "project": self.test_project,
            "status_list": self.sequence_status_list
        }

        # the test sequence
        self.test_sequence = Sequence(**self.kwargs)

    def test___auto_name__class_attribute_is_set_to_False(self):
        """testing if the __auto_name__ class attribute is set to False for
        Sequence class
        """
        self.assertFalse(Sequence.__auto_name__)

    def test_shots_attribute_defaults_to_empty_list(self):
        """testing if the shots attribute defaults to an empty list
        """
        #self.kwargs.pop("shots")
        new_sequence = Sequence(**self.kwargs)
        self.assertEqual(new_sequence.shots, [])

    def test_shots_attribute_is_set_None(self):
        """testing if a TypeError will be raised when the shots attribute will
        be set to None
        """
        self.assertRaises(TypeError, self.test_sequence, "shots", None)

    def test_shots_attribute_is_set_to_other_than_a_list(self):
        """testing if a TypeError will be raised when the shots attribute is
        tried to be set to something other than a list
        """
        test_values = [1, 1.2, "a string"]
        for test_value in test_values:
            self.assertRaises(
                TypeError,
                setattr,
                self.test_sequence,
                "shots",
                test_value
            )

    def test_shots_attribute_is_a_list_of_other_objects(self):
        """testing if a TypeError will be raised when the shots argument is a
        list of other type of objects
        """
        test_value = [1, 1.2, "a string"]
        self.assertRaises(
            TypeError,
            setattr,
            self.test_sequence,
            "shots",
            test_value
        )

    def test_shots_attribute_elements_tried_to_be_set_to_non_Shot_object(self):
        """testing if a TypeError will be raised when the individual elements
        in the shots list tried to be set to something other than a Shot
        instance
        """
        test_values = [1, 1.2, "a string", ["a", "list"]]
        for test_value in test_values:
            self.assertRaises(TypeError,
                              self.test_sequence.shots.append, test_value)

    def test_equality(self):
        """testing the equality of sequences
        """
        new_seq1 = Sequence(**self.kwargs)
        new_seq2 = Sequence(**self.kwargs)
        new_entity = Entity(**self.kwargs)

        self.kwargs["name"] = "a different sequence"
        new_seq3 = Sequence(**self.kwargs)

        self.assertTrue(new_seq1 == new_seq2)
        self.assertFalse(new_seq1 == new_seq3)
        self.assertFalse(new_seq1 == new_entity)

    def test_inequality(self):
        """testing the inequality of sequences
        """
        new_seq1 = Sequence(**self.kwargs)
        new_seq2 = Sequence(**self.kwargs)
        new_entity = Entity(**self.kwargs)

        self.kwargs["name"] = "a different sequence"
        new_seq3 = Sequence(**self.kwargs)

        self.assertFalse(new_seq1 != new_seq2)
        self.assertTrue(new_seq1 != new_seq3)
        self.assertTrue(new_seq1 != new_entity)

    def test_ReferenceMixin_initialization(self):
        """testing if the ReferenceMixin part is initialized correctly
        """
        link_type_1 = Type(
            name="Image",
            code='image',
            target_entity_type="Link"
        )

        link1 = Link(
            name="Artwork 1",
            full_path="/mnt/M/JOBs/TEST_PROJECT",
            filename="a.jpg",
            type=link_type_1
        )
        link2 = Link(
            name="Artwork 2",
            full_path="/mnt/M/JOBs/TEST_PROJECT",
            filename="b.jbg",
            type=link_type_1
        )
        references = [link1, link2]
        self.kwargs["references"] = references
        new_sequence = Sequence(**self.kwargs)
        self.assertEqual(new_sequence.references, references)

    def test_StatusMixin_initialization(self):
        """testing if the StatusMixin part is initialized correctly
        """
        status1 = Status(name="On Hold", code="OH")
        status2 = Status(name="Complete", code="CMPLT")

        status_list = StatusList(
            name="Project Statuses",
            statuses=[status1, status2],
            target_entity_type=Sequence
        )
        self.kwargs["status"] = 0
        self.kwargs["status_list"] = status_list
        new_sequence = Sequence(**self.kwargs)
        self.assertEqual(new_sequence.status_list, status_list)

    def test_TaskableEntity_initialization(self):
        """testing if the TaskableEntity part is initialized correctly
        """
        status1 = Status(name="On Hold", code="OH")

        task_status_list = StatusList(
            name="Task Statuses",
            statuses=[status1],
            target_entity_type=Task
        )

        project_status_list = StatusList(
            name="Project Statuses", statuses=[status1],
            target_entity_type=Project,
        )

        project_type = Type(
            name="Commercial",
            code='comm',
            target_entity_type=Project
        )

        new_project = Project(
            name="Commercial",
            code='comm',
            status_list=project_status_list,
            type=project_type,
            repository=self.test_repository,
        )

        self.kwargs["new_project"] = new_project

        new_sequence = Sequence(**self.kwargs)

        task1 = Task(
            name="Modeling",
            status=0,
            status_list=task_status_list,
            project=new_project,
            parent=new_sequence,
        )

        task2 = Task(
            name="Lighting",
            status=0,
            status_list=task_status_list,
            project=new_project,
            parent=new_sequence,
        )

        tasks = [task1, task2]

        self.assertItemsEqual(new_sequence.tasks, tasks)

        # UPDATE THIS: This test needs to be in the tests.db
        # because the property it is testing is using DBSession.query
        #
        #def test_sequences_attribute_is_updated_in_the_project_instance(self):
        #"""testing if the sequences attribute is updated in the Project
        #instance.
        #"""

        #status1 = Status(name="On Hold", code="OH")

        #task_status_list = StatusList(
        #name="Task Statuses",
        #statuses=[status1],
        #target_entity_type=Task
        #)

        #project_status_list = StatusList(
        #name="Project Statuses", statuses=[status1],
        #target_entity_type=Project
        #)

        #project_type = Type(
        #name="Commercial",
        #code='comm',
        #target_entity_type=Project,
        #)

        #new_project = Project(
        #name="Commercial",
        #code='comm',
        #status_list=project_status_list,
        #type=project_type,
        #repository=self.test_repository,
        #)

        #self.kwargs["project"] = new_project

        #new_sequence = Sequence(**self.kwargs)

        #task1 = Task(
        #   name="Modeling",
        #   status=0,
        #   status_list=task_status_list,
        #   project=new_project,
        #   parent=new_sequence,
        #)

        #task2 = Task(
        #   name="Lighting",
        #   status=0,
        #   status_list=task_status_list,
        #   project=new_project,
        #   parent=new_sequence,
        #)

        #tasks = [task1, task2]

        #self.assertIn(new_sequence, new_project.sequences)

    def test_ProjectMixin_initialization(self):
        """testing if the ProjectMixin part is initialized correctly
        """
        status1 = Status(name="On Hold", code="OH")

        project_status_list = StatusList(
            name="Project Statuses", statuses=[status1],
            target_entity_type=Project
        )

        project_type = Type(
            name="Commercial",
            code='comm',
            target_entity_type=Project
        )

        new_project = Project(
            name="Test Project",
            code='tp',
            status=project_status_list[0],
            status_list=project_status_list,
            type=project_type,
            repository=self.test_repository
        )

        self.kwargs["project"] = new_project
        new_sequence = Sequence(**self.kwargs)
        self.assertEqual(new_sequence.project, new_project)

    def test_plural_class_name(self):
        """testing the plural name of Sequence class
        """
        self.assertTrue(self.test_sequence.plural_class_name, "Sequences")

    def test___strictly_typed___is_False(self):
        """testing if the __strictly_typed__ class attribute is False for
        Sequence class.
        """
        self.assertEqual(Sequence.__strictly_typed__, False)
