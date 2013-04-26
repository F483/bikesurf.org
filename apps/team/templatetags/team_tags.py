# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import template
from django.utils.translation import ugettext as _

from apps.team.models import JoinRequest
from apps.team import control


register = template.Library()


@register.filter
def is_member(account, team): # TODO use condition_tag instead?
    return team and control.is_member(account, team)


@register.filter
def can_join(account, team): # TODO use control instead?
    member = is_member(account, team)
    requests = len(JoinRequest.objects.filter(team=team, requester=account)) > 0
    return not member and not requests


