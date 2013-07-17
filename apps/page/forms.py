# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import forms
from django.utils.translation import ugettext as _
from sanitizer.forms import SanitizedCharField
from apps.common.shortcuts import uslugify
from apps.page.models import Page
from config.settings import SANITIZER_ALLOWED_TAGS, SANITIZER_ALLOWED_ATTRIBUTES


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


class CreatePageForm(forms.Form):

    name = forms.CharField(label=_("PAGE_NAME"))
    content = SanitizedCharField(label=_("CONTENT"), widget=forms.Textarea,
                                 max_length=50000, allowed_tags=SANITIZER_ALLOWED_TAGS,
                                 allowed_attributes=SANITIZER_ALLOWED_ATTRIBUTES, 
                                 strip=False)
    order = forms.IntegerField(label=_("ORDER"), required=False)

    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop("team")
        super(CreatePageForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CreatePageForm, self).clean()
        name = cleaned_data.get("name").strip()
        link = uslugify(name)
        if len(link) < 3:
            raise forms.ValidationError(_("NAME_TO_SHORT"))
        if link in _RESERVED_NAMES:
            raise forms.ValidationError(_("NAME_RESERVED"))
        if bool(len(Page.objects.filter(name=name, team=self.team))):
            raise forms.ValidationError(_("NAME_USED"))
        if bool(len(Page.objects.filter(link=link, team=self.team))):
            raise forms.ValidationError(_("NAME_USED"))
        return cleaned_data


class EditPageForm(forms.Form):

    name = forms.CharField(label=_("PAGE_NAME"))
    content = SanitizedCharField(label=_("CONTENT"), widget=forms.Textarea,
                                 max_length=50000, allowed_tags=SANITIZER_ALLOWED_TAGS,
                                 allowed_attributes=SANITIZER_ALLOWED_ATTRIBUTES, 
                                 strip=False)
    order = forms.IntegerField(label=_("ORDER"), required=False)

    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop("page")
        super(EditPageForm, self).__init__(*args, **kwargs)
        self.fields["name"].initial = self.page.name
        self.fields["content"].initial = self.page.content
        self.fields["order"].initial = self.page.order

    def clean(self):
        cleaned_data = super(EditPageForm, self).clean()
        name = cleaned_data.get("name").strip()
        link = uslugify(name)
        if len(link) < 3:
            raise forms.ValidationError(_("NAME_TO_SHORT"))
        if link in _RESERVED_NAMES:
            raise forms.ValidationError(_("NAME_RESERVED"))
        if len(Page.objects.filter(name=name, team=self.page.team)) > 1:
            raise forms.ValidationError(_("NAME_USED"))
        if len(Page.objects.filter(link=link, team=self.page.team)) > 1:
            raise forms.ValidationError(_("NAME_USED"))
        return cleaned_data


