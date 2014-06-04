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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

import unittest

from stalker import (db, defaults, Entity, Link, Project, Repository, Sequence,
                     Status, StatusList, Task, Type)


class SequenceTester(unittest.TestCase):
    """Tests stalker.models.sequence.Sequence class
    """

    def setUp(self):
        """setup the test
        """
        db.setup()
        # db.init()
        # we just need statuses so create them instead of initializing the db
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

        # get statuses
        self.status_new = Status.query.filter_by(code='NEW').first()
        self.status_wfd = Status.query.filter_by(code='WFD').first()
        self.status_rts = Status.query.filter_by(code='RTS').first()
        self.status_wip = Status.query.filter_by(code='WIP').first()
        self.status_prev = Status.query.filter_by(code='PREV').first()
        self.status_hrev = Status.query.filter_by(code='HREV').first()
        self.status_drev = Status.query.filter_by(code='DREV').first()
        self.status_oh = Status.query.filter_by(code='OH').first()
        self.status_stop = Status.query.filter_by(code='STOP').first()
        self.status_cmpl = Status.query.filter_by(code='CMPL').first()

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
                self.status_new,
                self.status_wip,
                self.status_cmpl,
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

        self.sequence_status_list = \
            StatusList.query.filter_by(target_entity_type='Sequence').first()

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

    def test_TaskableEntity_initialization(self):
        """testing if the TaskableEntity part is initialized correctly
        """
        status1 = Status(name="On Hold", code="OH")

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
            project=new_project,
            parent=new_sequence,
        )

        task2 = Task(
            name="Lighting",
            status=0,
            project=new_project,
            parent=new_sequence,
        )

        tasks = [task1, task2]

        self.assertEqual(
            sorted(new_sequence.tasks, key=lambda x: x.name),
            sorted(tasks, key=lambda x: x.name)
        )

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
