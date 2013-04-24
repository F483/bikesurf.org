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
from apps.page.models import Page
from apps.page.forms import CreatePageForm, EditPageForm
from apps.team.utils import render_team_response as rtr
from apps.team.utils import assert_member
from apps.page import control
from django.forms import Form


@require_http_methods(["GET"])
def view(request, team_link, page_link):
    team = get_object_or_404(Team, link=team_link)
    page = get_object_or_404(Page, link=page_link, team=team)
    return rtr(team, page.link, request, "page/view.html", { "page" : page })


@login_required
@require_http_methods(["GET", "POST"])
def create(request, team_link):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    if request.method == "POST":
        form = CreatePageForm(request.POST, team=team)
        if form.is_valid():
            name = form.cleaned_data["name"].strip()
            content = form.cleaned_data["content"]
            order = form.cleaned_data["order"]
            page = control.create(account, team, name, content, order)
            return HttpResponseRedirect("/%s/%s" % (team.link, page.link))
    else:
        form = CreatePageForm(team=team)
    args = { 
        "form" : form, "form_title" : _("ADD_PAGE"),
        "cancle_url" : "/%s" % team.link
    }
    return rtr(team, None, request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def edit(request, team_link, page_link):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    page = get_object_or_404(Page, link=page_link, team=team)
    if request.method == "POST":
        form = EditPageForm(request.POST, page=page)
        if form.is_valid():
            name = form.cleaned_data["name"]
            content = form.cleaned_data["content"]
            order = form.cleaned_data["order"]
            control.edit(account, page, name, content, order)
            return HttpResponseRedirect("/%s/%s" % (team.link, page.link))
    else:
        form = EditPageForm(page=page)
    args = { 
        "form" : form, "form_title" : _("PAGE_EDIT"),
        "cancle_url" : "/%s/%s" % (team.link, page.link)
    }
    return rtr(team, page.link, request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def delete(request, team_link, page_link):
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    page = get_object_or_404(Page, link=page_link, team=team)

    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            control.delete(account, page)
            return HttpResponseRedirect("/%s" % team.link)
    else:
        form = Form()
    cancle_url = "/%s/%s" % (team.link, page.link)
    args = { 
        "form" : form, "form_title" : _("PAGE_DELETE?"), 
        "form_subtitle" : page.name, "cancle_url" : cancle_url
    }
    return rtr(team, page.link, request, "common/form.html", args)


