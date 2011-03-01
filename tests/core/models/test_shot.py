#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import Entity, Shot, Sequence, Asset, AssetType, Task
from stalker.ext.validatedList import ValidatedList






########################################################################
class ShotTester(mocker.MockerTestCase):
    """Tests the Shot class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        # create a Sequence
        self.mock_sequence = self.mocker.mock(Sequence)
        self.mock_sequence2 = self.mocker.mock(Sequence)
        self.mock_sequence3 = self.mocker.mock(Sequence)
        
        # create mock Tasks
        self.mock_task1 = self.mocker.mock(Task)
        self.mock_task2 = self.mocker.mock(Task)
        self.mock_task3 = self.mocker.mock(Task)
        
        # create mock Assets
        self.mock_asset1 = self.mocker.mock(Asset)
        self.mock_asset2 = self.mocker.mock(Asset)
        self.mock_asset3 = self.mocker.mock(Asset)
        
        # another shot with the same code
        self.mock_shot2 = self.mocker.mock(Shot)
        
        self.expect(self.mock_sequence.shots).\
            result([]).count(0, None)
        
        self.expect(self.mock_sequence3.shots).\
            result([]).count(0, None)
        
        self.expect(self.mock_sequence2.shots).\
            result([self.mock_shot2]).count(0, None)
        
        # the code parameter to be used in the original mock_shot and the
        # secondary mock_shot2
        code = "SH123"
        
        self.expect(self.mock_shot2.code).result(code).count(0, None)
        
        self.mocker.replay()
        
        self.cut_in_default = 1
        self.cut_duration_default = 1
        self.cut_out_default = 1
        
        self.kwargs = {
            "code": code,
            "description": "This is a test Shot",
            "assets": [self.mock_asset1, self.mock_asset2, self.mock_asset3],
            "sequence": self.mock_sequence,
            "cut_in": 112,
            "cut_out": 149,
            "cut_duration": 123,
        }
        
        # create a mock shot object
        self.mock_shot = Shot(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_name_attribute_is_a_uuid4_sequence(self):
        """testing if the name attribute is set to a proper uuid4 sequence
        """
        
        # the length is 32 character
        self.assertEquals(len(self.mock_shot.name), 32)
        
        import re
        
        # and all the characters are in [0-9a-f] range
        self.assertEquals(re.sub("[0-9a-f]+","", self.mock_shot.name), "")
    
    
    
    #----------------------------------------------------------------------
    def test_name_attribute_can_not_be_changed(self):
        """testing if the name attribute can not be changed
        """
        
        test_value = "new_name"
        before_value = self.mock_shot.name
        
        self.mock_shot.name = test_value
        
        self.assertEquals(self.mock_shot.name, before_value)
    
    
    
    #----------------------------------------------------------------------
    def test_sequence_argument_is_skipped(self):
        """testing if a ValueError will be raised when the sequence argument is
        skipped
        """
        
        self.kwargs.pop("sequence")
        self.assertRaises(ValueError, Shot, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_sequence_argument_is_None(self):
        """testing if a ValueError will be raised when the sequence argument is
        None
        """
        
        self.kwargs["sequence"] = None
        self.assertRaises(ValueError, Shot, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_sequence_argument_is_not_Sequence_instance(self):
        """testing if a ValueError will be raised when the given sequence
        argument is not an instance of stalker.core.models.Sequence
        """
        
        test_values = [1, 1.2, "sequence", ["a", "sequence"]]
        
        for test_value in test_values:
            self.kwargs["sequence"] = test_value
            self.assertRaises(ValueError, Shot, self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_sequence_argument_already_has_a_shot_with_the_same_code(self):
        """testing if a ValueError will be raised when the given sequence
        argument already has a shot with the same code
        """
        
        # lets try to assign the shot to the mock_sequence2 which has another
        # shot with the same code
        self.kwargs["sequence"] = self.mock_sequence2
        
        self.assertRaises(ValueError, Shot, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_sequence_attribute_is_read_only(self):
        """testing if the sequence attribute is read only
        """
        
        self.assertRaises(AttributeError, setattr,self.mock_shot, "sequence",
                          self.mock_sequence2)
    
    
    
    #----------------------------------------------------------------------
    def test_sequence_contains_shots(self):
        """testing if the current shot is going to be added to the sequence in
        the sequence object, so the Sequence.shots list will contain the
        current shot
        """
        
        self.assertIn(self.mock_shot, self.mock_shot.sequence.shots)
    
    
    
    #----------------------------------------------------------------------
    def test_sequence_argument_works_properly(self):
        """testing if the sequence argument works properly
        """
        
        self.assertEquals(self.mock_shot.sequence, self.kwargs["sequence"])
    
    
    
    #----------------------------------------------------------------------
    def test_assets_argument_is_None(self):
        """testing if no error will be raised when the assets argument is None
        """
        
        self.kwargs["assets"] = None
        self.kwargs["code"] = "SH123A"
        new_shot = Shot(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_is_set_to_None(self):
        """testing if no error will be raised when the assets attribute is set
        to None
        """
        
        self.mock_shot.assets = None
    
    
    
    #----------------------------------------------------------------------
    def test_assets_argument_set_to_None_defaults_to_empty_list(self):
        """testing if the assets argument is given as None will default the
        assets attribute to an empty list
        """
        
        self.kwargs["assets"] = None
        self.kwargs["code"] = "SH123A"
        new_shot = Shot(**self.kwargs)
        self.assertEquals(new_shot.assets, [])
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_is_set_to_None_defaults_to_empty_list(self):
        """testing if the assets attribute is set to None will set the assets
        to an empty list
        """
        
        self.mock_shot.assets = None
        self.assertEquals(self.mock_shot.assets, [])
    
    
    
    #----------------------------------------------------------------------
    def test_assets_argument_is_not_a_list(self):
        """testing if a ValueError will be raised when the assets argument is
        not a list
        """
        
        test_values = [1, 1.2, "a str"]
        
        for test_value in test_values:
            self.kwargs["assets"] = test_value
            self.assertRaises(ValueError, Shot, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_is_not_a_list(self):
        """testing if a ValueError will be raised when the assets attribute is
        not a list
        """
        
        test_values = [1, 1.2, "a str"]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_shot,
                "assets",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_assets_argument_is_not_a_list_of_Asset_instances(self):
        """testing if a ValueError will be raised when the assets argument is
        not a list of stalker.core.models.Asset instances
        """
        
        self.kwargs["assets"] = [1, 1.2, "an asset"]
        self.assertRaises(ValueError, Shot, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_is_not_a_list_of_Asset_instances(self):
        """testing if a ValueError will be raised when the assets attribute is
        not a list of stalker.core.models.Asset instances
        """
        
        test_value = [1, 1.2, "an asset"]
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_shot,
            "assets",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_assets_attribute_is_a_ValidatedList_instance(self):
        """testing if the assets attribute is an instance of ValidatedList
        """
        
        self.assertIsInstance(self.mock_shot.assets, ValidatedList)
    
    
    
    #----------------------------------------------------------------------
    def test_assets_argument_is_skipped_default_value_is_empty_list(self):
        """testing if the default value of assets is an empty list when the
        assets argument is skipped
        """
        
        self.kwargs.pop("assets")
        self.kwargs["code"] = "SH123A"
        new_shot = Shot(**self.kwargs)
        self.assertEquals(new_shot.assets, [])
    
    
    
    #----------------------------------------------------------------------
    def test_code_argument_is_None(self):
        """testing if a ValueError will be raised when the code argument is
        None
        """
        self.kwargs["code"] = None
        self.assertRaises(ValueError, Shot, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_code_attribute_is_None(self):
        """testing if a ValueError will be raised when the code argument is
        None
        """
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_shot,
            "code",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_code_argument_is_empty_string(self):
        """testing if a ValueError will be raised when the code argument is
        empty string
        """
        
        self.kwargs["code"] = ""
        self.assertRaises(ValueError, Shot, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_code_attribute_is_empty_string(self):
        """testing if a ValueError will be raised when the code attribute is
        empty string
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_shot,
            "code",
            ""
        )
    
    
    
    #----------------------------------------------------------------------
    def test_cut_in_argument_is_skipped_defaults_to_default_value(self):
        """testing if the cut_in argument is skipped the cut_in argument will
        be set to the default value
        """
        
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop("cut_in")
        new_shot = Shot(**self.kwargs)
        self.assertEquals(new_shot.cut_in, self.cut_in_default)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_in_argument_is_set_to_None_defaults_to_default_value(self):
        """testing if the cut_in argument is set to None the cut_in attribute
        is set to default value
        """
        
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_in"] = None
        new_shot = Shot(**self.kwargs)
        self.assertEquals(new_shot.cut_in, self.cut_in_default)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_in_argument_is_not_integer(self):
        """testing if a ValueError will be raised when the cut_in argument is
        not an instance of int
        """
        
        self.kwargs["cut_in"] = "a string"
        self.assertRaises(ValueError, Shot, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_in_attribute_is_not_integer(self):
        """testing if a ValueError will be used when the cut_in attribute is
        not an instance of int
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_shot,
            "cut_in",
            "a string"
        )
    
    
    
    #----------------------------------------------------------------------
    def test_cut_in_argument_is_bigger_than_cut_out_argument(self):
        """testing if the cut_out attribute is updated when the cut_in
        argument is bigger than cut_out argument
        """
        
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_in"] = self.kwargs["cut_out"] + 10
        new_shot = Shot(**self.kwargs)
        self.assertEquals(new_shot.cut_out, new_shot.cut_in)
        self.assertEquals(new_shot.cut_duration, 1)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_in_attribute_is_bigger_than_cut_out_attribute(self):
        """testing if the cut_out attribute is updated when the cut_in
        attribute is bigger than cut_out attribute
        """
        
        self.mock_shot.cut_in = self.mock_shot.cut_out + 10
        self.assertEquals(self.mock_shot.cut_out, self.mock_shot.cut_in)
        self.assertEquals(self.mock_shot.cut_duration, 1)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_out_argument_is_skipped_defaults_to_default_value(self):
        """testing if the cut_out argument is skipped the cut_out attribute
        will be set to the default value
        """
        
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop("cut_out")
        new_shot = Shot(**self.kwargs)
        self.assertEquals(new_shot.cut_out,
                          new_shot.cut_in + new_shot.cut_duration - 1)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_out_argument_is_set_to_None_defaults_to_default_value(self):
        """testing if the cut_out argument is set to None the cut_out attribute
        is set to default value
        """
        
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_out"] = None
        new_shot = Shot(**self.kwargs)
        self.assertEquals(new_shot.cut_out,
                          new_shot.cut_in + new_shot.cut_duration - 1)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_out_attribute_is_set_to_None_defaults_to_default_value(self):
        """testing if the cut_out attribute is set to None it is going to be
        set to default value
        """
        
        self.mock_shot.cut_out = None
        self.assertEquals(self.mock_shot.cut_out, self.mock_shot.cut_in +
                          self.mock_shot.cut_duration - 1)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_out_argument_is_not_integer(self):
        """testing if a ValueError will be raised when the cut_out argument is
        not an instance of int
        """
        
        self.kwargs["cut_out"] = "a string"
        self.assertRaises(ValueError, Shot, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_out_attribute_is_not_integer(self):
        """testing if a ValueError will be used when the cut_out attribute is
        not an instance of int
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_shot,
            "cut_out",
            "a string"
        )
    
    
    
    #----------------------------------------------------------------------
    def test_cut_out_argument_is_smaller_than_cut_in_argument(self):
        """testing if the cut_out attribute is updated when the cut_out
        argument is smaller than cut_in argument
        """
        
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_out"] = self.kwargs["cut_in"] - 10
        new_shot = Shot(**self.kwargs)
        self.assertEquals(new_shot.cut_out, new_shot.cut_in)
        self.assertEquals(new_shot.cut_duration, 1)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_out_attribute_is_smaller_than_cut_in_attribute(self):
        """testing if the cut_out attribute is updated when it is smaller than
        cut_in attribute
        """
        
        self.mock_shot.cut_out = self.mock_shot.cut_in - 10
        self.assertEquals(self.mock_shot.cut_out, self.mock_shot.cut_in)
        self.assertEquals(self.mock_shot.cut_duration, 1)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_duration_argument_is_skipped(self):
        """testing if the cut_duration attribute will be calculated from the
        cut_in and cut_out attributes when the cut_duration argument is skipped
        """
        
        self.kwargs["code"] = "SH123A"
        self.kwargs.pop("cut_duration")
        new_shot = Shot(**self.kwargs)
        self.assertEquals(new_shot.cut_duration, new_shot.cut_out -
                          new_shot.cut_in + 1)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_duration_argument_is_None(self):
        """testing if the value of cut_duration will be calculated from the
        cut_in and cut_out attributes.
        """
        
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = None
        new_shot = Shot(**self.kwargs)
        self.assertEquals(new_shot.cut_duration, new_shot.cut_out -
                          new_shot.cut_in + 1)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_duration_argument_is_not_instance_of_int(self):
        """testing if a ValueError will be raised when the cut_duration
        argument is not an instance of int
        """
        
        self.kwargs["cut_duration"] = "a string"
        self.assertRaises(ValueError, Shot, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_duration_attribute_is_not_instance_of_int(self):
        """testing if a ValueError will be raised when the cut_duration
        attribute is not an instance of int
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_shot,
            "cut_duration",
            "a string"
        )
    
    
    
    #----------------------------------------------------------------------
    def test_cut_duration_attribute_will_be_updated_when_cut_in_attribute_changed(self):
        """testing if the cut_duration attribute will be updated when the
        cut_in attribute changed
        """
        
        self.mock_shot.cut_in = 1
        self.assertEquals(self.mock_shot.cut_duration, self.mock_shot.cut_out -
                          self.mock_shot.cut_in + 1)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_duration_attribute_will_be_updated_when_cut_out_attribute_changed(self):
        """testing if the cut_duration attribute will be updated when the
        cut_out attribute changed
        """
        
        self.mock_shot.cut_out = 1000
        self.assertEquals(self.mock_shot.cut_duration, self.mock_shot.cut_out -
                          self.mock_shot.cut_in + 1)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_duration_attribute_changes_cut_out_attribute(self):
        """testing if changes in cut_duration attribute will also affect
        cut_out value.
        """
        
        first_cut_out = self.mock_shot.cut_out
        self.mock_shot.cut_in
        self.mock_shot.cut_duration = 245
        self.assertNotEquals(self.mock_shot.cut_out, first_cut_out)
        self.assertEquals(self.mock_shot.cut_out, self.mock_shot.cut_in +
                          self.mock_shot.cut_duration - 1)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_duration_attribute_is_zero(self):
        """testing if the cut_duration attribute will be set to 1 and the
        cut_out is updated to the same value with cut_in when the cut_duration
        attribute is set to zero
        """
        
        self.mock_shot.cut_duration = 0
        self.assertEquals(self.mock_shot.cut_out, self.mock_shot.cut_in)
        self.assertEquals(self.mock_shot.cut_duration, 1)
    
    
    
    
    #----------------------------------------------------------------------
    def test_cut_duration_attribute_is_negative(self):
        """testing if the cut_duration attribute will be set to 1  and the
        cut_out is updated to the same value with cut_in when the cut_duration
        attribute is set to a negative value
        """
        
        self.mock_shot.cut_duration = -100
        self.assertEquals(self.mock_shot.cut_out, self.mock_shot.cut_in)
        self.assertEquals(self.mock_shot.cut_duration, 1)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_duration_argument_is_zero_and_cut_out_argument_is_skipped(self):
        """testing if the cut_duration attribute will be set to 1 and the
        cut_out is updated to the same value with cut_in when the cut_duration
        argument is zero and there is no cut_out argument given
        """
        
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = 0
        self.kwargs.pop("cut_out")
        new_shot = Shot(**self.kwargs)
        self.assertEquals(new_shot.cut_duration, 1)
        self.assertEquals(new_shot.cut_out, new_shot.cut_in)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_duration_argument_is_negative_and_cut_out_argument_is_skipped(self):
        """testing if the cut_duration attribute is going to be set to 1 and
        the cut_out will be updated to the same value with the cut_in attribute
        when the cut_duration argument is given as zero and the cut_out
        argument is skipped
        """
        
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = -10
        self.kwargs.pop("cut_out")
        new_shot = Shot(**self.kwargs)
        self.assertEquals(new_shot.cut_duration, 1)
        self.assertEquals(new_shot.cut_out, new_shot.cut_in)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_duration_argument_is_zero_and_cut_out_argument_is_not_None(self):
        """testing if the cut_duration attribute is going to be set to 1 and
        cut_output will be calculated from cut_in and cut_duration when the
        cut_duration argument is given as zero and there is a cut_out argument
        given
        """
        
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = 0
        new_shot = Shot(**self.kwargs)
        self.assertEquals(new_shot.cut_duration, 1)
        self.assertEquals(new_shot.cut_out, new_shot.cut_in)
    
    
    
    #----------------------------------------------------------------------
    def test_cut_duration_argument_is_negative_and_cut_out_argument_is_not_None(self):
        """testing if the cut_duration attribute is going to be set to 1 and
        cut_output will be calculated from cut_in and cut_duration when the
        cut_duration argument is given as negative and there is a cut_out
        argument given
        """
        
        self.kwargs["code"] = "SH123A"
        self.kwargs["cut_duration"] = -100
        new_shot = Shot(**self.kwargs)
        self.assertEquals(new_shot.cut_duration, 1)
        self.assertEquals(new_shot.cut_out, new_shot.cut_in)
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing equality of shot objects
        """
        
        self.kwargs["code"] = "SH123A"
        new_shot1 = Shot(**self.kwargs)
        
        self.kwargs["sequence"] = self.mock_sequence3
        new_shot2 = Shot(**self.kwargs)
        # an entity with the same parameters
        # just set the name to the code too
        self.kwargs["name"] = self.kwargs["code"]
        new_entity = Entity(**self.kwargs)
        
        # another shot with different code
        self.kwargs["code"] = "SHOnetherShot"
        new_shot3 = Shot(**self.kwargs)
        
        self.assertFalse(new_shot1==new_shot2)
        self.assertFalse(new_shot1==new_entity)
        self.assertFalse(new_shot1==new_shot3)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing inequality of shot objects
        """
        
        self.kwargs["code"] = "SH123A"
        new_shot1 = Shot(**self.kwargs)
        
        self.kwargs["sequence"] = self.mock_sequence3
        new_shot2 = Shot(**self.kwargs)
        # an entity with the same parameters
        # just set the name to the code too
        self.kwargs["name"] = self.kwargs["code"]
        new_entity = Entity(**self.kwargs)
        
        # another shot with different code
        self.kwargs["code"] = "SHOnetherShot"
        new_shot3 = Shot(**self.kwargs)
        
        self.assertTrue(new_shot1!=new_shot2)
        self.assertTrue(new_shot1!=new_entity)
        self.assertTrue(new_shot1!=new_shot3)

    
    