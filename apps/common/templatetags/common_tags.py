# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django import template
from django.utils.translation import ugettext as _


ACTION_LABELS = { # TODO find a better way of doing this
        "BORROW" : _("BORROW"),
        "RESPOND" : _("RESPOND"),
        "CANCEL" : _("CANCEL"),
        "RATE" : _("RATE"),
        "DELETE" : _("DELETE"),
        "EDIT" : _("EDIT"),
        "ADD_BLOG" : _("ADD_BLOG"),
        "ADD_PAGE" : _("ADD_PAGE"),
        "BIKE_CREATE" : _("BIKE_CREATE"),
        "ADD_STATION" : _("ADD_STATION"),
        "ADD_PICTURE" : _("ADD_PICTURE"),
        "SET_PRIMARY_PICTURE" : _("SET_PRIMARY_PICTURE")
}


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
    """ % { "label" : ACTION_LABELS[label], "image" : image, "url" : url }


@register.simple_tag
def draw_delete(*args):
    return draw_action("/static/famfamfam/delete.png", "DELETE", *args)


@register.simple_tag
def draw_edit(*args):
    return draw_action("/static/famfamfam/pencil.png", "EDIT", *args)


@register.simple_tag
def draw_create(label, *args):
    return draw_action("/static/famfamfam/add.png", label, *args)

