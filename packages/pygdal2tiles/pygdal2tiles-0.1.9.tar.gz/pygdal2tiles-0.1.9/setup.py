#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import subprocess
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="National Drones",
    author_email='smartdata@nationaldrones.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="A fork of gdal2tiles without gdal specified so that it can easily be installed in a virtual environment. A python library for generating map tiles based on gdal2tiles.py script.",
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='gdal2tiles',
    name='pygdal2tiles',
    packages=find_packages(include=['gdal2tiles']),
    setup_requires=setup_requirements,
    extras_require={
        'billiard': ['billiard'],
    },
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/nationaldrones/gdal2tiles',
    version='0.1.9',
    zip_safe=False,
)
