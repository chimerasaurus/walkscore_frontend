"""
Unit tests for the WsLocation class.
"""
__author__ = 'James Malone'
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "James Malone"
__email__ = 'jamalone at gmail dot com'
__status__ = "Development"


# Imports
import unittest
from walkscore_frontend.wslocation import WsLocation

class TestWsLocation(unittest.TestCase):
    """Class to test WsLocation"""

    def setUp(self):
        """
        Setup the unit tests
        :return: Items needed for unit testing
        """
        self.simple_test_payload = {'name': 'Seattle', 'state': 'WA'}

    def test_simple_creation(self):
        """
        Test the creation of a simple WsLocation
        :return: OK if all unit tests pass
        """
        ws_loc = WsLocation(self.simple_test_payload)
        self.assertTrue(ws_loc is not None)
        self.assertTrue(ws_loc.name == 'Seattle')
        self.assertTrue(ws_loc.state == 'WA')
        self.assertRaises(AttributeError, getattr, ws_loc, "bad_attribute")


if __name__ == '__main__':
    unittest.main()