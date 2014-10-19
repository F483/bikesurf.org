#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE.TXT file)

from os import path
from setuptools import setup, find_packages

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as f:
  README = f.read()

setup(
  name='bikesurf.org',
  license = "MIT",
  author='Fabian Barkhau',
  author_email='fabian.barkhau@gmail.com',
  maintainer='Fabian Barkhau',
  maintainer_email='fabian.barkhau@gmail.com',
  version='1.0.0',
  description='A website for bike sharing.',
  long_description=README,
  classifiers=["Programming Language :: Python"],
  url='http://bikesurf.org',
  keywords='bike sharing',
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  install_requires=[ # TODO specify working versions
    'Django',
    'django-countries',
    'django-allauth',
    'django-html-sanitizer', # TODO use only 'bleach'?
    'django-imagekit',
    'django-rosetta',
    'python-dateutil',
    'Unidecode',
    'pillow', # PIL fork
    # 'psycopg2', # only when using postgres
    # TODO add 'Markdown',
    # TODO add 'django-bootstrap-form',
    # TODO add 'django-pagination',
    # TODO use 'django-debug-toolbar',
  ],
  dependency_links=[],
  #test_suite="tests",
)

