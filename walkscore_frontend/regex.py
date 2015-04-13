"""
Handles regular expression (regex) parsing for the walkscore_frontend module.
"""

# Imports for this module
from bs4 import BeautifulSoup
import re

# Constants for thos module
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

def parse_data_points(content):
    """
    Parse the page data and look for expected contents based on regular expressions.
    
    :param content: content to search
    :returns: parsed data based on the built-in regex searches
    :rtype: dict
    """
    parsed_data = {}
    for data_type in regex_filters.keys():
        for data_attribute in regex_filters[data_type].keys():
            value = None
            if data_type == 'int':
                value = regex_page_data_int(regex_filters[data_type][data_attribute], content)
            elif data_type == 'float':
                value = regex_page_data_float(regex_filters[data_type][data_attribute], content)
            elif data_type == 'table':
                value = regex_page_data_table(regex_filters[data_type][data_attribute], content)
            parsed_data[data_attribute] = value
    return parsed_data

def regex_page_data_int(pattern, content):
    """
    Extract an integer value from the text based on a pattern.
    
    :param pattern: regex pattern to match against
    :param content: content to search
    :returns: first int result for the given match
    :rtype: int
    """
    int_result = regex_page_data(pattern, content)
    if int_result is not None:
        int_result = int(int_result)
    return int_result


def regex_page_data_float(pattern, content):
    """
    Extract a floating point value from the text based on a pattern.
    
    :param pattern: regex pattern to match against
    :param content: content to search
    :returns: first float result for the given match
    :rtype: float
    """
    float_result = regex_page_data(pattern, content)
    if float_result is not None:
        float_result = float(float_result)
    return float_result


def regex_page_data_table(pattern, content):
    """
    Extract data from a table on the text based on an id and value.
    
    :param pattern: id and value of element to parse
    :param content: content to search
    :returns: array of data from the table
    :rtype: string array
    """
    attributes = pattern.split('=')
    table_data = []
    table = BeautifulSoup(content).find("table", attrs={attributes[0]:attributes[1]})

    if table is not None:
        headings = [th.get_text() for th in table.find("tr").find_all("th")]
        for idx, item in enumerate(headings): # Format the headings
            headings[idx] = re.sub('[!@#$]', '', item.lower().replace(' ', '_'))
        for row in table.findAll("tr")[1:]: # Iterate the table and parse the data
            cells = row.findAll("td")
            row_data = {}
            for i in range(0, len(cells) -1):
                row_data[headings[i]] = cells[i].get_text() # Fix mismatched links
                cell_link = cells[i].find('a')
                if cell_link is not None:
                    last_element = cell_link.get('href').split('/')[-1]
                    if last_element.replace('_', ' ') != row_data[headings[i]]:
                        row_data[headings[i]] = last_element.replace('_', ' ')
            table_data.append(row_data)
        return table_data
    else:
        return None


def regex_page_data(pattern, content):
    """
    Get a value from page data based on a regex pattern.
    
    :param pattern: regex pattern to match against
    :param content: content to search
    :returns: first result for the given match
    :rtype: object
    """
    
    result = re.search(pattern, content)
    if result is not None:
        result = result.group(1)
        if ',' in result:
            result = result.replace(',', '')
        return result
    else:
        return None