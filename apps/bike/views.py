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
from apps.bike import control
from apps.team.utils import render_team_response as rtr
from apps.team.utils import assert_member
from apps.bike import forms
from django.forms import Form


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
    base_link = "/%s/bike/view/%d" % (team.link, bike.id)
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
    #  size (default all)
    #  lights (default all)
    return filters


@require_http_methods(["GET"])
def view(request, team_link, bike_id, tab):
    team = get_object_or_404(Team, link=team_link)
    requires_login = tab != "OVERVIEW"
    requires_membership = tab != "OVERVIEW"
    logged_in = request.user.is_authenticated()

    if not logged_in and requires_login:
        raise Exception("TODO login redirect")
    account = logged_in and get_object_or_404(Account, user=request.user)
    if requires_membership and account not in team.members.all():
        raise PermissionDenied

    bike = get_object_or_404(Bike, id=bike_id, team=team)
    authorized = (account and account in team.members.all())
    template = _VIEW[tab]["template"]
    args = { 
        "bike" : bike, 
        "borrows" : bike.borrows.all(),
        "description_title" : _VIEW[tab]["description_title"],
        "description_content" : _VIEW[tab]["description_content"],
        "tabs" : _tabs(bike, team, tab, authorized), 
    }
    return rtr(team, "bikes", request, template, args)


@require_http_methods(["GET"])
def list(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    filters = _get_bike_filters(request, None, team)
    args = { "bikes" :  team.bikes.filter(**filters) }
    return rtr(team, "bikes", request, "bike/list.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def create(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    if request.method == "POST":
        form = forms.Create(request.POST, team=team, account=account)
        if form.is_valid():
            bike = control.create(
                team, form.cleaned_data["name"].strip(),
                form.cleaned_data["description"].strip(),
                form.cleaned_data["active"], form.cleaned_data["reserve"],
                form.cleaned_data["station"], form.cleaned_data["lockcode"],
                form.cleaned_data["size"], form.cleaned_data["lights"], 
            )
            url = "/%s/bike/view/%s" % (team.link, bike.id)
            return HttpResponseRedirect(url)
    else:
        form = forms.Create(team=team, account=account)
    args = { "form" : form, "form_title" : _("BIKE_CREATE") }
    return rtr(team, "bikes", request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def edit(request, team_link, bike_id):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    bike = get_object_or_404(Bike, id=bike_id, team=team)
    if request.method == "POST":
        form = forms.Edit(request.POST, bike=bike, account=account)
        if form.is_valid():
            control.edit(
                bike,
                form.cleaned_data["name"].strip(),
                form.cleaned_data["description"].strip(),
                form.cleaned_data["active"], form.cleaned_data["reserve"],
                form.cleaned_data["station"], form.cleaned_data["lockcode"],
                form.cleaned_data["size"], form.cleaned_data["lights"],
            )
            url = "/%s/bike/view/%s" % (team.link, bike.id)
            return HttpResponseRedirect(url)
    else:
        form = forms.Edit(bike=bike, account=account)
    args = { "form" : form, "form_title" : _("BIKE_EDIT") }
    return rtr(team, "bikes", request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def delete(request, team_link, bike_id):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    bike = get_object_or_404(Bike, id=bike_id, team=team)

    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            # TODO enusre db consistency and now open borrows
            bike.delete()
            return HttpResponseRedirect("/%s/bikes" % team.link)
    else:
        form = Form()
    args = { 
        "form" : form, "form_title" : _("BIKE_DELETE?"), 
        "object_name" : bike.name, "cancle_url" : "/%s/bikes" % team.link
    }
    return rtr(team, "bikes", request, "common/delete.html", args)



