#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 

# BOILERPLATE

import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from django.conf import settings

# PUT SCRIPT CODE HERE

for lang in settings.LANGUAGES:
  print lang[0].replace('-', '_')

