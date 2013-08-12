#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


# BOILERPLATE

import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_DIR)

from django.core.management import setup_environ
from config import settings

setup_environ(settings)

# PUT SCRIPT CODE HERE

