# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.http import HttpResponseRedirect
from common.shortcuts import render_response
from apps.site.forms import TeamSelectForm


def root(request):
    if request.user.is_authenticated():
        return __dashboard(request)
    else:
        return __index(request)


def __index(request):
    if request.method == 'POST':
        form = TeamSelectForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(form.cleaned_data['team'].get_url())
    else:
        form = TeamSelectForm()
    return render_response(request, 'site/index.html', { 'form' : form })


def __dashboard(request):
    return render_response(request, 'site/dashboard.html', {})


