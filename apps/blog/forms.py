# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import forms
from django.utils.translation import ugettext_lazy as _
from sanitizer.forms import SanitizedCharField
from config.settings import SANITIZER_ALLOWED_TAGS, SANITIZER_ALLOWED_ATTRIBUTES


class Create(forms.Form):

    name    = forms.CharField(label=_("TITLE"))
    content = SanitizedCharField(label=_("CONTENT"), widget=forms.Textarea,
                                 max_length=50000, allowed_tags=SANITIZER_ALLOWED_TAGS,
                                 allowed_attributes=SANITIZER_ALLOWED_ATTRIBUTES, 
                                 strip=False)


class Edit(forms.Form):

    name    = forms.CharField(label=_("TITLE"))
    content = SanitizedCharField(label=_("CONTENT"), widget=forms.Textarea,
                                 max_length=50000, allowed_tags=SANITIZER_ALLOWED_TAGS,
                                 allowed_attributes=SANITIZER_ALLOWED_ATTRIBUTES, 
                                 strip=False)

    def __init__(self, *args, **kwargs):
        blog = kwargs.pop("blog")
        super(Edit, self).__init__(*args, **kwargs)
        self.fields["name"].initial = blog.name
        self.fields["content"].initial = blog.content


