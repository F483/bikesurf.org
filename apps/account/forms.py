# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import re
from django.utils.translation import ugettext as _
from django.forms import Form
from django.forms import CharField
from django.forms import ChoiceField
from django.forms import Textarea
from django.forms import ValidationError
from django.forms import ImageField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from apps.account.models import SOURCE_CHOICES
from apps.account import control
from apps.link.models import SITE_CHOICES
from apps.link import control as link_control


USERNAME_REGEX = UserCreationForm().fields['username'].regex


class SetPassport(Form):

    passport = ImageField(label=_("PASSPORT"))


class Edit(Form):

    username = CharField(max_length=30, label=_("USERNAME"), required=False)
    first_name = CharField(max_length=30, label=_("FIRST_NAME"), required=False)
    last_name = CharField(max_length=30, label=_("LAST_NAME"), required=False)
    mobile = CharField(max_length=1024, label=_("MOBILE"), required=False)
    source = ChoiceField(choices=SOURCE_CHOICES, label=_("SOURCE"), 
                         initial="OTHER")
    description = CharField(label=_("DESCRIPTION"), widget=Textarea, 
                            required=False)

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop("account")
        super(Edit, self).__init__(*args, **kwargs)
        self.fields["username"].initial = self.account.user.username
        self.fields["first_name"].initial = self.account.user.first_name
        self.fields["last_name"].initial = self.account.user.last_name
        self.fields["mobile"].initial = self.account.mobile
        self.fields["source"].initial = self.account.source
        self.fields["description"].initial = self.account.description

    def clean_username(self):
        value = self.cleaned_data["username"].strip()
        if not USERNAME_REGEX.match(value):
            raise ValidationError(_("ERROR_BAD_USERNAME_FORMAT"))
        try:
            User.objects.get(username__iexact=value)
        except User.DoesNotExist:
            return value
        if value != self.account.user.username:
            raise ValidationError(_("ERROR_USERNAME_TAKEN"))
        return value


class LinkCreate(Form):

    site = ChoiceField(choices=SITE_CHOICES, label=_("SITE"), required=True)
    profile = CharField(max_length=1024, label=_("PROFILE"), required=True)

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop("account")
        super(LinkCreate, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(LinkCreate, self).clean()
        profile = self.cleaned_data["profile"]
        site = self.cleaned_data["site"]
        if control.site_link_exists(self.account, site):
            raise ValidationError(_("ERROR_LINK_PROFILE_FOR_SITE_EXISTS"))
        if not link_control.valid_profile_format(profile, site):
            raise ValidationError(_("ERROR_BAD_PROFILE_FORMAT"))
        if not control.can_create_link(self.account, site, profile):
            raise ValidationError(_("ERROR_CANNOT_CREATE_LINK"))
        return cleaned_data


class LinkDelete(Form):

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop("account")
        self.link = kwargs.pop("link")
        super(LinkDelete, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(LinkDelete, self).clean()
        if not control.can_delete_link(self.account, self.link):
            raise ValidationError(_("ERROR_CANNOT_DELETE_LINK"))
        return cleaned_data

