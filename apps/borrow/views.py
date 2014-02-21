# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import datetime

from dateutil.parser import parse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

from apps.team import control as team_control
from apps.account import control as account_control
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
    team = team_control.get_or_404(team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    borrow = get_object_or_404(Borrow, id=borrow_id)
    return team, account, borrow


def _filter_lender_borrows(borrows, form):
    today = datetime.datetime.now().date()
    
    # bike
    bike = form.cleaned_data["bike"]
    if bike:
        borrows = borrows.filter(bike=bike)

    # state
    state = form.cleaned_data["state"]
    if state:
        borrows = borrows.filter(state=state)

    # src
    src = form.cleaned_data["src"]
    if src:
        borrows = borrows.filter(src=src)

    # dest
    dest = form.cleaned_data["dest"]
    if dest:
        borrows = borrows.filter(dest=dest)

    # future
    if not form.cleaned_data["future"]:
        borrows = borrows.exclude(start__gt=today)

    # ongoing
    if not form.cleaned_data["ongoing"]:
        borrows = borrows.exclude(start__lte=today, finish__gte=today)

    # past
    if not form.cleaned_data["past"]:
        borrows = borrows.exclude(finish__lt=today)

    return borrows


@login_required
@require_http_methods(["GET", "POST"])
def lender_list(request, team_link):
    team = team_control.get_or_404(team_link)
    account = get_object_or_404(Account, user=request.user)
    assert_member(account, team)
    today = datetime.datetime.now().date()
    borrows = Borrow.objects.filter(team=team) 
    if request.method == "POST":
        form = forms.FilterListing(request.POST, team=team)
        if form.is_valid():
            borrows = _filter_lender_borrows(borrows, form)
    else:
        form = forms.FilterListing(team=team)
        borrows = borrows.exclude(finish__lt=today) # filter out past
    args = { 
        "filters" : form, "page_title" : _("TEAM_BORROWS"),
        "list_data" : control.to_list_data(borrows, team_link=True) 
    }
    return rtr(team, "borrows", request, "common/list.html", args)


@login_required
@require_http_methods(["GET"])
def borrower_list(request):
    account = get_object_or_404(Account, user=request.user)
    borrows = Borrow.objects.filter(borrower=account)
    args = { 
        "page_title" : _("YOUR_BORROWS"),
        "list_data" :  control.to_list_data(borrows) 
    }
    return render_response(request, "common/list.html", args)


@login_required
@require_http_methods(["GET"])
def arrivals(request):
    today = datetime.datetime.now().date()
    account = get_object_or_404(Account, user=request.user)
    borrows = control.arrivals(account)
    args = { 
        "page_title" : _("ARRIVALS"),
        "list_data" : control.to_list_data(
            borrows, team_link=True, columns="ARRIVALS"
        )
    }
    return render_response(request, "common/list.html", args)


@login_required
@require_http_methods(["GET"])
def departures(request):
    today = datetime.datetime.now().date()
    account = get_object_or_404(Account, user=request.user)
    borrows = control.departures(account)
    args = {
        "page_title" : _("DEPARTURES"),
        "list_data" : control.to_list_data(
            borrows, team_link=True, columns="DEPARTURES"
        )
    }
    return render_response(request, "common/list.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def create(request, team_link, bike_id):

    # get parameters
    start = request.GET.get('start', None)
    finish = request.GET.get('finish', None)
    try:
        start = start and parse(start).date() or None
        finish = finish and parse(finish).date() or None
    except ValueError:
        start = None
        finish = None

    team = team_control.get_or_404(team_link)
    account = get_object_or_404(Account, user=request.user)
    bike = get_object_or_404(Bike, id=bike_id)
    if request.method == "POST":
        form = forms.Create(request.POST, bike=bike, account=account, 
                            start=start, finish=finish)
        if form.is_valid():
            borrow = control.create(account, bike,
                                    form.cleaned_data["start"],
                                    form.cleaned_data["finish"],
                                    form.cleaned_data["note"].strip())
            return HttpResponseRedirect("/borrow/view/%s" % borrow.id)
    else:
        form = forms.Create(bike=bike, account=account, 
                            start=start, finish=finish)
    args = { 
        "form" : form, "form_title" : _("BORROW_CREATE"),
        "cancel_url" : "/%s/bike/view/%s" % (team_link, bike_id),
        "has_required_info" : account_control.has_required_info(account)
    }
    return rtr(team, "borrows", request, "borrow/create.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def borrower_edit(request, borrow_id):
    account = get_object_or_404(Account, user=request.user)
    borrow = get_object_or_404(Borrow, id=borrow_id)
    if request.method == "POST":
        form = forms.Edit(request.POST, borrow=borrow)
        if form.is_valid():
            control.borrower_edit(
                    account, borrow,
                    form.cleaned_data["start"],
                    form.cleaned_data["finish"],
                    form.cleaned_data["bike"],
                    form.cleaned_data["note"].strip()
            )
            return HttpResponseRedirect("/borrow/view/%s" % borrow.id)
    else:
        form = forms.Edit(borrow=borrow)
    args = { 
        "form" : form, "form_title" : _("BORROW_EDIT"),
        "cancel_url" : "/borrow/view/%s" % borrow.id
    }
    return render_response(request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def lender_edit(request, team_link, borrow_id):
    team, account, borrow = _get_team_models(request, team_link, borrow_id)
    if request.method == "POST":
        form = forms.Edit(request.POST, borrow=borrow)
        if form.is_valid():
            control.lender_edit(
                    account, borrow,
                    form.cleaned_data["start"],
                    form.cleaned_data["finish"],
                    form.cleaned_data["bike"],
                    form.cleaned_data["note"].strip()
            )
            url = "/%s/borrow/view/%s" % (team.link, borrow.id)
            return HttpResponseRedirect(url)
    else:
        form = forms.Edit(borrow=borrow)
    args = { "form" : form, "form_title" : _("BORROW_EDIT"),
        "cancel_url" : "/%s/borrow/view/%s" % (team.link, borrow.id)
    }
    return rtr(team, "borrows", request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def lender_edit_dest(request, team_link, borrow_id):
    team, account, borrow = _get_team_models(request, team_link, borrow_id)
    if request.method == "POST":
        form = forms.LenderEditDest(request.POST, borrow=borrow)
        if form.is_valid():
            control.lender_edit_dest(
                    account, borrow,
                    form.cleaned_data["dest"],
                    form.cleaned_data["note"].strip()
            )
            url = "/%s/borrow/view/%s" % (team.link, borrow.id)
            return HttpResponseRedirect(url)
    else:
        form = forms.LenderEditDest(borrow=borrow)
    args = { "form" : form, "form_title" : _("BORROW_EDIT"),
        "cancel_url" : "/%s/borrow/view/%s" % (team.link, borrow.id)
    }
    return rtr(team, "borrows", request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def respond(request, team_link, borrow_id):
    team, account, borrow = _get_team_models(request, team_link, borrow_id)
    if request.method == "POST":
        form = forms.Respond(request.POST, borrow=borrow, account=account)
        if form.is_valid():
            control.respond(account, borrow, form.cleaned_data["response"], 
                            form.cleaned_data["note"].strip())
            url = "/%s/borrow/view/%s" % (team.link, borrow.id)
            return HttpResponseRedirect(url)
    else:
        form = forms.Respond(borrow=borrow, account=account)
    email = account_control.get_email_or_404(borrow.borrower)
    args = { 
        "station" : control.accept_station(borrow),
        "email" : email, "links" : borrow.borrower.links.all(),
        "borrow" : borrow, "form" : form, "form_title" : _("BORROW_RESPOND"), 
        "cancel_url" : "/%s/borrow/view/%s" % (team_link, borrow_id)
    }
    return rtr(team, "borrows", request, "borrow/respond.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def lender_cancel(request, team_link, borrow_id):
    team, account, borrow = _get_team_models(request, team_link, borrow_id)
    if request.method == "POST":
        form = forms.Cancel(request.POST)
        if form.is_valid():
            control.cancel(account, borrow, form.cleaned_data["note"].strip())
            url = "/%s/borrow/view/%s" % (team.link, borrow.id)
            return HttpResponseRedirect(url)
    else:
        form = forms.Cancel()
    args = { 
        "form" : form, "form_title" : _("BORROW_CANCEL"), 
        "cancel_url" : "/%s/borrow/view/%s" % (team_link, borrow_id)
    }
    return rtr(team, "borrows", request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def lender_rate(request, team_link, borrow_id):
    team, account, borrow = _get_team_models(request, team_link, borrow_id)
    if request.method == "POST":
        form = forms.Rate(request.POST)
        if form.is_valid():
            rating = form.cleaned_data["rating"]
            note = form.cleaned_data["note"].strip()
            control.lender_rate(account, borrow, rating, note)
            url = "/%s/borrow/view/%s" % (team.link, borrow.id)
            return HttpResponseRedirect(url)
    else:
        form = forms.Rate()
    form_title = u"%s %s" % (_("RATE"), borrow)
    args = { 
        "form" : form, "form_title" : form_title, 
        "cancel_url" : "/%s/borrow/view/%s" % (team_link, borrow_id)
    }
    return rtr(team, "borrows", request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def borrower_rate(request, borrow_id):
    account = get_object_or_404(Account, user=request.user)
    borrow = get_object_or_404(Borrow, id=borrow_id)
    if account != borrow.borrower:
        raise PermissionDenied
    if request.method == "POST":
        form = forms.Rate(request.POST)
        if form.is_valid():
            rating = form.cleaned_data["rating"]
            note = form.cleaned_data["note"].strip()
            control.borrower_rate(account, borrow, rating, note)
            return HttpResponseRedirect("/borrow/view/%s" % borrow.id)
    else:
        form = forms.Rate()
    form_title = u"%s %s" % (_("RATE"), borrow)
    args = { 
        "form" : form, "form_title" : form_title, 
        "cancel_url" : "/borrow/view/%s" % borrow_id
    }
    return render_response(request, "common/form.html", args)


@login_required
@require_http_methods(["GET"])
def borrower_view(request, borrow_id):
    account = get_object_or_404(Account, user=request.user)
    borrow = get_object_or_404(Borrow, id=borrow_id)
    if account != borrow.borrower:
        raise PermissionDenied
    args = { "borrow" : borrow, "logs" : borrow.logs.all() }
    return render_response(request, "borrow/view.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def comment(request, **kwargs):
    borrow_id = kwargs["borrow_id"]
    team_link = kwargs.get("team_link")
    account = get_object_or_404(Account, user=request.user)
    team = team_link and team_control.get_or_404(team_link) or None
    borrow = get_object_or_404(Borrow, id=borrow_id)
    url_prefix = team and "/%s" % team.link or ""
    url = "%s/borrow/view/%s" % (url_prefix, borrow_id)
    if request.method == "POST":
        form = forms.Comment(request.POST)
        if form.is_valid():
            control.comment(account, borrow, form.cleaned_data["note"].strip()
            )
            return HttpResponseRedirect(url)
    else:
        form = forms.Comment()

    args = { 
        "form" : form, "form_title" : _("BORROW_COMMENT"), 
        "cancel_url" : url
    }
    if team:
        return rtr(team, "borrows", request, "common/form.html", args)
    return render_response(request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def borrower_cancel(request, borrow_id):
    account = get_object_or_404(Account, user=request.user)
    borrow = get_object_or_404(Borrow, id=borrow_id)
    if account != borrow.borrower:
        raise PermissionDenied
    if request.method == "POST":
        form = forms.Cancel(request.POST)
        if form.is_valid():
            control.cancel(account, borrow, form.cleaned_data["note"].strip())
            return HttpResponseRedirect("/borrow/view/%s" % borrow.id)
    else:
        form = forms.Cancel()
    args = { 
        "form" : form, "form_title" : _("BORROW_CANCEL"), 
        "cancel_url" : "/borrow/view/%s" % borrow_id
    }
    return render_response(request, "common/form.html", args)


@login_required
@require_http_methods(["GET"])
def lender_view(request, team_link, borrow_id):
    team, account, borrow = _get_team_models(request, team_link, borrow_id)
    args = { "borrow" : borrow, "logs" : borrow.logs.all() }
    return rtr(team, "borrows", request, "borrow/view.html", args)


