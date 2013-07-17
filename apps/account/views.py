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


PROFILE_UPDATED = _("PROFILE_UPDATED")


@login_required
@require_http_methods(["GET"])
def view(request):
    return render_response(request, "account/view.html", {})


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
        "form_title" :  account, 
    }
    return render_response(request, "common/form.html", args)


