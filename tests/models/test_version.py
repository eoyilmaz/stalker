# -*- coding: utf-8 -*-
# Copyright (c) 2009-2012, Erkan Ozgur Yilmaz
# 
# This module is part of Stalker and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import unittest
from stalker.conf import defaults
from stalker import (Link, Project, Repository, Sequence, Shot, Status,
                     StatusList, Task, Type, Version)
from stalker import db
from stalker.db.session import DBSession, ZopeTransactionExtension

import logging
from stalker import log
logger = logging.getLogger('stalker.models.version.Version')
logger.setLevel(log.logging_level)

class VersionTester(unittest.TestCase):
    """tests stalker.models.version.Version class
    """
    @classmethod
    def setUpClass(cls):
        """setting up the test in class level
        """
        DBSession.remove()
        DBSession.configure(extension=None)
    
    @classmethod
    def tearDownClass(cls):
        """clean up the test in class level
        """
        DBSession.remove()
        DBSession.configure(extension=ZopeTransactionExtension)
    
    def setUp(self):
        """setup the test
        """
        
        DBSession.remove()
        db.setup()
        
        # statuses
        self.test_status1 = Status(name="Status1", code="STS1")
        self.test_status2 = Status(name="Status2", code="STS2")
        self.test_status3 = Status(name="Status3", code="STS3")
        self.test_status4 = Status(name="Status4", code="STS4")
        self.test_status5 = Status(name="Status5", code="STS5")

        # status lists
        self.test_project_status_list = StatusList(
            name="Project Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
                ],
            target_entity_type=Project,
            )

        self.test_sequence_status_list = StatusList(
            name="Sequence Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
                ],
            target_entity_type=Sequence,
            )

        self.test_shot_status_list = StatusList(
            name="Shot Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
                ],
            target_entity_type=Shot,
            )

        self.test_task_status_list = StatusList(
            name="Task Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
                ],
            target_entity_type=Task,
            )

        self.test_version_status_list = StatusList(
            name="Version Status List",
            statuses=[
                self.test_status1,
                self.test_status2,
                self.test_status3,
                self.test_status4,
                self.test_status5,
                ],
            target_entity_type=Version,
        )

        # repository
        self.test_repo = Repository(
            name="Test Repository",
        )

        # a project type
        self.test_project_type = Type(
            name="Test",
            code='test',
            target_entity_type=Project,
        )

        # create a project
        self.test_project = Project(
            name="Test Project",
            code='tp',
            type=self.test_project_type,
            status_list=self.test_project_status_list,
            repository=self.test_repo,
        )

        # create a sequence
        self.test_sequence = Sequence(
            name="Test Sequence",
            code="SEQ1",
            project=self.test_project,
            status_list=self.test_sequence_status_list,
        )

        # create a shot
        self.test_shot1 = Shot(
            code="SH001",
            sequence=self.test_sequence,
            status_list=self.test_shot_status_list,
        )

        # create a group of Tasks for the shot
        self.test_task1 = Task(
            name="Task1",
            task_of=self.test_shot1,
            status_list=self.test_task_status_list,
            )

        # a Link for the source_file
        self.test_source_link = Link(
            name="Link1",
            path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/v001.ma",
            )

        # a Link for the input file
        self.test_input_link1 = Link(
            name="Input Link 1",
            path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/Outputs/"\
                 "SH001_beauty_v001.###.exr"
        )

        self.test_input_link2 = Link(
            name="Input Link 2",
            path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/Outputs/"\
                 "SH001_occ_v001.###.exr"
        )
        
        
        # a Link for the ouput file
        self.test_output_link1 = Link(
            name="Output Link 1",
            path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/Outputs/"\
                 "SH001_beauty_v001.###.exr"
        )

        self.test_output_link2 = Link(
            name="Output Link 2",
            path="/mnt/M/JOBs/TestProj/Seqs/TestSeq/Shots/SH001/FX/Outputs/"\
                 "SH001_occ_v001.###.exr"
        )
        

        # now create a version for the Task
        self.kwargs = {
            "name": "Version1",
            "take_name": "TestTake",
            "source_file": self.test_source_link,
            "inputs": [self.test_input_link1,
                       self.test_input_link2],
            "outputs": [self.test_output_link1,
                        self.test_output_link2],
            "version_of": self.test_task1,
            "status_list": self.test_version_status_list,
            }
        
        # and the Version
        self.test_version = Version(**self.kwargs)
        
        # set the published to False
        self.test_version.is_published = False
        
    def tearDown(self):
        """clean up test
        """
        DBSession.remove()
    
    def test___auto_name__class_attribute_is_set_to_True(self):
        """testing if the __auto_name__ class attribute is set to True for
        Version class
        """
        self.assertTrue(Version.__auto_name__)
     
    def test_take_name_argument_is_skipped_defaults_to_default_value(self):
        """testing if the take_name argument is skipped the take attribute is
        going to be set to the default value which is
        stalker.conf.defaults.DEFAULT_VERSION_TAKE_NAME
        """
        self.kwargs.pop("take_name")
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.take_name,
                         defaults.VERSION_TAKE_NAME)

    def test_take_name_argument_is_None(self):
        """testing if a TypeError will be raised when the take_name argument is
        None
        """
        self.kwargs["take_name"] = None
        self.assertRaises(TypeError, Version, **self.kwargs)

    def test_take_name_attribute_is_None(self):
        """testing if a TypeError will be raised when the take_name attribute
        is set to None
        """
        self.assertRaises(TypeError, setattr, self.test_version, "take_name",
                          None)

    def test_take_name_argument_is_empty_string(self):
        """testing if a ValueError will be raised when the take_name argument
        is given as an empty string
        """
        self.kwargs["take_name"] = ""
        self.assertRaises(ValueError, Version, **self.kwargs)

    def test_take_name_attribute_is_empty_string(self):
        """testing if a ValueError will be raised when the take_name attribute
        is set to an empty string
        """
        self.assertRaises(ValueError, setattr, self.test_version, "take_name",
                          "")

    def test_take_name_argument_is_not_a_string_will_be_converted_to_one(self):
        """testing if the given take_name argument is not a string will be
        converted to a proper string
        """
        test_values = [
            (1, "1"),
            (1.2, "12"),
            (["a list"], "alist"),
            ({"a": "dict"}, "adict")]

        for test_value in test_values:
            self.kwargs["take_name"] = test_value[0]
            new_version = Version(**self.kwargs)

            self.assertEqual(new_version.take_name, test_value[1])

    def test_take_name_attribute_is_not_a_string_will_be_converted_to_one(self):
        """testing if the given take_name attribute is not a string will be
        converted to a proper string
        """
        test_values = [
            (1, "1"),
            (1.2, "12"),
            (["a list"], "alist"),
            ({"a": "dict"}, "adict")]

        for test_value in test_values:
            self.test_version.take_name = test_value[0]
            self.assertEqual(self.test_version.take_name, test_value[1])

    def test_take_name_argument_is_formatted_to_empty_string(self):
        """testing if a ValueError will be raised when the take_name argument
        string is formatted to an empty string
        """
        self.kwargs["take_name"] = "##$½#$"
        self.assertRaises(ValueError, Version, **self.kwargs)

    def test_take_name_attribute_is_formatted_to_empty_string(self):
        """testing if a ValueError will be raised when the take_name argument
        string is formatted to an empty string
        """
        self.assertRaises(ValueError, setattr, self.test_version, "take_name",
                          "##$½#$")

#    def test_version_argument_is_skipped(self):
#        """testing if a TypeError will be raised when the version argument is
#        skipped
#        """
#        self.kwargs.pop("version")
#        self.assertRaises(TypeError, Version, **self.kwargs)
#
#    def test_version_argument_is_None(self):
#        """testing if a TypeError will be raised when the version argument is
#        None
#        """
#        self.kwargs["version"] = None
#        self.assertRaises(TypeError, Version, **self.kwargs)
#
#    def test_version_attribute_is_None(self):
#        """testing if a TypeError will be raised when the version attribute is
#        set to None
#        """
#        self.assertRaises(TypeError, self.test_version, "version", None)
#
#    def test_version_argument_is_0(self):
#        """testing if a ValueError will be raised when the version argument is
#        0
#        """
#        self.kwargs["version"] = 0
#        self.assertRaises(ValueError, Version, **self.kwargs)
#
#    def test_version_attribute_is_0(self):
#        """testing if a ValueError will be raised when the version attribute is
#        set to 0
#        """
#        self.assertRaises(ValueError, setattr, self.test_version, "version", 0)
#
#    def test_version_argument_is_negative(self):
#        """testing if a ValueError will be raised when the version argument is
#        negative
#        """
#        self.kwargs["version"] = -1
#        self.assertRaises(ValueError, Version, **self.kwargs)
#
#    def test_version_attribute_is_negative(self):
#        """testing if a ValueError will be raised when the version attribute is
#        negative
#        """
#        self.assertRaises(ValueError, setattr, self.test_version, "version",
#
    def test_version_of_argument_is_skipped(self):
        """testing if a TypeError will be raised when the version_of argument
        is skipped
        """
        self.kwargs.pop("version_of")
        self.assertRaises(TypeError, Version, **self.kwargs)

    def test_version_of_argument_is_None(self):
        """testing if a TypeError will be raised when the version_of argument
        is None
        """
        self.kwargs["version_of"] = None
        self.assertRaises(TypeError, Version, **self.kwargs)

    def test_version_of_attribute_is_None(self):
        """testing if a TypeError will be raised when the version_of attribute
        is None
        """
        self.assertRaises(TypeError, setattr, self.test_version,
                          "version_of", None)

    def test_version_of_argument_is_not_a_Task(self):
        """testing if a TypeError will be raised when the version_of argumment
        is not a Task instance
        """
        self.kwargs["version_of"] = "a task"
        self.assertRaises(TypeError, Version, **self.kwargs)

    def test_version_of_attribute_is_not_a_Task(self):
        """testing if a TypeError will be raised when the version_of attribute
        is not a Task instance
        """
        self.assertRaises(TypeError, setattr, self.test_version, "version_of",
                          "a task")

    def test_version_of_attribute_is_working_properly(self):
        """testing if the version_of attribute is working properly
        """
        new_task = Task(
            name="New Test Task",
            task_of=self.test_shot1,
            status_list=self.test_task_status_list,
            )

        self.assertIsNot(self.test_version.version_of, new_task)
        self.test_version.version_of = new_task
        self.assertIs(self.test_version.version_of, new_task)
    
    def test_version_number_attribute_is_automatically_generated(self):
        """testing if the version_number attribute is automatically generated
        """
        self.assertEqual(self.test_version.version_number, 1)
        DBSession.add(self.test_version)
        DBSession.commit()
        
        new_version = Version(**self.kwargs)
        DBSession.add(new_version)
        DBSession.commit()
        
        self.assertEqual(self.test_version.version_of, new_version.version_of)
        self.assertEqual(self.test_version.take_name, new_version.take_name)
        
        self.assertEqual(new_version.version_number, 2)
    
    def test_version_number_attribute_is_starting_from_1(self):
        """testing if the version_number attribute is starting from 1
        """
        self.assertEqual(self.test_version.version_number, 1)
    
    def test_version_number_attribute_is_set_to_a_lower_then_it_should_be(self):
        """testing if the version_number attribute will be set to a correct
        unique value when it is set to a lower number then it should be
        """
        
        self.test_version.version_number = -1
        self.assertEqual(self.test_version.version_number, 1)
        
        self.test_version.version_number = -10
        self.assertEqual(self.test_version.version_number, 1)
        
        DBSession.add(self.test_version)
        DBSession.commit()
        
        self.test_version.version_number = -100
        # it should be 1 again
        self.assertEqual(self.test_version.version_number, 1)
        
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.version_number, 2)
        
        new_version.version_number = 1
        self.assertEqual(new_version.version_number, 2)
        
        new_version.version_number = 100
        self.assertEqual(new_version.version_number, 100)
    
    def test_source_file_argument_is_skipped(self):
        """testing if the source_file will be None when the source_file
        argument is skipped
        """
        self.kwargs.pop("source_file")
        new_version = Version(**self.kwargs)
        self.assertIs(new_version.source_file, None)

    def test_source_file_argument_is_None(self):
        """testing if the source_file will be None when the source argument is
        None
        """
        self.kwargs["source_file"] = None
        new_version = Version(**self.kwargs)
        self.assertIs(new_version.source_file, None)

    def test_source_file_argument_is_not_a_Link_instance(self):
        """testing if a TypeError will be raised when the source_file argument
        is not a stalker.models.link.Link instance
        """
        self.kwargs["source_file"] = 123123
        self.assertRaises(TypeError, Version, **self.kwargs)

    def test_source_file_attribute_is_not_a_Link_instance(self):
        """testing if a TypeError will be raised when the source_file attribute
        is set to something other than a Link instance
        """
        self.assertRaises(TypeError, setattr, self.test_version, "source_file",
                          121)

    def test_source_file_argument_is_working_properly(self):
        """testing if the source_file argument is working properly
        """
        new_source_file = Link(name="Test Link", path="none")
        self.kwargs["source_file"] = new_source_file
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.source_file, new_source_file)

    def test_source_file_attribute_is_working_properly(self):
        """testing if the source_file attribute is working properly
        """
        new_source_file = Link(name="Test Link", path="empty string")
        self.assertNotEqual(self.test_version.source_file, new_source_file)
        self.test_version.source_file = new_source_file
        self.assertEqual(self.test_version.source_file, new_source_file)
    
    def test_inputs_argument_is_skipped(self):
        """testing if the inputs attribute will be an empty list when the
        inputs argument is skipped
        """
        self.kwargs.pop("inputs")
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.inputs, [])

    def test_inputs_argument_is_None(self):
        """testing if the inputs attribute will be an empty list when the
        inputs argument is None
        """
        self.kwargs["inputs"] = None
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.inputs, [])

    def test_inputs_attribute_is_None(self):
        """testing if a TypeError will be raised when the inputs argument is
        set to None
        """
        self.assertRaises(TypeError, setattr, self.test_version, "inputs",
                          None)
    
    def test_inputs_argument_is_not_a_list_of_Link_instances(self):
        """testing if a TypeError will be raised when the inputs attribute is
        set to something other than a Link instance
        """
        test_value = [132, "231123"]
        self.kwargs["inputs"] = test_value
        self.assertRaises(TypeError, Version, **self.kwargs)
    
    def test_inputs_attribute_is_not_a_list_of_Link_instances(self):
        """testing if a TypeError will be raised when the inputs attribute is
        set to something other than a Link instance
        """
        test_value = [132, "231123"]
        self.assertRaises(TypeError, setattr, self.test_version, "inputs",
                          test_value)
    
    def test_inputs_attribute_is_working_properly(self):
        """testing if the inputs attribute is working properly
        """
        self.kwargs.pop("inputs")
        new_version = Version(**self.kwargs)
        
        self.assertNotIn(self.test_input_link1, new_version.inputs)
        self.assertNotIn(self.test_input_link2, new_version.inputs)
        
        new_version.inputs = [self.test_input_link1, self.test_input_link2]
        
        self.assertIn(self.test_input_link1, new_version.inputs)
        self.assertIn(self.test_input_link2, new_version.inputs)
    
    def test_outputs_argument_is_skipped(self):
        """testing if the outputs attribute will be an empty list when the
        outputs argument is skipped
        """
        self.kwargs.pop("outputs")
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.outputs, [])

    def test_outputs_argument_is_None(self):
        """testing if the outputs attribute will be an empty list when the
        outputs argument is None
        """
        self.kwargs["outputs"] = None
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.outputs, [])

    def test_outputs_attribute_is_None(self):
        """testing if a TypeError will be raised when the outputs argument is
        set to None
        """
        self.assertRaises(TypeError, setattr, self.test_version, "outputs",
                          None)

    def test_outputs_argument_is_not_a_list_of_Link_instances(self):
        """testing if a TypeError will be raised when the outputs attribute is
        set to something other than a Link instance
        """
        test_value = [132, "231123"]
        self.kwargs["outputs"] = test_value
        self.assertRaises(TypeError, Version, **self.kwargs)

    def test_outputs_attribute_is_not_a_list_of_Link_instances(self):
        """testing if a TypeError will be raised when the outputs attribute is
        set to something other than a Link instance
        """
        test_value = [132, "231123"]
        self.assertRaises(TypeError, setattr, self.test_version, "outputs",
                          test_value)

    def test_outputs_attribute_is_working_properly(self):
        """testing if the outputs attribute is working properly
        """
        self.kwargs.pop("outputs")
        new_version = Version(**self.kwargs)

        self.assertNotIn(self.test_output_link1, new_version.outputs)
        self.assertNotIn(self.test_output_link2, new_version.outputs)

        new_version.outputs = [self.test_output_link1, self.test_output_link2]

        self.assertIn(self.test_output_link1, new_version.outputs)
        self.assertIn(self.test_output_link2, new_version.outputs)

    def test_is_published_attribute_is_False_by_default(self):
        """testing if the is_published attribute is False by default
        """
        self.assertEqual(self.test_version.is_published, False)

    def test_is_published_attribute_is_working_properly(self):
        """testing if the is_published attribute is working properly
        """
        self.test_version.is_published = True
        self.assertEqual(self.test_version.is_published, True)

        self.test_version.is_published = False
        self.assertEqual(self.test_version.is_published, False)
    
#    def test_tickets_attribute_is_not_set_to_a_list(self):
#        """testing if a TypeError will be raised when the tickets attribute is
#        not set to a list instance
#        """
#        self.assertRaises(TypeError, setattr, self.test_version, "reviews",
#                          123)
#
#    def test_reviews_attribute_is_not_accepting_anything_other_than_list_of_Reviews(self):
#        """testing if a TypeError will be raised when the elements of the
#        reivews attribute is set to something other than a Review
#        """
#        self.assertRaises(TypeError, setattr, self.test_version, "reviews",
#            [123])
#
#    def test_reviews_attribute_is_working_properly(self):
#        """testing if the reviews attribute is working properly
#        """
#        # create a couple of Reviews
#        rev1 = Review(name="Test Rev 1", to=self.test_version)
#        rev2 = Review(name="Test Rev 2", to=self.test_version)
#        rev3 = Review(name="Test Rev 3", to=self.test_version)
#
#        # create a new Version with no reviews
#        new_version = Version(**self.kwargs)
#
#        # now try to assign all the reviews to the new object
#        # this should work fine
#        test_reviews = [rev1, rev2, rev3]
#        new_version.reviews = test_reviews
#
#        self.assertEqual(new_version.reviews, test_reviews)
#
#    def test_reviews_attribute_updates_the_to_attribute_in_the_Review_instance(self):
#        """testing if the "to" attribute is updated with the current object
#        when it is set
#        """
#        # create a couple of Reviews
#        rev1 = Review(name="Test Rev 1", to=self.test_version)
#        rev2 = Review(name="Test Rev 2", to=self.test_version)
#        rev3 = Review(name="Test Rev 3", to=self.test_version)
#
#        # create a new Version with no reviews
#        new_version = Version(**self.kwargs)
#        
#        # now try to assign all the reviews to the new object
#        new_version.reviews = [rev1, rev2, rev3]
#
#        # now check if the reviews "to" attribute is pointing to the correct
#        # object
#        self.assertEqual(rev1.to, new_version)
#        self.assertEqual(rev2.to, new_version)
#        self.assertEqual(rev3.to, new_version)
#
#        # check the reviews are in the reviews list
#        self.assertIn(rev1, new_version.reviews)
#        self.assertIn(rev2, new_version.reviews)
#        self.assertIn(rev3, new_version.reviews)
#
#        # now try to remove the review from the reviews list and expect a
#        # TypeError
#        self.assertRaises(RuntimeError, new_version.reviews.remove, rev1)
#
#    def test_reviews_attribute_handles_assigning_the_same_review_twice(self):
#        """testing if assigning the same review twice or more will not break
#        anything or raise any exception
#        """
#        # create a couple of Reviews
#        rev1 = Review(name="Test Rev 1", to=self.test_version)
#        rev2 = Review(name="Test Rev 2", to=self.test_version)
#        rev3 = Review(name="Test Rev 3", to=self.test_version)
#
#        # now try to assign the same review again to the same object
#        self.test_version.reviews.append(rev1)
#
#        # now try the reverse
#        rev1.to = self.test_version
#
#        # the review should be in the list
#        self.assertIn(rev1, self.test_version.reviews)
