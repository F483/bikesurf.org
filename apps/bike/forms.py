# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext_lazy as _
from django.forms import Form
from django.forms import Textarea
from django.forms import ModelChoiceField
from django.forms import CharField
from django.forms import BooleanField
from django.forms import ChoiceField

from apps.bike.models import KIND_CHOICES
from apps.bike.models import GENDER_CHOICES
from apps.bike.models import SIZE_CHOICES


class Create(Form):

    owner = ModelChoiceField(label=_("OWNER"), queryset=None)
    name = CharField(label=_("NAME"))
    active = BooleanField(label=_("ACTIVE"), initial=True, required=False)
    reserve = BooleanField(label=_("RESERVE"), initial=False, required=False)
    station = ModelChoiceField(label=_("STATION"), queryset=None, required=False)
    lockcode = CharField(label=_("LOCKCODE"))
    keycode = CharField(label=_("KEYCODE"), required=False)
    kind = ChoiceField(choices=KIND_CHOICES, label=_("TYPE"))
    gender = ChoiceField(choices=GENDER_CHOICES, label=_("GENDER"))
    size = ChoiceField(choices=SIZE_CHOICES, label=_("SIZE"), initial="MEDIUM")
    lights = BooleanField(label=_("LIGHTS"), initial=False, required=False)
    fenders = BooleanField(label=_("FENDERS"), initial=False, required=False)
    rack = BooleanField(label=_("RACK"), initial=False, required=False)
    basket = BooleanField(label=_("BASKET"), initial=False, required=False)
    description = CharField(label=_("description"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        team = kwargs.pop("team")
        account = kwargs.pop("account")
        super(Create, self).__init__(*args, **kwargs)
        self.fields["owner"].queryset = team.members.all()
        self.fields["owner"].initial = account
        self.fields["station"].queryset = team.stations.all()


