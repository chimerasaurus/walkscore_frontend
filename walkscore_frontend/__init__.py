"""
Module to obtain data from the Walkscore website.
In my opinion, the Walkscore API is too limited for educational data gathering and related projects. This module
is designed to make it easier to scrape data from Walkscore.
This module is intended for educational and research purposes only.
"""

__author__ = 'James Malone'
__license__ = "MIT"
__version__ = "0.2"
__maintainer__ = "James Malone"
__email__ = 'jamalone at gmail dot com'
__status__ = "Development"

# Packages needed for this module
from bs4 import BeautifulSoup
import collections
import json
import re
import requests
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
    neighborhood_data = remove_unneeded_elements(neighborhood_data)

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
    city_data = remove_unneeded_elements(city_data)

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

def remove_unneeded_elements(dict_to_clean):
    """Pop unneeded elements from the given dictionary."""
    for key in attributes_to_remove:
        dict_to_clean.pop(key)
    return dict_to_clean

def merge_dicts(*dicts):
    """Merge dictionaries together."""
    return_dict = dict()
    for d in dicts:
        return_dict.update(d)
    return return_dict

def get_page_data(url):
    """Get the page data from the Walkscore website."""
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Cannot get data for city")
    page_data = str(r.content)
    return page_data


def get_json_data(url):
    """Get JSON data from the Walkscore website"""
    json_data = requests.get(url)
    if json_data.status_code != 200:
        raise Exception("Cannot get data for city")
    return json_data.json()


def regex_page_data_int(pattern, html):
    """Extract an integer value from the page based on a pattern."""
    result = regex_page_data(pattern, html)
    if result is not None:
        if ',' in result:
            result = result.replace(',', '')
        result = int(result)
    return result


def regex_page_data_float(pattern, html):
    """Extract a floating point value from the page based on a pattern."""
    result = regex_page_data(pattern, html)
    if result is not None:
        if ',' in result:
            result = result.replace(',', '')
        result = float(result)
    return result


def regex_page_data_table(pattern, html):
    """Extract data from a table on the page based on an id and value."""
    soup = BeautifulSoup(html)
    attributes = pattern.split('=')
    table_data = []
    table = soup.find("table", attrs={attributes[0]:attributes[1]})

    if table is not None:
        headings = [th.get_text() for th in table.find("tr").find_all("th")]

        # Format the headings
        for idx, item in enumerate(headings):
            headings[idx] = re.sub('[!@#$]', '', item.lower().replace(' ', '_'))

        # Iterate the table and parse the data
        for row in table.findAll("tr")[1:]:
            cells = row.findAll("td")
            row_data = {}
            for i in range(0, len(cells) -1):
                row_data[headings[i]] = cells[i].get_text()

                # Look for links which do not match the text and fix them
                cell_link = cells[i].find('a')
                if cell_link is not None:
                    last_element = cell_link.get('href').split('/')[-1]
                    if last_element.replace('_', ' ') != row_data[headings[i]]:
                        row_data[headings[i]] = last_element.replace('_', ' ')

            table_data.append(row_data)
        return table_data
    else:
        return None


def regex_page_data(pattern, html):
    """Get a value from page data based on a regex pattern. """
    result = re.search(pattern, html)
    if result is not None:
        return result.group(1)
    else:
        return None


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