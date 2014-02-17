# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import datetime

from django.utils.translation import ugettext as _
from django.forms import Form
from django.forms import BooleanField
from django.forms import DateField
from django.forms import ValidationError
from django.forms import CharField
from django.forms import Textarea
from django.forms import ChoiceField
from django.forms import TypedChoiceField
from django.forms import RadioSelect
from django.forms.widgets import DateInput
from django.core.exceptions import PermissionDenied
from django.forms import ModelChoiceField
from django.utils.safestring import mark_safe

from apps.borrow.models import Borrow
from apps.borrow.models import RATING_CHOICES, STATE_FILTER_CHOICES
from apps.borrow import control
from apps.team import control as team_control
from apps.account import control as account_control
from apps.station.forms import validate_station_active


RESPONSE_CHOICES = [
    ("ACCEPTED", _("ACCEPTED")),
    ("REJECTED", _("REJECTED")),
]


def _validate_borrow_timeframe(bike, start, finish, exclude=None, 
                               timetraveler=False):
    if not start:
        raise ValidationError(_("ERROR_IMPOSSIBLE_START_DATE"))
    if not finish:
        raise ValidationError(_("ERROR_IMPOSSIBLE_FINISH_DATE"))
    if finish < start:
        raise ValidationError(_("ERROR_FINISH_BEFORE_START"))
    today = datetime.datetime.now().date()
    if not timetraveler and start <= today:
        raise ValidationError(_("ERROR_START_NOT_IN_FUTURE"))
    if len(control.active_borrows_in_timeframe(bike, start, finish, 
                                               exclude=exclude)):
        raise ValidationError(_("ERROR_OTHER_BORROW_IN_TIMEFRAME"))


class FilterListing(Form): 

    bike = ModelChoiceField(
            label=_("BIKE"), queryset=None, required=False, empty_label=_("ALL")
    )
    state = ChoiceField(
            label=_("STATE"), choices=STATE_FILTER_CHOICES, initial="", 
            required=False
    )
    src = ModelChoiceField(
            label=_("STATION_FROM"), queryset=None, 
            required=False, empty_label=_("ALL")
    )
    dest = ModelChoiceField(
            label=_("STATION_TO"), queryset=None, 
            required=False, empty_label=_("ALL")
    )
    future = BooleanField(
            label=_("FUTURE_BORROWS"), initial=True, required=False
    )
    ongoing = BooleanField(
            label=_("ONGOING_BORROWS"), initial=True, required=False
    )
    past = BooleanField(
            label=_("PAST_BORROWS"), initial=False, required=False
    )

    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop("team")
        super(FilterListing, self).__init__(*args, **kwargs)
        self.fields["bike"].queryset = self.team.bikes.all()
        #self.fields["bike"].initial = self.borrow.bike
        stations = self.team.stations.all()
        self.fields["dest"].queryset = stations
        #self.fields["dest"].initial = self.borrow.dest
        self.fields["src"].queryset = stations
        #self.fields["src"].initial = self.borrow.dest


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

    start = DateField(
        label=_("START"), 
        widget=DateInput(attrs={'class': 'datepicker', 'readonly':' true'}), 
    )
    finish = DateField(
        label=_("FINISH"), 
        widget=DateInput(attrs={'class': 'datepicker', 'readonly':' true'}), 
    )

    note = CharField(label=_("BORROW_NOTE"), widget=Textarea)
    terms_accepted = BooleanField(label=mark_safe(_("ACCEPT_TERMS")), initial=False)
    # TODO have you donated? (use note for this)
    # TODO why do you want to bikesurf in xxx (use note for this)
    # TODO feedback (use note for this)
    #  \_ cat together with seperators and save in note

    # TODO receive newsletter (were spamming people?)
    # TODO link to terms

    def __init__(self, *args, **kwargs):
        self.bike = kwargs.pop("bike")
        self.account = kwargs.pop("account")
        start = kwargs.pop("start")
        finish = kwargs.pop("finish")
        super(Create, self).__init__(*args, **kwargs)
        today = datetime.datetime.now()
        start = start and start or (today + datetime.timedelta(days=1))
        finish = finish and finish or (start + datetime.timedelta(days=8))
        self.fields["start"].initial = start
        self.fields["finish"].initial = finish

    def clean(self):
        cleaned_data = super(Create, self).clean()

        # check timeframe
        start = cleaned_data.get("start")
        finish = cleaned_data.get("finish")
        _validate_borrow_timeframe(self.bike, start, finish)

        # must accept terms
        if not cleaned_data.get("terms_accepted"):
            raise ValidationError(_("ERROR_MUST_ACCEPT_TERMS"))

        # must have full name
        if not account_control.has_fullname(self.account):
            raise ValidationError(_("ERROR_ACCOUNT_REQUIRES_FULLNAME"))

        # must have a mobile
        if not account_control.has_mobile(self.account):
            raise ValidationError(_("ERROR_ACCOUNT_REQUIRES_MOBILE"))

        # must have a passport
        if not account_control.has_passport(self.account):
            raise ValidationError(_("ERROR_ACCOUNT_REQUIRES_PASSPORT"))

        # must have a other references
        if not account_control.has_other_references(self.account):
            raise ValidationError(_("ERROR_ACCOUNT_REQUIRES_OTHER_REFERENCES"))

        return cleaned_data


class Comment(Form):

    note = CharField(label=_("NOTE"), widget=Textarea)


class Cancel(Form):

    note = CharField(label=_("NOTE"), widget=Textarea)


class Rate(Form):

    note = CharField(label=_("NOTE"), widget=Textarea)
    rating = TypedChoiceField(choices=RATING_CHOICES, widget=RadioSelect)


class Edit(Form):

    start = DateField(
        label=_("START"), 
        widget=DateInput(attrs={'class': 'datepicker', 'readonly':' true'}), 
    )
    finish = DateField(
        label=_("FINISH"), 
        widget=DateInput(attrs={'class': 'datepicker', 'readonly':' true'}), 
    )
    bike = ModelChoiceField(
        label=_("BIKE"), queryset=None, required=True, empty_label=None
    )
    note = CharField(label=_("NOTE"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        self.borrow = kwargs.pop("borrow")
        super(Edit, self).__init__(*args, **kwargs)
        bikes = self.borrow.team.bikes.filter(active=True)
        self.fields["start"].initial = self.borrow.start
        self.fields["finish"].initial = self.borrow.finish
        self.fields["bike"].queryset = bikes
        self.fields["bike"].initial = self.borrow.bike

    def clean(self):
        cleaned_data = super(Edit, self).clean()
        start = cleaned_data.get("start")
        finish = cleaned_data.get("finish")
        bike = cleaned_data.get("bike")
        _validate_borrow_timeframe(bike, start, finish, exclude=self.borrow, 
                                   timetraveler=True)
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


