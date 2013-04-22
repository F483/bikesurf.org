# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ValidationError

from apps.account.models import Account
from apps.common.shortcuts import COUNTRIES
from apps.station import control


class Create(forms.Form):

    responsable = forms.ModelChoiceField(label=_("RESPONSABLE"), queryset=None)
    country = forms.ChoiceField(choices=COUNTRIES, label=_('COUNTRY'))
    postalcode = forms.CharField(label=_('POSTALCODE'))
    city = forms.CharField(label=_('CITY'))
    street = forms.CharField(label=_('STREET'))
    active = forms.BooleanField(label=_("ACTIVE"), initial=True, required=False)

    def __init__(self, *args, **kwargs):
        team = kwargs.pop("team")
        account = kwargs.pop("account")
        super(Create, self).__init__(*args, **kwargs)
        self.fields["responsable"].queryset = team.members.all()
        self.fields["responsable"].initial = account
        self.fields["country"].initial = team.country.code
        self.fields["city"].initial = team.name


class Edit(forms.Form):

    responsable = forms.ModelChoiceField(label=_("RESPONSABLE"), queryset=None)
    country = forms.ChoiceField(choices=COUNTRIES, label=_('COUNTRY'))
    postalcode = forms.CharField(label=_('POSTALCODE'))
    city = forms.CharField(label=_('CITY'))
    street = forms.CharField(label=_('STREET'))
    active = forms.BooleanField(label=_("ACTIVE"), required=False)

    def __init__(self, *args, **kwargs):
        self.station = kwargs.pop("station")
        self.account = kwargs.pop("account")
        super(Edit, self).__init__(*args, **kwargs)
        self.fields["responsable"].queryset = self.station.team.members.all()
        self.fields["responsable"].initial = self.station.responsable
        self.fields["country"].initial = self.station.country.code
        self.fields["postalcode"].initial = self.station.postalcode
        self.fields["city"].initial = self.station.city
        self.fields["street"].initial = self.station.street
        self.fields["active"].initial = self.station.active

    def clean(self):
        cleaned_data = super(Edit, self).clean()
        if (not cleaned_data.get("active") and 
                not control.can_deactivate(self.account, self.station)):
            raise ValidationError(_("CANNOT_DEACTIVATE_STATION_IN_USE"))
        return cleaned_data


class Delete(forms.Form):

    def __init__(self, *args, **kwargs):
        self.station = kwargs.pop("station")
        self.account = kwargs.pop("account")
        super(Delete, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(Delete, self).clean()
        if not control.can_delete(self.account, self.station):
            raise ValidationError(_("CANNOT_DELETE_STATION_IN_USE"))
        return cleaned_data


# TODO add delete form with validation
