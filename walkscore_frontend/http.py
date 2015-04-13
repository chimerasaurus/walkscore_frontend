"""
Performs HTTP work for the frontend. Uses the Requests library to communicate
via HTTP to WalkScore.
"""

# Imports for this module
import json
import requests

# Constants for this module
base_city_url = 'https://www.walkscore.com/%s/%s'
base_json_data_city_url = 'https://www.walkscore.com/auth/_pv/city_page/%s/%s?d=current'
base_neighborhood_url = 'https://www.walkscore.com/%s/%s/%s'
base_json_data_neighborhood_url = 'https://www.walkscore.com/auth/_pv/city_page/%s/%s/%s?d=current'

def get_json_data(url):
    """
    Return JSON formatted output of the content  from the given URL.
    
    :param url: url to access
    :returns: JSON-formatted content from given url
    :rtype: string (json)
    :raises Exception: if the request did not return HTTP code 200
    """
    json_data = requests.get(url)
    if json_data.status_code != 200:
        raise Exception("HTTP status other than 200 was returned")
    return json_data.json()


def get_page_data(url):
    """
    Return string formatted output of the content from the given URL.

    :param url: url to access
    :returns: content from given url
    :rtype: string (content)
    :raises Exception: if the request did not return HTTP code 200
    """
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("HTTP status other than 200 was returned")
    page_data = str(r.content)
    return page_data


def walkscore_city_url(city, state, json=False):
    """
    Return a well-formatted Walkscore URL a city.
    
    :param city: Name of the city (such as `Seattle`)
    :param state: Two-letter code of the state (such as `WA`)
    :param json: Whether to return the the JSON data URL (for some metadata)
    :returns: Walkscore URL for given city/state
    :rtype: string
    """
    if json == False:
        url_to_call = base_city_url
    else:
        url_to_call = base_json_data_city_url

    return url_to_call % (state, city.replace(' ', '_'))


def walkscore_neighborhood_url(neighborhood, city, state, json=False):
    """
    Return a well-formatted Walkscore URL a neighborhoods.
    
    :param neighborhood: Nane of the neighborhood (such as `Denny Triangle`)
    :param city: Name of the city (such as `Seattle`)
    :param state: Two-letter code of the state (such as `WA`)
    :param json: Whether to return the the JSON data URL (for some metadata)
    :returns: Walkscore URL for given neighborhood/city/state
    :rtype: string
    """
    if json == False:
        url_to_call = base_neighborhood_url
    else:
        url_to_call = base_json_data_neighborhood_url

    neighborhood = neighborhood.replace('/', '.slash.')

    return url_to_call % (state, city.replace(' ', '_'), neighborhood.replace(' ', '_'))