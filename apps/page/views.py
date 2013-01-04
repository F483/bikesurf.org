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


RESERVED_NAMES = [
    u"blog",
    u"bikes",
    u"borrows",
    u"stations",
    u"members",
    u"join_request",
    u"join_requested",
    u"join_requests",
    u"join_request_process",
    u"remove_requests",
    u"page",
]


@require_http_methods(["GET"])
def view(request, team_link, page_link):
    team = get_object_or_404(Team, link=team_link)
    page = get_object_or_404(Page, link=page_link, team=team)
    return rtr(team, page.link, request, "page/view.html", { "page" : page })


@login_required
@require_http_methods(["GET", "POST"])
def create(request, team_link):

    # get data
    team = get_object_or_404(Team, link=team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)

    if request.method == "POST":
        form = CreatePageForm(request.POST)
        if form.is_valid():

            # get data
            name = form.cleaned_data["name"].strip()
            content = form.cleaned_data["content"]
            order = form.cleaned_data["order"]
            link = uslugify(name)

            # check data
            data_ok = True
            if link in RESERVED_NAMES:
                form.errors["name"] = [_("NAME_RESERVED")]
                data_ok = False
            if len(link) < 3:
                form.errors["name"] = [_("NAME_TO_SHORT")]
                data_ok = False
            if bool(len(Page.objects.filter(name=name, team=team))):
                form.errors["name"] = [_("NAME_USED")]
                data_ok = False
            if bool(len(Page.objects.filter(link=link, team=team))):
                form.errors["name"] = [_("NAME_USED")]
                data_ok = False

            # create page
            if data_ok:
                page = Page()
                page.team = team
                page.name = name
                page.link = link
                page.content = content
                page.order = order
                page.created_by = account
                page.updated_by = account
                page.save()

                # TODO check for forbidden page names
                # TODO send messages

                return HttpResponseRedirect("/%s/%s" % (team.link, page.link))
    else:
        form = CreatePageForm()
    return rtr(team, None, request, "page/create.html", { "form" : form })


