# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.shortcuts import render_to_response


def root(request):
    #return render_to_response('site/dashboard.html', {})
    return render_to_response('site/index.html', {})

