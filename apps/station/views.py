# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import datetime

from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.forms import Form

from apps.common.shortcuts import render_response
from apps.account.models import Account
from apps.team import control as team_control
from apps.team.models import Team
from apps.team.utils import render_team_response as rtr
from apps.team.utils import assert_member
from apps.station.models import Station
from apps.station import forms
from apps.station import control


_VIEW = {
    "OVERVIEW" : {
        "template" : "station/view.html",
        "description_title" : "",
        "description_content" : "",
    },
    "BIKES" :    {
        "template" : "bike/list.html",
        "description_title" : _("STATION_BIKES_DESCRIPTION_TITLE"),
        "description_content" : _("STATION_BIKES_DESCRIPTION_CONTENT"),
    },
    "OUTGOING" : {
        "template" : "borrow/list.html",
        "description_title" : _("STATION_OUTGOING_DESCRIPTION_TITLE"),
        "description_content" : _("STATION_OUTGOING_DESCRIPTION_CONTENT"),
    },
    "INCOMING" : {
        "template" : "borrow/list.html",
        "description_title" : _("STATION_INCOMING_DESCRIPTION_TITLE"),
        "description_content" : _("STATION_INCOMING_DESCRIPTION_CONTENT"),
    },
}


def _tabs(station, team, selected):
    if team:
        base_link = "/%s/station/view/%d" % (team.link, station.id)
    else:
        base_link = "/station/view/%d" % station.id
    menu = [
        (base_link,              _("OVERVIEW"), selected == "OVERVIEW"),
        (base_link + "/bikes",   _("BIKES"),    selected == "BIKES"),
        (base_link + "/outgoing", _("OUTGOING"),  selected == "OUTGOING"),
        (base_link + "/incoming", _("INCOMING"),  selected == "INCOMING"),
    ]
    return menu


@login_required
@require_http_methods(["GET"])
def view(request, **kwargs):
    tab = kwargs["tab"]
    station_id = kwargs["station_id"]
    team_link = kwargs.get("team_link")
    account = get_object_or_404(Account, user=request.user)
    team = team_link and team_control.get_or_404(team_link)
    if team:
        assert_member(account, team)
        station = get_object_or_404(Station, id=station_id, team=team) 
    else:
        team = None
        station = get_object_or_404(Station, id=station_id, responsable=account)

    # load tab data
    today = datetime.datetime.now().date()
    bikes = []
    borrows = []
    if tab == "BIKES":
        bikes = station.bikes.all()
    elif tab == "OUTGOING":
        borrows = station.borrows_outgoing.filter(active=True, 
                                                  start__gte=today)
    elif tab == "INCOMING":
        borrows = station.borrows_incoming.filter(active=True, 
                                                  finish__gte=today)

    template_args = { 
        "station" : station, "bikes" : bikes, "borrows" : borrows,
        "description_title" : _VIEW[tab]["description_title"],
        "description_content" : _VIEW[tab]["description_content"],
        "tabs" : _tabs(station, team, tab),
    }
    template = _VIEW[tab]["template"]
    if team:
        return rtr(team, "stations", request, template, template_args)
    return render_response(request, template, template_args)


@login_required
@require_http_methods(["GET"])
def listing(request, **kwargs):
    team_link = kwargs.get("team_link")
    account = get_object_or_404(Account, user=request.user)
    columns = [
        _("RESPONSABLE"), _("POSTALCODE"), _("CITY"), _("STREET"), _("ACTIVE"),
    ]
    if team_link:
        team = team_control.get_or_404(team_link)
        assert_member(account, team)
        def station2entrie(s):
            return {
                "labels" : [ 
                    s.responsable, s.postalcode, s.city, s.street, s.active
                ], "url" : "/%s/station/view/%s" % (team.link, s.id)
            }
        stations = Station.objects.filter(team=team)
        entries = map(station2entrie, stations)
        args = { 
            "page_title" : _("STATIONS"),
            "list_data" : { "columns" : columns, "entries" : entries }
        }
        return rtr(team, "stations", request, "common/list.html", args)
    else:
        def station2entrie(s):
            return {
                "labels" : [ 
                    s.responsable, s.postalcode, s.city, s.street, s.active
                ], "url" : "/station/view/%s" % s.id
            }
        stations = Station.objects.filter(responsable=account)
        entries = map(station2entrie, stations)
        args = { 
            "page_title" : _("STATIONS"),
            "list_data" : { "columns" : columns, "entries" : entries }
        }
        return render_response(request, "common/list.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def create(request, team_link):
    team = team_control.get_or_404(team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    if request.method == "POST":
        form = forms.Create(request.POST, team=team, account=account)
        if form.is_valid():
            station = control.create(
                    account, team,
                    form.cleaned_data["responsable"],
                    form.cleaned_data["active"],
                    form.cleaned_data["street"].strip(),
                    form.cleaned_data["city"].strip(),
                    form.cleaned_data["postalcode"].strip()
            )
            url = "/%s/station/view/%s" % (team.link, station.id)
            return HttpResponseRedirect(url)
    else:
        form = forms.Create(team=team, account=account)
    args = { 
        "form" : form, "form_title" : _("ADD_STATION"),
        "cancel_url" : "/%s" % team.link
    }
    return rtr(team, "stations", request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def edit(request, team_link, station_id):
    account = get_object_or_404(Account, user=request.user)
    team = team_control.get_or_404(team_link)
    assert_member(account, team)
    station = get_object_or_404(Station, team=team, id=station_id)
    if request.method == "POST":
        form = forms.Edit(request.POST, station=station, account=account)
        if form.is_valid():
            station = control.edit( 
                    account, station,
                    form.cleaned_data["responsable"],
                    form.cleaned_data["active"],
                    form.cleaned_data["street"].strip(),
                    form.cleaned_data["city"].strip(),
                    form.cleaned_data["postalcode"].strip()
            )
            url = "/%s/station/view/%s" % (team.link, station.id)
            return HttpResponseRedirect(url)
    else:
        form = forms.Edit(station=station, account=account)
    args = { 
        "form" : form, "form_title" : _("ADD_STATION"),
        "cancel_url" : "/%s/station/view/%s" % (team.link, station.id)
    }
    return rtr(team, "stations", request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def delete(request, team_link, station_id):
    account = get_object_or_404(Account, user=request.user)
    team = team_control.get_or_404(team_link)
    assert_member(account, team)
    station = get_object_or_404(Station, team=team, id=station_id)
    if request.method == "POST":
        form = forms.Delete(request.POST, account=account, station=station)
        if form.is_valid():
            control.delete(account, station)
            return HttpResponseRedirect("/%s/stations" % team.link)
    else:
        form = forms.Delete(account=account, station=station)
    args = { 
        "form" : form, "form_title" : _("STATION_DELETE?"), 
        "form_subtitle" : str(station), 
        "cancel_url" : "/%s/station/view/%s" % (team.link, station.id)
    }
    return rtr(team, "stations", request, "common/form.html", args)


