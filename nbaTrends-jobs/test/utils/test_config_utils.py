#!/usr/bin/env python
"""Test Cases for Configuration Utils"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"
__email__ = "jordanalphonso1@yahoo.com"

from src.utils import config_utils

import os
import unittest

config_file_path = os.path.dirname(os.path.realpath(__file__)) + '/../resources/config_test.ini'


class ConfUtilsTests(unittest.TestCase):
    """Test Cases that validate the config_utils functions"""

    def setUp(self):
        """Reset Conf Utils file path to point to test resources config"""
        config_utils.conf.read(config_file_path)
        config_utils._init_conf()

    def test_get_string_item(self):
        """Test Conf utils function that returns a str value"""
        mstr = config_utils.get_config_string('spark_master', 'Spark')
        self.assertEquals('spark://fake-master:7077', mstr, 'spark_master does not match: %s' % mstr)
        self.assertTrue(isinstance(mstr, str), 'spark_master value is not a str')

    def test_get_int_item(self):
        """Test Conf utils function that returns a int value"""
        intV = config_utils.get_config_int('fake_int', 'Test')
        self.assertEquals(2, intV, 'fake_int value does not match: %i' % intV)
        self.assertTrue(isinstance(intV, int), 'fake_int value is not an int')

    def test_get_float_item(self):
        """Test Conf utils function that returns a float value"""
        flV = config_utils.get_config_float('fake_float', 'Test')
        self.assertEquals(2.10395, flV, 'fake_float value does not match: %d' % flV)
        self.assertTrue(isinstance(flV, float), 'fake_int value is not a float')

    def test_get_bool_item(self):
        """Test Conf utils function that returns a bool value"""
        boolV = config_utils.get_config_bool('fake_bool', 'Test')
        self.assertEquals(True, boolV, 'fake_bool value does not match: %s' % boolV)
        self.assertTrue(isinstance(boolV, bool), 'fake_bool value is not a bool')

    def test_get_item_without_section(self):
        """Test Conf utils function that item without section"""
        secV = config_utils.get_config_item('spark_master')
        self.assertEquals('spark://fake-master:7077', secV, 'spark_master value does not match: %s' % secV)
        self.assertTrue(isinstance(secV, str), 'spark_master value is not a str')

    def test_no_match_item(self):
        """Test Conf utils function with no match"""
        nnV = config_utils.get_config_float('non_exist', 'Spark')
        self.assertEquals(None, nnV, 'nnV value should be None')

    def test_no_match_item_without_section(self):
        """Test Conf utils function with no match"""
        nnV = config_utils.get_config_float('non_exist')
        self.assertEquals(None, nnV, 'nnV value should be None')


if __name__ == "__main__":
    unittest.main()
