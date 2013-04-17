# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError
from django.forms import Form
from django.forms import Textarea
from django.forms import ModelChoiceField
from django.forms import CharField
from django.forms import BooleanField
from django.forms import ChoiceField
from django.forms import ImageField

from apps.bike.models import SIZE_CHOICES


def _validate_capacity(station):
    bike_count = len(station.bikes.all())
    if bike_count >= station.capacity:
        raise ValidationError(_("STATION_AT_MAX_CAPACITY"))


class Create(Form):

    name = CharField(label=_("NAME"))
    image = ImageField(label=_("IMAGE"))
    active = BooleanField(label=_("ACTIVE"), initial=True, required=False)
    reserve = BooleanField(label=_("RESERVE"), initial=False, required=False)
    station = ModelChoiceField(
            label=_("STATION"), queryset=None, required=False, 
            validators=[_validate_capacity]
    )
    lockcode = CharField(label=_("LOCKCODE"))
    size = ChoiceField(choices=SIZE_CHOICES, label=_("SIZE"), initial="MEDIUM")
    lights = BooleanField(label=_("LIGHTS"), initial=False, required=False)
    description = CharField(label=_("description"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        team = kwargs.pop("team")
        account = kwargs.pop("account")
        super(Create, self).__init__(*args, **kwargs)
        self.fields["station"].queryset = team.stations.all()


class Edit(Form):

    name = CharField(label=_("NAME"))
    active = BooleanField(label=_("ACTIVE"), initial=True, required=False)
    reserve = BooleanField(label=_("RESERVE"), initial=False, required=False)
    station = ModelChoiceField(
            label=_("STATION"), queryset=None, required=False, 
            validators=[_validate_capacity]
    )
    lockcode = CharField(label=_("LOCKCODE"))
    size = ChoiceField(choices=SIZE_CHOICES, label=_("SIZE"), initial="MEDIUM")
    lights = BooleanField(label=_("LIGHTS"), initial=False, required=False)
    description = CharField(label=_("description"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        bike = kwargs.pop("bike")
        account = kwargs.pop("account")
        super(Edit, self).__init__(*args, **kwargs)
        self.fields["name"].initial = bike.name
        self.fields["active"].initial = bike.active
        self.fields["reserve"].initial = bike.reserve
        self.fields["station"].queryset = bike.team.stations.all()
        self.fields["station"].initial = bike.station
        self.fields["lockcode"].initial = bike.lockcode
        self.fields["size"].initial = bike.size
        self.fields["lights"].initial = bike.lights
        self.fields["description"].initial = bike.description


class Delete(Form):

    def __init__(self, *args, **kwargs):
        self.bike = kwargs.pop("bike")
        self.account = kwargs.pop("account")
        super(Delete, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(Delete, self).clean()

        # XXX see apps.bike.control.can_delete
        if len(self.bike.borrows.filter(active=True)): # active_borrows 
            raise ValidationError(_("BIKE_HAS_ACTIVE_BORROWS"))

        return cleaned_data


