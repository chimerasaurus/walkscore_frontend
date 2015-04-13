"""
Performs HTTP work for the frontend. Uses the Requests library to communicate
via HTTP to WalkScore.
"""

# Imports for this module
import json
import requests

def get_page_data(url):
    """
    Return string formatted output of the content from the given URL.

    :param url: url to grab data from
    :returns: page data from given url
    :rtype: string (content)
    :raises Exception: if the request did not return HTTP code 200
    """
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Cannot get data for city")
    page_data = str(r.content)
    return page_data


def get_json_data(url):
    """
    Return JSON formatted output of the content  from the given URL.
    
    :param url: url to grab data from
    :returns: page data from given url
    :rtype: string (json)
    :raises Exception: if the request did not return HTTP code 200
    """
    json_data = requests.get(url)
    if json_data.status_code != 200:
        raise Exception("Cannot get data for city")
    return json_data.json()