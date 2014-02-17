#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Hugo Geoffroy
    :contact: hugo@pstch.net
"""

from setuptools import setup, find_packages

setup(
    name='django-pstch-helpers',
    version='0.2',
    description='Various Django helpers that I use frequently in my projets',
    long_description="views, models, auto URL patterns, ...",
    url='https://github.com/pstch/django-pstch-helpers',
    author='Hugo Geoffroy',
    author_email='hugo@pstch.net',
    packages = find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms=['any'],
    test_suite='tests.runtests.runtests',
)
