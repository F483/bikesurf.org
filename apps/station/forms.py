# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext_lazy as _
from django import forms

from apps.account.models import Account
from apps.common.shortcuts import COUNTRIES


class CreateStationForm(forms.Form):

    responsable = forms.ModelChoiceField(label=_("RESPONSABLE"), queryset=None)
    country = forms.ChoiceField(choices=COUNTRIES, label=_('COUNTRY'))
    postalcode = forms.CharField(label=_('POSTALCODE'))
    city = forms.CharField(label=_('CITY'))
    street = forms.CharField(label=_('STREET'))
    capacity = forms.IntegerField(label=_("CAPACITY"), initial=1, min_value=0)
    active = forms.BooleanField(label=_("ACTIVE"), initial=True)

    def __init__(self, *args, **kwargs):
        team = kwargs.pop("team")
        account = kwargs.pop("account")
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields["responsable"].queryset = team.members.all()
        self.fields["responsable"].initial = account
        self.fields["country"].initial = team.country.code
        self.fields["city"].initial = team.name

