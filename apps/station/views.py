# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from apps.account.models import Account
from apps.team.models import Team
from apps.team.utils import render_team_response as rtr
from apps.team.utils import assert_member
from apps.station.models import Station


@login_required
@require_http_methods(["GET"])
def list(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    args = { "stations" : Station.objects.filter(owner__team=team) }
    return rtr(team, "stations", request, "station/list.html", args)


