# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import datetime
from django.utils.translation import ugettext_lazy as _
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

from apps.borrow.models import Borrow
from apps.borrow.models import RATING_CHOICES
from apps.borrow import control
from apps.team import control as team_control


RESPONSE_CHOICES = [
    ("ACCEPTED", _("ACCEPTED")),
    ("MEETUP",   _("MEETUP")),
    ("REJECTED", _("REJECTED")),
]


class Respond(Form):
    
    response = ChoiceField(choices=RESPONSE_CHOICES, label=_('RESPONES'))
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
                raise ValidationError(_("TO_LATE_TO_ACCEPT"))
            if not self.borrow.bike.active:
                raise ValidationError(_("BIKE_NOT_ACTIVE"))
            if self.borrow.bike.reserve:
                raise ValidationError(_("IS_RESERVE_BIKE"))
            if not self.borrow.bike.station:
                raise ValidationError(_("BIKE_STATION_UNKNOWN"))
            if not self.borrow.bike.station.active:
                raise ValidationError(_("BIKE_STATION_INACTIVE"))
            if control.active_borrows_in_timeframe(bike, start, finish):
                raise ValidationError(_("OTHER_BORROW_IN_TIMEFRAME"))
        return cleaned_data


class Create(Form):

    start = DateField(label=_("START"), widget=SelectDateWidget())
    finish = DateField(label=_("FINISH"), widget=SelectDateWidget())
    note = CharField(label=_("NOTE"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        self.bike = kwargs.pop("bike")
        super(Create, self).__init__(*args, **kwargs)
        self.fields["start"].initial = datetime.datetime.now() # TODO add a day
        self.fields["finish"].initial = datetime.datetime.now() # TODO add 8 days

    def clean(self):
        cleaned_data = super(Create, self).clean()
        today = datetime.datetime.now().date()
        start = cleaned_data.get("start")
        finish = cleaned_data.get("finish")

        # check timeframe
        if start <= today:
            raise ValidationError(_("START_NOT_IN_FUTURE"))
        if finish < start:
            raise ValidationError(_("FINISH_BEFORE_START"))
        if len(control.active_borrows_in_timeframe(self.bike, start, finish)):
            raise ValidationError(_("OTHER_BORROW_IN_TIMEFRAME"))
        # TODO check for borrows from the same person in overlaping timeframes
        return cleaned_data


class Cancel(Form):

    note = CharField(label=_("NOTE"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        self.borrow = kwargs.pop("borrow")
        self.account = kwargs.pop("account")
        super(Cancel, self).__init__(*args, **kwargs)


class Rate(Form):

    note = CharField(label=_("NOTE"), widget=Textarea)
    rating = TypedChoiceField(choices=RATING_CHOICES, widget=RadioSelect)

    def __init__(self, *args, **kwargs):
        self.borrow = kwargs.pop("borrow")
        self.account = kwargs.pop("account")
        super(Rate, self).__init__(*args, **kwargs)

