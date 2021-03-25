# -*- coding: utf-8 -*-

import unittest
import pytest

from stalker.models.budget import Good


class GoodTestCase(unittest.TestCase):
    """tests the stalker.models.budget.Good class
    """

    def setUp(self):
        """set up the test
        """
        super(GoodTestCase, self).setUp()
        self.kwargs = {
            'name': 'Comp',
            'cost': 10,
            'msrp': 12,
            'unit': 'TL/hour'
        }

    def test_cost_argument_is_skipped(self):
        """testing if the cost attribute value will be 0.0 if the cost argument
        is skipped
        """
        self.kwargs.pop('cost')
        g = Good(**self.kwargs)
        assert g.cost == 0

    def test_cost_argument_is_None(self):
        """testing if the cost attribute value will be 0.0 if the cost argument
        is None
        """
        self.kwargs['cost'] = None
        g = Good(**self.kwargs)
        assert g.cost == 0

    def test_cost_attribute_is_None(self):
        """testing if the cost attribute will be 0.0 if it is set to None
        """
        g = Good(**self.kwargs)
        assert g.cost != 0
        g.cost = None
        assert g.cost == 0

    def test_cost_argument_is_not_a_number(self):
        """testing if a TypeError will be raised if cost argument is not a
        number
        """
        self.kwargs['cost'] = 'not a number'
        with pytest.raises(TypeError) as cm:
            g = Good(**self.kwargs)

        assert str(cm.value) == \
            'Good.cost should be a non-negative number, not str'

    def test_cost_attribute_is_not_a_number(self):
        """testing if a TypeError will be raised if the cost attribute is set
        to something other than a number
        """
        g = Good(**self.kwargs)
        with pytest.raises(TypeError) as cm:
            g.cost = 'not a number'

        assert str(cm.value) == \
            'Good.cost should be a non-negative number, not str'

    def test_cost_argument_is_zero(self):
        """testing if it is totally ok to set the cost to 0
        """
        self.kwargs['cost'] = 0
        g = Good(**self.kwargs)
        assert g.cost == 0.0

    def test_cost_attribute_is_zero(self):
        """testing if it is totally ok to test the cost attribute to 0
        """
        g = Good(**self.kwargs)
        assert g.cost != 0.0
        g.cost = 0.0
        assert g.cost == 0.0

    def test_cost_argument_is_negative(self):
        """testing if a ValueError will be raised if the cost argument is a
        negative number
        """
        self.kwargs['cost'] = -10
        with pytest.raises(ValueError) as cm:
            g = Good(**self.kwargs)

        assert str(cm.value) == 'Good.cost should be a non-negative number'

    def test_cost_attribute_is_negative(self):
        """testing if ValueError will be raised if the cost attribute is set to
        a negative number
        """
        g = Good(**self.kwargs)
        with pytest.raises(ValueError) as cm:
            g.cost = -10

        assert str(cm.value) == 'Good.cost should be a non-negative number'

    def test_cost_argument_is_working_properly(self):
        """testing if the cost argument value is properly passed to the cost
        attribute
        """
        test_value = 113
        self.kwargs['cost'] = test_value
        g = Good(**self.kwargs)
        assert g.cost == test_value

    def test_cost_attribute_is_working_properly(self):
        """testing if the cost attribute value can be properly changed
        """
        test_value = 145
        g = Good(**self.kwargs)
        assert g.cost != test_value

        g.cost = test_value
        assert g.cost == test_value

    def test_msrp_argument_is_skipped(self):
        """testing if the msrp attribute value will be 0.0 if the msrp argument
        is skipped
        """
        self.kwargs.pop('msrp')
        g = Good(**self.kwargs)
        assert g.msrp == 0

    def test_msrp_argument_is_None(self):
        """testing if the msrp attribute value will be 0.0 if the msrp argument
        is None
        """
        self.kwargs['msrp'] = None
        g = Good(**self.kwargs)
        assert g.msrp == 0

    def test_msrp_attribute_is_None(self):
        """testing if the msrp attribute will be 0.0 if it is set to None
        """
        g = Good(**self.kwargs)
        assert g.msrp != 0
        g.msrp = None
        assert g.msrp == 0

    def test_msrp_argument_is_not_a_number(self):
        """testing if a TypeError will be raised if msrp argument is not a
        number
        """
        self.kwargs['msrp'] = 'not a number'
        with pytest.raises(TypeError) as cm:
            g = Good(**self.kwargs)

        assert str(cm.value) == \
            'Good.msrp should be a non-negative number, not str'

    def test_msrp_attribute_is_not_a_number(self):
        """testing if a TypeError will be raised if the msrp attribute is set
        to something other than a number
        """
        g = Good(**self.kwargs)
        with pytest.raises(TypeError) as cm:
            g.msrp = 'not a number'

        assert str(cm.value) == \
            'Good.msrp should be a non-negative number, not str'

    def test_msrp_argument_is_zero(self):
        """testing if it is totally ok to set the msrp to 0
        """
        self.kwargs['msrp'] = 0
        g = Good(**self.kwargs)
        assert g.msrp == 0.0

    def test_msrp_attribute_is_zero(self):
        """testing if it is totally ok to test the msrp attribute to 0
        """
        g = Good(**self.kwargs)
        assert g.msrp != 0.0
        g.msrp = 0.0
        assert g.msrp == 0.0

    def test_msrp_argument_is_negative(self):
        """testing if a ValueError will be raised if the msrp argument is a
        negative number
        """
        self.kwargs['msrp'] = -10
        with pytest.raises(ValueError) as cm:
            g = Good(**self.kwargs)

        assert str(cm.value) == \
            'Good.msrp should be a non-negative number'

    def test_msrp_attribute_is_negative(self):
        """testing if ValueError will be raised if the msrp attribute is set to
        a negative number
        """
        g = Good(**self.kwargs)
        with pytest.raises(ValueError) as cm:
            g.msrp = -10

        assert str(cm.value) == \
            'Good.msrp should be a non-negative number'

    def test_msrp_argument_is_working_properly(self):
        """testing if the msrp argument value is properly passed to the msrp
        attribute
        """
        test_value = 113
        self.kwargs['msrp'] = test_value
        g = Good(**self.kwargs)
        assert g.msrp == test_value

    def test_msrp_attribute_is_working_properly(self):
        """testing if the msrp attribute value can be properly changed
        """
        test_value = 145
        g = Good(**self.kwargs)
        assert g.msrp != test_value

        g.msrp = test_value
        assert g.msrp == test_value

    def test_unit_argument_is_skipped(self):
        """testing if the unit attribute will be an empty string if the unit
        argument is skipped
        """
        self.kwargs.pop('unit')
        g = Good(**self.kwargs)
        assert g.unit == ''

    def test_unit_argument_is_None(self):
        """testing if the unit attribute will be an empty string if the unit
        argument is None
        """
        self.kwargs['unit'] = None
        g = Good(**self.kwargs)
        assert g.unit == ''

    def test_unit_attribute_is_set_to_None(self):
        """testing if the unit attribute will be an empty string if it is set
        to None
        """
        g = Good(**self.kwargs)
        assert g.unit != ''
        g.unit = None
        assert g.unit == ''

    def test_unit_argument_is_not_a_string(self):
        """testing if a TypeError will be raised if the unit argument is not a
        string
        """
        self.kwargs['unit'] = 12312
        with pytest.raises(TypeError) as cm:
            g = Good(**self.kwargs)

        assert str(cm.value) == \
            'Good.unit should be a string, not int'

    def test_unit_attribute_is_not_a_string(self):
        """testing if a TypeError will be raised if the unit attribute is set
        to a value which is not a string
        """
        g = Good(**self.kwargs)
        with pytest.raises(TypeError) as cm:
            g.unit = 2342

        assert str(cm.value) == \
            'Good.unit should be a string, not int'

    def test_unit_argument_is_working_properly(self):
        """testing if the unit argument value is properly passed to the unit
        attribute
        """
        test_value = 'this is my unit'
        self.kwargs['unit'] = test_value
        g = Good(**self.kwargs)
        assert g.unit == test_value

    def test_unit_attribute_is_working_properly(self):
        """testing if the unit attribute value can be changed properly
        """
        test_value = 'this is my unit'
        g = Good(**self.kwargs)
        assert g.unit != test_value
        g.unit = test_value
        assert g.unit == test_value

    def test_client_argument_is_skipped(self):
        """testing if a Good can be created without a Client
        """
        self.kwargs.pop('client', None)
        g = Good(**self.kwargs)
        assert g is not None
        assert isinstance(g, Good)

    def test_client_argument_is_none(self):
        """testing if a Good can be created without a Client
        """
        self.kwargs['client'] = None
        g = Good(**self.kwargs)
        assert g is not None
        assert isinstance(g, Good)

    def test_client_argument_is_not_a_client_instance(self):
        """testing if a TypeError will be raised if the client argument is not
        a Client instance
        """
        self.kwargs['client'] = 'not a client'
        with pytest.raises(TypeError) as cm:
            Good(**self.kwargs)

        assert str(cm.value) == \
            'Good.client attribute should be a stalker.models.client.Client ' \
            'instance, not str'

    def test_client_attribute_is_set_to_a_value_other_than_a_client(self):
        """testing if a TypeError will be raised when the client attribute is
        set to a value other than a Client instance
        """
        g = Good(**self.kwargs)
        with pytest.raises(TypeError) as cm:
            g.client = 'not a client'

        assert str(cm.value) == \
            'Good.client attribute should be a stalker.models.client.Client ' \
            'instance, not str'

    def test_client_argument_is_working_properly(self):
        """testing if the client argument is working properly
        """
        from stalker.models.client import Client
        client = Client(name='Test Client')
        self.kwargs['client'] = client
        g = Good(**self.kwargs)
        assert g.client == client

    def test_client_attribute_is_working_properly(self):
        """testing if the client attribute is working properly
        """
        from stalker.models.client import Client
        client = Client(name='Test Client')
        g = Good(**self.kwargs)
        assert g.client != client
        g.client = client
        assert g.client == client
