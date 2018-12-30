#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='PyspotifyCtypesProxy',
    version='0.5',
    description='An embedded proxy server intended for players that cannot integrate libspotify easily.',
    author='Mikel Azkolain',
    author_email='azkotoki@gmail.com',
    url='http://forge.azkotoki.org/pyspotify-ctypes',
    package_dir = {'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
)
