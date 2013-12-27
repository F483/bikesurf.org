# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from apps.common.shortcuts import render_response
from apps.account.models import Account
from apps.team.models import Team
from apps.team.models import JoinRequest
from apps.team.models import RemoveRequest
from apps.team import forms
from apps.team.utils import render_team_response as rtr
from apps.team.utils import assert_member
from apps.team import control
from apps.link.models import Link


@login_required
@require_http_methods(["GET", "POST"])
def link_delete(request, team_link, link_id):
    account = get_object_or_404(Account, user=request.user)
    team = control.get_or_404(team_link)
    link = get_object_or_404(Link, id=link_id)
    if request.method == "POST":
        form = forms.LinkDelete(request.POST, team=team, link=link, account=account)
        if form.is_valid():
            control.link_delete(account, team, link)
            return HttpResponseRedirect("/%s" % team.link)
    else:
        form = forms.LinkDelete(team=team, link=link, account=account)
    args = { 
        "form" : form, "form_title" : _("LINK_DELETE?"), 
        "form_subtitle" : link.get_label(), 
        "cancel_url" : "/%s" % team.link
    }
    return rtr(team, "", request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def link_create(request, team_link):
    account = get_object_or_404(Account, user=request.user)
    team = control.get_or_404(team_link)
    if request.method == "POST":
        form = forms.LinkCreate(request.POST, team=team, account=account)
        if form.is_valid():
            control.link_create(
                account, team,
                form.cleaned_data["site"], 
                form.cleaned_data["profile"].strip(), 
            )
            return HttpResponseRedirect("/%s" % team.link)
    else:
        form = forms.LinkCreate(team=team, account=account)
    args = { 
        "form" : form, "cancel_url" : "/%s" % team.link, 
        "form_title" :  account, "form_subtitle" : _("ADD_LINK_SUBTITLE")
    }
    return rtr(team, "", request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def replace_logo(request, team_link):
    account = get_object_or_404(Account, user=request.user)
    team = control.get_or_404(team_link)
    assert_member(account, team)
    if request.method == "POST":
        form = forms.ReplaceLogo(request.POST, request.FILES)
        if form.is_valid():
            logo = form.cleaned_data["logo"]
            control.replace_logo(account, team, logo)
            return HttpResponseRedirect("/%s" % team.link)
    else:
        form = forms.ReplaceLogo()
    args = { 
        "form" : form, "form_title" : _("REPLACE_LOGO"), 
        "multipart_form" : True, "cancel_url" : "/%s" % team.link
    }
    return render_response(request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    account = get_object_or_404(Account, user=request.user)
    if request.method == "POST":
        form = forms.CreateTeam(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data["name"].strip()
            country = form.cleaned_data["country"]
            logo = form.cleaned_data["logo"]
            application = form.cleaned_data["application"]
            team = control.create(account, name, country, logo, application)
            return HttpResponseRedirect("/%s/created" % team.link)
    else:
        form = forms.CreateTeam()
    args = { 
        "form" : form, "form_title" : _("CREATE_TEAM"), 
        "multipart_form" : True, "cancel_url" : "/"
    }
    return render_response(request, "common/form.html", args)


@login_required
@require_http_methods(["GET"])
def created(request, team_link):
    account = get_object_or_404(Account, user=request.user)
    team = get_object_or_404(Team, link=team_link, active=False)
    return render_response(request, "team/created.html", { "team" : team })


@login_required
@require_http_methods(["GET"])
def members(request, team_link):
    team = control.get_or_404(team_link)
    args = { 
        "members" : team.members.all(),
        "page_title" : _("MEMBERS")
    }
    return rtr(team, "members", request, "team/members.html", args)


#################
# JOIN REQUESTS #
#################


@login_required
@require_http_methods(["GET"])
def join_request_list(request, team_link):
    team = control.get_or_404(team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    template = "team/join_request/list.html"
    args = { "join_requests" : JoinRequest.objects.filter(team=team) }
    return rtr(team, "join_request/list", request, template, args)


@login_required
@require_http_methods(["GET", "POST"])
def join_request_create(request, team_link):
    team = control.get_or_404(team_link)
    account = get_object_or_404(Account, user=request.user)
    if request.method == "POST":
        form = forms.CreateJoinRequest(request.POST)
        if form.is_valid():
            application = form.cleaned_data["application"]
            jr = control.create_join_request(account, team, application)
            return HttpResponseRedirect("/%s/join_request/created" % team_link)
    else:
        form = forms.CreateJoinRequest()
    args = { 
        "form" : form, "form_title" : _("JOIN_REQUEST"),
        "cancel_url" : "/%s" % team.link
    }
    return rtr(team, "join_request/list", request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def join_request_process(request, team_link, join_request_id):
    team = control.get_or_404(team_link)
    account = get_object_or_404(Account, user=request.user)
    jr = get_object_or_404(JoinRequest, id=join_request_id)
    if request.method == "POST":
        form = forms.ProcessJoinRequest(request.POST)
        if form.is_valid():
            response = form.cleaned_data["response"]
            status = form.cleaned_data["status"]
            control.process_join_request(account, jr, response, status)
            return HttpResponseRedirect("/%s/join_request/list" % team_link)
    else:
        form = forms.ProcessJoinRequest()
    args = { 
        "form" : form, "form_title" : "PROCESS_JOIN_REQUEST",
        "cancel_url" : "/%s/join_request/list" % team.link
    }
    return rtr(team, "join_request/list", request, "common/form.html", args)


@login_required
@require_http_methods(["GET"])
def join_request_created(request, team_link):
    team = control.get_or_404(team_link)
    template = "team/join_request/created.html"
    return rtr(team, "join_request/list", request, template, {})


###################
# REMOVE REQUESTS #
###################


@login_required
@require_http_methods(["GET", "POST"])
def remove_request_create(request, team_link, concerned_id):
    team = control.get_or_404(team_link)
    account = get_object_or_404(Account, user=request.user)
    concerned = get_object_or_404(Account, id=concerned_id)
    if request.method == "POST":
        form = forms.CreateRemoveRequest(request.POST)
        if form.is_valid():
            reason = form.cleaned_data["reason"]
            control.create_remove_request(account, concerned, team, reason)
            return HttpResponseRedirect("/%s/remove_request/created" % team_link)
    else:
        form = forms.CreateRemoveRequest()
    args = { 
        "form" : form, "form_title" : _("REMOVE_REQUEST_CREATE"),
        "form_subtitle" : concerned,
        "cancel_url" : "/%s/members" % team.link
    }
    return rtr(team, "remove_request/list", request, "common/form.html", args)


@login_required
@require_http_methods(["GET"])
def remove_request_created(request, team_link):
    team = control.get_or_404(team_link)
    template = "team/remove_request/created.html"
    return rtr(team, "remove_request/list", request, template, {})


@login_required
@require_http_methods(["GET"])
def remove_request_list(request, team_link):
    team = control.get_or_404(team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    template = "team/remove_request/list.html"
    args = { "remove_requests" : RemoveRequest.objects.filter(team=team) }
    return rtr(team, "remove_request/list", request, template, args)


@login_required
@require_http_methods(["GET", "POST"])
def remove_request_process(request, team_link, remove_request_id):
    team = control.get_or_404(team_link)
    account = get_object_or_404(Account, user=request.user)
    remove_request = get_object_or_404(RemoveRequest, id=remove_request_id)
    if request.method == "POST":
        form = forms.ProcessRemoveRequest(request.POST)
        if form.is_valid():
            response = form.cleaned_data["response"]
            status = form.cleaned_data["status"]
            control.process_remove_request(account, remove_request, 
                                           response, status)
            return HttpResponseRedirect("/%s/remove_request/list" % team_link)
    else:
        form = forms.ProcessRemoveRequest()
    args = { 
        "form" : form, "form_title" : "PROCESS_REMOVE_REQUEST", 
        "cancel_url" : "/%s/remove_request/list" % team.link
    }
    return rtr(team, "remove_request/list", request, "common/form.html", args)


