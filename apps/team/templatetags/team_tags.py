# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import template
from django.utils.translation import ugettext as _

from apps.team.models import JoinRequest
from apps.team import control
from apps.common.templatetags.common_tags import condition_tag


register = template.Library()


@register.filter
def is_member(account, team): # TODO use condition_tag instead!
    return team and control.is_member(account, team)


@register.filter
def can_join(account, team): # TODO use control and condition_tag instead!
    member = is_member(account, team)
    requests = len(JoinRequest.objects.filter(team=team, requester=account)) > 0
    return not member and not requests


@register.tag
@condition_tag
def if_can_process_join_request(account, join_request):
    return control.can_process_join_request(account, join_request)


@register.tag
@condition_tag
def if_can_create_remove_request(requester, concerned, team):
    return control.can_create_remove_request(requester, concerned, team)


@register.tag
@condition_tag
def if_can_process_remove_request(account, remove_request):
    return control.can_process_remove_request(account, remove_request)


