# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext_lazy as _
from django.forms import Form
from django.forms import ImageField
from django.forms import ModelChoiceField


class Create(Form):

    image = ImageField(label=_("IMAGE"))


class Add(Form):

    image = ImageField(label=_("IMAGE"))


class SetPrimary(Form):

    picture = ModelChoiceField(
            label='TEST', empty_label=_("WHICH?"), queryset=None
    ) 

    def __init__(self, *args, **kwargs):
        self.gallery = kwargs.pop("gallery")
        super(SetPrimary, self).__init__(*args, **kwargs)
        self.fields["picture"].queryset = self.gallery.pictures.all()

