# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from apps.common.shortcuts import render_response
from apps.page.models import Page
from apps.common.shortcuts import get_object_or_none


ENTRIE_NAMES = {
    "blog" : _("BLOG"),
    "bikes" : _("BIKES"),
    "members" : _("MEMBERS"),
    "borrows" : _("BORROWS"),
    "stations" : _("STATIONS"),
    "join_requests" : _("JOIN_REQUESTS"),
    "remove_requests" : _("REMOVE_REQUESTS"),
}


def assert_member(account, team):
    if account not in team.members.all():
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
        entrie("join_requests"),
        entrie("remove_requests"),
    ]
    return menu


def render_team_response(team, current, request, template, args):
    donate_page = get_object_or_none(Page, team=team, link="donate")
    args.update({
        "team_menu_public" : _get_team_menue_public(team, current),
        "team_menu_intern" : _get_team_menue_intern(team, current),
        "current_team" : team,
        "donation_page" : donate_page,
    })
    return render_response(request, template, args)


