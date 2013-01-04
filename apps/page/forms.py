# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import forms
from django.utils.translation import ugettext_lazy as _


class CreatePageForm(forms.Form):

    name = forms.CharField(label=_("NAME"))
    content = forms.CharField(label=_("CONTENT"), widget=forms.Textarea)
    order = forms.IntegerField(label=_("ORDER"))


