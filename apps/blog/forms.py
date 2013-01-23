# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import forms
from django.utils.translation import ugettext_lazy as _


class CreateBlogForm(forms.Form):

    name = forms.CharField(label=_("TITLE"))
    content = forms.CharField(label=_("CONTENT"), widget=forms.Textarea)


