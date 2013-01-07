# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import template
from django.utils.translation import ugettext as _

from apps.team.models import JoinRequest


register = template.Library()


@register.simple_tag
def draw_bool(value):
    if bool(value):
        return '<img src="/static/famfamfam/tick.png" alt="%s">' % _("TRUE")
    return '<img src="/static/famfamfam/cross.png" alt="%s">' % _("FALSE")


@register.simple_tag
def draw_action(image, label, *args):
    url = reduce(lambda a, b: str(a) + str(b), args)
    return """
        <a href="%(url)s"> 
            %(label)s <img src="%(image)s" alt="%(label)s"> 
        </a>
    """ % { "label" : _(label), "image" : image, "url" : url }


# TODO move to borrow app
@register.simple_tag
def draw_borrow(*args):
    image = "/static/famfamfam/arrow_rotate_clockwise.png"
    return draw_action(image, "BORROW", *args)


@register.simple_tag
def draw_delete(*args):
    return draw_action("/static/famfamfam/delete.png", "DELETE", *args)


@register.simple_tag
def draw_edit(*args):
    return draw_action("/static/famfamfam/pencil.png", "EDIT", *args)


@register.simple_tag
def draw_create(label, *args):
    return draw_action("/static/famfamfam/add.png", label, *args)


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


