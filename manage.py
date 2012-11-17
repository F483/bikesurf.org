#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bikesurfing.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


