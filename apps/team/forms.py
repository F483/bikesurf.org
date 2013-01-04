# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import forms
from django.utils.translation import ugettext_lazy as _
from django_countries.countries import COUNTRIES
from apps.team.models import STATUS_CHOICES


class CreateTeamForm(forms.Form):

    name = forms.CharField(label=_('NAME'))
    country = forms.ChoiceField(choices=COUNTRIES, label=_('COUNTRY')) # TODO empty_label


class CreateJoinRequestForm(forms.Form):

    application = forms.CharField(label=_('REASON'), widget=forms.Textarea)


class ProcessJoinRequestForm(forms.Form):

    response = forms.CharField(label=_('RESPONSE'), widget=forms.Textarea)
    status = forms.ChoiceField(choices=STATUS_CHOICES[1:], label=_('STATUS'))


