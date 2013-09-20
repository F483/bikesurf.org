# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import datetime

from django.utils.translation import ugettext as _
from django.forms import Form
from django.forms import DateField
from django.forms import ValidationError
from django.forms import CharField
from django.forms import Textarea
from django.forms import ChoiceField
from django.forms import TypedChoiceField
from django.forms import RadioSelect
from django.forms.extras.widgets import SelectDateWidget
from django.core.exceptions import PermissionDenied
from django.forms import ModelChoiceField

from apps.borrow.models import Borrow
from apps.borrow.models import RATING_CHOICES
from apps.borrow import control
from apps.team import control as team_control
from apps.station.forms import validate_station_active


RESPONSE_CHOICES = [
    ("ACCEPTED", _("ACCEPTED")),
    ("MEETUP",   _("MEETUP")),
    ("REJECTED", _("REJECTED")),
]


def _validate_borrow_timeframe(bike, start, finish):
    today = datetime.datetime.now().date()
    if start <= today:
        raise ValidationError(_("ERROR_START_NOT_IN_FUTURE"))
    if finish < start:
        raise ValidationError(_("ERROR_FINISH_BEFORE_START"))
    if len(control.active_borrows_in_timeframe(bike, start, finish)):
        raise ValidationError(_("ERROR_OTHER_BORROW_IN_TIMEFRAME"))


class Respond(Form):
    
    response = ChoiceField(choices=RESPONSE_CHOICES, label=_('RESPONSE'))
    note = CharField(label=_("NOTE"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        self.borrow = kwargs.pop("borrow")
        self.account = kwargs.pop("account")
        super(Respond, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(Respond, self).clean()
        bike = self.borrow.bike
        start = self.borrow.start
        finish = self.borrow.finish
        if cleaned_data.get("response") != "REJECTED":
            today = datetime.datetime.now().date()
            if self.borrow.finish <= today:
                raise ValidationError(_("ERROR_TO_LATE_TO_ACCEPT"))
            if not self.borrow.bike.active:
                raise ValidationError(_("ERROR_BIKE_NOT_ACTIVE"))
            if self.borrow.bike.reserve:
                raise ValidationError(_("ERROR_IS_RESERVE_BIKE"))
            if not self.borrow.bike.station:
                raise ValidationError(_("ERROR_BIKE_STATION_UNKNOWN"))
            if not self.borrow.bike.station.active:
                raise ValidationError(_("ERROR_BIKE_STATION_INACTIVE"))
            if control.active_borrows_in_timeframe(bike, start, finish):
                raise ValidationError(_("ERROR_OTHER_BORROW_IN_TIMEFRAME"))
        return cleaned_data


class Create(Form):

    start = DateField(label=_("START"), widget=SelectDateWidget())
    finish = DateField(label=_("FINISH"), widget=SelectDateWidget())
    note = CharField(label=_("NOTE"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        self.bike = kwargs.pop("bike")
        super(Create, self).__init__(*args, **kwargs)
        today = datetime.datetime.now()
        tomorrow = today + datetime.timedelta(days=1)
        eightdays = today + datetime.timedelta(days=8)
        self.fields["start"].initial = tomorrow
        self.fields["finish"].initial = eightdays

    def clean(self):
        cleaned_data = super(Create, self).clean()
        start = cleaned_data.get("start")
        finish = cleaned_data.get("finish")
        if not start:
            raise ValidationError(_("ERROR_IMPOSSIBLE_START_DATE"))
        if not finish:
            raise ValidationError(_("ERROR_IMPOSSIBLE_FINISH_DATE"))
        _validate_borrow_timeframe(self.bike, start, finish)
        return cleaned_data


class Comment(Form):

    note = CharField(label=_("NOTE"), widget=Textarea)


class Cancel(Form):

    note = CharField(label=_("NOTE"), widget=Textarea)


class Rate(Form):

    note = CharField(label=_("NOTE"), widget=Textarea)
    rating = TypedChoiceField(choices=RATING_CHOICES, widget=RadioSelect)


class BorrowerEdit(Form):

    start = DateField(label=_("START"), widget=SelectDateWidget())
    finish = DateField(label=_("FINISH"), widget=SelectDateWidget())
    bike = ModelChoiceField(
            label=_("BIKE"), queryset=None, required=True, empty_label=None
    )
    note = CharField(label=_("NOTE"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        self.borrow = kwargs.pop("borrow")
        self.account = kwargs.pop("account")
        super(BorrowerEdit, self).__init__(*args, **kwargs)
        bikes = self.borrow.team.bikes.filter(active=True)
        self.fields["start"].initial = self.borrow.start
        self.fields["finish"].initial = self.borrow.finish
        self.fields["bike"].queryset = bikes
        self.fields["bike"].initial = self.borrow.bike

    def clean(self):
        cleaned_data = super(BorrowerEdit, self).clean()
        start = cleaned_data.get("start")
        finish = cleaned_data.get("finish")
        if not start:
            raise ValidationError(_("ERROR_IMPOSSIBLE_START_DATE"))
        if not finish:
            raise ValidationError(_("ERROR_IMPOSSIBLE_FINISH_DATE"))
        bike = cleaned_data.get("bike")
        _validate_borrow_timeframe(bike, start, finish)
        return cleaned_data


class LenderEditBike(Form):

    bike = ModelChoiceField(
            label=_("BIKE"), queryset=None, required=True, empty_label=None
    )
    note = CharField(label=_("NOTE"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        self.borrow = kwargs.pop("borrow")
        super(LenderEditBike, self).__init__(*args, **kwargs)
        bikes = self.borrow.team.bikes.filter(active=True)
        self.fields["bike"].queryset = bikes
        self.fields["bike"].initial = self.borrow.bike

    def clean(self):
        cleaned_data = super(LenderEditBike, self).clean()
        bike = cleaned_data.get("bike")
        start = self.borrow.start
        finish = self.borrow.finish
        if len(control.active_borrows_in_timeframe(bike, start, finish)):
            raise ValidationError(_("ERROR_OTHER_BORROW_IN_TIMEFRAME"))
        return cleaned_data


class LenderEditDest(Form):

    dest = ModelChoiceField(
            label=_("DESTINATION_STATION"), queryset=None, required=True, 
            validators=[validate_station_active], empty_label=None
    )
    note = CharField(label=_("NOTE"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        self.borrow = kwargs.pop("borrow")
        super(LenderEditDest, self).__init__(*args, **kwargs)
        stations = self.borrow.team.stations.filter(active=True)
        self.fields["dest"].queryset = stations
        self.fields["dest"].initial = self.borrow.dest


