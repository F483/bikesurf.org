# -*- coding: utf-8 -*-
# Copyright (c) 2014 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE.TXT file)

import bleach
import markdown
import datetime
from django import template
from django.utils.safestring import mark_safe
from apps.common.templatetags.condition_tag import condition_tag
from django.utils.translation import ugettext as _

register = template.Library()

@register.simple_tag
def gen_qrcode(typenumber, tag_id, data):
  return """
    <div id="%(id)s"></div>
    <script type="text/javascript">
      append_qrcode(%(typenumber)s,"%(id)s","%(data)s");
    </script>
  """ % { "id" : tag_id, "data" : data, "typenumber" : typenumber }

@register.simple_tag
def render_button(label, url, button_classes, icon_classes=None):
  args = { 
    "label" : label, "url" : url, 
    "button_classes" : button_classes, 
    "icon_classes" : icon_classes 
  }
  if icon_classes:
    return """
      <a href="%(url)s" class="%(button_classes)s">
        <i class="%(icon_classes)s"></i> %(label)s
      </a>
    """ % args
  return """<a href="%(url)s" class="%(button_classes)s">%(label)s</a>""" % args

@register.simple_tag
def render_button_edit(label, url, button_classes):
  return render_button(label, url, button_classes, "fa fa-pencil")

@register.simple_tag
def render_button_delete(label, url, button_classes):
  return render_button(label, url, button_classes, "fa fa-trash-o")

@register.simple_tag
def render_button_cancel(label, url, button_classes):
  return render_button(label, url, button_classes, "fa fa-minus-circle")

@register.simple_tag
def render_boolean(value):
  if value:
    return """<i class="fa fa-check"></i>"""
  else:
    return """<i class="fa fa-times"></i>"""

@register.filter
def render_markdown(usertext):
  tags = [
    'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'h1', 'h2', 'h3', 
    'h4', 'h5', 'h6', 'hr', 'i', 'img', 'li', 'ol', 'p', 'pre', 'strong', 'ul'
  ]
  attributes = {
    'a': ['href', 'title'], 
    'abbr': ['title'], 
    'acronym': ['title'],
    'img' : ['src', 'alt', 'title']
  }
  html = markdown.markdown(usertext) # docs say use bleach instead of safe_mode 
  return mark_safe(bleach.clean(html, tags=tags, attributes=attributes))

@register.tag
@condition_tag
def if_user_in_group(user, groupname):
  return bool(user.groups.filter(name=groupname))

@register.filter
def mul(a, b):
  return a * b

@register.filter
def div(a, b):
  if not b:
    return b
  return a / b

@register.filter
def render_percent(ratio):
  percent = ratio * 100
  return "%0.1f%%" % percent

@register.filter
def unixtime_to_datetime(unixtime):
  return datetime.datetime.fromtimestamp(unixtime)

@register.filter
def unixtime_to_date(unixtime):
  return unixtime_to_datetime(unixtime).date()




ACTION_LABELS = { # TODO find a better way of doing this
        "BORROW" : _("BORROW"),
        "PROCESS_REQUEST" : _("PROCESS_REQUEST"),
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
        "SET_AS_PRIMARY_PICTURE" : _("SET_AS_PRIMARY_PICTURE"),
        "CHANGE_DEST" : _("CHANGE_DEST"),
        "CHANGE_BIKE" : _("CHANGE_BIKE"),
        "ADD_LINK" : _("ADD_LINK"),
        "REPLACE_LOGO" : _("REPLACE_LOGO"),
        "SET_PASSPORT" : _("SET_PASSPORT"),
        "CREATE_TEAM" : _("CREATE_TEAM"),
        "COMMENT" : _("COMMENT"),
        "CHANGE_PASSWORD" : _("CHANGE_PASSWORD"),
        "CHANGE_EMAIL" : _("CHANGE_EMAIL"),
}


@register.simple_tag
def draw_list_label(obj):
    if type(obj) == type(True):
        return draw_bool(obj)
    return obj


@register.simple_tag
def draw_bool(value):
    if bool(value):
        return '<img src="/static/famfamfam/tick.png" alt="%s">' % _("TRUE")
    return '<img src="/static/famfamfam/cross.png" alt="%s">' % _("FALSE")


@register.simple_tag
def draw_action(image, label, *args): 
    # TODO change to draw_action(image, label, format_url, *url_format_args)
    url = reduce(lambda a, b: str(a) + str(b), args)
    # TODO put this in teamplate instead
    return """
        <a href="%(url)s" class="action">
            <img src="%(image)s" alt="%(label)s"> %(label)s
        </a>
    """ % { "label" : ACTION_LABELS[label], "image" : image, "url" : url }


@register.simple_tag
def draw_delete(*args):
    return draw_action("/static/famfamfam/delete.png", "DELETE", *args)


@register.simple_tag
def draw_edit(*args):
    return draw_action("/static/famfamfam/pencil.png", "EDIT", *args)


@register.simple_tag
def draw_comment(*args):
    return draw_action("/static/famfamfam/comment_add.png", "COMMENT", *args)


@register.simple_tag
def draw_create(label, *args):
    return draw_action("/static/famfamfam/add.png", label, *args)





