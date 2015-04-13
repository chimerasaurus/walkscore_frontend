"""
This is a module to unit test the walkscoreapi Python library.
"""

__author__ = 'James Malone'
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "James Malone"
__email__ = 'jamalone at gmail dot com'
__status__ = "Development"

import unittest
from walkscore_frontend import *
from walkscore_frontend import frontend
from walkscore_frontend import wslocation

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
        city_data = data_for_city(city, state)

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
        neighborhood_data = data_for_neighborhood(neighborhood, city, state)

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
        
        
    def test_city(self):
        """
        Test the city method.
        :return: Pass if a City object is created with valid data
        """
        # Input params
        city = 'Seattle'
        state = 'WA'
        
        # Get the City
        seattle = get_city(city, state)
        
        # Valide a City object is returned
        assert isinstance(seattle, wslocation.City)
        
        # Validate the basic city data looks valid
        self.assertEqual(seattle.name, city)
        self.assertEqual(seattle.state, state)
        self.assertIn(seattle.walk_score, range(1, 100))
        self.assertIn(seattle.bike_score, range(1, 100))
        self.assertIn(seattle.transit_score, range(1, 100))
        self.assertIn(len(seattle.neighborhoods), range(90, 120))
        self.assertGreater(seattle.population, 600000)
        self.assertIn(seattle.restaurant_average, range(1, 4))
        self.assertIn(seattle.restaurants, range(2000, 5000))

        # Validate the JSON data
        self.assertEqual(seattle.lat, 47.6202)
        self.assertEqual(seattle.lng, -122.351)
        self.assertGreaterEqual(seattle.date, 1423966612)
        
    
    def test_neighborhood(self):
        """
        Test the neighborhood method.
        :return: Pass if the method is working properly
        """
        # Input params
        city = 'Seattle'
        state = 'WA'
        neighborhood = 'Denny Triangle'

        # Get the data
        denny_tri = get_neighborhood(neighborhood, city, state)

        # Valide a City object is returned
        assert isinstance(denny_tri, wslocation.Neighborhood)

        # Validate the basic neighborhood data looks valid
        self.assertEqual(denny_tri.name, neighborhood)
        self.assertEqual(denny_tri.city, city)
        self.assertEqual(denny_tri.state, state)
        self.assertIn(denny_tri.walk_score, range(1, 101))
        self.assertIn(denny_tri.bike_score, range(1, 101))
        self.assertIn(denny_tri.transit_score, range(1, 101))
        self.assertGreater(denny_tri.population, 3000)
        self.assertIn(denny_tri.restaurant_average, range(20, 50))
        self.assertIn(denny_tri.restaurants, range(200, 500))

        # Validate JSON data
        self.assertEqual(denny_tri.lat, 47.6165)
        self.assertEqual(denny_tri.lng, -122.337)
        self.assertGreaterEqual(denny_tri.date, 1423966838)

if __name__ == '__main__':
    unittest.main()