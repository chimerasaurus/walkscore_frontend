"""
Unit tests for the http module.
"""

# Imports
import unittest
from walkscore_frontend.http import *

class TestHttp(unittest.TestCase):
    """Class to test http"""

    def setUp(self):
        """
        Setup the unit tests
        :return: Items needed for unit testing
        """
        self.good_url = 'http://www.walkscore.com/WA/Seattle'
        self.bad_url = 'https://www.walkscore.com/fdfadsfdfdsfdas'
        self.good_json_url = 'https://www.walkscore.com/auth/_pv/city_page/WA/Seattle?d=current'
        self.bad_json_url = 'https://www.walkscore.com/basjsonurl'

    def test_get_page_datas(self):
        """
        Test URLs to ensure they work with good URLs and fail with bad URLs.
        
        :return: Pass if URLs are handled properly
        """
        # Test a valid URL
        self.assertTrue(get_page_data(self.good_url) is not None)
        self.assertTrue(get_json_data(self.good_json_url) is not None)
        
        # Test a bogus URL
        with self.assertRaises(Exception):
            get_page_data(self.bad_url)
            get_json_data(self.bad_json_url)