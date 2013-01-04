# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import forms
from django.utils.translation import ugettext_lazy as _
from django_countries.countries import COUNTRIES
from django.core.exceptions import ValidationError
from apps.common.shortcuts import uslugify
from apps.team.models import STATUS_CHOICES
from apps.team.models import Team


_RESERVED_NAMES = [
    u"team",
]

def _validate_name(value):
    name = value.strip()
    link = uslugify(name)
    if len(link) < 3:
        raise ValidationError(_("NAME_TO_SHORT"))
    if link in _RESERVED_NAMES:
        raise ValidationError(_("NAME_RESERVED"))
    if bool(len(Team.objects.filter(link=link))):
        raise ValidationError(_("NAME_USED"))
    if bool(len(Team.objects.filter(name=name))):
        raise ValidationError(_("NAME_USED"))


class CreateTeamForm(forms.Form):

    name = forms.CharField(label=_('NAME'), validators=[_validate_name])
    country = forms.ChoiceField(choices=COUNTRIES, label=_('COUNTRY')) # TODO empty_label


class CreateJoinRequestForm(forms.Form):

    application = forms.CharField(label=_('REASON'), widget=forms.Textarea)


class ProcessJoinRequestForm(forms.Form):

    response = forms.CharField(label=_('RESPONSE'), widget=forms.Textarea)
    status = forms.ChoiceField(choices=STATUS_CHOICES[1:], label=_('STATUS'))


