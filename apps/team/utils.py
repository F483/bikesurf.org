# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from apps.common.shortcuts import render_response
from apps.page.models import Page
from apps.common.shortcuts import get_object_or_none
from apps.team import control


ENTRIE_NAMES = {
    "blog" : _("BLOG"),
    "bikes" : _("BIKES"),
    "members" : _("MEMBERS"),
    "borrows" : _("BORROWS"),
    "stations" : _("STATIONS"),
    "join_request/list" : _("JOIN_REQUESTS"),
    "remove_request/list" : _("REMOVE_REQUESTS"),
}


def assert_member(account, team):
    if not control.is_member(account, team):
        raise PermissionDenied


def _get_team_menue_public(team, current):
    """ return [(url, label, selected), ...] """
    url = lambda pl: "/%s/%s" % (team.link, pl)
    entrie = lambda e: (url(e), ENTRIE_NAMES[e], current==e)
    menu = [ 
        entrie("blog"),
        entrie("bikes"),
    ]
    page_entrie = lambda p: (url(p.link), p.name, p.link == current)
    return menu + map(page_entrie, team.pages.all())


def _get_team_menue_intern(team, current):
    """ return [(url, label, selected), ...] """
    url = lambda pl: "/%s/%s" % (team.link, pl)
    entrie = lambda e: (url(e), ENTRIE_NAMES[e], current==e)
    menu = [ 
        entrie("members"),
        entrie("borrows"),
        entrie("stations"),
        entrie("join_request/list"),
        entrie("remove_request/list"),
    ]
    return menu


def render_team_response(team, current, request, template, args):
    args.update({
        "team_menu_public" : _get_team_menue_public(team, current),
        "team_menu_intern" : _get_team_menue_intern(team, current),
        "current_team" : team,
        "current_team_links" : team.links.all(),
    })
    return render_response(request, template, args)


