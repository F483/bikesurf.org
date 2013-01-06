# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from apps.common.shortcuts import uslugify
from apps.page.models import Page


_RESERVED_NAMES = [
    u"blog",
    u"bikes",
    u"borrows",
    u"stations",
    u"members",
    u"join_request",
    u"join_requested",
    u"join_requests",
    u"join_request_process",
    u"remove_requests",
]


def _validate_name(value):
    name = value.strip()
    link = uslugify(name)
    if len(link) < 3:
        raise ValidationError(_("NAME_TO_SHORT"))
    if link in _RESERVED_NAMES:
        raise ValidationError(_("NAME_RESERVED"))
    if bool(len(Page.objects.filter(name=name, team=team))):
        raise ValidationError(_("NAME_USED"))
    if bool(len(Page.objects.filter(link=link, team=team))):
        raise ValidationError(_("NAME_USED"))


class CreatePageForm(forms.Form):

    name = forms.CharField(label=_("NAME"), validators=[_validate_name])
    content = forms.CharField(label=_("CONTENT"), widget=forms.Textarea)
    order = forms.IntegerField(label=_("ORDER"))


