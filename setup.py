#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import versify
import os

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')) as fp:
    install_requires = fp.read()

setup(

    name='versify',

    version=versify.__version__,

    packages=find_packages(),

    author="Willy K.",

    author_email="willy.konguem@gmail.com",

    description="Client for DBT API Platform",

    long_description=open('README.md').read(),

    install_requires=install_requires,

    include_package_data=True,

    url='https://github.com/willinprogress/python-versify',

    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
)
