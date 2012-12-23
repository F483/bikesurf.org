# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.http import HttpResponseRedirect
from common.shortcuts import render_response
from apps.site.forms import TeamSelectForm


    #if request.user.is_authenticated():
def root(request):
    if request.method == 'POST':
        form = TeamSelectForm(request.POST)
        if form.is_valid():
            team_link = form.cleaned_data['team'].link
            return HttpResponseRedirect("/%s" % team_link)
    else:
        form = TeamSelectForm()
    return render_response(request, 'site/index.html', { 'form' : form })
