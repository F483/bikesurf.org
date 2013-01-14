# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from apps.common.shortcuts import render_response
from apps.account.models import Account
from apps.team.models import Team
from apps.bike.models import Bike
from apps.team.utils import render_team_response as rtr
from apps.team.utils import assert_member
from apps.borrow.models import Borrow
from apps.borrow import forms
from apps.borrow import control


def _get_team_models(request, team_link, borrow_id):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    borrow = get_object_or_404(Borrow, id=borrow_id)
    return team, account, borrow


@login_required
@require_http_methods(["GET"])
def list_team(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    args = { "borrows" : Borrow.objects.filter(bike__team=team) }
    return rtr(team, "borrows", request, "borrow/list_team.html", args)


@login_required
@require_http_methods(["GET"])
def list_my(request):
    account = get_object_or_404(Account, user=request.user)
    args = { "borrows" : Borrow.objects.filter(borrower=account) }
    return render_response(request, "borrow/list_my.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def create(request, team_link, bike_id):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    bike = get_object_or_404(Bike, id=bike_id)
    if request.method == "POST":
        form = forms.Create(request.POST, bike=bike)
        if form.is_valid():
            borrow, log = control.create(bike, account, 
                                         form.cleaned_data["start"],
                                         form.cleaned_data["finish"],
                                         form.cleaned_data["note"].strip())
            # TODO return HttpResponseRedirect("/borrow/view/%s" % borrow.id)
            return HttpResponseRedirect("/%s/borrows" % team.link)
    else:
        form = forms.Create(bike=bike)
    args = { "form" : form, "bike" : bike }
    return rtr(team, "borrows", request, "borrow/create.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def respond(request, team_link, borrow_id):
    team, account, borrow = _get_team_models(request, team_link, borrow_id)
    if request.method == "POST":
        form = forms.Respond(request.POST, borrow=borrow, account=account)
        if form.is_valid():
            control.respond(account, borrow, form.cleaned_data["response"], 
                            form.cleaned_data["note"].strip())
            # TODO redirect here when view is done
            # url = "/%s/borrow/view/%s" % (team.id, borrow.id)
            # return HttpResponseRedirect(url)
            return HttpResponseRedirect("/%s/borrows" % team.link)
    else:
        form = forms.Respond(borrow=borrow, account=account)
    args = { "form" : form, "borrow" : borrow }
    return rtr(team, "borrows", request, "borrow/respond.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def cancel_team(request, team_link, borrow_id):
    team, account, borrow = _get_team_models(request, team_link, borrow_id)
    if request.method == "POST":
        form = forms.Cancel(request.POST, borrow=borrow, account=account)
        if form.is_valid():
            control.cancel(account, borrow, form.cleaned_data["note"].strip())
            # TODO redirect here when view is done
            # url = "/%s/borrow/view/%s" % (team.id, borrow.id)
            # return HttpResponseRedirect(url)
            return HttpResponseRedirect("/%s/borrows" % team.link)
    else:
        form = forms.Cancel(borrow=borrow, account=account)
    args = { "form" : form, "borrow" : borrow }
    return rtr(team, "borrows", request, "borrow/cancel_team.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def rate_team(request, team_link, borrow_id):
    team, account, borrow = _get_team_models(request, team_link, borrow_id)
    if request.method == "POST":
        form = forms.RateTeam(request.POST, borrow=borrow, account=account)
        if form.is_valid():
            rating = form.cleaned_data["rating"]
            note = form.cleaned_data["note"].strip()
            control.rate_team(account, borrow, rating, note)
            # TODO redirect here when view is done
            # url = "/%s/borrow/view/%s" % (team.id, borrow.id)
            # return HttpResponseRedirect(url)
            return HttpResponseRedirect("/%s/borrows" % team.link)
    else:
        form = forms.RateTeam(borrow=borrow, account=account)
    args = { "form" : form, "borrow" : borrow }
    return rtr(team, "borrows", request, "borrow/rate_team.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def rate_my(request, borrow_id):
    pass # TODO


@login_required
@require_http_methods(["GET"])
def cancel_my(request, borrow_id):
    pass # TODO


@login_required
@require_http_methods(["GET"])
def view_my(request, borrow_id):
    pass # TODO


@login_required
@require_http_methods(["GET"])
def view_team(request, team_link, borrow_id):
    pass # TODO


