#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from setuptools import setup

with open('normalizer/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='normalizer',
    version=version,
    description='Transform text into a single canonical form',
    author="Yadegari and Ahmadi",
    packages=['normalizer'],
    install_requires=[],
    python_requires='>=3.6',
    include_package_data=False,
    zip_safe=False)
