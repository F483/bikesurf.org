# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from apps.common.shortcuts import render_response
from apps.site.forms import TeamSelectForm
from django.contrib.auth.decorators import login_required


@require_http_methods(['GET', 'POST'])
def root(request):
    # index
    if request.method == 'POST':
        form = TeamSelectForm(request.POST)
        if form.is_valid():
            team_link = form.cleaned_data['team'].link
            return HttpResponseRedirect("/%s" % team_link)
    else:
        form = TeamSelectForm()
    return render_response(request, 'site/index.html', { 'form' : form })


@login_required
@require_http_methods(['GET'])
def profile(request):
    return render_response(request, 'site/profile.html', {})

