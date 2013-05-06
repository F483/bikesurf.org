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
from apps.account.models import Account
from apps.team.models import Team
from apps.team.models import JoinRequest
from apps.team.models import RemoveRequest
from apps.team.forms import CreateTeamForm
from apps.team.forms import CreateJoinRequestForm
from apps.team.forms import CreateRemoveRequestForm
from apps.team.forms import ProcessJoinRequestForm
from apps.team.forms import ProcessRemoveRequestForm
from apps.team.utils import render_team_response as rtr
from apps.team.utils import assert_member
from apps.team import control


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    account = get_object_or_404(Account, user=request.user)
    if request.method == "POST":
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"].strip()
            country = form.cleaned_data["country"]
            team = control.create(account, name, country)
            return HttpResponseRedirect("/%s" % team.link)
    else:
        form = CreateTeamForm()
    args = { "form" : form, "form_title" : _("CREATE_TEAM") }
    return render_response(request, "common/form.html", args)


@require_http_methods(["GET"])
def members(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    args = { "members" : team.members.all() }
    return rtr(team, "members", request, "team/members.html", args)


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
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    if request.method == "POST":
        form = CreateJoinRequestForm(request.POST)
        if form.is_valid():
            application = form.cleaned_data["application"]
            jr = control.create_join_request(account, team, application)
            return HttpResponseRedirect("/%s/join_requested" % team_link)
    else:
        form = CreateJoinRequestForm()
    args = { "form" : form, "form_title" : _("JOIN_REQUEST") }
    return rtr(team, "join_requests", request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def join_request_process(request, team_link, join_request_id):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    jr = get_object_or_404(JoinRequest, id=join_request_id)
    if request.method == "POST":
        form = ProcessJoinRequestForm(request.POST)
        if form.is_valid():
            response = form.cleaned_data["response"]
            status = form.cleaned_data["status"]
            control.process_join_request(account, jr, response, status)
            return HttpResponseRedirect("/%s/join_requests" % team_link)
    else:
        form = ProcessJoinRequestForm()
    args = { "form" : form, "form_title" : "PROCESS_JOIN_REQUEST" }
    return rtr(team, "join_requests", request, "common/form.html", args)


@login_required
@require_http_methods(["GET"])
def join_requested(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    return rtr(team, "join_requests", request, "team/join_requested.html", {})


###################
# REMOVE REQUESTS #
###################


@login_required
@require_http_methods(["GET", "POST"])
def remove_request(request, team_link, concerned_id): # TODO rename to create_remove_request
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    concerned = get_object_or_404(Account, id=concerned_id)
    if request.method == "POST":
        form = CreateRemoveRequestForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data["reason"]
            control.create_remove_request(account, concerned, team, reason)
            return HttpResponseRedirect("/%s/remove_requested" % team_link)
    else:
        form = CreateRemoveRequestForm()
    args = { 
        "form" : form, "form_title" : _("REMOVE_REQUEST"),
        "form_subtitle" : concerned
    }
    return rtr(team, "remove_requests", request, "common/form.html", args)


@login_required
@require_http_methods(["GET"])
def remove_requested(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    return rtr(team, "remove_requests", request, "team/remove_requested.html", {})


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
@require_http_methods(["GET", "POST"])
def remove_request_process(request, team_link, remove_request_id):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    remove_request = get_object_or_404(RemoveRequest, id=remove_request_id)
    if request.method == "POST":
        form = ProcessRemoveRequestForm(request.POST)
        if form.is_valid():
            response = form.cleaned_data["response"]
            status = form.cleaned_data["status"]
            control.process_remove_request(account, remove_request, 
                                           response, status)
            return HttpResponseRedirect("/%s/remove_requests" % team_link)
    else:
        form = ProcessRemoveRequestForm()
    args = { "form" : form, "form_title" : "PROCESS_REMOVE_REQUEST" }
    return rtr(team, "remove_requests", request, "common/form.html", args)


