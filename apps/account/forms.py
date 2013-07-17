# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext as _
from django.forms import Form
from django.forms import CharField
from django.forms import ChoiceField
from django.forms import Textarea
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from apps.account.models import SOURCE_CHOICES


USERNAME_REGEX = UserCreationForm().fields['username'].regex


class Edit(Form):

    username = CharField(max_length=30, label=_("USERNAME"), required=False)
    first_name = CharField(max_length=30, label=_("FIRST_NAME"), required=False)
    last_name = CharField(max_length=30, label=_("LAST_NAME"), required=False)
    mobile = CharField(max_length=1024, label=_("MOBILE"), required=False)
    source = ChoiceField(choices=SOURCE_CHOICES, label=_("SOURCE"), 
                         initial="OTHER")
    description = CharField(label=_("DESCRIPTION"), widget=Textarea, 
                            required=False)

    # TODO show help text (name and mobile private)

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
        # copied from /usr/local/lib/python2.7/dist-packages/allauth/account/forms.py
        value = self.cleaned_data["username"]
        if not USERNAME_REGEX.match(value):
            raise ValidationError(_("Usernames can only contain "
                                    "letters, digits and @/./+/-/_."))
        try:
            User.objects.get(username__iexact=value)
        except User.DoesNotExist:
            return value
        raise ValidationError(_("This username is already taken. Please "
                                "choose another."))


