# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import forms
from django.utils.translation import ugettext_lazy as _
from apps.common.shortcuts import HUMAN_LINK_LEN as HLL


class CreatePageForm(forms.Form):

    link = forms.CharField(label="bikesurf.org/<team>/", min_length=3, max_length=HLL)
    name = forms.CharField(label=_("NAME"))
    content = forms.CharField(label=_("CONTENT"), widget=forms.Textarea)
    order = forms.IntegerField(label=_("ORDER"))


