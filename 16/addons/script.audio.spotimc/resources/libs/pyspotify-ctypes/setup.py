#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='PyspotifyCtypes',
    version='0.6',
    description='Ctypes-based Spotify bindings for python',
    author='Mikel Azkolain',
    author_email='azkotoki@gmail.com',
    url='http://forge.azkotoki.org/pyspotify-ctypes',
    package_dir = {'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
)
