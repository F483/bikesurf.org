# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


import os
import random
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from apps.common.shortcuts import render_response
from apps.site.forms import TeamSelectForm
from config.settings import PROJECT_DIR


@require_http_methods(['GET', 'POST'])
def index(request):
    if request.method == 'POST':
        form = TeamSelectForm(request.POST)
        if form.is_valid():
            team_link = form.cleaned_data['team'].link
            return HttpResponseRedirect("/%s" % team_link)
    else:
        form = TeamSelectForm()
    imgdir = os.path.join("apps", "site", "static", "site", "splash")
    img = random.choice(os.listdir(os.path.join(PROJECT_DIR, imgdir)))
    splash_bg = os.path.join("/static", "site", "splash", img)
    args = { 'form' : form, "splash_bg" : splash_bg }
    return render_response(request, 'site/index.html', args)


@require_http_methods(['GET'])
def terms(request):
    return render_response(request, 'site/terms.html', {})

@require_http_methods(['GET'])
def donate(request):
    return render_response(request, 'site/donate.html', {})
