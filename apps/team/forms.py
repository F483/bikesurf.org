# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import forms
from django.utils.translation import ugettext_lazy as _
from django_countries.countries import COUNTRIES
from apps.common.shortcuts import HUMAN_LINK_LEN as HLL
from apps.team.models import STATUS_CHOICES


class CreateTeamForm(forms.Form):

    link = forms.CharField(label='bikesurf.org/', min_length=3, max_length=HLL)
    name = forms.CharField(label=_('NAME'))
    country = forms.ChoiceField(choices=COUNTRIES, label=_('COUNTRY')) # TODO empty_label


class CreateJoinRequestForm(forms.Form):

    application = forms.CharField(label=_('REASON'), widget=forms.Textarea)


class ProcessJoinRequestForm(forms.Form):

    response = forms.CharField(label=_('RESPONSE'), widget=forms.Textarea)
    status = forms.ChoiceField(choices=STATUS_CHOICES[1:], label=_('STATUS'))


class CreatePageForm(forms.Form):

    link = forms.CharField(label='bikesurf.org/<team>/', min_length=3, max_length=HLL)
    name = forms.CharField(label=_('NAME'))
    content = forms.CharField(label=_('CONTENT'), widget=forms.Textarea)
    order = forms.IntegerField(label=_('ORDER'))


