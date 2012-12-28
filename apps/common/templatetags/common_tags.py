# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import template


register = template.Library()


@register.simple_tag
def draw_bool(value):
    if bool(value):
        return '<img src="/static/icons/accept.png">'
    return '<img src="/static/icons/reject.png">'


