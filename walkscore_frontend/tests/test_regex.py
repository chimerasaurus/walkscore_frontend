"""
Unit tests for the regex module.
"""

# Imports
import unittest
from walkscore_frontend.regex import *

class TestRegex(unittest.TestCase):
    """Class to test regex"""

    def setUp(self):
        """
        Setup the unit tests
        
        :return: Items needed for unit testing
        """
        self.pattern = '\D*(\d*)\D+'
        self.bogus_pattern = '\s+'
        self.content = 'test1234-test'

    def test_regex_page_data(self):
        """
        Test a positive and negative match of regex data
        
        :return: Pass if the method works and fails properly
        """
        # Test valid regex and content
        result_data = regex_page_data(self.pattern, self.content)
        self.assertEqual('1234', result_data)
        
        # Test a bogus regex
        bad_json_data = regex_page_data(self.bogus_pattern, self.content)
        self.assertEqual(bad_json_data, None)
        