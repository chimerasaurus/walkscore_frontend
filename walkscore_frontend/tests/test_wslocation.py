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
from walkscore_frontend.wslocation import City
from walkscore_frontend.wslocation import Neighborhood
from walkscore_frontend.wslocation import WsLocation

class TestWsLocation(unittest.TestCase):
    """Class to test WsLocation"""

    def setUp(self):
        """
        Setup the unit tests
        :return: Items needed for unit testing
        """
        self.simple_city_test_payload = {'name': 'Seattle', 'state': 'WA'}
        self.simple_nh_test_payload = {'name': 'Denny Triangle', 'city': 'Seattle', 'state': 'WA'}

    def test_simple_creation(self):
        """
        Test the creation of a simple WsLocation
        :return: OK if all unit tests pass
        """
        ws_loc = WsLocation(self.simple_city_test_payload)
        self.assertTrue(ws_loc is not None)
        self.assertTrue(ws_loc.name == 'Seattle')
        self.assertTrue(ws_loc.state == 'WA')
        self.assertRaises(AttributeError, getattr, ws_loc, "bad_attribute")
        
    def test_city_creation(self):
        """
        Test the creation of a simple test_city_creation
        :return: Pass if the city is created OK
        """
        city = City(self.simple_city_test_payload)
        self.assertTrue(city is not None)
        self.assertTrue(city.name == 'Seattle')
        self.assertTrue(city.state == 'WA')
        self.assertRaises(AttributeError, getattr, city, "bad_attribute")

    def test_nh_creation(self):
        """
        Test the creation of a simple test_city_creation
        :return: Pass if the city is created OK
        """
        nh = Neighborhood(self.simple_nh_test_payload)
        self.assertTrue(nh is not None)
        self.assertTrue(nh.name == 'Denny Triangle')
        self.assertTrue(nh.city == 'Seattle')
        self.assertTrue(nh.state == 'WA')
        self.assertRaises(AttributeError, getattr, nh, "bad_attribute")

if __name__ == '__main__':
    unittest.main()