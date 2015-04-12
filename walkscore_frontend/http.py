import json
import requests

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