# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from unidecode import unidecode


def uslugify(ustr):
    """ because slugify is shit with unicode """
    return slugify(unidecode(ustr))


def render_response(request, template, args):
    user = request.user
    args.update({
        'current_user' : user,
        'current_account' : user.is_authenticated() and user.account_set.all()[0] or None,
        'message_count' : 0, # TODO get count
        'borrow_count' : 0, # TODO get count
    })
    args.update(csrf(request))
    # TODO check if mobile and use mobile template if exists
    return render_to_response(template, args)

