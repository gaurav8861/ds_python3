#!/usr/bin/env python

"""
Installation script for CDS Tiering Engine

Copyright 2019 Cray Inc, All rights reserved.
"""

from setuptools import setup, find_packages

with open('.version') as fp:
    VERS = fp.readline().strip()

setup(
    name='test',
    version=VERS,
    description='test',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
    }
)
