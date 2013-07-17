# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext as _
from django.forms import Form
from django.forms import ImageField
from django.forms import ModelChoiceField


class Create(Form):

    image = ImageField(label=_("IMAGE"))


class Add(Form):

    image = ImageField(label=_("IMAGE"))


