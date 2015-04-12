"""
Unit tests for the utils module.
"""
__author__ = 'James Malone'
__license__ = "MIT"
__version__ = "0.2"
__maintainer__ = "James Malone"
__email__ = 'jamalone at gmail dot com'
__status__ = "Development"


# Imports
import unittest
from walkscore_frontend.utils import *

class TestUtils(unittest.TestCase):
    """Class to test utils"""

    def setUp(self):
        """
        Setup the unit tests
        :return: Items needed for unit testing
        """
        self.test_dict_1 = {'a': 1, 'b': '2'}
        self.test_dict_2 = {'c': '3', 'd': '4'}
        self.test_dict_3 = {'a': 1, 'b': True, 'c': '3', 'd': "False"}

    def test_merge_dicts(self):
        """
        Test the merging of two dictionaries
        :return: Pass if the dicts are merged OK
        """
        merged_dict = merge_dicts(self.test_dict_1, self.test_dict_2)
        self.assertEqual(4, len(merged_dict.keys()))
        self.assertEqual(1, merged_dict['a'])
        self.assertEqual('4', merged_dict['d'])
        
    def test_remove_unneeded_elements(self):
        """
        Test the remove_unneeded_elements method to clean a dict
        :return: Pass if the method cleans the dict properly
        """
        elements_to_remove = ['a', 'c']
        clean_dict = remove_unneeded_elements(self.test_dict_3, elements_to_remove)
        self.assertEqual(2, len(clean_dict.keys()))
        self.assertEqual(True, clean_dict['b'])
        self.assertEqual('False', clean_dict['d'])
        

if __name__ == '__main__':
    unittest.main()