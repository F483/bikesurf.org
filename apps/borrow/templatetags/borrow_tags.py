# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import template
from django.utils.translation import ugettext as _

from apps.common.templatetags.common_tags import draw_action


register = template.Library()


@register.simple_tag
def draw_borrow(bike):
    if bike.active and not bike.reserve and bike.station:
        image = "/static/famfamfam/arrow_rotate_clockwise.png"
        url = "/%s/borrow/create/%i" % (bike.team.link, bike.id)
        return draw_action(image, "BORROW", url)
    return ""


@register.simple_tag
def draw_respond(account, borrow):
    if borrow.state == "REQUEST" and account in borrow.bike.team.members.all():
        image = "/static/famfamfam/bullet_go.png"
        url = "/%s/borrow/respond/%i" % (borrow.bike.team.link, borrow.id)
        return draw_action(image, "RESPOND", url)
    return ""


