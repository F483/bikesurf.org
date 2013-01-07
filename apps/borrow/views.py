# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from apps.account.models import Account
from apps.team.models import Team
from apps.bike.models import Bike
from apps.team.utils import render_team_response as rtr
from apps.team.utils import assert_member
from apps.borrow.models import Borrow
from apps.borrow.models import Log
from apps.borrow.forms import CreateBorrowForm


@login_required
@require_http_methods(["GET"])
def list_team(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    args = { "borrows" : Borrow.objects.filter(bike__team=team) }
    return rtr(team, "borrows", request, "borrow/list.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def create(request, team_link, bike_id):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    bike = get_object_or_404(Bike, id=bike_id)
    if request.method == "POST":
        form = CreateBorrowForm(request.POST, bike=bike)
        if form.is_valid():

            borrow = Borrow()
            borrow.bike = bike
            borrow.borrower = account
            borrow.start = form.cleaned_data["start"]
            borrow.finish = form.cleaned_data["finish"]
            borrow.active = False
            borrow.state = "REQUEST"
            borrow.src = bike.station
            borrow.dest = bike.station
            borrow.save()

            log = Log()
            log.borrow = borrow
            log.initiator = account
            log.state = borrow.state
            log.note = form.cleaned_data["application"].strip()
            log.save()

            # TODO return HttpResponseRedirect("/borrow/view/%s" % borrow.id)
            return HttpResponseRedirect("/%s/borrows" % team.link)
    else:
        form = CreateBorrowForm(bike=bike)
    args = { "form" : form, "bike" : bike }
    return rtr(team, "borrows", request, "borrow/create.html", args)


@login_required
@require_http_methods(["GET"])
def list_my(request):
    pass # TODO


@login_required
@require_http_methods(["GET"])
def view_my(request, borrow_id):
    pass # TODO


@login_required
@require_http_methods(["GET"])
def view_team(request, team_link, borrow_id):
    pass # TODO


