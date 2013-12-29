# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import template
from django.utils.translation import ugettext as _

from apps.common.templatetags.common_tags import draw_action
from apps.common.templatetags.common_tags import draw_comment
from apps.common.templatetags.common_tags import draw_edit
from apps.borrow import control
from apps.team import control as team_control


register = template.Library()


@register.simple_tag
def borrow_draw_comment(account, borrow, team):
    if control.can_comment(account, borrow):
        url_prefix = team and "/%s" % team.link or ""
        url = "%s/borrow/comment/%s" % (url_prefix, borrow.id)
        return draw_comment(url)
    return ""


@register.simple_tag
def borrow_draw_borrower_edit(account, borrow):
    if control.borrower_can_edit(account, borrow):
        return draw_edit("/borrow/edit/%i" % borrow.id)
    return ""


@register.simple_tag
def borrow_draw_lender_edit_dest(account, borrow):
    if control.lender_can_edit_dest(account, borrow):
        url = "/%s/borrow/edit_dest/%i" % (borrow.team.link, borrow.id)
        image = "/static/famfamfam/pencil.png"
        return draw_action(image, "CHANGE_DEST", url)
    return ""


@register.simple_tag
def borrow_draw_lender_edit_bike(account, borrow):
    if control.lender_can_edit(account, borrow):
        url = "/%s/borrow/edit_bike/%i" % (borrow.team.link, borrow.id)
        image = "/static/famfamfam/pencil.png"
        return draw_action(image, "CHANGE_BIKE", url)
    return ""


@register.simple_tag
def borrow_draw(bike):
    if control.can_borrow(bike):
        image = "/static/famfamfam/arrow_rotate_clockwise.png"
        url = "/%s/borrow/create/%i" % (bike.team.link, bike.id)
        return draw_action(image, "BORROW", url)
    return ""


@register.simple_tag
def borrow_draw_respond(account, borrow):
    if control.can_respond(account, borrow):
        image = "/static/famfamfam/bullet_go.png"
        url = "/%s/borrow/respond/%i" % (borrow.team.link, borrow.id)
        return draw_action(image, "RESPOND", url)
    return ""


@register.simple_tag
def borrow_draw_cancel(account, borrow, team):
    if control.can_cancel(account, borrow):
        image = "/static/famfamfam/cancel.png"
        if team:
            url = "/%s/borrow/cancel/%i" % (team.link, borrow.id)
        else:
            url = "/borrow/cancel/%i" % borrow.id
        return draw_action(image, "CANCEL", url)
    return ""


@register.simple_tag
def borrow_draw_rate(account, borrow, team):
    if team and control.lender_can_rate(account, borrow):
        image = "/static/famfamfam/star.png"
        url = "/%s/borrow/rate/%i" % (borrow.team.link, borrow.id)
        return draw_action(image, "RATE", url)
    elif not team and control.borrower_can_rate(account, borrow):
        image = "/static/famfamfam/star.png"
        url = "/borrow/rate/%i" % borrow.id
        return draw_action(image, "RATE", url)
    return ""


@register.simple_tag
def borrow_draw_status(borrow):
    images = {
        "REQUEST" : "/static/famfamfam/arrow_rotate_clockwise.png",
        "ACCEPTED" : "/static/famfamfam/tick.png",
        "REJECTED" : "/static/famfamfam/cross.png",
        "CANCELED" : "/static/famfamfam/cancel.png",
        "FINISHED" : "/static/famfamfam/star.png",
    }
    return '<img src="%s" alt="%s">' % (images[borrow.state], borrow.state)


