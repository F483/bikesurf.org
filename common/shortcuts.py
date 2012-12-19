# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.core.context_processors import csrf
from django.shortcuts import render_to_response


def render_response(request, template, args):
    args.update({'user' : request.user})
    args.update(csrf(request))
    return render_to_response(template, args)


