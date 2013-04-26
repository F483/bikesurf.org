# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import template
from django.utils.translation import ugettext as _

from apps.common.templatetags.common_tags import draw_action
from apps.borrow import control
from apps.team import control as team_control


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
    is_request = borrow.state == "REQUEST"
    if is_request and team_control.is_member(account, borrow.bike.team):
        image = "/static/famfamfam/bullet_go.png"
        url = "/%s/borrow/respond/%i" % (borrow.bike.team.link, borrow.id)
        return draw_action(image, "RESPOND", url)
    return ""


@register.simple_tag
def draw_cancel(account, borrow, team):
    if control.can_cancel(account, borrow):
        image = "/static/famfamfam/cancel.png"
        if team:
            url = "/%s/borrow/cancel/%i" % (team.link, borrow.id)
        else:
            url = "/borrow/cancel/%i" % borrow.id
        return draw_action(image, "CANCEL", url)
    return ""


@register.simple_tag
def draw_rate(account, borrow, team):
    if team and control.can_rate_team(account, borrow):
        image = "/static/famfamfam/star.png"
        url = "/%s/borrow/rate/%i" % (borrow.bike.team.link, borrow.id)
        return draw_action(image, "RATE", url)
    elif not team and control.can_rate_my(account, borrow):
        image = "/static/famfamfam/star.png"
        url = "/borrow/rate/%i" % borrow.id
        return draw_action(image, "RATE", url)
    return ""


@register.simple_tag
def draw_status(borrow):
    images = {
        "REQUEST" : "/static/famfamfam/arrow_rotate_clockwise.png",
        "MEETUP" : "/static/famfamfam/cup.png",
        "ACCEPTED" : "/static/famfamfam/tick.png",
        "REJECTED" : "/static/famfamfam/cross.png",
        "CANCELED" : "/static/famfamfam/cancel.png",
        "FINISHED" : "/static/famfamfam/star.png",
    }
    return '<img src="%s" alt="%s">' % (images[borrow.state], borrow.state)


