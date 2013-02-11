# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from apps.common.shortcuts import render_response


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


def _get_team_menue(team, current):
    """ return [(url, label, selected, members_only), ...] """
    url = lambda pl: "/%s/%s" % (team.link, pl)
    entrie = lambda n, m: (url(n), ENTRIE_NAMES[n], current==n, m)
    menu = [ 
        entrie("blog", False),
        entrie("bikes", False),
        entrie("members", False),
        entrie("borrows", True),
        entrie("stations", True),
        entrie("join_requests", True),
        entrie("remove_requests", True),
    ]
    page_entrie = lambda p: (url(p.link), p.name, p.link == current, False)
    return menu + map(page_entrie, team.pages.all())


def render_team_response(team, current, request, template, args):
    args.update({
        "team_menu" : _get_team_menue(team, current),
        "current_team" : team,
    })
    return render_response(request, template, args)


