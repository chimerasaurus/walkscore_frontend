"""
Walkscore frontend to interact with the Walkscore website without using the
limited API. Returns data about cities and neighborhoods from Walkscore.
"""

__author__ = 'James Malone'
__license__ = "MIT"
__version__ = "0.2"
__maintainer__ = "James Malone"
__email__ = 'jamalone at gmail dot com'
__status__ = "Development"

# Packages needed for this module
from walkscore_frontend.http import *
from walkscore_frontend.regex import *
from walkscore_frontend.utils import *
from walkscore_frontend.wslocation import City
from walkscore_frontend.wslocation import Neighborhood

base_city_url = 'https://www.walkscore.com/%s/%s'
base_neighborhood_url = 'https://www.walkscore.com/%s/%s/%s'
base_json_data_city_url = 'https://www.walkscore.com/auth/_pv/city_page/%s/%s?d=current'
base_json_data_neighborhood_url = 'https://www.walkscore.com/auth/_pv/city_page/%s/%s/%s?d=current'
regex_filters = {
    'int':
        {
            'walk_score': '\/\/pp.walk.sc\/badge\/walk\/score\/(\d+)\.svg',
            'transit_score': '\/\/pp.walk.sc\/badge\/transit\/score\/(\d+)\.svg',
            'bike_score': '\/\/pp.walk.sc\/badge\/bike\/score\/(\d+)\.svg',
            'population': 'with\s+(\S+)\s+residents',
            'restaurants': 'about\s+(\S+)\s+restaurants'
        },
    'float':
        {
            'restaurant_average': 'average\s+of\s+(\S+)\s+restaurants',
        },
    'table':
        {
            'neighborhoods': 'id=hoods-list-table',
        },
}
attributes_to_remove = ['walkscore','path', 'key', 'thumb', 'page', 'title', 'slug']

def get_city(name, state):
    """
    Return a City object with data for this city.
    
    :param name: Name of the city (such as `Seattle`)
    :param content: Two-letter code of the state (such as `WA`)
    :returns: City object with data about the specified city
    :rtype: City
    """
    city_data = data_for_city(name, state)
    return City(city_data)

def get_neighborhood(name, city, state):
    """
    Return a Neighborhood object with data for this neighborhood.
    
    :param name: Nane of the neighborhood (such as `Denny Triangle`)
    :param city: Name of the city (such as `Seattle`)
    :param content: Two-letter code of the state (such as `WA`)
    :returns: Neighborhood object with data about the specified city
    :rtype: Neighborhood
    """
    nh_data = data_for_neighborhood(name, city, state)
    return Neighborhood(nh_data)

def data_for_neighborhood(name, city, state):
    """Get the Walkscore data for the given neighborhood."""
    # Basic details for the neighborhood
    neighborhood_basics = {'name': name, 'city': city, 'state': state}
    
    try:
        # Get most of the data from WS
        nh_url = walkscore_neighborhood_url(name, city, state)
        ws_data = get_page_data(nh_url)
        neighborhood_base_data = parse_data_points(ws_data)

        # Get JSON data from WS for things like lat and long
        nh_json_data = walkscore_neighborhood_url(name, city, state, True)
        nh_json_data = get_json_data(nh_json_data)
    except:
        return None

    # Merge the hashes
    neighborhood_data = merge_dicts(neighborhood_basics, neighborhood_base_data, nh_json_data)
    neighborhood_data = remove_unneeded_elements(neighborhood_data, attributes_to_remove)

    return neighborhood_data


def data_for_city(name, state):
    """Get the Walkscore data for the given city."""
    # Basic details on the city
    city_basics = {'name': name, 'state': state}

    # Get most of the data from WS
    try:
        city_url = walkscore_city_url(name, state)
        ws_data = get_page_data(city_url)
        base_city_data = parse_data_points(ws_data)

        # Get JSON data for things like lat and long
        city_json_url = walkscore_city_url(name, state, True)
        json_city_data = get_json_data(city_json_url)
    except:
        return None

    # Merge the hashes
    city_data = merge_dicts(base_city_data, json_city_data, city_basics)
    city_data = remove_unneeded_elements(city_data, attributes_to_remove)

    return city_data

def parse_data_points(html):
    """Parse the page data and look for expected contents based on regular expressions."""
    parsed_data = {}
    for data_type in regex_filters.keys():
        if data_type == 'int':
            for data_attribute in regex_filters[data_type].keys():
                value = regex_page_data_int(regex_filters[data_type][data_attribute], html)
                parsed_data[data_attribute] = value
        elif data_type == 'float':
            for data_attribute in regex_filters[data_type].keys():
                value = regex_page_data_float(regex_filters[data_type][data_attribute], html)
                parsed_data[data_attribute] = value
        elif data_type == 'table':
            for data_attribute in regex_filters[data_type].keys():
                value = regex_page_data_table(regex_filters[data_type][data_attribute], html)
                parsed_data[data_attribute] = value
    return parsed_data

def walkscore_city_url(city, state, json=False):
    """Return a well-formatted Walkscore URL for cities."""
    if json == False:
        url_to_call = base_city_url
    else:
        url_to_call = base_json_data_city_url

    return url_to_call % (state, city.replace(' ', '_'))


def walkscore_neighborhood_url(name, city, state, json=False):
    """Return a well-formatted Walkscore URL for neighborhoods."""
    if json == False:
        url_to_call = base_neighborhood_url
    else:
        url_to_call = base_json_data_neighborhood_url

    name = name.replace('/', '.slash.')

    return url_to_call % (state, city.replace(' ', '_'), name.replace(' ', '_'))