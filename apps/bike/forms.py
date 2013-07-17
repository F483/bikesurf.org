# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext as _
from django.forms import ValidationError
from django.forms import Form
from django.forms import Textarea
from django.forms import ModelChoiceField
from django.forms import CharField
from django.forms import BooleanField
from django.forms import ChoiceField
from django.forms import ImageField

from apps.bike.models import SIZE_CHOICES
from apps.bike import control
from apps.station.forms import validate_station_active


class Create(Form):

    name = CharField(label=_("NAME"))
    image = ImageField(label=_("IMAGE"))
    active = BooleanField(label=_("ACTIVE"), initial=True, required=False)
    reserve = BooleanField(label=_("RESERVE"), initial=False, required=False)
    station = ModelChoiceField(
            label=_("STATION"), queryset=None, required=True, 
            validators=[validate_station_active]
    )
    lockcode = CharField(label=_("LOCKCODE"))
    size = ChoiceField(choices=SIZE_CHOICES, label=_("SIZE"), initial="MEDIUM")
    lights = BooleanField(label=_("LIGHTS"), initial=False, required=False)
    description = CharField(label=_("DESCRIPTION"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        team = kwargs.pop("team")
        account = kwargs.pop("account")
        super(Create, self).__init__(*args, **kwargs)
        self.fields["station"].queryset = team.stations.filter(active=True)


class Edit(Form):

    name = CharField(label=_("NAME"))
    active = BooleanField(label=_("ACTIVE"), initial=True, required=False)
    reserve = BooleanField(label=_("RESERVE"), initial=False, required=False)
    station = ModelChoiceField(
            label=_("STATION"), queryset=None, required=True,
            validators=[validate_station_active]
    )
    lockcode = CharField(label=_("LOCKCODE"))
    size = ChoiceField(choices=SIZE_CHOICES, label=_("SIZE"), initial="MEDIUM")
    lights = BooleanField(label=_("LIGHTS"), initial=False, required=False)
    description = CharField(label=_("description"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        self.bike = kwargs.pop("bike")
        self.account = kwargs.pop("account")
        super(Edit, self).__init__(*args, **kwargs)
        self.fields["name"].initial = self.bike.name
        self.fields["active"].initial = self.bike.active
        self.fields["reserve"].initial = self.bike.reserve
        self.fields["station"].queryset = self.bike.team.stations.all()
        self.fields["station"].initial = self.bike.station
        self.fields["lockcode"].initial = self.bike.lockcode
        self.fields["size"].initial = self.bike.size
        self.fields["lights"].initial = self.bike.lights
        self.fields["description"].initial = self.bike.description

    def clean(self):
        cleaned_data = super(Edit, self).clean()
        station = cleaned_data.get("station")
        active = cleaned_data.get("active")

        if (not active and self.bike.active and
                not control.can_deactivate(self.account, self.bike)):
            raise ValidationError(_("ERROR_CANNOT_DEACTIVATE_BIKE_IN_USE"))

        if (station != self.bike.station and
                not control.can_change_station(self.account, self.bike, station)):
            raise ValidationError(_("ERROR_CANNOT_CHANGE_STATION_BIKE_IN_USE"))

        return cleaned_data


class Delete(Form):

    def __init__(self, *args, **kwargs):
        self.bike = kwargs.pop("bike")
        self.account = kwargs.pop("account")
        super(Delete, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(Delete, self).clean()
        if not control.can_delete(self.account, self.bike):
            raise ValidationError(_("ERROR_CANNOT_DELETE_BIKE_IN_USE"))
        return cleaned_data


