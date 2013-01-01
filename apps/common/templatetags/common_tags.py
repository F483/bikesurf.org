# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import template
from apps.team.models import JoinRequest


register = template.Library()


@register.simple_tag
def draw_bool(value):
    if bool(value):
        return '<img src="/static/icons/accept.png">'
    return '<img src="/static/icons/reject.png">'


# TODO move to team app
@register.filter
def is_member(account, team):
    return account in team.members.all()


# TODO move to team app
@register.filter
def can_join(account, team):
    member = is_member(account, team)
    requests = len(JoinRequest.objects.filter(team=team, requester=account)) > 0
    return not member and not requests


