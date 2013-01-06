# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import re
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from apps.common.shortcuts import render_response
from apps.common.shortcuts import uslugify
from apps.account.models import Account
from apps.team.models import Team
from apps.team.models import JoinRequest
from apps.team.models import RemoveRequest
from apps.borrow.models import Borrow
from apps.team.forms import CreateTeamForm
from apps.team.forms import CreateJoinRequestForm
from apps.team.forms import ProcessJoinRequestForm
from apps.team.utils import render_team_response as rtr
from apps.team.utils import assert_member


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    account = get_object_or_404(Account, user=request.user)
    if request.method == "POST":
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"].strip()
            team = Team()
            team.name = name
            team.link = uslugify(name)
            team.country = form.cleaned_data["country"]
            team.created_by = account
            team.updated_by = account
            team.save()
            team.members.add(account)
            return HttpResponseRedirect("/%s" % team.link)
    else:
        form = CreateTeamForm()
    return render_response(request, "team/create.html", { "form" : form })


#################
# JOIN REQUESTS #
#################


@login_required
@require_http_methods(["GET"])
def join_requests(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    template = "team/join_requests.html"
    args = { "join_requests" : JoinRequest.objects.filter(team=team) }
    return rtr(team, "join_requests", request, template, args)


@login_required
@require_http_methods(["GET", "POST"])
def join_request(request, team_link):

    # get data
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)

    # check permission to create join request
    if account in team.members.all():
        raise PermissionDenied # already a member
    filters = {"team" : team, "requester" : account, "status" : "PENDING"}
    if len(JoinRequest.objects.filter(**filters)) > 0:
        raise PermissionDenied # already requested

    if request.method == "POST":
        form = CreateJoinRequestForm(request.POST)
        if form.is_valid():

            # create join request
            jr = JoinRequest()
            jr.team = team
            jr.requester = account
            jr.application = form.cleaned_data["application"]
            jr.save()

            # TODO send messages

            return HttpResponseRedirect("/%s/join_requested" % team_link)
    else:
        form = CreateJoinRequestForm()
    template = "team/join_request.html"
    return rtr(team, None, request, template, { "form" : form })


@login_required
@require_http_methods(["GET", "POST"])
def join_request_process(request, team_link, join_request_id):

    # get data
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    jr = get_object_or_404(JoinRequest, id=join_request_id)
    
    # check permission to process join request
    assert_member(account, team)
    if jr.status != "PENDING":
        raise PermissionDenied # already processed

    if request.method == "POST":
        form = ProcessJoinRequestForm(request.POST)
        if form.is_valid():

            # process join request
            jr.processor = account
            jr.response = form.cleaned_data["response"]
            jr.status = form.cleaned_data["status"]
            jr.save()
            if jr.status == 'ACCEPTED':
                jr.team.members.add(jr.requester)

            # TODO send messages

            return HttpResponseRedirect("/%s/join_requests" % team_link)
    else:
        form = ProcessJoinRequestForm()
    template = "team/join_request_process.html"
    args = { "join_request" : jr, "form" : form }
    return rtr(team, "join_requests", request, template, args)


@login_required
@require_http_methods(["GET"])
def join_requested(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    return rtr(team, None, request, "team/join_requested.html", {})




##########
# OTHERS #
##########


@login_required
@require_http_methods(["GET"])
def remove_requests(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    template = "team/remove_requests.html"
    args = { "remove_requests" : RemoveRequest.objects.filter(team=team) }
    return rtr(team, "remove_requests", request, template, args)


@login_required
@require_http_methods(["GET"])
def borrows(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    args = { "borrows" : Borrow.objects.filter(bike__team=team) }
    return rtr(team, "borrows", request, "team/borrows.html", args)


@require_http_methods(["GET"])
def members(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    args = { "members" : team.members.all() }
    return rtr(team, "members", request, "team/members.html", args)


