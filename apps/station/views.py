# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from apps.account.models import Account
from apps.team.models import Team
from apps.team.utils import render_team_response as rtr
from apps.team.utils import assert_member
from apps.station.models import Station
from apps.station.forms import CreateStationForm


@login_required
@require_http_methods(["GET"])
def list(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    args = { "stations" : Station.objects.filter(team=team) }
    return rtr(team, "stations", request, "station/list.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def create(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    if request.method == "POST":
        form = CreateStationForm(request.POST, team=team, account=account)
        if form.is_valid():
            station = Station()
            station.team = team
            station.responsable = form.cleaned_data["responsable"]
            station.capacity = form.cleaned_data["capacity"]
            station.active = form.cleaned_data["active"]
            station.street = form.cleaned_data["street"].strip()
            station.city = form.cleaned_data["city"].strip()
            station.postalcode = form.cleaned_data["postalcode"].strip()
            station.country = form.cleaned_data["country"].strip()
            station.save()
            return HttpResponseRedirect("/%s/stations" % team.link)
    else:
        form = CreateStationForm(team=team, account=account)
    args = { "form" : form }
    return rtr(team, "stations", request, "station/create.html", args)

