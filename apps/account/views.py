# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.views.decorators.http import require_http_methods
from apps.common.shortcuts import render_response
from django.contrib.auth.decorators import login_required


@login_required
@require_http_methods(['GET'])
def profile(request):
    return render_response(request, 'account/profile.html', {})

