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


_RESERVED_NAMES = [
    u"team",
]

def _validate_name(value):
    name = value.strip()
    link = uslugify(name)
    if len(link) < 3:
        raise ValidationError(_("NAME_TO_SHORT"))
    if link in _RESERVED_NAMES:
        raise ValidationError(_("NAME_RESERVED"))
    if bool(len(Team.objects.filter(link=link))):
        raise ValidationError(_("NAME_USED"))
    if bool(len(Team.objects.filter(name=name))):
        raise ValidationError(_("NAME_USED"))


class CreateTeam(Form):

    name    = CharField(label=_('TEAM_NAME'), validators=[_validate_name])
    country = ChoiceField(choices=COUNTRIES, label=_('COUNTRY'))
    logo   = ImageField(label=_("LOGO"))


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


