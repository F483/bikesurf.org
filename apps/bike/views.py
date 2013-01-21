# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from apps.common.shortcuts import render_response
from apps.account.models import Account
from apps.team.models import Team
from apps.bike.models import Bike
from apps.team.utils import render_team_response as rtr
from apps.team.utils import assert_member
from apps.bike import forms

_VIEW = {
    "OVERVIEW" : {
        "template" : "bike/view.html",
        "description_title" : "",
        "description_content" : "",
    },
    "BORROWS" :    {
        "template" : "borrow/list.html",
        "description_title" : _("BIKE_BORROWS_DESCRIPTION_TITLE"),
        "description_content" : _("BIKE_BORROWS_DESCRIPTION_CONTENT"),
    },
}

def _tabs(bike, team, selected, authorized):
    if team:
        base_link = "/%s/bike/view/%d" % (team.link, bike.id)
    else:
        base_link = "/bike/view/%d" % bike.id
    overview = (base_link,              _("OVERVIEW"), selected == "OVERVIEW")
    borrows =  (base_link + "/borrows", _("BORROWS"),  selected == "BORROWS")
    if authorized:
        return [overview, borrows]
    return [overview]


def _get_bike_filters(request, form, team):
    filters = {}
    logged_in = request.user.is_authenticated()
    account = logged_in and get_object_or_404(Account, user=request.user) or 0
    if not logged_in or account not in team.members.all():
        filters.update({ "reserve" : False, "active" : True })

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
    return filters


@require_http_methods(["GET"])
def view(request, **kwargs):
    tab = kwargs["tab"]
    bike_id = kwargs["bike_id"]
    team_link = kwargs.get("team_link")
    team = team_link and get_object_or_404(Team, link=team_link) or None

    requires_login = not team or tab != "OVERVIEW"
    requires_membership = team and tab != "OVERVIEW"
    logged_in = request.user.is_authenticated()

    if not logged_in and requires_login:
        raise Exception("TODO login redirect")
    account = logged_in and get_object_or_404(Account, user=request.user)
    if requires_membership and account not in team.members.all():
        raise PermissionDenied

    if team:
        bike = get_object_or_404(Bike, id=bike_id, team=team)
    else:
        bike = get_object_or_404(Bike, id=bike_id, owner=account)

    authorized = (account and account == bike.owner or 
                  account and account in bike.members.all())

    template = _VIEW[tab]["template"]
    args = { 
        "bike" : bike, 
        "borrows" : bike.borrows.all(),
        "description_title" : _VIEW[tab]["description_title"],
        "description_content" : _VIEW[tab]["description_content"],
        "tabs" : _tabs(bike, team, tab, authorized), 
    }
    if team:
        return rtr(team, "bikes", request, template, args)
    return render_response(request, template, args)


@require_http_methods(["GET"])
def list_team(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    filters = _get_bike_filters(request, None, team)
    args = { "bikes" :  team.bikes.filter(**filters) }
    return rtr(team, "bikes", request, "bike/list.html", args)


@login_required
@require_http_methods(["GET"])
def list_my(request):
    account = get_object_or_404(Account, user=request.user)
    args = { "bikes" :  Bike.objects.filter(owner=account) }
    return render_response(request, "bike/list.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def create(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    if request.method == "POST":
        form = forms.Create(request.POST, team=team, account=account)
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
            url = "/%s/bike/view/%s" % (team.link, bike.id)
            return HttpResponseRedirect(url)
    else:
        form = forms.Create(team=team, account=account)
    args = { "form" : form, "form_title" : _("BIKE_CREATE") }
    return rtr(team, "bikes", request, "form.html", args)


