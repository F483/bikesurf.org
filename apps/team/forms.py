# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import forms
from django.utils.translation import ugettext_lazy as _
from django_countries.countries import COUNTRIES


class CreateTeamForm(forms.Form):

    link = forms.CharField(label='bikesurf.org/')
    name = forms.CharField(label=_('NAME'))
    country = forms.ChoiceField(choices=COUNTRIES, label=_('COUNTRY')) # TODO empty_label

