# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.core.context_processors import csrf
from django.shortcuts import render_to_response


# A human readable link id for urls
HUMAN_LINK_LEN = 128
HUMAN_LINK_FORMAT = "[a-z0-9-_]{3,%i}" % HUMAN_LINK_LEN


def render_response(request, template, args):
    user = request.user
    args.update({
        'current_user' : user,
        'current_account' : user.is_authenticated() and user.account_set.all()[0] or None,
        'message_count' : 0, # TODO get count
        'borrow_count' : 0, # TODO get count
    })
    args.update(csrf(request))
    return render_to_response(template, args)

