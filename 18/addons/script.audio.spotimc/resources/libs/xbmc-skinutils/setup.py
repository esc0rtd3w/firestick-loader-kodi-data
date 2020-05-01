#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='XbmcSkinUtils',
    version='0.4',
    description='Utility package with enhancements for XBMC addons that use skins.',
    author='Mikel Azkolain',
    author_email='azkotoki@gmail.com',
    url='http://forge.azkotoki.org/xbmc-skinutils',
    package_dir = {'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
)
