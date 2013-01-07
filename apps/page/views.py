# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from apps.common.shortcuts import uslugify
from apps.account.models import Account
from apps.team.models import Team
from apps.page.models import Page
from apps.page.forms import CreatePageForm
from apps.team.utils import render_team_response as rtr
from apps.team.utils import assert_member


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
            page = Page()
            page.team = team
            page.name = name
            page.link = uslugify(name)
            page.content = form.cleaned_data["content"]
            page.order = form.cleaned_data["order"]
            page.created_by = account
            page.updated_by = account
            page.save()
            # TODO send messages
            return HttpResponseRedirect("/%s/%s" % (team.link, page.link))
    else:
        form = CreatePageForm(team=team)
    return rtr(team, None, request, "page/create.html", { "form" : form })


