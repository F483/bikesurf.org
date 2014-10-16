# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


ID = r"[0-9]+"
SLUG = r"[a-z0-9\-]+"
USERNAME = r"[\w.@+-]+" # see django.contrib.auth.forms.UserCreationForm


def _build_arg(name, pattern):
    return "(?P<%s>%s)" % (name, pattern)


def arg_id(name):
    return _build_arg(name, ID)


def arg_slug(name):
    return _build_arg(name, SLUG)


def arg_username(name):
    return _build_arg(name, USERNAME)

