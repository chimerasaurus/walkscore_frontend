****************************************
Walkscore Frontend
****************************************

Wrapper front-end on the Walkscore website designed to make scraping data from Walkscore easier. While
Walkscore has its own API, it is limited and only returns some of the data available through the web UI.
This wrapper scrapes data from the web UI to provide more granular data than is available via the API.

Please note, **this module is for educational purposes only.**

.. image:: https://readthedocs.org/projects/walkscore-frontend/badge/?version=latest
 :target: https://readthedocs.org/projects/walkscore-frontend/?badge=latest
 :alt: Documentation Status
 
.. image:: https://travis-ci.org/evilsoapbox/walkscore_frontend.svg?branch=master
    :target: https://travis-ci.org/evilsoapbox/walkscore_frontend
 
.. image:: https://coveralls.io/repos/evilsoapbox/walkscore_frontend/badge.svg?branch=master
   :target: https://coveralls.io/r/evilsoapbox/walkscore_frontend?branch=master

---------------
Installation
---------------

You can install this module via pip::

 pip install walkscore-api-binding

Alternatively, you can install the latest from this repository::

 git clone git@github.com:evilsoapbox/walkscore_frontend.git
 python setup.py install

Dependencies
~~~~~~~~~~~~~~~~~~~~~~
This module requires the following libraries to function.

* requests
* BeautifulSoup4
* nose

---------------
Usage
---------------

Use this module via reference, such as::

 import walkscore_frontend
 wrapper = walkscore_frontend()

You can then call a number of functions to pull data:

* ``data_for_city(name, state)``
* ``data_for_neighborhood(name, city, state)``

Definitions
~~~~~~~~~~~~~~~~~~~~~~
There are a few key terms and concepts used in this wrapper and the Walkscore website.

State
  A state within the United States. This is represented by the two-letter state code
  commonly used for a given state, such as ``CA`` for ``California``.
City
  A city within a state. This is the full name of the city and includes any punctuation
  in the city name, such as ``Winston-Salem``.
Neighborhood
  A section within a city. Generally cities contain one or more neighborhoods.

Documentation
~~~~~~~~~~~~~~~~~~~~~~
Better documentation for this project is available at `ReadTheDocs <http://walkscore-frontend.readthedocs.org/en/latest/index.html>`_ 

TODO
--------
* **Better errorhandling** - Add better error and exception handling
* **Support for "simple" pages** - Some Walkscore cities and pages have a new and/or simple layout
