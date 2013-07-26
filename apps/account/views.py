# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.views.decorators.http import require_http_methods
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from apps.account.models import Account
from apps.common.shortcuts import render_response
from apps.account import forms
from apps.account import control
from apps.link.models import Link


PROFILE_UPDATED = _("PROFILE_UPDATED")


@login_required
@require_http_methods(["GET", "POST"])
def link_delete(request, link_id):
    account = get_object_or_404(Account, user=request.user)
    link = get_object_or_404(Link, id=link_id)
    if request.method == "POST":
        form = forms.LinkDelete(request.POST, link=link, account=account)
        if form.is_valid():
            control.link_delete(account, link)
            return HttpResponseRedirect("/accounts/profile/")
    else:
        form = forms.LinkDelete(link=link, account=account)
    args = { 
        "form" : form, "form_title" : _("LINK_DELETE?"), 
        "form_subtitle" : link.get_label(), 
        "cancel_url" : "/accounts/profile/"
    }
    return render_response(request, "common/form.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def link_create(request):
    account = get_object_or_404(Account, user=request.user)
    if request.method == "POST":
        form = forms.LinkCreate(request.POST, account=account)
        if form.is_valid():
            control.link_create(
                account, 
                form.cleaned_data["site"], 
                form.cleaned_data["profile"].strip(), 
            )
            return HttpResponseRedirect("/accounts/profile/")
    else:
        form = forms.LinkCreate(account=account)
    args = { 
        "form" : form, "cancel_url" : "/accounts/profile/", 
        "form_title" :  account, "form_subtitle" : _("ADD_LINK_SUBTITLE")
    }
    return render_response(request, "common/form.html", args)


@login_required
@require_http_methods(["GET"])
def view(request):
    account = get_object_or_404(Account, user=request.user)
    args = { "links" : account.links.all() }
    return render_response(request, "account/view.html", args)


@login_required
@require_http_methods(["GET", "POST"])
def edit(request):
    account = get_object_or_404(Account, user=request.user)
    if request.method == "POST":
        form = forms.Edit(request.POST, account=account)
        if form.is_valid():
            control.edit(
                account, 
                form.cleaned_data["username"].strip(), 
                form.cleaned_data["first_name"].strip(), 
                form.cleaned_data["last_name"].strip(), 
                form.cleaned_data["mobile"].strip(), 
                form.cleaned_data["source"], 
                form.cleaned_data["description"].strip()
            )
            return HttpResponseRedirect("/accounts/profile/")
    else:
        form = forms.Edit(account=account)
    args = { 
        "form" : form, "cancel_url" : "/accounts/profile/", 
        "form_title" :  account, "form_subtitle" : _("USER_PRIVECY_INFORMATION")
    }
    return render_response(request, "common/form.html", args)


