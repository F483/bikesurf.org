# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import template
from django.utils.translation import ugettext as _

from apps.team import control
from apps.common.templatetags.condition_tag import condition_tag


register = template.Library()


@register.tag
@condition_tag
def if_member(account, team):
    return account and control.is_member(account, team)


@register.tag
@condition_tag
def if_can_join(account, team):
    return account and control.can_join(account, team)


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


