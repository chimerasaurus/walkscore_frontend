"""
This is a module to unit test the walkscoreapi Python library.
"""

__author__ = 'James Malone'
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "James Malone"
__email__ = 'jamalone at gmail dot com'
__status__ = "Development"

import walkscore_frontend
import unittest


class TestWalkscoreFrontend(unittest.TestCase):

    def setUp(self):
        pass

    def test_data_for_city(self):
        """
        Test the data_for_city method.
        :return: Pass if the method is working properly
        """
        # Input params
        city = 'Seattle'
        state = 'WA'
        city_data = walkscore_frontend.data_for_city(city, state)

        # Validate the hash is not null
        self.assertTrue(city_data is not None)

        # Validate the basic city data looks valid
        self.assertEqual(city_data['name'], city)
        self.assertEqual(city_data['state'], state)
        self.assertIn(city_data['walk_score'], range(1, 100))
        self.assertIn(city_data['bike_score'], range(1, 100))
        self.assertIn(city_data['transit_score'], range(1, 100))
        self.assertIn(len(city_data['neighborhoods']), range(90, 120))
        self.assertGreater(city_data['population'], 600000)
        self.assertIn(city_data['restaurant_average'], range(1, 4))
        self.assertIn(city_data['restaurants'], range(2000, 5000))

        # Validate the JSON data
        self.assertEqual(city_data['lat'], 47.6202)
        self.assertEqual(city_data['lng'], -122.351)
        self.assertGreaterEqual(city_data['date'], 1423966612)


    def test_data_for_neighborhood(self):
        """
        Test the data_for_neighborhood method.
        :return: Pass if the method is working properly
        """
        # Input params
        city = 'Seattle'
        state = 'WA'
        neighborhood = 'Denny Triangle'

        # Get the data
        neighborhood_data = walkscore_frontend.data_for_neighborhood(neighborhood, city, state)

        # Validate the hash is not null
        self.assertTrue(neighborhood_data is not None)

        # Validate the basic neighborhood data looks valid
        self.assertEqual(neighborhood_data['name'], neighborhood)
        self.assertEqual(neighborhood_data['city'], city)
        self.assertEqual(neighborhood_data['state'], state)
        self.assertIn(neighborhood_data['walk_score'], range(1, 101))
        self.assertIn(neighborhood_data['bike_score'], range(1, 101))
        self.assertIn(neighborhood_data['transit_score'], range(1, 101))
        self.assertGreater(neighborhood_data['population'], 3000)
        self.assertIn(neighborhood_data['restaurant_average'], range(20, 50))
        self.assertIn(neighborhood_data['restaurants'], range(200, 500))

        # Validate JSON data
        self.assertEqual(neighborhood_data['lat'], 47.6165)
        self.assertEqual(neighborhood_data['lng'], -122.337)
        self.assertGreaterEqual(neighborhood_data['date'], 1423966838)

class TestCity(unittest.TestCase):

    def test_city_creation(self):
        city_data = walkscore_frontend.data_for_city('Seattle', 'WA')
        c = walkscore_frontend.City(city_data)

        # Validate the basic city data
        self.assertEqual(c.name, 'Seattle')

if __name__ == '__main__':
    unittest.main()