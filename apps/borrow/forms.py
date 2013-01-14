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
from apps.borrow import control


RESPONSES = [
    "ACCEPTED",
    "MEETUP",
    "REJECTED",
]
RESPONSE_CHOICES = [(response, _(response)) for response in RESPONSES]


class Respond(Form):
    
    response = ChoiceField(choices=RESPONSE_CHOICES, label=_('RESPONES'))
    note = CharField(label=_("NOTE"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        self.borrow = kwargs.pop("borrow")
        self.account = kwargs.pop("account")
        super(Respond, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(Respond, self).clean()

        # sanity check
        if self.account not in self.borrow.bike.team.members.all():
            raise PermissionDenied
        if self.borrow.state != "REQUEST":
            raise PermissionDenied
        if self.borrow.active:
            raise Exception("This should NEVER be possable!")

        # check request is still valid
        if cleaned_data.get("response") != "REJECTED":
            today = datetime.datetime.now().date()
            if self.borrow.start <= today:
                raise ValidationError(_("START_TIME_PASSED"))
            if not self.borrow.bike.active:
                raise ValidationError(_("BIKE_NOT_ACTIVE"))

        return cleaned_data


class Create(Form):

    start = DateField(label=_("START"), widget=SelectDateWidget())
    finish = DateField(label=_("FINISH"), widget=SelectDateWidget())
    note = CharField(label=_("NOTE"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        self.bike = kwargs.pop("bike")
        super(Create, self).__init__(*args, **kwargs)
        self.fields["start"].initial = datetime.datetime.now()
        self.fields["finish"].initial = datetime.datetime.now()

    def clean(self):
        cleaned_data = super(Create, self).clean()
        today = datetime.datetime.now().date()
        start = cleaned_data.get("start")
        finish = cleaned_data.get("finish")

        # check bike
        if not self.bike.active:
            raise PermissionDenied
        if self.bike.reserve:
            raise PermissionDenied
        if not self.bike.station:
            raise PermissionDenied

        # check timeframe
        if start <= today:
            raise ValidationError(_("START_NOT_IN_FUTURE"))
        if finish < start:
            raise ValidationError(_("FINISH_BEFORE_START"))
        
        # other borrows starting in timeframe
        if len(Borrow.objects.filter(bike=self.bike, active=True, 
                                     start__gte=start, start__lte=finish)):
            raise ValidationError(_("OTHER_BORROW_IN_TIMEFRAME"))

        # other borrows finishing in timeframe
        if len(Borrow.objects.filter(bike=self.bike, active=True,
                                     finish__gte=start, finish__lte=finish)):
            raise ValidationError(_("OTHER_BORROW_IN_TIMEFRAME"))

        return cleaned_data


class Cancel(Form):

    note = CharField(label=_("NOTE"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        self.borrow = kwargs.pop("borrow")
        self.account = kwargs.pop("account")
        super(Cancel, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(Cancel, self).clean()
        if not control.can_cancel(self.account, self.borrow): # TODO test it
            raise PermissionDenied
        return cleaned_data



RATING_CHOICES = [
    (0, _("0")),
    (1, _("1")),
    (2, _("2")),
    (3, _("3")),
    (4, _("4")),
    (5, _("5")),
]

class RateTeam(Form):

    note = CharField(label=_("NOTE"), widget=Textarea)
    rating = TypedChoiceField(choices=RATING_CHOICES, widget=RadioSelect, coerce=int)

    def __init__(self, *args, **kwargs):
        self.borrow = kwargs.pop("borrow")
        self.account = kwargs.pop("account")
        super(RateTeam, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RateTeam, self).clean()
        if not control.can_rate_team(self.account, self.borrow): # TODO test it
            raise PermissionDenied
        return cleaned_data


