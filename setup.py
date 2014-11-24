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
  install_requires=[
    'Django==1.7',
    'Markdown==2.5.2',
    'Pillow==2.6.1', # PIL fork
    'Unidecode==0.04.16',
    'argparse==1.2.1',
    'bleach==1.4',
    'django-allauth==0.18.0',
    'django-appconf==0.6',
    'django-countries==2.1.2',
    'django-html-sanitizer==0.1.4', # TODO use only bleach
    'django-imagekit==3.2.4',
    'django-rosetta==0.7.4',
    'html5lib==1.0b3',
    'oauthlib==0.6.3',
    'pilkit==1.1.12',
    'polib==1.0.5', # because rosetta requires an old buggy version
    #'psycopg2==2.5.4', # only needed when using postgres
    'python-dateutil==2.2',
    'python-openid==2.2.5',
    'requests==2.4.3',
    'requests-oauthlib==0.4.2',
    'six==1.8.0',
    'wsgiref==0.1.2',

    # TODO add 'Markdown',
    # TODO add 'django-bootstrap-form',
    # TODO add 'django-pagination',
    # TODO use 'django-debug-toolbar',
  ],
  dependency_links=[],
  #test_suite="tests",
)

