from setuptools import setup

setup(name='walkscore_frontend',
    version='0.1',
    description='Front-end (scrape API) for the Walkscore website',
    url='http://github.com/evilsoapbox',
    author='James Malone',
    author_email='jamalone@gmail.com',
    license='MIT',
    packages=['walkscore_frontend'],
    install_requires=[
        'beautifulsoup4',
        'requests'
    ],
    zip_safe=False)