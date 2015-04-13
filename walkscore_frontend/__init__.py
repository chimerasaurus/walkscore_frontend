"""
Walkscore frontend to interact with the Walkscore website without using the
limited API. Returns data about cities and neighborhoods from Walkscore.
"""

__author__ = 'James Malone'
__license__ = "MIT"
__version__ = "0.3"
__maintainer__ = "James Malone"
__email__ = 'jamalone at gmail dot com'
__status__ = "Development"

# Packages needed for this module
from walkscore_frontend.http import *
from walkscore_frontend.regex import *
from walkscore_frontend.utils import *
from walkscore_frontend.wslocation import City
from walkscore_frontend.wslocation import Neighborhood

attributes_to_remove = ['walkscore','path', 'key', 'thumb', 'page', 'title', 'slug']

def get_city(city, state):
    """
    Return a City object with data for this city.
    
    :param city: Name of the city (such as `Seattle`)
    :param state: Two-letter code of the state (such as `WA`)
    :returns: City object with data about the specified city
    :rtype: City
    """
    city_data = data_for_city(city, state)
    return City(city_data)

def get_neighborhood(neighborhood, city, state):
    """
    Return a Neighborhood object with data for this neighborhood.
    
    :param neighborhood: Nane of the neighborhood (such as `Denny Triangle`)
    :param city: Name of the city (such as `Seattle`)
    :param state: Two-letter code of the state (such as `WA`)
    :returns: Neighborhood object with data about the specified neighborhood
    :rtype: Neighborhood
    """
    nh_data = data_for_neighborhood(neighborhood, city, state)
    return Neighborhood(nh_data)


def data_for_city(city, state):
    """
    Get the Walkscore data for the given city.
    
    :param city: Name of the city (such as `Seattle`)
    :param state: Two-letter code of the state (such as `WA`)
    :returns: Walkscore data about the specified neighborhood
    :rtype: dict
    """
    # Basic details on the city
    city_basics = {'name': city, 'state': state}

    # Get most of the data from WS
    try:
        city_url = walkscore_city_url(city, state)
        ws_data = get_page_data(city_url)
        base_city_data = parse_data_points(ws_data)

        # Get JSON data for things like lat and long
        city_json_url = walkscore_city_url(city, state, True)
        json_city_data = get_json_data(city_json_url)
    except:
        return None

    # Merge the hashes
    city_data = merge_dicts(base_city_data, json_city_data, city_basics)
    city_data = remove_unneeded_elements(city_data, attributes_to_remove)

    return city_data


def data_for_neighborhood(neighborhood, city, state):
    """
    Get the Walkscore data for the given neighborhood.
    
    :param neighborhood: Nane of the neighborhood (such as `Denny Triangle`)
    :param city: Name of the city (such as `Seattle`)
    :param state: Two-letter code of the state (such as `WA`)
    :returns: Walkscore data about the specified neighborhood
    :rtype: dict
    """
    # Basic details for the neighborhood
    neighborhood_basics = {'name': neighborhood, 'city': city, 'state': state}
    
    try:
        # Get most of the data from WS
        nh_url = walkscore_neighborhood_url(neighborhood, city, state)
        ws_data = get_page_data(nh_url)
        neighborhood_base_data = parse_data_points(ws_data)

        # Get JSON data from WS for things like lat and long
        nh_json_data = walkscore_neighborhood_url(neighborhood, city, state, True)
        nh_json_data = get_json_data(nh_json_data)
    except:
        return None

    # Merge the hashes
    neighborhood_data = merge_dicts(neighborhood_basics, neighborhood_base_data, nh_json_data)
    neighborhood_data = remove_unneeded_elements(neighborhood_data, attributes_to_remove)

    return neighborhood_data