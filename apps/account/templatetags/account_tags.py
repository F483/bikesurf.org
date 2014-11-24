# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import template
from django.utils.translation import ugettext as _
from apps.common.templatetags.condition_tag import condition_tag
from apps.account import control


register = template.Library()


@register.tag
@condition_tag
def if_can_view_account(current_account, view_account):
    return (current_account and view_account and 
            control.can_view_account(current_account, view_account))

