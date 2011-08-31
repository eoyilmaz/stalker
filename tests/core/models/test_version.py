#-*- coding: utf-8 -*-



import unittest
from stalker.conf import defaults
from stalker.core.models import (Version, Repository, Type, Project, Status,
                                 StatusList, Sequence, Shot, Task, Link,
                                 Review)






########################################################################
class VersionTester(unittest.TestCase):
    """tests stalker.core.models.Version class
    """
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
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
        
        # repository
        self.test_repo = Repository(
            name="Test Repository",
        )
        
        # a project type
        self.test_project_type = Type(
            name="Test",
            target_entity_type=Project,
        )
        
        # create a project
        self.test_project = Project(
            name="Test Project",
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
            "take": "TestTake",
            "source_file": self.test_source_link,
            "outputs": [self.test_output_link1,
                        self.test_output_link2,],
            "task": self.test_task1,
        }
        
        # and the Version
        self.test_version = Version(**self.kwargs)
        
        # set the published to False
        self.test_version.published = False
    
    
    
    #----------------------------------------------------------------------
    def test_take_argument_is_skipped_defaults_to_default_value(self):
        """testing if the take argument is skipped the take attribute is going
        to be set to the default value which is
        stalker.conf.defaults.DEFAULT_VERSION_TAKE_NAME
        """
        
        self.kwargs.pop("take")
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.take, defaults.DEFAULT_VERSION_TAKE_NAME)
    
    
    
    #----------------------------------------------------------------------
    def test_take_argument_is_None_defaults_to_default_value(self):
        """testing if the take argument is None the take attribute is going to
        be set to the default value which is
        stalker.conf.defaults.DEFAULT_VERSION_TAKE_NAME
        """
        
        self.kwargs["take"] = None
        new_version = Version(**self.kwargs)
        self.assertEqual(new_version.take, defaults.DEFAULT_VERSION_TAKE_NAME)
    
    
    
    #----------------------------------------------------------------------
    def test_take_attribute_is_None_defaults_to_default_value(self):
        """testing if the take attribute is set to None it is going to be set
        to the default value which is
        stalker.conf.defaults.DEFAULT_VERSION_TAKE_NAME
        """
        
        self.test_version.take = None
        self.assertEqual(self.test_version.take,
                         defaults.DEFAULT_VERSION_TAKE_NAME)
    
    
    
    #----------------------------------------------------------------------
    def test_take_argument_is_empty_string(self):
        """testing if a ValueError will be raised when the take argument is an
        empty string
        """
        
        self.kwargs["take"] = ""
        self.assertRaises(ValueError, Version, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_take_attribute_is_empty_string(self):
        """testing if a ValueError will be raised when the take attribute is
        set to an empty string
        """
        
        self.assertRaises(ValueError, setattr, self.test_version, "take", "")
    
    
    
    #----------------------------------------------------------------------
    def test_take_argument_is_not_a_string_will_be_converted_to_one(self):
        """testing if the given take argument is not a string will be converted
        to a proper string
        """
        
        test_values = [
            (1, "1"),
            (1.2, "1.2"),
            (["a list"], "a list"),
            ({"a": "dict"}, "a dict")]        
        for test_value in test_values:
            self.kwargs["take"] = test_value[0]
            new_version = Version(**self.kwargs)
            
            self.assertEqual(new_version.take, test_value[1])
    
    
    
    #----------------------------------------------------------------------
    def test_take_attribute_is_not_a_string_will_be_converted_to_one(self):
        """testing if the given take attribute is not a string will be
        converted to a proper string
        """
        
        test_values = [
            (1, "1"),
            (1.2, "1.2"),
            (["a list"], "a list"),
            ({"a": "dict"}, "a dict")]
        
        for test_value in test_values:
            self.test_version.take = test_value[0]
            self.assertEqual(self.test_version.take, test_value[1])
    
    
    
    #----------------------------------------------------------------------
    def test_take_argument_is_formatted_to_empty_string(self):
        """testing if a ValueError will be raised when the take argument string
        is formatted to an empty string
        """
        
        self.kwargs["take"] = "##$½#$"
        self.assertRaises(ValueError, Version, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_take_attribute_is_formatted_to_empty_string(self):
        """testing if a ValueError will be raised when the take argument string
        is formatted to an empty string
        """
        
        self.assertRaises(ValueError, setattr, self.test_version, "take",
                          "##$½#$")
    
    
    
    #----------------------------------------------------------------------
    def test_version_argument_is_skipped(self):
        """testing if a TypeError will be raised when the version argument is
        skipped
        """
        
        self.kwargs.pop("version")
        self.assertRaises(TypeError, Version, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_version_argument_is_None(self):
        """testing if a TypeError will be raised when the version argument is
        None
        """
        
        self.kwargs["version"] = None
        self.assertRaises(TypeError, Version, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_version_attribute_is_read_only(self):
        """testing if an AttributeError will be raised when the version
        attribute is set to something
        """
        
        self.assertRaises(AttributeError, setattr, self.test_version,
                          "version", 123)
    
    
    
    #----------------------------------------------------------------------
    def test_version_argument_is_0(self):
        """testing if a ValueError will be raised when the version argument is
        0
        """
        
        self.kwargs["version"] = 0
        self.assertRaises(ValueError, Version, **self.kwargs)
    
    
    
    ##----------------------------------------------------------------------
    #def test_version_attribute_is_0(self):
        #"""testing if a ValueError will be raised when the version attribute is
        #set to 0
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_version_argument_is_negative(self):
        """testing if a ValueError will be raised when the version argument is
        negative
        """
        
        self.kwargs["version"] = -1
        self.assertRaises(ValueError, Version, **self.kwargs)
    
    
    
    ##----------------------------------------------------------------------
    #def test_version_attribute_is_negative(self):
        #"""testing if a ValueError will be raised when the version attribute is
        #negative
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_set_to_None(self):
        """testing if nothing happens when the reviews attribute is set to None
        """
        
        # should work without giving any errors
        self.test_version.reviews = None
        
        # and it should set it to an empty list (or something like a list)
        self.assertIsInstance(self.test_version.reviews, list)
        self.assertEqual(len(self.test_version), 0)
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the reviews attribute is
        not a list instance
        """
        
        self.assertRaises(TypeError, setattr, self.test_version, "reviews", 1)
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_not_a_list_of_Review_instances(self):
        """testing if a TypeError will be raised when the reviews attribute is
        set to a list of other objects
        """
        
        self.assertRaises(TypeError, setattr, self.test_version, "reviews",
                          ["test", "reviews"])
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_working_properly(self):
        """testing if the reviews attribute is working properly
        """
        
        # create a review
        new_review = Review(
            name="Test Review",
            
        )
    
    
    
    #----------------------------------------------------------------------
    def test_reviews_attribute_is_a_ValidatedList(self):
        """testinf if the reviews attribute is a ValidatedList instance
        """
        
        self.assertIsInstance(self.test_version.reviews, ValidatedList)
    
    
    
    #----------------------------------------------------------------------
    def test_review_attribute_updating_backref_attribute(self):
        
        self.fail("test is not implemented yet")
    
    
    
    ##----------------------------------------------------------------------
    #def test_published_attribute_is_set_to_non_bool_value(self):
        #"""testing if the published attribute is set to a non bool value will
        #be converted to a bool value
        #"""
        
        #test_value = "no bool value"
        #self.test_version.published = test_value
        #self.assertEqual(self.test_version.published, bool(test_value))
    
    
    
    ##----------------------------------------------------------------------
    #def test_published_attribute_defaults_to_false(self):
        #"""testing if the default value of published for newly created Versions
        #is False
        #"""
        
        #new_version = Version(**self.kwargs)
        #self.assertEqual(new_version.published, False)
    
    
    
    ##----------------------------------------------------------------------
    #def test_published_attribute_is_working_properly(self):
        #"""testing if the published attribute is working properly
        #"""
        
        #test_value = True
        #new_version = Version(**self.kwargs)
        #new_version.published = test_value
        #self.assertEqual(new_version.published, test_value)
        
        #test_value = False
        #new_version.published = test_value
        #self.assertEqual(new_version.published, test_value)
    
    
    
    
