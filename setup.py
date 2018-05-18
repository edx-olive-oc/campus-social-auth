#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0111,W6005,W6100
from __future__ import absolute_import, print_function

__version__ = '1.0.0'

from setuptools import setup


setup(
    name='campus-social-auth',
    version=__version__,
    description="""A custom Campus authentication backend""",
    packages=[
        'campus_social_auth',
    ],
    include_package_data=True,
    install_requires=[
        "Django>=1.8,<2.1"
    ],
    license="AGPL 3.0",
)
