# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms import ImageField
from django.forms import ChoiceField
from django.forms import CharField
from django.forms import Textarea

from apps.common.shortcuts import uslugify
from apps.team.models import STATUS_CHOICES
from apps.team.models import Team
from apps.common.shortcuts import COUNTRIES
from apps.link.models import SITE_CHOICES
from apps.team import control
from apps.link import control as link_control


_RESERVED_NAMES = [
    u"team",
]

def _validate_name(value):
    name = value.strip()
    link = uslugify(name)
    if len(link) < 3:
        raise ValidationError(_("ERROR_NAME_TO_SHORT"))
    if link in _RESERVED_NAMES:
        raise ValidationError(_("ERROR_NAME_RESERVED"))
    if bool(len(Team.objects.filter(link=link))):
        raise ValidationError(_("ERROR_NAME_USED"))
    if bool(len(Team.objects.filter(name=name))):
        raise ValidationError(_("ERROR_NAME_USED"))


class ReplaceLogo(Form):

    logo        = ImageField(label=_("LOGO"))


class CreateTeam(Form):

    name        = CharField(label=_('TEAM_NAME'), validators=[_validate_name])
    country     = ChoiceField(choices=COUNTRIES, label=_('COUNTRY'))
    logo        = ImageField(label=_("LOGO"))
    application = CharField(label=_('APPLICATION'), widget=Textarea)


class CreateJoinRequest(Form):

    application = CharField(label=_('JOIN_REQUEST_REASON'), widget=Textarea)


class ProcessJoinRequest(Form):

    response = CharField(label=_('RESPONSE'), widget=Textarea)
    status   = ChoiceField(choices=STATUS_CHOICES[1:], label=_('STATUS'))


class CreateRemoveRequest(Form):

    reason = CharField(label=_('REASON'), widget=Textarea)


class ProcessRemoveRequest(Form):

    response = CharField(label=_('RESPONSE'), widget=Textarea)
    status = ChoiceField(choices=STATUS_CHOICES[1:], label=_('STATUS'))


class LinkCreate(Form):

    site = ChoiceField(choices=SITE_CHOICES, label=_("SITE"), required=True)
    profile = CharField(max_length=1024, label=_("URL"), required=True)

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop("account")
        self.team = kwargs.pop("team")
        super(LinkCreate, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(LinkCreate, self).clean()
        profile = self.cleaned_data["profile"]
        site = self.cleaned_data["site"]
        if control.site_link_exists(self.team, site):
            raise ValidationError(_("ERROR_LINK_PROFILE_FOR_SITE_EXISTS"))
        if not link_control.valid_profile_format(profile, site):
            raise ValidationError(_("ERROR_BAD_PROFILE_FORMAT"))
        if not control.can_create_link(self.account, self.team, site, profile):
            raise ValidationError(_("ERROR_CANNOT_CREATE_LINK"))
        return cleaned_data


class LinkDelete(Form):

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop("account")
        self.link = kwargs.pop("link")
        self.team = kwargs.pop("team")
        super(LinkDelete, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(LinkDelete, self).clean()
        if not control.can_delete_link(self.account, self.team, self.link):
            raise ValidationError(_("ERROR_CANNOT_DELETE_LINK"))
        return cleaned_data

