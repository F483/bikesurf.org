# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from apps.account.models import Account
from apps.team.models import Team
from apps.bike.models import Bike
from apps.team.utils import render_team_response as rtr
from apps.team.utils import assert_member
from apps.bike.forms import CreateBikeForm


def _get_bike_filters(request, form):
    # filters 
    #  date from and to
    #  active (only members)
    #  reserve (only members)
    #  kind (default all)
    #  gender (default all)
    #  size (default all)
    #  lights (default all)
    #  fenders (default all)
    #  rack (default all)
    #  basket (default all)
    return {}


@require_http_methods(["GET"])
def list(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    filters = _get_bike_filters(request, None)
    args = { "bikes" :  team.bikes.filter(**filters) }
    return rtr(team, "bikes", request, "bike/list.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def create(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    if request.method == "POST":
        form = CreateBikeForm(request.POST, team=team, account=account)
        if form.is_valid():
            bike = Bike()
            bike.team = team
            bike.owner = form.cleaned_data["owner"]
            bike.name = form.cleaned_data["name"].strip()
            bike.description = form.cleaned_data["description"].strip()
            bike.active = form.cleaned_data["active"]
            bike.reserve = form.cleaned_data["reserve"]
            bike.station = form.cleaned_data["station"]
            bike.lockcode = form.cleaned_data["lockcode"]
            bike.keycode = form.cleaned_data["keycode"]
            bike.kind = form.cleaned_data["kind"]
            bike.gender = form.cleaned_data["gender"]
            bike.size = form.cleaned_data["size"]
            bike.lights = form.cleaned_data["lights"]
            bike.fenders = form.cleaned_data["fenders"]
            bike.basket = form.cleaned_data["rack"]
            bike.save()
            return HttpResponseRedirect("/%s/bikes" % team.link)
    else:
        form = CreateBikeForm(team=team, account=account)
    args = { "form" : form }
    return rtr(team, "bikes", request, "bike/create.html", args)


