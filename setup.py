# Imports for this setup script
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

# Setup metadata
setup(name='walkscore_frontend',
    version='0.3',
    description='Front-end (scraper API) for the Walkscore website',
    long_description=readme(),
    url='http://github.com/evilsoapbox/walkscore_frontend',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: GIS',
        'Natural Language :: English',
        'Intended Audience :: Science/Research',
    ],
    keywords='walkscore frontend data walk transitscore bikescore',
    author='James Malone',
    author_email='jamalone@gmail.com',
    license='MIT',
    packages=['walkscore_frontend'],
    install_requires=[
        'beautifulsoup4',
        'requests',
        'nose',
    ],
    include_package_data=True,
    zip_safe=False)