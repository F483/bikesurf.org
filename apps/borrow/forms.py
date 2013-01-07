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
from django.forms.extras.widgets import SelectDateWidget
from apps.borrow.models import Borrow


class CreateBorrowForm(Form):

    start = DateField(label=_("START"), widget=SelectDateWidget())
    finish = DateField(label=_("FINISH"), widget=SelectDateWidget())
    application = CharField(label=_("APPLICATION"), widget=Textarea)

    def __init__(self, *args, **kwargs):
        self.bike = kwargs.pop("bike")
        super(CreateBorrowForm, self).__init__(*args, **kwargs)
        self.fields["start"].initial = datetime.datetime.now()
        self.fields["finish"].initial = datetime.datetime.now()

    def clean(self):
        cleaned_data = super(CreateBorrowForm, self).clean()
        today = datetime.datetime.now().date()
        start = cleaned_data.get("start")
        finish = cleaned_data.get("finish")

        # check bike
        if not self.bike.active:
            raise ValidationError(_("BIKE_INACTIVE"))
        if self.bike.reserve:
            raise ValidationError(_("RESERVE_BIKE"))
        if self.bike.station is None:
            raise ValidationError(_("NO_BIKE_STATION"))

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




