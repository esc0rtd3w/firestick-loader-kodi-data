#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='TaskUtils',
    version='0.2',
    description='A passive background task manager.',
    author='Mikel Azkolain',
    author_email='azkotoki@gmail.com',
    url='http://github.com/mazkolain/taskutils',
    package_dir = {'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
)
