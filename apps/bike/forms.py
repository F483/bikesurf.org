# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext_lazy as _
from django import forms

from apps.bike.models import KIND_CHOICES
from apps.bike.models import GENDER_CHOICES
from apps.bike.models import SIZE_CHOICES


class CreateBikeForm(forms.Form):

    owner = forms.ModelChoiceField(label=_("OWNER"), queryset=None)
    name = forms.CharField(label=_("NAME"))
    active = forms.BooleanField(label=_("ACTIVE"), initial=True, required=False)
    reserve = forms.BooleanField(label=_("RESERVE"), initial=False, required=False)
    station = forms.ModelChoiceField(label=_("STATION"), queryset=None, required=False)
    lockcode = forms.CharField(label=_("LOCKCODE"))
    keycode = forms.CharField(label=_("KEYCODE"), required=False)
    kind = forms.ChoiceField(choices=KIND_CHOICES, label=_("TYPE"))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label=_("GENDER"))
    size = forms.ChoiceField(choices=SIZE_CHOICES, label=_("SIZE"), initial="MEDIUM")
    lights = forms.BooleanField(label=_("LIGHTS"), initial=False, required=False)
    fenders = forms.BooleanField(label=_("FENDERS"), initial=False, required=False)
    rack = forms.BooleanField(label=_("RACK"), initial=False, required=False)
    basket = forms.BooleanField(label=_("BASKET"), initial=False, required=False)
    description = forms.CharField(label=_("description"), widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        team = kwargs.pop("team")
        account = kwargs.pop("account")
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields["owner"].queryset = team.members.all()
        self.fields["owner"].initial = account
        self.fields["station"].queryset = team.stations.all()



